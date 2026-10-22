import os
import zipfile
import zlib

import numpy as np

# file where all sensors are saved
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "station_data.npz")
DAYS = 7
HOURS = 24


# custom exceptions
class StationError(Exception):
    # parent class for all my errors
    pass


class SensorNotFoundError(StationError):
    # unknown sensor id
    pass


class DuplicateSensorError(StationError):
    # sensor id already used
    pass


class InvalidInputError(StationError):
    # other wrong input (empty text, wrong menu choice, bad day)
    pass


class DataFileError(StationError):
    # saved data file cannot be used
    pass


class DataFileMissingError(DataFileError):
    # saved data file does not exist
    pass


def simulate_readings(base, swing, noise_std, seed):
    # makes 7 days x 24 hours of fake readings
    rng = np.random.default_rng(seed)  # fixed seed -> same data every time
    hours = np.arange(HOURS)  # 0, 1, ..., 23
    daily_cycle = swing * np.sin(2 * np.pi * (hours - 9) / HOURS)
    week_trend = np.linspace(0, 1, DAYS).reshape(DAYS, 1)  # slow change over the week
    noise = rng.normal(0, noise_std, DAYS * HOURS).reshape(DAYS, HOURS)
    # broadcasting: (7, 1) + (24,) + (7, 24) -> (7, 24)
    return base + week_trend + daily_cycle + noise


class Sensor:
    kind = "Sensor"
    base_value = 0.0
    daily_swing = 0.0
    noise_std = 1.0

    def __init__(self, sensor_id, location, readings):
        self.sensor_id = sensor_id
        self.location = location
        try:
            # readings are always a 2D array with shape (7, 24)
            self.readings = np.array(readings, dtype=float).reshape(DAYS, HOURS)
        except ValueError:
            raise InvalidInputError(f"Readings must have {DAYS * HOURS} values.") from None

    @classmethod
    def create(cls, sensor_id, location):
        # new sensor with simulated readings, seed comes from the id
        seed = zlib.crc32(sensor_id.encode("utf-8"))
        readings = simulate_readings(cls.base_value, cls.daily_swing, cls.noise_std, seed)
        return cls(sensor_id, location, readings)

    def unit(self):
        return ""

    def alert_threshold(self):
        return float("inf")

    def extra_summary(self):
        # subclasses can add one more line to the summary
        return ""

    def average(self):
        return self.readings.mean()

    def summary(self):
        # returns a tuple (min, max, mean)
        return self.readings.min(), self.readings.max(), self.readings.mean()

    def std(self):
        return self.readings.std()

    def peak(self):
        # returns a tuple (day, hour) of the highest reading
        day, hour = np.unravel_index(np.argmax(self.readings), self.readings.shape)
        return int(day), int(hour)

    def lowest(self):
        # returns a tuple (day, hour) of the lowest reading
        day, hour = np.unravel_index(np.argmin(self.readings), self.readings.shape)
        return int(day), int(hour)

    def daily_averages(self):
        # one average for each day (axis=1 goes across the hours)
        return self.readings.mean(axis=1)

    def hourly_averages(self):
        # one average for each hour (axis=0 goes across the days)
        return self.readings.mean(axis=0)

    def normalized(self):
        # subtract the daily mean from every reading, keepdims lets broadcasting work
        return self.readings - self.readings.mean(axis=1, keepdims=True)

    def alert_mask(self):
        # True where the reading is above the threshold
        return self.readings > self.alert_threshold()

    def status(self):
        # "ALERT" for readings above the threshold, "ok" for the others
        return np.where(self.alert_mask(), "ALERT", "ok")

    def alert_records(self):
        # list comprehension: (day, hour, value) for every alert reading
        days, hours = np.where(self.alert_mask())
        values = self.readings[self.alert_mask()]
        return [(int(d), int(h), float(v)) for d, h, v in zip(days, hours, values)]

    def moving_average(self, day):
        # 3-hour moving average of one day, 24 values -> 22 values
        window = np.ones(3) / 3
        return np.convolve(self.readings[day], window, mode="valid")

    def __str__(self):
        return (
            f"[{self.sensor_id}] {self.kind} sensor at {self.location} | "
            f"mean {self.average():.2f} {self.unit()} | "
            f"alert above {self.alert_threshold():.2f} {self.unit()}"
        )


class TemperatureSensor(Sensor):
    kind = "Temperature"
    base_value = 20.0
    daily_swing = 6.0
    noise_std = 1.5

    def unit(self):
        return "°C"

    def alert_threshold(self):
        return 25.0

    def to_fahrenheit(self):
        # no loop, the whole array is converted at once
        return self.readings * 9 / 5 + 32

    def extra_summary(self):
        return f"Mean in Fahrenheit: {self.to_fahrenheit().mean():.2f} °F"


class HumiditySensor(Sensor):
    kind = "Humidity"
    base_value = 55.0
    daily_swing = -15.0  # humidity is lower in the afternoon
    noise_std = 4.0

    def unit(self):
        return "%"

    def alert_threshold(self):
        return 65.0


# used when loading, picks the class by the saved type
SENSOR_TYPES = {"temperature": TemperatureSensor, "humidity": HumiditySensor}


