import numpy as np

rng = np.random.default_rng(42)
days = np.arange(1,8)
hours = np.array(range(24))

class SensorNotFoundError(Exception):
    pass

class Sensor:

    def __init__(self, sensor_id, location):
        self.sensor_id = sensor_id
        self.location = location

        self.readings = rng.normal(20, 5, 168).reshape(7 ,24)

    def __str__(self):
        return f"Sensor {self.sensor_id} at {self.location}"

    def alert_threshold(self):
        return 0

    def unit(self):
        return ""

    def summary(self):
        return (self.readings.min(), self.readings.max(), self.readings.mean())

    def std(self):
        return self.readings.std()

    def peak(self):
        index = self.readings.argmax()
        return (index // 24, index % 24)

    def lowest(self):
        index = self.readings.argmin()
        return (index // 24, index % 24)

    def daily_average(self):
        return self.readings.mean(axis=1)

    def hourly_average(self):
        return self.readings.mean(axis=0)

    def alerts(self, threshold):
        mask = self.readings > threshold
        rows, cols = np.where(mask)

        return [(rows[i] + 1, cols[i], self.readings[rows[i], cols[i]]) for i in range(len(rows))]

    def normalized(self):
        return self.readings - self.daily_average().reshape(7, 1)

    def moving_average(self):
        averages = np.convolve(self.readings.flatten(), np.ones(3) / 3, mode="valid")
        averages = np.append(averages, [0, 0]).reshape(7, 24)

        return averages[:, :22]

    def compare_sensors(self, other):
        return np.corrcoef(
            self.readings.flatten(),
            other.readings.flatten()
        )[0, 1]

class TemperatureSensor(Sensor):

    def alert_threshold(self):
        return 25

    def unit(self):
        return "C"

    def to_fahrenheit(self):
        return self.readings * 9 / 5 + 32

class HumiditySensor (Sensor):

    def alert_threshold(self):
        return 70

    def unit(self):
        return "%"

class Station:

    def __init__(self):
        self.sensors = {}

    def __len__(self):
        return len(self.sensors)

    def add_sensor(self, sensor_id, sensor):
        self.sensors[sensor_id] = sensor

    def get_sensor(self, sensor_id):
        if sensor_id not in self.sensors:
            raise SensorNotFoundError("Unknown sensor.")

        return self.sensors[sensor_id]

    def rank_sensors(self):
        ids = list(self.sensors.keys())
        averages = np.array([self.sensors[sensor_id].readings.mean() for sensor_id in ids])

        order = np.argsort(averages)[::-1]

        for i in order:
            print(f"{self.sensors[ids[i]]}: {averages[i]:.2f}")

    def shared_locations(self):
        temp = {s.location for s in self.sensors.values() if isinstance(s, TemperatureSensor)}
        hum = {s.location for s in self.sensors.values() if isinstance(s, HumiditySensor)}

        return temp & hum

station = Station()

def save_sensors():
    sensors = list(station.sensors.values())

    np.savez("sensors.npz",
             ids=[s.sensor_id for s in sensors],
             types=[type(s).__name__ for s in sensors],
             locations=[s.location for s in sensors],
             readings=[s.readings for s in sensors])

def load_sensors():
    try:
        data = np.load("sensors.npz")

        for i in range(len(data["ids"])):
            sensor_id = str(data["ids"][i])
            location = str(data["locations"][i])

            if data["types"][i] == "TemperatureSensor":
                sensor = TemperatureSensor(sensor_id, location)
            else:
                sensor = HumiditySensor(sensor_id, location)

            sensor.readings = data["readings"][i]
            station.add_sensor(sensor.sensor_id, sensor)

        print(f"Loaded {len(station)} sensors.")

    except FileNotFoundError:
        print("No saved data found.")

load_sensors()

while True:
    print(
    "\n1. Add sensor (temperature / humidity)"
    "\n2. Show sensor summary (min, max, mean, std)"
    "\n3. Show daily readings and averages (with Fahrenheit and normalized)"
    "\n4. Show alerts (readings above threshold)"
    "\n5. Show 3-hour moving average"
    "\n6. Rank sensors by average (and shared locations)"
    "\n7. Compare two sensors (correlation)"
    "\n8. Save and exit")

    choice = input("What would you like to do? ")

    if choice == "1":
        sensor_type = input("Choose sensor type (temperature/humidity): ").lower()
        sensor_id = input("Enter sensor ID: ")
        location = input("Enter location: ")

        if sensor_type == "temperature":
            sensor = TemperatureSensor(sensor_id, location)
            station.add_sensor(sensor_id, sensor)
            print("Added", sensor)
        elif sensor_type == "humidity":
            sensor = HumiditySensor(sensor_id,location)
            station.add_sensor(sensor_id, sensor)
            print("Added", sensor)
        else:
            print("Invalid sensor type!")

    elif choice == "2":
        sensor_id = input("Enter sensor ID: ")

        try:
            sensor = station.get_sensor(sensor_id)
            low, high, avg = sensor.summary()
            print(f"Min: {low:.2f}  Max: {high:.2f}  Mean: {avg:.2f}  Std: {sensor.std():.2f} {sensor.unit()}")

            day, hour = sensor.peak()
            print(f"Highest reading: day {day + 1} at hour {hour}")

            day, hour = sensor.lowest()
            print(f"Lowest reading: day {day + 1} at hour {hour}")

        except SensorNotFoundError as error:
            print(error)

    elif choice == "3":
        sensor_id = input("Enter sensor ID: ")

        try:
            sensor = station.get_sensor(sensor_id)
            averages = sensor.daily_average()

            for day in range(7):
                print(f"Day {days[day]}: {np.round(sensor.readings[day], 2)}")
                print(f"Average: {averages[day]:.2f}")

            print("Hourly averages:")
            print(np.round(sensor.hourly_average(), 2))

            if isinstance(sensor, TemperatureSensor):
                print("Readings in Fahrenheit:")
                print(np.round(sensor.to_fahrenheit(), 2))

            print("Normalized readings (daily average subtracted):")
            print(np.round(sensor.normalized(), 2))

        except SensorNotFoundError as error:
            print(error)

    elif choice == "4":
        sensor_id = input("Enter sensor ID: ")

        try:
            sensor = station.get_sensor(sensor_id)
            threshold = input(f"Enter threshold (press Enter for {sensor.alert_threshold()}): ")

            if threshold == "":
                threshold = sensor.alert_threshold()

            alerts = sensor.alerts(float(threshold))

            if len(alerts) == 0:
                print("No alerts. All readings are within the threshold.")
            else:
                print(f"{len(alerts)} readings above threshold:")

                for day, hour, value in alerts:
                    print(f"ALERT: day {day} at hour {hour}: {value:.2f} {sensor.unit()}")

        except SensorNotFoundError as error:
            print(error)
        except ValueError:
            print("Please enter a valid number.")

    elif choice == "5":
        sensor_id = input("Enter sensor ID: ")

        try:
            sensor = station.get_sensor(sensor_id)
            averages = sensor.moving_average()

            for day in range(7):
                for hour in range(22):
                    print(
                        f"Day {day + 1}, hours {hour}-{hour + 2}: "
                        f"{averages[day, hour]:.2f}"
                    )

        except SensorNotFoundError as error:
            print(error)

    elif choice == "6":
        print(f"Ranking {len(station)} sensors:")
        station.rank_sensors()

        shared = station.shared_locations()

        if len(shared) == 0:
            print("No location has both sensor types.")
        else:
            print("Locations with both sensor types:", shared)

    elif choice == "7":
        sensor_id1 = input("Enter first sensor ID: ")
        sensor_id2 = input("Enter second sensor ID: ")

        try:
            sensor1 = station.get_sensor(sensor_id1)
            sensor2 = station.get_sensor(sensor_id2)

            correlation = sensor1.compare_sensors(sensor2)
            print(f"Correlation: {correlation:.2f}")

        except SensorNotFoundError as error:
            print(error)

    elif choice == "8":
        save_sensors()
        print("Sensors saved.")
        break

    else:
        print("Invalid choice, please enter a number from 1 to 8.")
