import numpy as np
import os

class SensorError(Exception):
    pass

class Sensor:
    def __init__(self, sensor_id, location, readings=None, seed=42):
        self.sensor_id = sensor_id
        self.location = location
        if readings is not None:
            self.readings = np.array(readings)
        else:
            rng = np.random.default_rng(seed=seed)
            self.readings = rng.normal(loc=20.0, scale=5.0, size=7 * 24).reshape(7, 24)

    def unit(self):
        return "units"

    def alert_threshold(self):
        return 30.0  

    def summary(self):
        flat = self.readings
        mn = float(np.min(flat))
        mx = float(np.max(flat))
        mean_val = float(np.mean(flat))
        return (mn, mx, mean_val)

    def peak_reading(self):
        flat_idx = np.argmax(self.readings)
        day, hour = divmod(flat_idx, 24)
        return (int(day), int(hour))

    def lowest_reading(self):
        flat_idx = np.argmin(self.readings)
        day, hour = divmod(flat_idx, 24)
        return (int(day), int(hour))

    def hourly_averages(self):
        return np.mean(self.readings, axis=0)

    def normalized(self):
        # subtract each day's mean from that day's readings (broadcasting)
        return self.readings - np.mean(self.readings, axis=1, keepdims=True)

    def __str__(self):
        # Mixed string formatting: using concatenation +
        return "Sensor ID: " + self.sensor_id + ", Location: " + self.location + ", Type: Generic"

class TemperatureSensor(Sensor):
    def alert_threshold(self):
        return 32.0  

    def unit(self):
        return "°C"

    def to_fahrenheit(self):
        return self.readings * 9 / 5 + 32

    def __str__(self):
        # Mixed string formatting: using .format()
        return "Temperature Sensor [{}] at {}".format(self.sensor_id, self.location)

class HumiditySensor(Sensor):
    def alert_threshold(self):
        return 80.0  

    def unit(self):
        return "%"

    def __str__(self):
        # Mixed string formatting: using f-string
        return f"Humidity Sensor [{self.sensor_id}] at {self.location}"

class Station:
    def __init__(self):
        self.sensors = {}  

    def __len__(self):
        return len(self.sensors)

    def unique_locations(self):
        locs = set()
        for s in self.sensors.values():
            locs.add(s.location)
        return locs

    def shared_locations(self):
        temp_locs = set()
        hum_locs = set()
        for s in self.sensors.values():
            if isinstance(s, TemperatureSensor):
                temp_locs.add(s.location)
            elif isinstance(s, HumiditySensor):
                hum_locs.add(s.location)
        return temp_locs.intersection(hum_locs)

    def add_sensor(self, sensor):
        if sensor.sensor_id in self.sensors:
            raise SensorError("Sensor ID '" + sensor.sensor_id + "' already exists.")
        self.sensors[sensor.sensor_id] = sensor

    def get_sensor(self, sensor_id):
        if sensor_id not in self.sensors:
            raise SensorError("Sensor ID '" + sensor_id + "' not found.")
        return self.sensors[sensor_id]

    def save_data(self, filename="sensor_data.npz"):
        ids = list(self.sensors.keys())
        np.savez(filename,
                 ids=np.array(ids),
                 locations=np.array([self.sensors[sid].location for sid in ids]),
                 types=np.array([type(self.sensors[sid]).__name__ for sid in ids]),
                 readings=np.array([self.sensors[sid].readings for sid in ids]))

    def load_data(self, filename="sensor_data.npz"):
        if not os.path.exists(filename):
            raise FileNotFoundError("Missing data file: " + filename)
        loaded = np.load(filename)
        kinds = {"TemperatureSensor": TemperatureSensor, "HumiditySensor": HumiditySensor}
        for sid, loc, kind, readings in zip(loaded["ids"], loaded["locations"], loaded["types"], loaded["readings"]):
            self.sensors[str(sid)] = kinds[str(kind)](str(sid), str(loc), readings)


def show_menu():
    print("\n--- Sensor Data Analyzer Menu ---")
    print("1. Add sensor (temperature / humidity)")
    print("2. Show sensor summary (min, max, mean, std)")
    print("3. Show daily averages")
    print("4. Show alerts (readings above threshold)")
    print("5. Show 3-hour moving average")
    print("6. Rank sensors by average")
    print("7. Compare two sensors (correlation)")
    print("8. Save and exit")

def add_new_sensor(station):
    stype = input("Enter type (temp/humidity): ").strip().lower()
    sid = input("Enter sensor ID: ").strip()
    loc = input("Enter location: ").strip()
    seed = 42 + len(station)
    if stype == "temp":
        sensor = TemperatureSensor(sid, loc, seed=seed)
    elif stype == "humidity":
        sensor = HumiditySensor(sid, loc, seed=seed)
    else:
        raise SensorError("Invalid sensor type entered.")
    station.add_sensor(sensor)
    print("Sensor " + sid + " added successfully.")
    print("Unique locations: " + ", ".join(sorted(station.unique_locations())))
    both = station.shared_locations()
    if both:
        print("Locations with both temperature and humidity sensors: " + ", ".join(sorted(both)))

