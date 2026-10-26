# Sensor Data Analyzer

import numpy as np

DATA_FILE = "sensor_data.npz"


# Custom exceptions
class SensorNotFoundError(Exception):
    """Raised when the user types a sensor id that does not exist."""
    pass


class InvalidInputError(Exception):
    """Raised when the user types something we cannot use."""
    pass


# Sensor classes 
class Sensor:
    def __init__(self, sensor_id, location, readings=None, seed=1):
        self.sensor_id = sensor_id
        self.location = location
        if readings is None:
            # no data given, so make fake data
            self.readings = self.simulate_readings(seed)
        else:
            # data given 
            self.readings = np.array(readings).reshape(7, 24)

   
    def sensor_type(self):
        return "generic"

    def unit(self):
        return ""

    def alert_threshold(self):
        return 0

    def base_value(self):
        return 0

    def swing(self):
        return 0

    # creating the data
    def simulate_readings(self, seed):
        rng = np.random.default_rng(seed)            
        noise = rng.normal(0, 1.5, 168)                
        hours = np.arange(24)                          
        one_day = -np.cos(2 * np.pi * hours / 24)      
        cycle = np.tile(one_day, 7)                    
        trend = np.linspace(0, 2, 168)                 
        flat = self.base_value() + self.swing() * cycle + trend + noise
        return flat.reshape(7, 24)                     # 7 days, 24 hours

    # statistics
    def summary(self):
        # returns a tuple (min, max, mean)
        return (self.readings.min(), self.readings.max(), self.readings.mean())

    def std(self):
        return self.readings.std()

    def peak(self):
        # returns a tuple (day, hour) of the highest reading
        index = self.readings.argmax()        # position in the flattened array
        day, hour = divmod(index, 24)
        return (int(day), int(hour))

    def lowest(self):
        index = self.readings.argmin()
        day, hour = divmod(index, 24)
        return (int(day), int(hour))

    def daily_averages(self):
        return self.readings.mean(axis=1)     # one number per day (7 numbers)

    def hourly_averages(self):
        return self.readings.mean(axis=0)     # one number per hour (24 numbers)

    def normalized(self):
        # subtract each day's mean from that day's readings (broadcasting)
        daily = self.daily_averages()
        return self.readings - daily[:, np.newaxis]

    # alerts
    def alert_mask(self):
        return self.readings > self.alert_threshold()      # True / False array

    def alert_count(self):
        return int(self.alert_mask().sum())                # True counts as 1

    def alert_status(self):
        # mark every reading as "ALERT" or "ok"
        return np.where(self.alert_mask(), "ALERT", "ok")

    def alert_records(self):
        # list of (day, hour, value) for every alert reading
        days, hours = np.where(self.alert_mask())
        records = [(int(d), int(h), self.readings[d, h]) for d, h in zip(days, hours)]
        return records

    #  moving average 
    def moving_average(self):
        flat = self.readings.flatten()         
        window = np.ones(3) / 3                
        return np.convolve(flat, window, mode="valid")

    def __str__(self):
        return f"{self.sensor_id} ({self.sensor_type()}) at {self.location}, unit: {self.unit()}"


class TemperatureSensor(Sensor):
    def sensor_type(self):
        return "temperature"

    def unit(self):
        return "C"

    def alert_threshold(self):
        return 26

    def base_value(self):
        return 20

    def swing(self):
        return 5

    def to_fahrenheit(self):
        
        return self.readings * 9 / 5 + 32


class HumiditySensor(Sensor):
    def sensor_type(self):
        return "humidity"

    def unit(self):
        return "%"

    def alert_threshold(self):
        return 65

    def base_value(self):
        return 55

    def swing(self):
        return -12      # humidity is highest at night, lowest at noon


