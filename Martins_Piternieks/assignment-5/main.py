import os

import numpy as np

# ----- Global Settings -----
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sensors.npz")
DAYS = 7
HOURS = 24


# ----- Custom Exceptions -----
class SensorNotFoundError(Exception):
    """Raised when a sensor ID does not exist in the station."""


class DuplicateSensorError(Exception):
    """Raised when a sensor ID is already used."""


# ----- Sensor Base Class -----
class Sensor:
    def __init__(self, sensor_id, location, readings=None, seed=0):
        self.sensor_id = sensor_id
        self.location = location
        # readings is a NumPy array with shape (7 days, 24 hours)
        if readings is None:
            readings = self.simulate_readings(seed)
        self.readings = readings

    # values that the subclasses change
    def kind(self):
        return "generic"

    def unit(self):
        return ""

    def alert_threshold(self):
        return 0.0

    def base_value(self):
        return 0.0

    def daily_swing(self):
        return 0.0

    def simulate_readings(self, seed):
        rng = np.random.default_rng(seed)
        # 7 * 24 = 168 random values around the base value
        noise = rng.normal(loc=self.base_value(), scale=2.0, size=DAYS * HOURS)
        table = noise.reshape(DAYS, HOURS)
        # a smooth day/night cycle: one value for each of the 24 hours
        cycle = self.daily_swing() * np.sin(np.linspace(0, 2 * np.pi, HOURS, endpoint=False))
        # broadcasting: the (24,) cycle is added to every one of the 7 rows
        return table + cycle

    # ----- Statistics -----
    def summary(self):
        # returns a tuple: (min, max, mean)
        return self.readings.min(), self.readings.max(), self.readings.mean()

    def std(self):
        return self.readings.std()

    def peak(self):
        # argmax gives a position in the flattened array (0..167)
        # divmod turns it into a tuple: (day, hour)
        return divmod(int(self.readings.argmax()), HOURS)

    def lowest(self):
        return divmod(int(self.readings.argmin()), HOURS)

    def daily_averages(self):
        return self.readings.mean(axis=1)  # one value per day -> shape (7,)

    def hourly_averages(self):
        return self.readings.mean(axis=0)  # one value per hour -> shape (24,)

    def normalized(self):
        # subtract each day's mean from that day's readings (broadcasting)
        return self.readings - self.daily_averages().reshape(DAYS, 1)

    # ----- Alerts -----
    def alert_mask(self):
        return self.readings > self.alert_threshold()  # True / False array

    def alert_records(self):
        days, hours = np.where(self.alert_mask())
        values = self.readings[self.alert_mask()]
        return [(int(d), int(h), float(v)) for d, h, v in zip(days, hours, values)]

    # ----- Moving average -----
    def moving_average(self, day, window=3):
        weights = np.ones(window) / window
        return np.convolve(self.readings[day], weights, mode="valid")

    def __str__(self):
        return f"[{self.sensor_id}] {self.kind()} sensor at {self.location} ({self.unit()})"


# ----- TemperatureSensor (inherits from Sensor) -----
class TemperatureSensor(Sensor):
    def kind(self):
        return "temperature"

    def unit(self):
        return "°C"

    def alert_threshold(self):
        return 25.0

    def base_value(self):
        return 20.0

    def daily_swing(self):
        return 4.0  # warmer during the day

    def to_fahrenheit(self):
        # vectorized: works on the whole array at once, no loop
        return self.readings * 9 / 5 + 32


# ----- HumiditySensor (inherits from Sensor) -----
class HumiditySensor(Sensor):
    def kind(self):
        return "humidity"

    def unit(self):
        return "%"

    def alert_threshold(self):
        return 65.0

    def base_value(self):
        return 55.0

    def daily_swing(self):
        return -10.0  # drier during the day


SENSOR_TYPES = {"temperature": TemperatureSensor, "humidity": HumiditySensor}