def show_summary(station):
    sid = input("Enter sensor ID: ").strip()
    sensor = station.get_sensor(sid)
    mn, mx, mean_val = sensor.summary()
    std_val = float(np.std(sensor.readings))
    print(f"Summary for {sid}: Min={mn:.2f}{sensor.unit()}, Max={mx:.2f}{sensor.unit()}, Mean={mean_val:.2f}{sensor.unit()}, Std={std_val:.2f}")
    day, hour = sensor.peak_reading()
    print("Highest reading: Day " + str(day + 1) + ", Hour " + str(hour + 1))
    day, hour = sensor.lowest_reading()
    print("Lowest reading: Day " + str(day + 1) + ", Hour " + str(hour + 1))
    max_dev = float(np.max(np.abs(sensor.normalized())))
    print("Largest deviation from a daily mean: {:.2f}{}".format(max_dev, sensor.unit()))

def show_daily_averages(station):
    sid = input("Enter sensor ID: ").strip()
    sensor = station.get_sensor(sid)
    daily_avgs = np.mean(sensor.readings, axis=1)
    for day, avg in enumerate(daily_avgs, start=1):
        print("Day {} Average: {:.2f}{}".format(day, avg, sensor.unit()))
    hourly_avgs = sensor.hourly_averages()
    hours = np.arange(1, 25)
    print("Hourly averages: " + str(np.round(hourly_avgs, 2)))
    print("Highest average at hour " + str(hours[np.argmax(hourly_avgs)]) + ", lowest average at hour " + str(hours[np.argmin(hourly_avgs)]))
    if isinstance(sensor, TemperatureSensor):
        print("Daily averages in Fahrenheit: " + str(np.round(np.mean(sensor.to_fahrenheit(), axis=1), 2)))

def show_alerts(station):
    sid = input("Enter sensor ID: ").strip()
    sensor = station.get_sensor(sid)
    thresh = sensor.alert_threshold()
    mask = sensor.readings > thresh
    alert_count = int(np.sum(mask))
    print("Total readings above threshold (" + str(thresh) + sensor.unit() + "): " + str(alert_count))
    status = np.where(mask, "ALERT", "ok")
    alerts = [(int(d), int(h), float(sensor.readings[d, h]), str(status[d, h])) for d, h in zip(*np.where(mask))]
    for d, h, val, tag in alerts[:10]:
        print("  " + tag + " - Day " + str(d+1) + ", Hour " + str(h+1) + f": {val:.2f}{sensor.unit()}")

def show_moving_average(station):
    sid = input("Enter sensor ID: ").strip()
    sensor = station.get_sensor(sid)
    flat_readings = sensor.readings.flatten()
    weights = np.ones(3) / 3.0
    moving_avg = np.convolve(flat_readings, weights, mode='valid')
    print("First 10 values of 3-hour moving average: " + str(np.round(moving_avg[:10], 2)))

def show_ranking(station):
    if len(station.sensors) == 0:
        print("No sensors available.")
        return
    sids = list(station.sensors.keys())
    means = [np.mean(station.sensors[sid].readings) for sid in sids]
    sorted_indices = np.argsort(means)[::-1]
    print("Sensors ranked by average value (highest to lowest):")
    for rank, idx in enumerate(sorted_indices, 1):
        print(str(rank) + ". " + sids[idx] + " - Mean: " + "{:.2f}".format(means[idx]))

def compare_sensors(station):
    sid1 = input("Enter first sensor ID: ").strip()
    sid2 = input("Enter second sensor ID: ").strip()
    s1 = station.get_sensor(sid1)
    s2 = station.get_sensor(sid2)
    flat1 = s1.readings.flatten()
    flat2 = s2.readings.flatten()
    corr_matrix = np.corrcoef(flat1, flat2)
    corr_val = corr_matrix[0, 1]
    print("Correlation coefficient between {} and {}: {:.2f}".format(sid1, sid2, corr_val))


def main():
    station = Station()
    filename = "sensor_data.npz"

    try:
        station.load_data(filename)
        print("Previous sensor data loaded successfully.")
    except Exception:
        print("Starting with a fresh sensor network (no previous data found).")

    while True:
        show_menu()

        choice = input("Enter your choice (1-8): ").strip()

        try:
            # Scrambled order of option checks
            if choice == "3":
                show_daily_averages(station)

            elif choice == "1":
                add_new_sensor(station)

            elif choice == "5":
                show_moving_average(station)

            elif choice == "2":
                show_summary(station)

            elif choice == "4":
                show_alerts(station)

            elif choice == "7":
                compare_sensors(station)

            elif choice == "6":
                show_ranking(station)

            elif choice == "8":
                station.save_data(filename)
                print("Data saved successfully. Exiting program. Goodbye!")
                break

            else:
                print("Invalid menu choice. Please select between 1 and 8.")

        except SensorError as e:
            print("Error: " + str(e))
        except FileNotFoundError as e:
            print("File Error: " + str(e))
        except Exception as e:
            print("An unexpected error occurred: " + str(e))

if __name__ == "__main__":
    main()