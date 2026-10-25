# Akhil Kammalan Kandy, ak23204, Assignment 5 - Sensor Data Analyzer

import os
import numpy as np

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sensors_data.npz")
DAYS = 7
HOURS = 24
WINDOW_SIZE = 3
EXIT_CHOICE = "8"

DAY_NAMES = np.array(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
HOUR_INDICES = np.arange(HOURS)
DAILY_CYCLE = np.sin(np.linspace(0, 2 * np.pi, HOURS, endpoint=False))

MENU = """
 Sensor Data Analyzer
1. Add sensor (temperature / humidity)
2. Show sensor summary (min, max, mean, std)
3. Show daily averages
4. Show alerts (readings above threshold)
5. Show 3-hour moving average
6. Rank sensors by average
7. Compare two sensors (correlation)
8. Save and exit"""


# Custom errors

class SensorError(Exception):
    # Base error
    pass


class UnknownSensorError(SensorError):
    # Sensor ID is missing
    pass


class DuplicateSensorError(SensorError):
    # Sensor ID already exists
    pass


class InvalidInputError(SensorError):
    # Input is invalid
    pass


# Sensor types

class Sensor:
    # Base sensor

    type_name = "generic"
    label = "Generic"
    default_mean = 0.0
    default_std = 1.0

    def __init__(self, sensor_id, location, readings=None, seed=42):
        self.sensor_id = sensor_id
        self.location = location
        if readings is None:
            self.readings = self._simulate_readings(seed)
        else:
            self.readings = np.array(readings, dtype=float).reshape(DAYS, HOURS)

    def _simulate_readings(self, seed):
        rng = np.random.default_rng(seed)
        noise = rng.normal(loc=self.default_mean, scale=self.default_std, size=DAYS * HOURS)
        grid = noise.reshape(DAYS, HOURS) + DAILY_CYCLE
        return np.round(grid, 2)

    def alert_threshold(self):
        return 0.0

    def unit(self):
        return ""

    def summary(self):
        # Return basic statistics
        return (
            float(np.min(self.readings)),
            float(np.max(self.readings)),
            float(np.mean(self.readings)),
        )

    def std_dev(self):
        return float(np.std(self.readings))

    def peak_time(self):
        # Find the highest reading
        flat_idx = int(np.argmax(self.readings))
        return (flat_idx // HOURS, flat_idx % HOURS)

    def lowest_time(self):
        # Find the lowest reading
        flat_idx = int(np.argmin(self.readings))
        return (flat_idx // HOURS, flat_idx % HOURS)

    def daily_averages(self):
        return self.readings.mean(axis=1)

    def hourly_averages(self):
        return self.readings.mean(axis=0)

    def normalized_readings(self):
        # Center each day around its mean
        return self.readings - self.daily_averages()[:, np.newaxis]

    def alert_mask_and_labels(self):
        # Mark readings above the threshold
        threshold = self.alert_threshold()
        mask = self.readings > threshold
        labels = np.where(mask, "ALERT", "OK")
        return mask, labels

    def alert_records(self):
        # Build alert records
        mask, labels = self.alert_mask_and_labels()
        coords = np.argwhere(mask)
        return [
            (
                str(DAY_NAMES[int(day)]),
                int(HOUR_INDICES[int(hour)]),
                float(self.readings[int(day), int(hour)]),
                str(labels[int(day), int(hour)]),
            )
            for day, hour in coords
        ]

    def moving_average(self, window=WINDOW_SIZE):
        # Calculate the moving average
        kernel = np.ones(window) / window
        return np.convolve(self.readings.ravel(), kernel, mode="valid")

    def __str__(self):
        min_v, max_v, mean_v = self.summary()
        return (
            f"[{self.sensor_id}] {self.label} Sensor @ {self.location} "
            f"(mean: {mean_v:.2f}{self.unit()}, min: {min_v:.2f}{self.unit()}, "
            f"max: {max_v:.2f}{self.unit()}, threshold: {self.alert_threshold():.2f}{self.unit()})"
        )


class TemperatureSensor(Sensor):
    # Temperature sensor

    type_name = "temperature"
    label = "Temperature"
    default_mean = 22.0
    default_std = 4.5

    def alert_threshold(self):
        return 28.0

    def unit(self):
        return "°C"

    def to_fahrenheit(self):
        # Convert readings to Fahrenheit
        return self.readings * 1.8 + 32.0


class HumiditySensor(Sensor):
    # Humidity sensor

    type_name = "humidity"
    label = "Humidity"
    default_mean = 60.0
    default_std = 12.0

    def _simulate_readings(self, seed):
        readings = super()._simulate_readings(seed)
        return np.clip(readings, 0.0, 100.0)

    def alert_threshold(self):
        return 80.0

    def unit(self):
        return "%"


SENSOR_TYPES = {cls.type_name: cls for cls in (TemperatureSensor, HumiditySensor)}


# Sensor station

class Station:
    # Stores sensors by ID

    def __init__(self):
        self.sensors = {}
        self.locations = set()

    def __len__(self):
        return len(self.sensors)

    def ensure_id_available(self, sensor_id):
        if sensor_id in self.sensors:
            raise DuplicateSensorError(f"Sensor ID '{sensor_id}' is already in use.")

    def add_sensor(self, sensor):
        self.ensure_id_available(sensor.sensor_id)
        self.sensors[sensor.sensor_id] = sensor
        self.locations.add(sensor.location)

    def get_sensor(self, sensor_id):
        try:
            return self.sensors[sensor_id]
        except KeyError:
            raise UnknownSensorError(f"No sensor with ID '{sensor_id}'.") from None

    def dual_sensor_locations(self):
        # Find locations with both sensor types
        temp_locs = {
            s.location for s in self.sensors.values() if isinstance(s, TemperatureSensor)
        }
        hum_locs = {
            s.location for s in self.sensors.values() if isinstance(s, HumiditySensor)
        }
        return temp_locs & hum_locs

    def rank_by_average(self):
        # Rank sensors by average reading
        if not self.sensors:
            return []
        sensor_list = list(self.sensors.values())
        averages = np.array([s.summary()[2] for s in sensor_list])
        order = np.argsort(averages)[::-1]
        sorted_averages = np.sort(averages)[::-1]
        return [(sensor_list[int(i)], float(sorted_averages[idx])) for idx, i in enumerate(order)]

    def correlate(self, id_a, id_b):
        # Compare two sensors
        sensor_a = self.get_sensor(id_a)
        sensor_b = self.get_sensor(id_b)
        matrix = np.corrcoef(sensor_a.readings.ravel(), sensor_b.readings.ravel())
        return float(matrix[0, 1])

    def save(self, path=DATA_FILE):
        ids = np.array([s.sensor_id for s in self.sensors.values()], dtype=str)
        types = np.array([s.type_name for s in self.sensors.values()], dtype=str)
        locations = np.array([s.location for s in self.sensors.values()], dtype=str)
        if self.sensors:
            readings = np.array([s.readings for s in self.sensors.values()], dtype=float)
        else:
            readings = np.empty((0, DAYS, HOURS), dtype=float)
        np.savez(path, ids=ids, types=types, locations=locations, readings=readings)

    def load(self, path=DATA_FILE):
        try:
            with np.load(path, allow_pickle=False) as data:
                ids = data["ids"]
                types = data["types"]
                locations = data["locations"]
                readings = data["readings"]
        except FileNotFoundError:
            raise
        except (OSError, ValueError, KeyError) as error:
            raise SensorError(f"Could not read '{path}': {error}") from None

        self.sensors = {}
        self.locations = set()
        for sensor_id, s_type, loc, arr in zip(ids, types, locations, readings):
            cls = SENSOR_TYPES.get(str(s_type))
            if cls is None:
                raise SensorError(f"Unknown sensor type '{s_type}' in data file.")
            self.add_sensor(cls(str(sensor_id), str(loc), readings=arr))


# Input functions

def read_text(prompt):
    text = input(prompt).strip()
    if not text:
        raise InvalidInputError("Input cannot be empty.")
    return text


def read_seed(prompt, default_seed):
    text = input(prompt).strip()
    if not text:
        return default_seed
    try:
        return int(text)
    except ValueError:
        raise InvalidInputError(f"'{text}' is not a valid integer seed.") from None


# Menu actions

def add_sensor_action(station):
    kind = read_text("Sensor type - (t)emperature or (h)umidity: ").lower()
    if kind in ("t", "temp", "temperature"):
        cls = TemperatureSensor
    elif kind in ("h", "hum", "humidity"):
        cls = HumiditySensor
    else:
        raise InvalidInputError("Sensor type must be 't' (temperature) or 'h' (humidity).")

    sensor_id = read_text("Sensor ID: ")
    station.ensure_id_available(sensor_id)
    location = read_text("Location: ").title()
    default_seed = len(station) + 101
    seed = read_seed(f"Random seed (press Enter for {default_seed}): ", default_seed)

    sensor = cls(sensor_id, location, seed=seed)
    station.add_sensor(sensor)
    print(f"Added: {sensor}")

    both = station.dual_sensor_locations()
    if both:
        print(f"Locations with both temperature & humidity sensors: {', '.join(sorted(both))}")


def show_summary_action(station):
    sensor = station.get_sensor(read_text("Sensor ID: "))
    min_val, max_val, mean_val = sensor.summary()
    std_val = sensor.std_dev()
    peak_day, peak_hour = sensor.peak_time()
    low_day, low_hour = sensor.lowest_time()
    unit = sensor.unit()

    print(f"\nSummary for {sensor}")
    print(f"  Min : {min_val:.2f}{unit} (on {DAY_NAMES[peak_day if min_val == max_val else low_day]} at {low_hour:02d}:00)")
    print(f"  Max : {max_val:.2f}{unit} (on {DAY_NAMES[peak_day]} at {peak_hour:02d}:00)")
    print(f"  Mean: {mean_val:.2f}{unit}")
    print(f"  Std : {std_val:.2f}{unit}")

    if isinstance(sensor, TemperatureSensor):
        fahr = sensor.to_fahrenheit()
        print(
            f"  Fahrenheit: min {np.min(fahr):.2f}°F, "
            f"max {np.max(fahr):.2f}°F, mean {np.mean(fahr):.2f}°F"
        )


def show_daily_averages_action(station):
    sensor = station.get_sensor(read_text("Sensor ID: "))
    daily_means = np.round(sensor.daily_averages(), 2)
    hourly_means = np.round(sensor.hourly_averages(), 2)
    normalized = sensor.normalized_readings()
    unit = sensor.unit()

    print(f"\nDaily report for {sensor.sensor_id} ({sensor.location}):")
    for day_idx in range(DAYS):
        day_norm_max = float(np.max(np.abs(normalized[day_idx])))
        print(
            f"  Day {day_idx + 1} ({DAY_NAMES[day_idx]}): "
            f"average = {daily_means[day_idx]:.2f}{unit} "
            f"(max deviation from daily mean: {day_norm_max:.2f}{unit})"
        )

    peak_hr = int(np.argmax(hourly_means))
    low_hr = int(np.argmin(hourly_means))
    print(
        f"Hourly average across 7 days: lowest at {low_hr:02d}:00 ({hourly_means[low_hr]:.2f}{unit}), "
        f"highest at {peak_hr:02d}:00 ({hourly_means[peak_hr]:.2f}{unit})"
    )


def show_alerts_action(station):
    sensor = station.get_sensor(read_text("Sensor ID: "))
    mask, _ = sensor.alert_mask_and_labels()
    alert_count = int(np.sum(mask))
    records = sensor.alert_records()
    unit = sensor.unit()

    print(
        f"\nAlerts for {sensor.sensor_id} "
        f"(threshold > {sensor.alert_threshold():.2f}{unit}): {alert_count} alert(s) found."
    )
    if not records:
        print("  No readings exceeded the threshold.")
        return
    for day_name, hour, value, status in records[:15]:
        print(f"  [{status}] {day_name} {hour:02d}:00 -> {value:.2f}{unit}")
    if len(records) > 15:
        print(f"  ... and {len(records) - 15} more alert(s).")


def show_moving_average_action(station):
    sensor = station.get_sensor(read_text("Sensor ID: "))
    mov_avg = np.round(sensor.moving_average(WINDOW_SIZE), 2)
    unit = sensor.unit()

    print(
        f"\n{WINDOW_SIZE}-hour moving average for {sensor.sensor_id} "
        f"({len(mov_avg)} windows across {DAYS} days):"
    )
    print(f"  Overall moving average: min {np.min(mov_avg):.2f}{unit}, max {np.max(mov_avg):.2f}{unit}")
    print("  First 12 windows:")
    preview = ", ".join(f"{val:.2f}{unit}" for val in mov_avg[:12])
    print(f"    {preview}")


def rank_sensors_action(station):
    if len(station) == 0:
        print("No sensors registered yet.")
        return
    ranked = station.rank_by_average()
    print(f"\nSensor ranking by average reading ({len(station)} sensor(s)):")
    for rank, (sensor, avg_val) in enumerate(ranked, start=1):
        print(
            f"  {rank}. [{sensor.sensor_id}] {sensor.label} @ {sensor.location} "
            f"- average: {avg_val:.2f}{sensor.unit()}"
        )
    all_locs = ", ".join(sorted(station.locations)) or "none"
    both_locs = ", ".join(sorted(station.dual_sensor_locations())) or "none"
    print(f"All locations: {all_locs}")
    print(f"Locations with both temperature and humidity: {both_locs}")


def compare_sensors_action(station):
    if len(station) < 2:
        print("At least 2 sensors are required to compare.")
        return
    id_a = read_text("First sensor ID: ")
    id_b = read_text("Second sensor ID: ")
    corr = station.correlate(id_a, id_b)
    sensor_a = station.get_sensor(id_a)
    sensor_b = station.get_sensor(id_b)

    print(f"\nCorrelation between [{sensor_a.sensor_id}] and [{sensor_b.sensor_id}]: {corr:.2f}")
    if np.isnan(corr):
        print("  Correlation is undefined (one of the sensors has zero variance).")
    elif abs(corr) >= 0.7:
        print("  Strong relationship between the two sensors.")
    elif abs(corr) >= 0.3:
        print("  Moderate relationship between the two sensors.")
    else:
        print("  Weak or no linear relationship between the two sensors.")


ACTIONS = {
    "1": add_sensor_action,
    "2": show_summary_action,
    "3": show_daily_averages_action,
    "4": show_alerts_action,
    "5": show_moving_average_action,
    "6": rank_sensors_action,
    "7": compare_sensors_action,
}


# Main program

def save_and_exit(station):
    try:
        station.save()
    except OSError as error:
        print(f"Error: could not save data ({error}). Returning to the menu.")
        return False
    print(f"Saved {len(station)} sensor(s) to {os.path.basename(DATA_FILE)}. Goodbye!")
    return True


def handle_choice(station, choice):
    if choice == EXIT_CHOICE:
        return not save_and_exit(station)
    action = ACTIONS.get(choice)
    if action is None:
        print(f"Error: '{choice}' is not a menu option. Choose 1-8.")
        return True
    try:
        action(station)
    except SensorError as error:
        print(f"Error: {error}")
    return True


def main():
    station = Station()
    try:
        station.load()
        print(f"Loaded {len(station)} sensor(s) from {os.path.basename(DATA_FILE)}.")
    except FileNotFoundError:
        print("No saved data file found. Starting with an empty station.")
    except SensorError as error:
        print(f"Warning: {error}. Starting with an empty station.")

    running = True
    try:
        while running:
            print(MENU)
            choice = input("Choose an option (1-8): ").strip()
            running = handle_choice(station, choice)
    except (EOFError, KeyboardInterrupt):
        print("\nInput closed - saving and exiting.")
        save_and_exit(station)


if __name__ == "__main__":
    main()
