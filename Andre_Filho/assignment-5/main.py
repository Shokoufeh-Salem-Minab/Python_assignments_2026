# Assignment 5 - Sensor Data Analyzer
# Andre Filho

import numpy as np

DATA_FILE = "sensors.npz"
SEED = 42
RNG = np.random.default_rng(SEED)


class SensorError(Exception):
    pass


class Sensor:
    def __init__(self, sensor_id, location, readings):
        self.sensor_id = sensor_id
        self.location = location
        self.readings = readings

    def alert_threshold(self):
        raise NotImplementedError

    def unit(self):
        raise NotImplementedError

    def extra_info(self):
        return ""

    def summary(self):
        return (self.readings.min(), self.readings.max(), self.readings.mean())

    def daily_average(self):
        return self.readings.mean(axis=1)

    def hourly_average(self):
        return self.readings.mean(axis=0)

    def peak(self):
        day, hour = np.unravel_index(np.argmax(self.readings), self.readings.shape)
        return (day, hour)

    def trough(self):
        day, hour = np.unravel_index(np.argmin(self.readings), self.readings.shape)
        return (day, hour)

    def normalized(self):
        return self.readings - self.daily_average().reshape(-1, 1)

    def deviation_extremes(self):
        normalized = self.normalized()
        return normalized.min(), normalized.max()

    def alerts(self):
        mask = self.readings > self.alert_threshold()
        return np.where(mask, "ALERT", "ok")

    def moving_average(self, hours=3):
        window = np.ones(hours) / hours
        return np.convolve(self.readings.flatten(), window, mode="valid")

    def __str__(self):
        low, high, mean = self.summary()
        return (f"{self.sensor_id} ({self.location}, {self.unit()}): "
                f"min={low:.2f} max={high:.2f} mean={mean:.2f}")


class TemperatureSensor(Sensor):
    def alert_threshold(self):
        return 30.0

    def unit(self):
        return "C"

    def extra_info(self):
        fahrenheit = self.readings * 9 / 5 + 32
        return f"average in Fahrenheit: {fahrenheit.mean():.2f}"


class HumiditySensor(Sensor):
    def alert_threshold(self):
        return 80.0

    def unit(self):
        return "%"


def generate_readings(base, amplitude, noise_std):
    hours = np.arange(24)
    daily_cycle = base + amplitude * np.sin(hours / 24 * 2 * np.pi)
    noise = RNG.normal(0, noise_std, size=7 * 24).reshape(7, 24)
    return daily_cycle + noise


class Station:
    def __init__(self):
        self.sensors = {}

    def __len__(self):
        return len(self.sensors)

    def add_sensor(self, sensor):
        if sensor.sensor_id in self.sensors:
            raise SensorError("That sensor ID is already used.")
        self.sensors[sensor.sensor_id] = sensor

    def get_sensor(self, sensor_id):
        try:
            return self.sensors[sensor_id]
        except KeyError:
            raise SensorError(f"There is no sensor with ID {sensor_id}.")

    def locations(self):
        return {sensor.location for sensor in self.sensors.values()}

    def mixed_locations(self):
        temp_locations = {s.location for s in self.sensors.values() if isinstance(s, TemperatureSensor)}
        humidity_locations = {s.location for s in self.sensors.values() if isinstance(s, HumiditySensor)}
        return temp_locations & humidity_locations

    def rank_by_average(self):
        ids = list(self.sensors)
        averages = np.array([self.sensors[sensor_id].readings.mean() for sensor_id in ids])
        order = np.argsort(averages)[::-1]
        return [(ids[i], averages[i]) for i in order]

    def compare(self, id1, id2):
        first = self.get_sensor(id1)
        second = self.get_sensor(id2)
        matrix = np.corrcoef(first.readings.flatten(), second.readings.flatten())
        return matrix[0, 1]

    def save(self):
        data = {}
        for sensor_id, sensor in self.sensors.items():
            data[sensor_id] = sensor.readings
            data[sensor_id + "__location"] = sensor.location
            data[sensor_id + "__kind"] = type(sensor).__name__
        np.savez(DATA_FILE, **data)

    def load(self):
        try:
            archive = np.load(DATA_FILE, allow_pickle=True)
        except FileNotFoundError:
            return
        ids = [key for key in archive.files if "__" not in key]
        for sensor_id in ids:
            location = str(archive[sensor_id + "__location"])
            kind = str(archive[sensor_id + "__kind"])
            readings = archive[sensor_id]
            cls = TemperatureSensor if kind == "TemperatureSensor" else HumiditySensor
            self.sensors[sensor_id] = cls(sensor_id, location, readings)


