
import numpy as np

class InvalidSensor(Exception):
    pass

class Sensor:
    def __init__(self, sensor_id, location, readings):
        self.sensor_id = sensor_id
        self.location = location
        self.readings = readings.reshape(7, 24)

    def alert_threshold(self):
        return 30

    def unit(self):
        return ""

    def summary(self):
        return np.min(self.readings), np.max(self.readings), np.mean(self.readings)

    def __str__(self):
        return f"{self.sensor_id}: {self.location}, {self.unit()}"

class TemperatureSensor(Sensor):
    def alert_threshold(self):
        return 30

    def unit(self):
        return "Celsius"

    def fahrenheit(self):
        return self.readings * 9 / 5 + 32

class HumiditySensor(Sensor):
    def alert_threshold(self):
        return 70

    def unit(self):
        return "%"

class Station:
    def __init__(self):
        self.sensors = {}

    def __len__(self):
        return len(self.sensors)

    def get_sensor(self, sid):
        if sid not in self.sensors:
            raise InvalidSensor("Sensor ID not found")
        return self.sensors[sid]

    def locations(self):
        return {s.location for s in self.sensors.values()}

    def save(self):
        data = {}
        for sid, s in self.sensors.items():
            data[sid] = [s.location, s.unit(), s.readings]
        np.savez("sensors.npz", **{
            sid: np.array([loc, unit], dtype=object)
            for sid, (loc, unit) in data.items()
        }, **{
            sid + "_readings": readings
            for sid, (readings) in data.items()
        })

    def load(self):
        try:
            data = np.load("sensors.npz", allow_pickle=True)
            for sid in data.files:
                if sid.endswith("_readings"):
                    continue
                loc, unit = data[sid]
                readings = data[sid + "_readings"]
                if unit == "Celsius":
                    self.sensors[sid] = TemperatureSensor(sid, loc, readings)
                else:
                    self.sensors[sid] = HumiditySensor(sid, loc, readings)
        except FileNotFoundError:
            pass

def main():
    station = Station()
    station.load()

    while True:
        print("\n1. Add sensor\n2. Show summary\n3. Daily averages")
        print("4. Show alerts\n5. Moving average\n6. Rank sensors")
        print("7. Compare sensors\n8. Save and exit")

        try:
            choice = input("Choose: ")

            if choice == "1":
                sid = input("Sensor ID: ")
                if sid in station.sensors:
                    raise InvalidSensor("Sensor ID already exists")
                location = input("Location: ")
                kind = input("Temperature or humidity? ").lower()

                if kind not in ("temperature", "humidity"):
                    raise ValueError("Invalid sensor type")

                rng = np.random.default_rng(42 + len(station))
                base = 20 if kind == "temperature" else 60
                readings = rng.normal(base, 5, 168).reshape(7, 24)
                readings = np.array(readings)

                if kind == "temperature":
                    sensor = TemperatureSensor(sid, location, readings)
                else:
                    sensor = HumiditySensor(sid, location, readings)

                station.sensors[sid] = sensor
                print("Sensor added")

            elif choice == "2":
                s = station.get_sensor(input("Sensor ID: "))
                minimum, maximum, average = s.summary()
                peak = np.unravel_index(np.argmax(s.readings), s.readings.shape)
                low = np.unravel_index(np.argmin(s.readings), s.readings.shape)
                print(f"Min: {minimum:.2f}, Max: {maximum:.2f}")
                print(f"Mean: {average:.2f}, Std: {np.std(s.readings):.2f}")
                print("Peak day and hour:", peak)
                print("Lowest day and hour:", low)
                print("Fahrenheit:", np.round(s.fahrenheit(), 2) if isinstance(s, TemperatureSensor) else "N/A")
                print("Normalized:", np.round(s.readings - s.readings.mean(axis=1, keepdims=True), 2))

            elif choice == "3":
                s = station.get_sensor(input("Sensor ID: "))
                for day, avg in enumerate(s.readings.mean(axis=1), 1):
                    print(f"Day {day}: {avg:.2f}")
                print("Hourly averages:", np.round(s.readings.mean(axis=0), 2))

            elif choice == "4":
                s = station.get_sensor(input("Sensor ID: "))
                mask = s.readings > s.alert_threshold()
                alerts = [(int(d + 1), int(h), round(float(s.readings[d, h]), 2))
                          for d, h in zip(*np.where(mask))]
                print("Alert count:", np.count_nonzero(mask))
                print("Alerts:", alerts)
                print(np.where(mask, "alert", "normal"))

            elif choice == "5":
                s = station.get_sensor(input("Sensor ID: "))
                print(np.round(np.convolve(s.readings.ravel(), np.ones(3) / 3, mode="valid"), 2))

            elif choice == "6":
                ranking = sorted(station.sensors.values(), key=lambda s: np.mean(s.readings), reverse=True)
                for s in ranking:
                    print(s.sensor_id, round(float(np.mean(s.readings)), 2))

            elif choice == "7":
                s1 = station.get_sensor(input("First sensor ID: "))
                s2 = station.get_sensor(input("Second sensor ID: "))
                print("Correlation:", round(float(np.corrcoef(s1.readings.ravel(), s2.readings.ravel())[0, 1]), 2))
                temp = {s.location for s in station.sensors.values() if isinstance(s, TemperatureSensor)}
                hum = {s.location for s in station.sensors.values() if isinstance(s, HumiditySensor)}
                print("Common locations:", temp & hum)

            elif choice == "8":
                station.save()
                print("Saved")
                break

            else:
                print("Invalid choice")

        except (ValueError, InvalidSensor, TypeError) as e:
            print("Error:", e)

    station.save()

if __name__ == "__main__":
    main()