# Station class
class Station:
    def __init__(self):
        self.sensors = {}        

    def __len__(self):
        return len(self.sensors)

    def make_sensor(self, type_name, sensor_id, location, readings=None, seed=1):
        if type_name == "temperature":
            return TemperatureSensor(sensor_id, location, readings, seed)
        elif type_name == "humidity":
            return HumiditySensor(sensor_id, location, readings, seed)
        else:
            raise InvalidInputError("Type must be temperature or humidity.")

    def add_sensor(self, type_name, sensor_id, location):
        if sensor_id == "" or location == "":
            raise InvalidInputError("Id and location cannot be empty.")
        if sensor_id in self.sensors:
            raise InvalidInputError("A sensor with that id already exists.")
        seed = len(self.sensors) + 1      # different seed for every sensor
        sensor = self.make_sensor(type_name, sensor_id, location, None, seed)
        self.sensors[sensor_id] = sensor
        return sensor

    def get_sensor(self, sensor_id):
        if sensor_id not in self.sensors:
            raise SensorNotFoundError("No sensor with id '" + sensor_id + "'.")
        return self.sensors[sensor_id]

   
    def all_locations(self):
        return {s.location for s in self.sensors.values()}

    def locations_with_both(self):
        temp_places = {s.location for s in self.sensors.values()
                       if isinstance(s, TemperatureSensor)}
        humid_places = {s.location for s in self.sensors.values()
                        if isinstance(s, HumiditySensor)}
        return temp_places & humid_places        # set intersection

   
    def ranking(self):
        if len(self.sensors) == 0:
            raise InvalidInputError("There are no sensors yet.")
        ids = list(self.sensors.keys())
        averages = np.array([self.sensors[i].readings.mean() for i in ids])
        order = np.argsort(averages)[::-1]       # biggest average first
        return [(ids[i], averages[i]) for i in order]

    def correlation(self, id1, id2):
        first = self.get_sensor(id1)
        second = self.get_sensor(id2)
        table = np.corrcoef(first.readings.flatten(), second.readings.flatten())
        return table[0, 1]

    
    def save(self, filename):
        ids = list(self.sensors.keys())
        locations = [self.sensors[i].location for i in ids]
        types = [self.sensors[i].sensor_type() for i in ids]
        all_readings = np.array([self.sensors[i].readings for i in ids])
        np.savez(filename, ids=np.array(ids), locations=np.array(locations),
                 types=np.array(types), readings=all_readings)

    def load(self, filename):
        data = np.load(filename)
        ids = data["ids"]
        locations = data["locations"]
        types = data["types"]
        readings = data["readings"]
        self.sensors = {}
        for i in range(len(ids)):
            sensor = self.make_sensor(str(types[i]), str(ids[i]),
                                      str(locations[i]), readings[i])
            self.sensors[str(ids[i])] = sensor


# Menu functions (each one does one job)
def print_menu():
    print()
    print("1. Add sensor (temperature / humidity)")
    print("2. Show sensor summary (min, max, mean, std)")
    print("3. Show daily averages")
    print("4. Show alerts (readings above threshold)")
    print("5. Show 3-hour moving average")
    print("6. Rank sensors by average")
    print("7. Compare two sensors (correlation)")
    print("8. Save and exit")


def print_status(station):
    print()
    print("=" * 50)
    print("Sensors in station:", len(station))
    print("Locations:", sorted(station.all_locations()))
    print("Locations with both types:", sorted(station.locations_with_both()))
    print("=" * 50)


def get_choice():
    text = input("Choose an option (1-8): ").strip()
    try:
        number = int(text)
    except ValueError:
        raise InvalidInputError("Please type a number, not '" + text + "'.")
    if number < 1 or number > 8:
        raise InvalidInputError("The number must be between 1 and 8.")
    return number


def ask_sensor(station):
    sensor_id = input("Sensor id: ").strip()
    return station.get_sensor(sensor_id)


def add_sensor_menu(station):
    kind = input("Type (T for temperature / H for humidity): ").strip().lower()
    if kind == "t":
        kind = "temperature"
    if kind == "h":
        kind = "humidity"
    sensor_id = input("New sensor id: ").strip()
    location = input("Location: ").strip()
    sensor = station.add_sensor(kind, sensor_id, location)
    print("Added:", sensor)


