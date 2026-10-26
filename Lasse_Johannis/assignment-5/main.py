# Homework 5 - Sensor Data Analyzer
# Lasse Johannis

import numpy as np

data_file = "station_data.npz"


# ----- custom exceptions -----
class SensorNotFoundError(Exception):
    pass


class InvalidDayError(Exception):
    pass


# ----- sensor classes -----
class Sensor:
    def __init__(self, sensor_id, location, readings):
        self.sensor_id = sensor_id
        self.location = location
        self.readings = readings  # NumPy array, shape (7, 24)

    def kind(self):
        return "sensor"

    def unit(self):
        return ""

    def alert_threshold(self):
        return 0

    def base_value(self):
        return 0

    def spread(self):
        return 1

    # 7 days x 24 hours of simulated readings
    def simulate(self, seed):
        rng = np.random.default_rng(seed)
        hours = np.arange(24)
        day_cycle = 3 - np.abs(hours - 14) / 3  # highest at 14:00
        noise = rng.normal(self.base_value(), self.spread(), 7 * 24)
        self.readings = noise.reshape(7, 24) + day_cycle  # broadcasting (7, 24) + (24,)

    # returns (min, max, mean)
    def summary(self):
        return (self.readings.min(), self.readings.max(), self.readings.mean())

    # returns (day, hour) of the highest reading
    def peak(self):
        index = np.argmax(self.readings)
        return (index // 24 + 1, index % 24)

    def lowest(self):
        index = np.argmin(self.readings)
        return (index // 24 + 1, index % 24)

    def daily_averages(self):
        return self.readings.mean(axis=1)

    def hourly_averages(self):
        return self.readings.mean(axis=0)

    # readings minus the mean of their day
    def normalized(self):
        return self.readings - self.readings.mean(axis=1, keepdims=True)

    def alert_mask(self):
        return self.readings > self.alert_threshold()

    # list of (day, hour, value) for every reading above the threshold
    def alert_records(self):
        flat = self.readings.reshape(7 * 24)
        positions = np.where(flat > self.alert_threshold())[0]
        return [(position // 24 + 1, position % 24, flat[position]) for position in positions]

    def moving_average(self, day):
        if day < 1 or day > 7:
            raise InvalidDayError()
        return np.convolve(self.readings[day - 1], np.ones(3) / 3, mode="valid")

    def __str__(self):
        return f"{self.sensor_id} - {self.kind()} sensor at {self.location} ({self.readings.size} readings in {self.unit()})"


class TemperatureSensor(Sensor):
    def kind(self):
        return "temperature"

    def unit(self):
        return "°C"

    def alert_threshold(self):
        return 25

    def base_value(self):
        return 20

    def spread(self):
        return 2

    def to_fahrenheit(self):
        return self.readings * 9 / 5 + 32


class HumiditySensor(Sensor):
    def kind(self):
        return "humidity"

    def unit(self):
        return "%"

    def alert_threshold(self):
        return 65

    def base_value(self):
        return 55

    def spread(self):
        return 5


# ----- station -----
class Station:
    def __init__(self):
        self.sensors = {}  # {sensor_id: Sensor}

    def __len__(self):
        return len(self.sensors)

    def add_sensor(self, sensor):
        self.sensors[sensor.sensor_id] = sensor

    def get_sensor(self, sensor_id):
        if sensor_id not in self.sensors:
            raise SensorNotFoundError()
        return self.sensors[sensor_id]

    def locations(self, kind):
        result = set()
        for sensor in self.sensors.values():
            if kind == "all" or sensor.kind() == kind:
                result.add(sensor.location)
        return result

    # locations that have both a temperature and a humidity sensor
    def shared_locations(self):
        return self.locations("temperature") & self.locations("humidity")

    # sensors sorted by average value, highest first
    def ranking(self):
        sensors = list(self.sensors.values())
        averages = np.array([sensor.readings.mean() for sensor in sensors])
        order = np.argsort(-averages)
        return [sensors[i] for i in order]

    def correlation(self, id1, id2):
        sensor1 = self.get_sensor(id1)
        sensor2 = self.get_sensor(id2)
        return np.corrcoef(sensor1.readings.reshape(7 * 24), sensor2.readings.reshape(7 * 24))[0, 1]

    def save(self, filename):
        sensors = list(self.sensors.values())
        np.savez(filename,
                 ids=np.array([sensor.sensor_id for sensor in sensors]),
                 locations=np.array([sensor.location for sensor in sensors]),
                 kinds=np.array([sensor.kind() for sensor in sensors]),
                 readings=np.array([sensor.readings for sensor in sensors]))

    def load(self, filename):
        try:
            data = np.load(filename)
        except FileNotFoundError:
            print("No saved data found. Starting with an empty station.")
            return
        except ValueError:
            print("Saved data is damaged. Starting with an empty station.")
            return
        for i in range(len(data["ids"])):
            if data["kinds"][i] == "temperature":
                sensor = TemperatureSensor(str(data["ids"][i]), str(data["locations"][i]), data["readings"][i])
            else:
                sensor = HumiditySensor(str(data["ids"][i]), str(data["locations"][i]), data["readings"][i])
            self.add_sensor(sensor)


# ----- menu functions -----
def ask_sensor(station, text):
    print("Sensors:", ", ".join(station.sensors))
    return station.get_sensor(input(text))


def add_sensor(station):
    sensor_id = input("Enter sensor ID: ")
    if sensor_id == "" or sensor_id in station.sensors:
        print("Error: sensor ID is empty or already exists.")
        return
    location = input("Enter location: ")
    if location == "":
        print("Error: location cannot be empty.")
        return
    kind = input("Temperature or humidity sensor? (t/h): ")
    if kind == "t":
        sensor = TemperatureSensor(sensor_id, location, None)
    elif kind == "h":
        sensor = HumiditySensor(sensor_id, location, None)
    else:
        print("Error: please enter t or h.")
        return
    sensor.simulate(100 + len(station))
    station.add_sensor(sensor)
    print("Added:", sensor)
    print("All locations:", station.locations("all"))
    print("Locations with temperature and humidity:", station.shared_locations())


def show_summary(station):
    try:
        sensor = ask_sensor(station, "Enter sensor ID: ")
    except SensorNotFoundError:
        print("Error: unknown sensor ID.")
        return
    low, high, mean = sensor.summary()
    peak_day, peak_hour = sensor.peak()
    low_day, low_hour = sensor.lowest()
    unit = sensor.unit()
    print("\n========== SUMMARY", sensor.sensor_id, "==========")
    print(sensor)
    print(f"Min: {low:.2f} {unit}   Max: {high:.2f} {unit}   Mean: {mean:.2f} {unit}   Std: {sensor.readings.std():.2f}")
    print(f"Highest reading: day {peak_day}, {peak_hour}:00")
    print(f"Lowest reading: day {low_day}, {low_hour}:00")
    if sensor.kind() == "temperature":
        print(f"Mean in Fahrenheit: {sensor.to_fahrenheit().mean():.2f} °F")


def show_daily_averages(station):
    try:
        sensor = ask_sensor(station, "Enter sensor ID: ")
    except SensorNotFoundError:
        print("Error: unknown sensor ID.")
        return
    averages = sensor.daily_averages()
    deviations = np.abs(sensor.normalized()).max(axis=1)
    print("\n========== DAILY REPORT", sensor.sensor_id, "==========")
    for day in range(7):
        print(f"Day {day + 1}: average {averages[day]:.2f} {sensor.unit()}, largest deviation from daily mean {deviations[day]:.2f}")
    hourly = sensor.hourly_averages()
    print(f"Hour with the highest average: {np.argmax(hourly)}:00 ({hourly.max():.2f} {sensor.unit()})")


def show_alerts(station):
    try:
        sensor = ask_sensor(station, "Enter sensor ID: ")
    except SensorNotFoundError:
        print("Error: unknown sensor ID.")
        return
    mask = sensor.alert_mask()
    marks = np.where(mask, "!", ".")
    print("\n========== ALERTS", sensor.sensor_id, "(above", sensor.alert_threshold(), sensor.unit() + ") ==========")
    print("Number of alerts:", mask.sum())
    for day in range(7):
        print("Day", day + 1, "".join(marks[day]))
    for day, hour, value in sensor.alert_records():
        print(f"ALERT: day {day}, {hour}:00 -> {value:.2f} {sensor.unit()}")


def show_moving_average(station):
    try:
        sensor = ask_sensor(station, "Enter sensor ID: ")
        day = int(input("Enter day (1-7): "))
        averages = sensor.moving_average(day)
    except SensorNotFoundError:
        print("Error: unknown sensor ID.")
        return
    except ValueError:
        print("Error: day must be a number.")
        return
    except InvalidDayError:
        print("Error: day must be between 1 and 7.")
        return
    print("\n========== 3-HOUR MOVING AVERAGE", sensor.sensor_id, "day", day, "==========")
    print(np.round(averages, 2))


def show_ranking(station):
    print("\n========== RANKING BY AVERAGE ==========")
    if len(station) == 0:
        print("No sensors yet.")
        return
    place = 1
    for sensor in station.ranking():
        print(f"{place}. {sensor.sensor_id} ({sensor.location}): {sensor.readings.mean():.2f} {sensor.unit()}")
        place += 1


def compare_sensors(station):
    try:
        print("Sensors:", ", ".join(station.sensors))
        id1 = input("Enter first sensor ID: ")
        id2 = input("Enter second sensor ID: ")
        correlation = station.correlation(id1, id2)
    except SensorNotFoundError:
        print("Error: unknown sensor ID.")
        return
    print(f"Correlation between {id1} and {id2}: {correlation:.2f}")


def show_menu():
    print("\n========== SENSOR DATA ANALYZER ==========")
    print("1. Add sensor (temperature / humidity)")
    print("2. Show sensor summary (min, max, mean, std)")
    print("3. Show daily averages")
    print("4. Show alerts (readings above threshold)")
    print("5. Show 3-hour moving average")
    print("6. Rank sensors by average")
    print("7. Compare two sensors (correlation)")
    print("8. Save and exit")


station = Station()
station.load(data_file)
print("Sensors loaded:", len(station))

running = True
while running:
    show_menu()
    choice = input("Enter your choice: ")

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
        compare_sensors(station)
    elif choice == "8":
        station.save(data_file)
        print("Data saved to", data_file + ". Goodbye!")
        running = False
    else:
        print("Invalid choice. Please enter a number from 1 to 8.")
