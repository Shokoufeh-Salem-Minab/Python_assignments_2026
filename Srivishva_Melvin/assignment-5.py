# Homework 5
# Srivishva Melvin - sm25017
# Program created on: 22/10/2026

import numpy as np

DATA_FILE = "sensors.npz"
SEED = 42
PROFILES = {"temperature": (22, 5, 1.5), "humidity": (55, -10, 4)} # (average value, daily swing, noise) used to simulate each kind of sensor

class SensorError(Exception):
    pass

def simulate(kind, seed):
    base, swing, noise = PROFILES[kind]
    rng = np.random.default_rng(seed)
    hours = np.linspace(0, 2 * np.pi, 24, endpoint=False)
    cycle = swing * np.sin(hours - np.pi / 2) # smooth day/night curve
    values = rng.normal(base, noise, 7 * 24).reshape(7, 24)
    return values + cycle 

class Sensor:

    def __init__(self, sensor_id, location, readings):
        self.sensor_id = sensor_id
        self.location = location
        self.readings = readings # NumPy array, shape (7, 24)
        self.kind = "sensor"

    def alert_threshold(self):
        return 100

    def unit(self):
        return ""

    def summary(self):
        return (self.readings.min(), self.readings.max(), self.readings.mean())

    def peak(self):
        day, hour = divmod(self.readings.argmax(), 24) # argmax gives one position in the whole array, divmod by 24 turns it into (day, hour)
        return (day + 1, hour) 

    def lowest(self):
        day, hour = divmod(self.readings.argmin(), 24)
        return (day + 1, hour)

    def daily_averages(self):
        return self.readings.mean(axis=1) # one average per row (day)

    def hourly_averages(self):
        return self.readings.mean(axis=0) # one average per column (hour)

    def normalized(self):
        return self.readings - self.daily_averages().reshape(7, 1)
    
    def alert_mask(self):
        return self.readings > self.alert_threshold()

    def alert_flags(self):
        return np.where(self.alert_mask(), "ALERT", "ok")

    def alert_records(self):
        days, hours = np.where(self.alert_mask())
        values = self.readings[self.alert_mask()]
        return [(days[i] + 1, hours[i], values[i]) for i in range(len(days))]

    def moving_average(self, day): # average of every 3 consecutive hours of one day
        return np.convolve(self.readings[day - 1], np.ones(3) / 3, mode="valid")

    def __str__(self):
        return f"[{self.sensor_id}] {self.kind} sensor at {self.location}, average {self.readings.mean():.2f} {self.unit()}"

class TemperatureSensor(Sensor):

    def __init__(self, sensor_id, location, readings):
        super().__init__(sensor_id, location, readings)
        self.kind = "temperature"

    def alert_threshold(self):
        return 28

    def unit(self):
        return "C"

    def to_fahrenheit(self):
        return self.readings * 9 / 5 + 32

class HumiditySensor(Sensor):

    def __init__(self, sensor_id, location, readings):
        super().__init__(sensor_id, location, readings)
        self.kind = "humidity"

    def alert_threshold(self):
        return 70

    def unit(self):
        return "%"

def make_sensor(kind, sensor_id, location, readings):
    if kind == "temperature":
        return TemperatureSensor(sensor_id, location, readings)
    elif kind == "humidity":
        return HumiditySensor(sensor_id, location, readings)
    else:
        raise SensorError("Unknown sensor type " + kind)

class Station:
    def __init__(self):
        self.sensors = {}

    def __len__(self):
        return len(self.sensors)

    def add(self, sensor):
        if sensor.sensor_id in self.sensors:
            raise SensorError("Sensor " + sensor.sensor_id + " already exists")
        self.sensors[sensor.sensor_id] = sensor

    def get(self, sensor_id):
        if sensor_id not in self.sensors:
            raise SensorError("No sensor with ID " + sensor_id)
        return self.sensors[sensor_id]

    def create(self, kind, sensor_id, location):
        readings = simulate(kind, SEED + len(self)) # gets a different seed for every sensor
        self.add(make_sensor(kind, sensor_id, location, readings))

    def locations(self):
        return {s.location for s in self.sensors.values()}

    def locations_with_both(self):
        temp = {s.location for s in self.sensors.values() if s.kind == "temperature"}
        humid = {s.location for s in self.sensors.values() if s.kind == "humidity"}
        return temp & humid 

    def ranking(self):
        sensors = list(self.sensors.values())
        averages = np.array([s.readings.mean() for s in sensors])
        order = np.argsort(averages)[::-1]
        return [sensors[i] for i in order]

    def save(self):
        sensors = list(self.sensors.values())
        np.savez(DATA_FILE,
                 ids=np.array([s.sensor_id for s in sensors]),
                 kinds=np.array([s.kind for s in sensors]),
                 places=np.array([s.location for s in sensors]),
                 readings=np.array([s.readings for s in sensors]))

    def load(self):
        with np.load(DATA_FILE) as data:
            ids = data["ids"]
            kinds = data["kinds"]
            places = data["places"]
            readings = data["readings"]
            for i in range(len(ids)):
                if readings[i].shape != (7, 24):
                    raise SensorError("Saved readings have the wrong shape")
                self.add(make_sensor(str(kinds[i]), str(ids[i]), str(places[i]), readings[i]))

