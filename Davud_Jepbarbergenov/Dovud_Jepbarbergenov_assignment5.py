import json
import numpy as np


class UnknownSensorError(Exception):
    pass


class Sensor:
    def init(self, sensor_id, location, readings):
        self.sensor_id = sensor_id
        self.location = location
        self.readings = np.array(readings).reshape(7, 24)

    def alert_threshold(self):
        raise NotImplementedError

    def unit(self):
        raise NotImplementedError

    def summary(self):
        return (
            np.min(self.readings),
            np.max(self.readings),
            np.mean(self.readings)
        )

    def peak_time(self):
        index = np.argmax(self.readings)
        day = index // 24 + 1
        hour = index % 24
        return day, hour

    def str(self):
        return f"{self.sensor_id} - {self.location}"


class TemperatureSensor(Sensor):
    def alert_threshold(self):
        return 30

    def unit(self):
        return "Celsius"


class HumiditySensor(Sensor):
    def alert_threshold(self):
        return 80

    def unit(self):
        return "percent"


class Station:
    def init(self):
        self.sensors = {}

    def len(self):
        return len(self.sensors)

    def add_sensor(self, sensor):
        if sensor.sensor_id in self.sensors:
            raise ValueError("This sensor ID already exists.")

        self.sensors[sensor.sensor_id] = sensor

    def get_sensor(self, sensor_id):
        if sensor_id not in self.sensors:
            raise UnknownSensorError("Sensor not found.")

        return self.sensors[sensor_id]

    def locations(self):
        return {sensor.location for sensor in self.sensors.values()}

    def shared_locations(self):
        temperature_locations = {
            sensor.location for sensor in self.sensors.values()
            if isinstance(sensor, TemperatureSensor)
        }

        humidity_locations = {
            sensor.location for sensor in self.sensors.values()
            if isinstance(sensor, HumiditySensor)
        }

        return temperature_locations & humidity_locations

    def save(self):
        data = []

        for sensor in self.sensors.values():
            item = {
                "sensor_id": sensor.sensor_id,
                "location": sensor.location,
                "type": "temperature"
                        if isinstance(sensor, TemperatureSensor)
                        else "humidity",
                "readings": sensor.readings.tolist()
            }

            data.append(item)

        with open("sensors.json", "w") as file:
            json.dump(data, file, indent=4)

    def load(self):
        try:
            with open("sensors.json", "r") as file:
                data = json.load(file)

            for item in data:
                if item["type"] == "temperature":
                    sensor = TemperatureSensor(
                        item["sensor_id"],
                        item["location"],
                        item["readings"]
                    )
                else:
                    sensor = HumiditySensor(
                        item["sensor_id"],
                        item["location"],
                        item["readings"]
                    )

                self.sensors[sensor.sensor_id] = sensor

        except FileNotFoundError:
            print("No saved sensor data found. Starting fresh.")
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
            print("Could not load sensor data:", error)


def create_readings(sensor_type, sensor_id):
    # Use a fixed seed so the sample readings can be reproduced.
    seed = 2026 + sum(ord(char) for char in sensor_id)
    rng = np.random.default_rng(seed)

    if sensor_type == "temperature":
        readings = rng.normal(22, 5, 7 * 24)
    else:
        readings = rng.normal(60, 15, 7 * 24)

    hours = np.arange(7 * 24)
    readings = np.array(readings + np.sin(hours / 24))

    return readings.reshape(7, 24)
def add_sensor(station):
    sensor_id = input("Sensor ID: ").strip()
    location = input("Location: ").strip()
    sensor_type = input("Type (temperature/humidity): ").lower().strip()

    if not sensor_id or not location:
        print("ID and location cannot be empty.")
        return

    if sensor_type not in ("temperature", "humidity"):
        print("Enter temperature or humidity.")
        return

    readings = create_readings(sensor_type, sensor_id)

    if sensor_type == "temperature":
        sensor = TemperatureSensor(sensor_id, location, readings)
    else:
        sensor = HumiditySensor(sensor_id, location, readings)

    try:
        station.add_sensor(sensor)
        print("Sensor added:", sensor)
    except ValueError as error:
        print(error)


