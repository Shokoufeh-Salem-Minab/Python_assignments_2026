import numpy as np


class SensorNotFoundError(Exception):
    pass


class Sensor:
    def __init__(self, sensor_id: str, location: str, readings=None):
        self.sensor_id = sensor_id
        self.location = location
        if readings is not None:
            self.readings = np.array(readings)
        else:
            rng = np.random.default_rng(seed=42)
            base = np.arange(7 * 24) * 0.05
            noise = rng.normal(loc=20.0, scale=3.0, size=7 * 24)
            self.readings = (base + noise).reshape(7, 24)

    def alert_threshold(self) -> float:
        return 30.0

    def unit(self) -> str:
        return "units"

    def summary(self) -> tuple[float, float, float]:
        return (
            float(np.min(self.readings)),
            float(np.max(self.readings)),
            float(np.mean(self.readings)),
        )

    def peak(self) -> tuple[int, int]:
        day, hour = np.unravel_index(np.argmax(self.readings), (7, 24))
        return int(day), int(hour)

    def lowest(self) -> tuple[int, int]:
        day, hour = np.unravel_index(np.argmin(self.readings), (7, 24))
        return int(day), int(hour)

    def __str__(self) -> str:
        return f"{self.sensor_id} ({self.location}, {self.__class__.__name__})"


class TemperatureSensor(Sensor):
    def alert_threshold(self) -> float:
        return 28.0

    def unit(self) -> str:
        return "°C"

    def to_fahrenheit(self) -> np.ndarray:
        return (self.readings * 9 / 5) + 32


class HumiditySensor(Sensor):
    def __init__(self, sensor_id: str, location: str, readings=None):
        super().__init__(sensor_id, location, readings)
        if readings is None:
            rng = np.random.default_rng(seed=100)
            base = np.linspace(40, 60, 7 * 24)
            noise = rng.normal(loc=0.0, scale=5.0, size=7 * 24)
            self.readings = (base + noise).reshape(7, 24)

    def alert_threshold(self) -> float:
        return 70.0

    def unit(self) -> str:
        return "%"


class Station:
    def __init__(self):
        self.sensors: dict[str, Sensor] = {}

    def __len__(self) -> int:
        return len(self.sensors)

    def add_sensor(self, sensor: Sensor):
        self.sensors[sensor.sensor_id] = sensor

    def get_sensor(self, sensor_id: str) -> Sensor:
        if sensor_id not in self.sensors:
            raise SensorNotFoundError(f"Sensor '{sensor_id}' not found.")
        return self.sensors[sensor_id]

    def unique_locations(self) -> set[str]:
        return {s.location for s in self.sensors.values()}

    def shared_locations(self) -> set[str]:
        temp_locs = {
            s.location
            for s in self.sensors.values()
            if isinstance(s, TemperatureSensor)
        }
        hum_locs = {
            s.location
            for s in self.sensors.values()
            if isinstance(s, HumiditySensor)
        }
        return temp_locs & hum_locs

    def rank(self) -> list[tuple[str, float]]:
        if not self.sensors:
            return []
        ids = list(self.sensors.keys())
        means = np.array([np.mean(s.readings) for s in self.sensors.values()])
        sorted_indices = np.argsort(means)[::-1]
        return [(ids[i], float(means[i])) for i in sorted_indices]


def add_sensor_action(station: Station):
    stype = input("Type (T for Temp / H for Hum): ").strip().upper()
    if stype not in ("T", "H"):
        print("Invalid type.")
        return
    sid = input("Sensor ID: ").strip()
    loc = input("Location: ").strip()
    sensor = (
        TemperatureSensor(sid, loc) if stype == "T" else HumiditySensor(sid, loc)
    )
    station.add_sensor(sensor)
    print(f"Added {sensor}.")
    print(f"Locations: {station.unique_locations()}")
    print(f"Locations with both: {station.shared_locations()}")


def summary_action(station: Station):
    sid = input("Sensor ID: ").strip()
    s = station.get_sensor(sid)
    min_v, max_v, mean_v = s.summary()
    peak_day, peak_hour = s.peak()
    low_day, low_hour = s.lowest()
    std_v = float(np.std(s.readings))
    print(
        f"Min: {min_v:.2f} (Day {low_day}, Hour {low_hour}), "
        f"Max: {max_v:.2f} (Day {peak_day}, Hour {peak_hour}), "
        f"Mean: {mean_v:.2f}, Std: {std_v:.2f} {s.unit()}"
    )