def ask_text(message):
    text = input(message).strip()
    if text == "":
        raise SensorError("This field cannot be empty.")
    return text


def add_sensor(station):
    kind = input("Temperature (1) or humidity (2) sensor? ")
    if kind not in ("1", "2"):
        raise SensorError("Please choose 1 or 2.")
    sensor_id = ask_text("Sensor ID: ")
    location = ask_text("Location: ")
    if kind == "1":
        readings = generate_readings(base=20.0, amplitude=8.0, noise_std=1.5)
        sensor = TemperatureSensor(sensor_id, location, readings)
    else:
        readings = generate_readings(base=50.0, amplitude=15.0, noise_std=5.0)
        sensor = HumiditySensor(sensor_id, location, readings)
    station.add_sensor(sensor)
    print("Sensor added.")


def show_summary(station):
    sensor = station.get_sensor(ask_text("Sensor ID: "))
    low, high, mean = sensor.summary()
    peak_day, peak_hour = sensor.peak()
    low_day, low_hour = sensor.trough()
    dev_min, dev_max = sensor.deviation_extremes()
    print(sensor)
    print(f"std: {sensor.readings.std():.2f}")
    print(f"peak reading on day {peak_day + 1}, hour {peak_hour}")
    print(f"lowest reading on day {low_day + 1}, hour {low_hour}")
    print(f"deviation from daily mean: {dev_min:.2f} to {dev_max:.2f}")
    extra = sensor.extra_info()
    if extra:
        print(extra)


def show_daily_averages(station):
    sensor = station.get_sensor(ask_text("Sensor ID: "))
    for day, average in enumerate(sensor.daily_average(), 1):
        print(f"day {day}: {average:.2f}")
    print("hourly pattern:", np.round(sensor.hourly_average(), 2))


def show_alerts(station):
    sensor = station.get_sensor(ask_text("Sensor ID: "))
    marks = sensor.alerts()
    count = int((marks == "ALERT").sum())
    print(f"{count} alert readings above {sensor.alert_threshold():.2f} {sensor.unit()}")
    alert_hours = [(day + 1, hour) for day, hour in np.argwhere(marks == "ALERT")]
    for day, hour in alert_hours:
        print(f"day {day}, hour {hour}: ALERT")


def show_moving_average(station):
    sensor = station.get_sensor(ask_text("Sensor ID: "))
    print(np.round(sensor.moving_average(), 2))


def show_ranking(station):
    if len(station) == 0:
        print("There are no sensors yet.")
        return
    for place, (sensor_id, average) in enumerate(station.rank_by_average(), 1):
        print(f"{place}. {sensor_id}: {average:.2f}")
    print("Locations:", ", ".join(sorted(station.locations())))
    mixed = station.mixed_locations()
    if mixed:
        print("Locations with both sensor types:", ", ".join(sorted(mixed)))
    else:
        print("No location has both sensor types.")


def show_comparison(station):
    id1 = ask_text("First sensor ID: ")
    id2 = ask_text("Second sensor ID: ")
    correlation = station.compare(id1, id2)
    print(f"correlation: {correlation:.2f}")


def print_menu():
    print()
    print("========== SENSOR STATION ==========")
    print("1. Add sensor (temperature / humidity)")
    print("2. Show sensor summary")
    print("3. Show daily averages")
    print("4. Show alerts")
    print("5. Show 3-hour moving average")
    print("6. Rank sensors by average")
    print("7. Compare two sensors")
    print("8. Save and exit")


def main():
    station = Station()
    station.load()

    while True:
        print_menu()
        try:
            choice = input("Choose an option: ").strip()
        except EOFError:
            choice = "8"

        try:
            if choice == "1":
                add_sensor(station)
            elif choice == "2":
                show_summary(station)
            elif choice == "3":
                show_daily_averages(station)
            elif choice == "4":
                show_alerts(station)
            elif choice == "5":
                show_moving_average(station)
            elif choice == "6":
                show_ranking(station)
            elif choice == "7":
                show_comparison(station)
            elif choice == "8":
                station.save()
                print("Data saved. Goodbye!")
                break
            else:
                print("Invalid option, please try again.")
        except SensorError as error:
            print("Error:", error)


main()