def show_summary(station):
    try:
        sensor_id = input("Sensor ID: ").strip()
        sensor = station.get_sensor(sensor_id)

        minimum, maximum, average = sensor.summary()

        print("Sensor:", sensor)
        print(f"Minimum: {minimum:.2f}")
        print(f"Maximum: {maximum:.2f}")
        print(f"Average: {average:.2f}")
        print(f"Standard deviation: {np.std(sensor.readings):.2f}")

        day, hour = sensor.peak_time()
        print(f"Highest reading: day {day}, hour {hour}:00")

        lowest_index = np.argmin(sensor.readings)
        print(f"Lowest reading: day {lowest_index // 24 + 1}, "
              f"hour {lowest_index % 24}:00")

        # Convert Celsius to Fahrenheit using a NumPy operation.
        if isinstance(sensor, TemperatureSensor):
            fahrenheit = sensor.readings * 9 / 5 + 32
            print(f"Average in Fahrenheit: {np.mean(fahrenheit):.2f}")

        # Subtract each day's average from that day's readings.
        daily_means = np.mean(sensor.readings, axis=1, keepdims=True)
        normalized = sensor.readings - daily_means
        print("First five normalized readings:",
              np.round(normalized[0, :5], 2))

    except UnknownSensorError as error:
        print(error)


def show_daily_averages(station):
    try:
        sensor = station.get_sensor(input("Sensor ID: ").strip())

        daily_averages = np.mean(sensor.readings, axis=1)

        for day in range(7):
            print(f"Day {day + 1}: {daily_averages[day]:.2f}")

        hourly_averages = np.mean(sensor.readings, axis=0)
        print("Average for each hour:")
        print(np.round(hourly_averages, 2))

    except UnknownSensorError as error:
        print(error)


def show_alerts(station):
    try:
        sensor = station.get_sensor(input("Sensor ID: ").strip())

        threshold = sensor.alert_threshold()
        mask = sensor.readings > threshold
        positions = np.where(mask)

        alerts = [
            (int(day) + 1, int(hour),
             float(sensor.readings[day, hour]))
            for day, hour in zip(*positions)
        ]

        print("Alert threshold:", threshold)
        print("Number of alerts:", len(alerts))

        if not alerts:
            print("No alerts found.")
        else:
            for day, hour, value in alerts:
                print(f"Day {day}, hour {hour}:00 - {value:.2f}")

    except UnknownSensorError as error:
        print(error)


def show_moving_average(station):
    try:
        sensor = station.get_sensor(input("Sensor ID: ").strip())

        readings = sensor.readings.flatten()
        averages = np.convolve(
            readings, np.ones(3) / 3, mode="valid"
        )

        print("First 20 moving averages:")
        print(np.round(averages[:20], 2))

    except UnknownSensorError as error:
        print(error)


def rank_sensors(station):
    if len(station) == 0:
        print("No sensors available.")
        return

    sensors = list(station.sensors.values())
    averages = np.array([
        np.mean(sensor.readings) for sensor in sensors
    ])

    order = np.argsort(averages)[::-1]

    for index in order:
        sensor = sensors[index]
        print(f"{sensor.sensor_id}: "
              f"{np.mean(sensor.readings):.2f} {sensor.unit()}")
    def compare_sensors(station):
     try:
        id1 = input("First sensor ID: ").strip()
        id2 = input("Second sensor ID: ").strip()

        sensor1 = station.get_sensor(id1)
        sensor2 = station.get_sensor(id2)

        correlation = np.corrcoef(
            sensor1.readings.flatten(),
            sensor2.readings.flatten()
        )[0, 1]

        print(f"Correlation: {correlation:.2f}")

    except UnknownSensorError as error:
        print(error)


def main():
    station = Station()
    station.load()

    while True:
        print("\n--- Sensor Data Analyzer ---")
        print("1. Add sensor")
        print("2. Show sensor summary")
        print("3. Show daily averages")
        print("4. Show alerts")
        print("5. Show 3-hour moving average")
        print("6. Rank sensors by average")
        print("7. Compare two sensors")
        print("8. Save and exit")

        choice = input("Choose an option: ").strip()

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
            rank_sensors(station)
        elif choice == "7":
            compare_sensors(station)
        elif choice == "8":
            try:
                station.save()
                print("Data saved. Goodbye!")
            except OSError as error:
                print("Could not save data:", error)
            break
        else:
            print("Please choose a number from 1 to 8.")

        print("Number of sensors:", len(station))
        print("Locations:", station.locations())
        print("Locations with both sensor types:",
              station.shared_locations())


if __name__ == "__main__":
    main()