def daily_action(station: Station):
    sid = input("Sensor ID: ").strip()
    s = station.get_sensor(sid)
    daily_avgs = s.readings.mean(axis=1)
    hourly_avgs = s.readings.mean(axis=0)
    normalized = s.readings - daily_avgs.reshape(-1, 1)

    for day, avg in enumerate(daily_avgs):
        print(f"Day {day}: {avg:.2f} {s.unit()}")

    print(f"Hourly averages: {np.round(hourly_avgs, 2)}")
    print(f"Normalized mean check: {np.mean(normalized):.2f}")

    if isinstance(s, TemperatureSensor):
        f_daily = s.to_fahrenheit().mean(axis=1)
        print(f"Fahrenheit Daily Avgs: {np.round(f_daily, 2)}")


def alerts_action(station: Station):
    sid = input("Sensor ID: ").strip()
    s = station.get_sensor(sid)
    thresh = s.alert_threshold()
    mask = s.readings > thresh
    alert_count = int(np.sum(mask))
    status = np.where(mask, "ALERT", "NORMAL")
    d_idx, h_idx = np.where(mask)
    alerts = [
        (int(d), int(h), float(s.readings[d, h]), str(status[d, h]))
        for d, h in zip(d_idx, h_idx)
    ]
    print(f"Total alerts: {alert_count} (Threshold: {thresh:.2f})")
    for d, h, val, tag in alerts:
        print(f"  [{tag}] Day {d}, Hour {h}: {val:.2f} {s.unit()}")


def moving_average_action(station: Station):
    sid = input("Sensor ID: ").strip()
    s = station.get_sensor(sid)
    ma = np.convolve(s.readings.flatten(), np.ones(3) / 3, mode="valid")
    print(f"3-hour MA ({len(ma)} windows): {np.round(ma[:5], 2)}")


def rank_action(station: Station):
    ranked = station.rank()
    if not ranked:
        print("No sensors to rank.")
        return
    for sid, mean_val in ranked:
        print(f"{sid}: {mean_val:.2f}")


def compare_action(station: Station):
    sid1 = input("First Sensor ID: ").strip()
    sid2 = input("Second Sensor ID: ").strip()
    s1 = station.get_sensor(sid1)
    s2 = station.get_sensor(sid2)
    r = np.corrcoef(s1.readings.flatten(), s2.readings.flatten())[0, 1]
    print(f"Correlation: {r:.2f}")


def save_and_exit_action(station: Station):
    to_save = {
        f"{'Temp' if isinstance(s, TemperatureSensor) else 'Hum'}:{s.sensor_id}:{s.location}": s.readings
        for s in station.sensors.values()
    }
    np.savez("sensors.npz", **to_save)
    print("Saved and exiting.")


def load_sensors(station: Station):
    try:
        with np.load("sensors.npz", allow_pickle=True) as data:
            for key in data.files:
                s_type, s_id, loc = key.split(":")
                cls = TemperatureSensor if s_type == "Temp" else HumiditySensor
                s = cls(s_id, loc, readings=data[key])
                station.add_sensor(s)
    except FileNotFoundError:
        pass


def main():
    station = Station()
    load_sensors(station)

    while True:
        print(
            "\n1. Add sensor (temperature / humidity)\n"
            "2. Show sensor summary (min, max, mean, std)\n"
            "3. Show daily averages\n"
            "4. Show alerts (readings above threshold)\n"
            "5. Show 3-hour moving average\n"
            "6. Rank sensors by average\n"
            "7. Compare two sensors (correlation)\n"
            "8. Save and exit"
        )
        choice = input("Enter choice (1-8): ").strip()

        try:
            if choice == "1":
                add_sensor_action(station)
            elif choice == "2":
                summary_action(station)
            elif choice == "3":
                daily_action(station)
            elif choice == "4":
                alerts_action(station)
            elif choice == "5":
                moving_average_action(station)
            elif choice == "6":
                rank_action(station)
            elif choice == "7":
                compare_action(station)
            elif choice == "8":
                save_and_exit_action(station)
                break
            else:
                print("Invalid choice. Enter 1-8.")
        except (SensorNotFoundError, ValueError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()