# ----- Station Class -----
class Station:
    def __init__(self):
        # sensors are stored as {sensor_id: Sensor}
        self.sensors = {}

    def __len__(self):
        return len(self.sensors)

    def add_sensor(self, sensor):
        if sensor.sensor_id in self.sensors:
            raise DuplicateSensorError(f"Sensor '{sensor.sensor_id}' already exists.")
        self.sensors[sensor.sensor_id] = sensor

    def get_sensor(self, sensor_id):
        if sensor_id not in self.sensors:
            raise SensorNotFoundError(f"Sensor '{sensor_id}' was not found.")
        return self.sensors[sensor_id]

    def next_seed(self):
        return 100 + len(self.sensors)

    # ----- Sets -----
    def locations(self, kind=None):
        return {s.location for s in self.sensors.values() if kind is None or s.kind() == kind}

    def shared_locations(self):
        # set intersection: places that have BOTH sensor types
        return self.locations("temperature") & self.locations("humidity")

    # ----- Ranking and Correlation -----
    def ranking(self):
        ids = np.array(list(self.sensors.keys()))
        averages = np.array([s.readings.mean() for s in self.sensors.values()])
        order = np.argsort(averages)[::-1]  # biggest average first
        return ids[order], averages[order]

    def correlation(self, id_a, id_b):
        a = self.get_sensor(id_a).readings.ravel()
        b = self.get_sensor(id_b).readings.ravel()
        return np.corrcoef(a, b)[0, 1]

    # ----- Saving and Loading -----
    def save(self, path):
        sensors = list(self.sensors.values())
        readings = np.array([s.readings for s in sensors]) if sensors else np.empty((0, DAYS, HOURS))
        np.savez(
            path,
            ids=np.array([s.sensor_id for s in sensors], dtype=str),
            kinds=np.array([s.kind() for s in sensors], dtype=str),
            locations=np.array([s.location for s in sensors], dtype=str),
            readings=readings,
        )

    def load(self, path):
        # raises FileNotFoundError if the file is missing
        with np.load(path) as data:
            rows = zip(data["ids"], data["kinds"], data["locations"], data["readings"])
            for sensor_id, kind, location, readings in rows:
                sensor_class = SENSOR_TYPES[str(kind)]
                self.add_sensor(sensor_class(str(sensor_id), str(location), readings))


# ----- Input Helpers -----
def ask_text(prompt):
    text = input(prompt).strip()
    if not text:
        raise ValueError("Input cannot be empty.")
    return text


def ask_number(prompt, low, high):
    number = int(input(prompt))  # raises ValueError for text like "abc"
    if number < low or number > high:
        raise ValueError(f"Please enter a number from {low} to {high}.")
    return number


def ask_sensor(station, prompt="Sensor ID: "):
    return station.get_sensor(input(prompt).strip())


def hour_label(hour):
    return f"{hour:02d}:00"


# ----- Menu Actions -----
def add_sensor(station):
    kind = ask_text("Type (t = temperature, h = humidity): ").lower()
    if kind not in ("t", "h"):
        raise ValueError("Type must be 't' or 'h'.")
    sensor_id = ask_text("Sensor ID: ")
    location = ask_text("Location: ")
    sensor_class = TemperatureSensor if kind == "t" else HumiditySensor
    station.add_sensor(sensor_class(sensor_id, location, seed=station.next_seed()))
    print(f"Added: {station.get_sensor(sensor_id)}")


def show_summary(station):
    sensor = ask_sensor(station)
    low, high, mean = sensor.summary()  # tuple unpacking
    day, hour = sensor.peak()
    low_day, low_hour = sensor.lowest()
    unit = sensor.unit()
    print(f"\n{sensor}")
    print(f"Min:  {low:.2f} {unit}  (day {low_day + 1}, {hour_label(low_hour)})")
    print(f"Max:  {high:.2f} {unit}  (day {day + 1}, {hour_label(hour)})")
    print(f"Mean: {mean:.2f} {unit}")
    print(f"Std:  {sensor.std():.2f} {unit}")
    if isinstance(sensor, TemperatureSensor):
        fahrenheit = sensor.to_fahrenheit()
        print(f"In °F -> min {fahrenheit.min():.2f}, max {fahrenheit.max():.2f}, mean {fahrenheit.mean():.2f}")