def summary_menu(station):
    sensor = ask_sensor(station)
    low, high, mean = sensor.summary()          # unpack the tuple
    unit = sensor.unit()
    print(sensor)
    print(f"Min:  {low:.2f} {unit}")
    print(f"Max:  {high:.2f} {unit}")
    print(f"Mean: {mean:.2f} {unit}")
    print(f"Std:  {sensor.std():.2f}")
    peak_day, peak_hour = sensor.peak()         # unpack another tuple
    print(f"Highest reading: day {peak_day + 1}, hour {peak_hour}:00")
    low_day, low_hour = sensor.lowest()
    print(f"Lowest reading:  day {low_day + 1}, hour {low_hour}:00")
    if isinstance(sensor, TemperatureSensor):
        fahrenheit = sensor.to_fahrenheit()
        print(f"Max in Fahrenheit: {fahrenheit.max():.2f} F")


def daily_menu(station):
    sensor = ask_sensor(station)
    daily = sensor.daily_averages()
    print("Daily report for", sensor.sensor_id)
    for day in range(7):
        print(f"  Day {day + 1}: {daily[day]:.2f} {sensor.unit()}")
    hourly = sensor.hourly_averages()
    print(f"Hottest/highest hour on average: {hourly.argmax()}:00 ({hourly.max():.2f})")
    print(f"Lowest hour on average:          {hourly.argmin()}:00 ({hourly.min():.2f})")
    print("Day 1 after subtracting its daily mean (normalized):")
    print(np.round(sensor.normalized()[0], 2))


def alerts_menu(station):
    sensor = ask_sensor(station)
    threshold = sensor.alert_threshold()
    print(f"Threshold for {sensor.sensor_id}: {threshold} {sensor.unit()}")
    print("Total alert readings:", sensor.alert_count())
    status = sensor.alert_status()
    alerts_per_day = (status == "ALERT").sum(axis=1)
    for day in range(7):
        print(f"  Day {day + 1}: {alerts_per_day[day]} alerts")
    records = sensor.alert_records()
    print("First alert records (day, hour, value):")
    for day, hour, value in records[:10]:
        print(f"  day {day + 1}, hour {hour}:00, value {value:.2f}")


def moving_menu(station):
    sensor = ask_sensor(station)
    moving = sensor.moving_average()
    print("Number of moving average values:", len(moving))
    print("First 10 values:", np.round(moving[:10], 2))
    day, hour = divmod(int(moving.argmax()), 24)
    print(f"Highest 3-hour average: {moving.max():.2f}, "
          f"starting at day {day + 1}, hour {hour}:00")


def rank_menu(station):
    result = station.ranking()
    print("Sensors ranked by average (highest first):")
    place = 1
    for sensor_id, average in result:
        print(f"  {place}. {sensor_id}: {average:.2f}")
        place = place + 1


def correlation_menu(station):
    id1 = input("First sensor id: ").strip()
    id2 = input("Second sensor id: ").strip()
    value = station.correlation(id1, id2)
    print(f"Correlation between {id1} and {id2}: {value:.2f}")
    if value > 0.5:
        print("They move together.")
    elif value < -0.5:
        print("They move in opposite directions.")
    else:
        print("They are only weakly related.")


def save_and_exit(station):
    try:
        station.save(DATA_FILE)
        print("Data saved to", DATA_FILE, "- goodbye!")
    except OSError:
        print("Could not save the file.")


def run_choice(choice, station):
    # returns False when the program should stop
    if choice == 1:
        add_sensor_menu(station)
    elif choice == 2:
        summary_menu(station)
    elif choice == 3:
        daily_menu(station)
    elif choice == 4:
        alerts_menu(station)
    elif choice == 5:
        moving_menu(station)
    elif choice == 6:
        rank_menu(station)
    elif choice == 7:
        correlation_menu(station)
    elif choice == 8:
        save_and_exit(station)
        return False
    return True


def main():
    station = Station()

    try:
        station.load(DATA_FILE)
        print("Loaded", len(station), "sensor(s) from", DATA_FILE)
    except FileNotFoundError:
        print("No data file found. Starting with an empty station.")
    except (ValueError, KeyError, OSError):
        print("Data file could not be read. Starting with an empty station.")

    running = True
    while running:
        print_status(station)
        print_menu()
        try:
            choice = get_choice()
            running = run_choice(choice, station)
        except (InvalidInputError, SensorNotFoundError) as error:
            print("Error:", error)
        except (EOFError, KeyboardInterrupt):
            print()
            save_and_exit(station)
            running = False


main()