class Station:
    def __init__(self):
        self.sensors = {}  # {sensor_id: Sensor}

    def __len__(self):
        # number of sensors
        return len(self.sensors)

    def check_id_free(self, sensor_id):
        # ids must be unique
        if sensor_id in self.sensors:
            raise DuplicateSensorError(f"Sensor ID '{sensor_id}' already exists.")

    def add_sensor(self, sensor):
        self.check_id_free(sensor.sensor_id)
        self.sensors[sensor.sensor_id] = sensor

    def get_sensor(self, sensor_id):
        # find sensor by id, error if it does not exist
        try:
            return self.sensors[sensor_id]
        except KeyError:
            raise SensorNotFoundError(f"No sensor with ID '{sensor_id}'.") from None

    def locations(self):
        # set of unique locations
        return {sensor.location for sensor in self.sensors.values()}

    def locations_with_both(self):
        # set intersection: locations that have a temperature AND a humidity sensor
        temp = {s.location for s in self.sensors.values() if isinstance(s, TemperatureSensor)}
        humid = {s.location for s in self.sensors.values() if isinstance(s, HumiditySensor)}
        return temp & humid

    def ranking(self):
        # sensors sorted by average, highest first
        sensors = list(self.sensors.values())
        averages = np.array([s.average() for s in sensors])
        order = np.argsort(averages)[::-1]  # argsort is lowest first, so reverse it
        return [(sensors[i], averages[i]) for i in order]

    def save(self, path):
        # all sensors go into one .npz file
        sensors = list(self.sensors.values())
        np.savez(
            path,
            ids=np.array([s.sensor_id for s in sensors], dtype=str),
            locations=np.array([s.location for s in sensors], dtype=str),
            kinds=np.array([s.kind.lower() for s in sensors], dtype=str),
            readings=np.array([s.readings for s in sensors]).reshape(-1, DAYS, HOURS),
        )

    @classmethod
    def from_data(cls, data):
        # build a station from the arrays that were loaded from the file
        station = cls()
        ids = data["ids"].tolist()
        locations = data["locations"].tolist()
        kinds = data["kinds"].tolist()
        for sensor_id, location, kind, readings in zip(ids, locations, kinds, data["readings"]):
            station.add_sensor(SENSOR_TYPES[kind](sensor_id, location, readings))
        return station

    @classmethod
    def load(cls, path):
        # read the station from the .npz file
        try:
            with np.load(path) as data:
                return cls.from_data(data)
        except FileNotFoundError:
            raise DataFileMissingError(f"No saved data found at '{path}'.") from None
        except (OSError, ValueError, KeyError, EOFError, zipfile.BadZipFile, StationError) as error:
            backup_bad_file(path)
            raise DataFileError(f"Saved data could not be read ({error}).") from None


def backup_bad_file(path):
    # keep the broken file as .bak so it is not overwritten
    try:
        os.replace(path, path + ".bak")
    except OSError:
        pass


def ask(prompt):
    return input(prompt).strip()


def ask_required(prompt):
    # input that cannot be empty
    text = ask(prompt)
    if not text:
        raise InvalidInputError("This field cannot be empty.")
    return text


def ask_day():
    # asks for a day 1-7, returns it as an index 0-6
    text = ask(f"Day (1-{DAYS}): ")
    try:
        day = int(text)
    except ValueError:
        raise InvalidInputError("Day must be a whole number.") from None
    if not 1 <= day <= DAYS:
        raise InvalidInputError(f"Day must be between 1 and {DAYS}.")
    return day - 1


def describe_correlation(value):
    # words for the correlation number
    strength = "strong" if abs(value) >= 0.7 else "moderate" if abs(value) >= 0.3 else "weak"
    direction = "positive" if value > 0 else "negative"
    return f"{strength} {direction} correlation"


# menu option 1
def add_sensor_action(station):
    kind = ask("Sensor type - (t)emperature or (h)umidity: ").lower()
    if kind not in ("t", "h"):
        raise InvalidInputError("Type must be 't' or 'h'.")
    sensor_id = ask_required("Sensor ID: ")
    station.check_id_free(sensor_id)
    location = ask_required("Location: ")
    sensor_class = TemperatureSensor if kind == "t" else HumiditySensor
    sensor = sensor_class.create(sensor_id, location)
    station.add_sensor(sensor)
    print("Added (7 days x 24 hours of simulated readings):")
    print(sensor)


# menu option 2
def show_summary_action(station):
    sensor = station.get_sensor(ask_required("Sensor ID: "))
    low, high, mean = sensor.summary()  # tuple unpacking
    peak_day, peak_hour = sensor.peak()
    low_day, low_hour = sensor.lowest()
    unit = sensor.unit()
    print(sensor)
    print(f"Min: {low:.2f} {unit} (day {low_day + 1}, {low_hour:02d}:00)")
    print(f"Max: {high:.2f} {unit} (day {peak_day + 1}, {peak_hour:02d}:00)")
    print(f"Mean: {mean:.2f} {unit}")
    print(f"Std: {sensor.std():.2f} {unit}")
    if sensor.extra_summary():
        print(sensor.extra_summary())