def show_daily_averages(station):
    sensor = ask_sensor(station)
    averages = np.round(sensor.daily_averages(), 2)
    biggest_jump = np.round(sensor.normalized().max(axis=1), 2)
    print(f"\nDaily report for {sensor}")
    for day in range(DAYS):
        print(f"Day {day + 1}: average {averages[day]:.2f} {sensor.unit()}, "
              f"highest point {biggest_jump[day]:.2f} above that day's average")
    busiest_hour = int(sensor.hourly_averages().argmax())
    print(f"On average the highest hour is {hour_label(busiest_hour)}")


def show_alerts(station):
    sensor = ask_sensor(station)
    records = sensor.alert_records()
    unit = sensor.unit()
    print(f"\nThreshold: {sensor.alert_threshold():.2f} {unit}")
    print(f"Alert readings: {len(records)} of {sensor.readings.size}")
    lines = [f"ALERT  day {d + 1}, {hour_label(h)} -> {v:.2f} {unit}" for d, h, v in records]
    for line in lines:
        print(line)


def show_moving_average(station):
    sensor = ask_sensor(station)
    day = ask_number(f"Day (1-{DAYS}): ", 1, DAYS) - 1
    averages = np.round(sensor.moving_average(day), 2)
    print(f"\n3-hour moving average for day {day + 1} ({sensor.unit()}):")
    for start, value in enumerate(averages):
        print(f"{hour_label(start)} - {hour_label(start + 2)}: {value:.2f}")


def show_ranking(station):
    if len(station) == 0:
        print("There are no sensors yet.")
        return
    ids, averages = station.ranking()
    print("\nSensors ranked by average value:")
    for place, (sensor_id, average) in enumerate(zip(ids, averages), start=1):
        sensor = station.get_sensor(str(sensor_id))
        print(f"{place}. {sensor_id} ({sensor.location}): {average:.2f} {sensor.unit()}")


def compare_sensors(station):
    id_a = ask_text("First sensor ID: ")
    id_b = ask_text("Second sensor ID: ")
    value = station.correlation(id_a, id_b)
    print(f"Correlation between {id_a} and {id_b}: {value:.2f}")
    if value > 0.5:
        print("They usually go up and down together.")
    elif value < -0.5:
        print("When one goes up, the other usually goes down.")
    else:
        print("There is no strong connection between them.")


def show_locations(station):
    print(f"\nStation has {len(station)} sensors.")
    print(f"Locations: {', '.join(sorted(station.locations())) or '-'}")
    shared = station.shared_locations()
    print(f"With both temperature and humidity: {', '.join(sorted(shared)) or '-'}")


# ----- Start-Up -----
def add_demo_sensors(station):
    demo = [
        TemperatureSensor("T1", "Kitchen", seed=1),
        HumiditySensor("H1", "Kitchen", seed=2),
        TemperatureSensor("T2", "Garage", seed=3),
        HumiditySensor("H2", "Bathroom", seed=4),
    ]
    for sensor in demo:
        station.add_sensor(sensor)


def load_station():
    station = Station()
    try:
        station.load(DATA_FILE)
        print(f"Loaded {len(station)} sensors from {os.path.basename(DATA_FILE)}.")
    except FileNotFoundError:
        print("No saved data found. Starting with demo sensors.")
        add_demo_sensors(station)
    return station


def print_menu():
    print("\n===== SENSOR DATA ANALYZER =====")
    print("1. Add sensor (temperature / humidity)")
    print("2. Show sensor summary (min, max, mean, std)")
    print("3. Show daily averages")
    print("4. Show alerts (readings above threshold)")
    print("5. Show 3-hour moving average")
    print("6. Rank sensors by average")
    print("7. Compare two sensors (correlation)")
    print("8. Save and exit")


ACTIONS = {
    "1": add_sensor,
    "2": show_summary,
    "3": show_daily_averages,
    "4": show_alerts,
    "5": show_moving_average,
    "6": show_ranking,
    "7": compare_sensors,
}


def main():
    station = load_station()
    show_locations(station)

    running = True
    while running:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "8":
            station.save(DATA_FILE)
            print("Data saved. Goodbye!")
            running = False
        elif choice in ACTIONS:
            try:
                ACTIONS[choice](station)
            except (ValueError, SensorNotFoundError, DuplicateSensorError) as error:
                print(f"Error: {error}")
        else:
            print("Invalid choice, please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