def add_demo_sensors(station):
    station.create("temperature", "T1", "Lab")
    station.create("temperature", "T2", "Roof")
    station.create("humidity", "H1", "Lab")

def start_station():
    station = Station()
    try:
        station.load()
        print("Loaded", len(station), "sensors from", DATA_FILE)
    except FileNotFoundError:
        print("No data file yet, starting with 3 demo sensors")
        add_demo_sensors(station)
    except Exception:
        print("The data file is damaged, starting with 3 demo sensors")
        station = Station()
        add_demo_sensors(station)
    return station

def input_check(text):
    userInput = input(text).strip()
    if userInput == "":
        raise SensorError("This field cannot be empty")
    return userInput

def ask_sensor(station, text="Sensor ID: "):
    print("Sensors:", ", ".join(station.sensors))
    return station.get(input_check(text).upper())

def show_menu():
    print("\nSensor Data Analyzer: ")
    print("1. Add sensor (temperature / humidity)")
    print("2. Show sensor summary (min, max, mean, std)")
    print("3. Show daily averages")
    print("4. Show alerts (readings above threshold)")
    print("5. Show 3-hour moving average")
    print("6. Rank sensors by average")
    print("7. Compare two sensors (correlation)")
    print("8. Save and exit")

def add_sensor(station):
    letter = input_check("Temperature or humidity? (t/h): ").lower()
    if letter != "t" and letter != "h":
        raise SensorError("Please type t (for temperature) or h (for humidity)")
    sensor_id = input_check("Sensor ID: ").upper()
    location = input_check("Location: ").title()
    if letter == "t":
        kind = "temperature"
    else:
        kind = "humidity"
    station.create(kind, sensor_id, location)
    print("Added:", station.get(sensor_id))

def show_summary(station):
    sensor = ask_sensor(station)
    low, high, mean = sensor.summary()
    peak_day, peak_hour = sensor.peak()
    low_day, low_hour = sensor.lowest()
    u = sensor.unit()
    print("\n" + str(sensor))
    print(f"Min is {low:.2f} {u}, Max is {high:.2f} {u}, Mean is {mean:.2f} {u} and Std is {sensor.readings.std():.2f} {u}")
    print(f"Highest: day {peak_day}, hour {peak_hour}:00 and Lowest: day {low_day}, hour {low_hour}:00")
    if sensor.kind == "temperature":
        f = sensor.to_fahrenheit()
        print(f"In Fahrenheit: min {f.min():.2f}, max {f.max():.2f}, mean {f.mean():.2f} F")

def show_daily_averages(station):
    sensor = ask_sensor(station)
    u = sensor.unit()
    averages = sensor.daily_averages()
    for day in np.arange(1, 8):
        print(f"Day {day}: {averages[day - 1]:.2f} {u}")
    hourly = sensor.hourly_averages()
    print(f"Highest hourly average: {hourly.argmax()}:00 ({hourly.max():.2f} {u})")
    print(f"Biggest gap from a day's average: {np.abs(sensor.normalized()).max():.2f} {u}")

def show_alerts(station):
    sensor = ask_sensor(station)
    per_day = (sensor.alert_flags() == "ALERT").sum(axis=1)
    print(f"\nThreshold: {sensor.alert_threshold()} {sensor.unit()}")
    print(f"Alert readings: {per_day.sum()} out of {sensor.readings.size}")
    print("Alerts per day:", per_day)
    for day, hour, value in sensor.alert_records():
        print(f"ALERT day {day}, hour {hour}:00 = {value:.2f} {sensor.unit()}")

def show_moving_average(station):
    sensor = ask_sensor(station)
    day = int(input_check("Day (1-7): ")) # int to raise error in values like symbolds or letters entered"
    if day < 1 or day > 7:
        raise SensorError("Day must be between 1 and 7")
    print(f"3-hour moving average for day {day} (average of every 3 consecutive hours): ")
    print(np.round(sensor.moving_average(day), 2))

def show_ranking(station):
    place = 1
    for sensor in station.ranking():
        print(f"{place}. {sensor}")
        place += 1
    print("Locations:", ", ".join(sorted(station.locations())))
    both = station.locations_with_both()
    if len(both) == 0:
        print("Locations with both types: none")
    else:
        print("Locations with both types:", ", ".join(sorted(both)))

def compare_sensors(station):
    first = ask_sensor(station, "First sensor ID: ")
    second = ask_sensor(station, "Second sensor ID: ")
    table = np.corrcoef(first.readings.flatten(), second.readings.flatten())
    print(f"Correlation between {first.sensor_id} and {second.sensor_id}: {table[0, 1]:.2f}")

def run_option(choice, station):
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
    else:
        print("Enter a number from 1 to 8")

def main():
    station = start_station()
    running = True
    while running:
        show_menu()
        choice = input("Choose an option: \n").strip()
        try:
            if choice == "8":
                station.save()
                print("Data saved. Goodbye!")
                running = False
            else:
                run_option(choice, station)
        except SensorError as error:
            print("Error:", error)
        except ValueError:
            print("Error: please enter a whole number")
        except OSError:
            print("Error: could not save the data file")

if __name__ == "__main__":
    main()