# menu option 3
def show_daily_action(station):
    sensor = station.get_sensor(ask_required("Sensor ID: "))
    averages = sensor.daily_averages()
    swings = np.abs(sensor.normalized()).max(axis=1)  # biggest difference from the daily mean
    print(f"Daily report for {sensor.sensor_id}:")
    for day in range(DAYS):
        print(f"Day {day + 1}: average {averages[day]:.2f} {sensor.unit()} | "
              f"biggest difference from it {swings[day]:.2f}")
    hour = int(np.argmax(sensor.hourly_averages()))
    print(f"Highest hourly average: {sensor.hourly_averages()[hour]:.2f} {sensor.unit()} "
          f"at {hour:02d}:00")


# menu option 4
def show_alerts_action(station):
    sensor = station.get_sensor(ask_required("Sensor ID: "))
    records = sensor.alert_records()
    per_day = (sensor.status() == "ALERT").sum(axis=1)  # alerts in each day
    print(f"Threshold: {sensor.alert_threshold():.2f} {sensor.unit()}")
    print(f"Alerts: {len(records)} of {sensor.readings.size} readings")
    for day in range(DAYS):
        print(f"Day {day + 1}: {per_day[day]} alert(s)")
    for day, hour, value in records[:10]:
        print(f"  day {day + 1}, {hour:02d}:00 -> {value:.2f} {sensor.unit()}")
    if len(records) > 10:
        print(f"  ... and {len(records) - 10} more")


# menu option 5
def show_moving_average_action(station):
    sensor = station.get_sensor(ask_required("Sensor ID: "))
    day = ask_day()
    averages = sensor.moving_average(day)
    print(f"3-hour moving average, day {day + 1} ({len(averages)} values, "
          f"first value = hours 0-2):")
    print(np.array2string(averages, formatter={"float_kind": "{:.2f}".format}))


# menu option 6
def show_ranking_action(station):
    if len(station) == 0:
        print("No sensors yet.")
        return
    print("Sensors ranked by average (highest first):")
    for place, (sensor, average) in enumerate(station.ranking(), start=1):
        print(f"{place}. {sensor.sensor_id} ({sensor.kind}, {sensor.location}) - "
              f"{average:.2f} {sensor.unit()}")
    print("Locations: " + ", ".join(sorted(station.locations())))
    both = station.locations_with_both()
    print("Locations with temperature and humidity: " + (", ".join(sorted(both)) or "none"))


# menu option 7
def compare_sensors_action(station):
    first = station.get_sensor(ask_required("First sensor ID: "))
    second = station.get_sensor(ask_required("Second sensor ID: "))
    # corrcoef gives a 2x2 matrix, [0, 1] is the correlation of the two sensors
    value = np.corrcoef(first.readings.ravel(), second.readings.ravel())[0, 1]
    if np.isnan(value):
        print("Correlation cannot be calculated (a sensor has no variation).")
        return
    print(f"Correlation of {first.sensor_id} and {second.sensor_id}: {value:.2f} "
          f"({describe_correlation(value)})")


# menu number -> function
ACTIONS = {
    "1": add_sensor_action,
    "2": show_summary_action,
    "3": show_daily_action,
    "4": show_alerts_action,
    "5": show_moving_average_action,
    "6": show_ranking_action,
    "7": compare_sensors_action,
}

MENU = """
===== Sensor Data Analyzer =====
1. Add sensor (temperature / humidity)
2. Show sensor summary (min, max, mean, std)
3. Show daily averages
4. Show alerts (readings above threshold)
5. Show 3-hour moving average
6. Rank sensors by average
7. Compare two sensors (correlation)
8. Save and exit"""


def load_station():
    # load saved data when the program starts
    try:
        station = Station.load(DATA_FILE)
        print(f"Loaded {len(station)} sensor(s).")
    except DataFileMissingError:
        print("No saved data yet, starting with an empty station.")
        station = Station()
    except DataFileError as error:
        print(f"{error} Starting with an empty station.")
        station = Station()
    return station


def save_data(station):
    try:
        station.save(DATA_FILE)
        print(f"Saved {len(station)} sensor(s) to {DATA_FILE}.")
    except OSError as error:
        print(f"Error: could not save data ({error}).")


def run_choice(station, choice):
    # runs one menu choice, returns False when the user picks 8 (exit)
    if choice == "8":
        return False
    if choice not in ACTIONS:
        raise InvalidInputError("Please enter a number from 1 to 8.")
    ACTIONS[choice](station)
    return True


def main():
    station = load_station()
    running = True
    # main menu loop, runs until the user chooses 8
    while running:
        print(MENU)
        try:
            running = run_choice(station, ask("Choose an option (1-8): "))
        except StationError as error:
            # any of my errors: show message and go back to the menu
            print(f"Error: {error}")
        except (EOFError, KeyboardInterrupt):
            # Ctrl+C or closed input: save and exit
            print("\nInput closed. Saving and exiting.")
            running = False
    # save everything when the program ends
    save_data(station)


if __name__ == "__main__":
    main()
