import numpy as np


DATA_FILE = "sensor_data.npz"
HOURS = np.arange(24)


class SensorNotFoundError(Exception):
	"""Raised when a requested sensor ID is not in the station."""


class Sensor:
	def __init__(self, sensor_id, location, readings):
		self.sensor_id = str(sensor_id)
		self.location = str(location)
		self.readings = np.array(readings, dtype=float).reshape(7, 24)

	def alert_threshold(self):
		raise NotImplementedError

	def unit(self):
		raise NotImplementedError

	def summary(self):
		return (float(np.min(self.readings)), float(np.max(self.readings)),
				float(np.mean(self.readings)))

	def peak_time(self):
		return tuple(int(value) for value in np.unravel_index(
			np.argmax(self.readings), self.readings.shape))

	def daily_averages(self):
		return self.readings.mean(axis=1)

	def hourly_averages(self):
		return self.readings.mean(axis=0)

	def normalized_readings(self):
		return self.readings - self.daily_averages()[:, np.newaxis]

	def __str__(self):
		return f"{self.sensor_id} ({type(self).__name__}, {self.location})"


class TemperatureSensor(Sensor):
	def alert_threshold(self):
		return 30.0

	def unit(self):
		return "°C"

	def fahrenheit_readings(self):
		return self.readings * (9 / 5) + 32


class HumiditySensor(Sensor):
	def alert_threshold(self):
		return 80.0

	def unit(self):
		return "%"


class Station:
	def __init__(self):
		self.sensors = {}
		self.rng = np.random.default_rng(2025)

	def __len__(self):
		return len(self.sensors)

	def add_sensor(self, sensor):
		if sensor.sensor_id in self.sensors:
			raise ValueError(f"Sensor ID '{sensor.sensor_id}' already exists.")
		self.sensors[sensor.sensor_id] = sensor

	def get_sensor(self, sensor_id):
		try:
			return self.sensors[str(sensor_id)]
		except KeyError as error:
			raise SensorNotFoundError(f"Unknown sensor ID: {sensor_id}") from error

	def locations(self):
		return {sensor.location for sensor in self.sensors.values()}

	def locations_with_both_types(self):
		temperature_locations = {s.location for s in self.sensors.values()
								 if isinstance(s, TemperatureSensor)}
		humidity_locations = {s.location for s in self.sensors.values()
							  if isinstance(s, HumiditySensor)}
		return temperature_locations & humidity_locations

	def save(self, filename=DATA_FILE):
		sensors = list(self.sensors.values())
		ids = np.array([s.sensor_id for s in sensors], dtype=str)
		locations = np.array([s.location for s in sensors], dtype=str)
		kinds = np.array(["temperature" if isinstance(s, TemperatureSensor)
						  else "humidity" for s in sensors], dtype=str)
		readings = (np.stack([s.readings for s in sensors]) if sensors
					else np.empty((0, 7, 24)))
		np.savez_compressed(filename, ids=ids, locations=locations,
							kinds=kinds, readings=readings)

	def load(self, filename=DATA_FILE):
		try:
			with np.load(filename, allow_pickle=False) as data:
				ids = data["ids"]
				locations = data["locations"]
				kinds = data["kinds"]
				readings = data["readings"]
		except FileNotFoundError:
			print(f"No saved data found ({filename}); starting with an empty station.")
			return
		except (OSError, ValueError, KeyError) as error:
			print(f"Could not load saved data: {error}. Starting empty.")
			return

		for sensor_id, location, kind, values in zip(ids, locations, kinds, readings):
			sensor_class = {"temperature": TemperatureSensor,
							"humidity": HumiditySensor}.get(str(kind))
			if sensor_class is not None:
				self.sensors[str(sensor_id)] = sensor_class(sensor_id, location, values)

	def create_sensor(self, sensor_id, location, kind):
		settings = {
			"temperature": (TemperatureSensor, 20.0, 6.0),
			"humidity": (HumiditySensor, 55.0, 15.0),
		}
		sensor_class, center, spread = settings[kind]
		readings = np.array(self.rng.normal(center, spread, size=7 * 24)).reshape(7, 24)
		sensor = sensor_class(sensor_id, location, readings)
		self.add_sensor(sensor)
		return sensor


def print_sensor_summary(sensor):
	minimum, maximum, average = sensor.summary()
	standard_deviation = np.std(sensor.readings)
	day, hour = sensor.peak_time()
	print(f"{sensor}: min={minimum:.2f} {sensor.unit()}, max={maximum:.2f} {sensor.unit()}, "
		  f"mean={average:.2f} {sensor.unit()}, std={standard_deviation:.2f}")
	print(f"Peak reading: day {day + 1}, hour {hour:02d}:00")
	if isinstance(sensor, TemperatureSensor):
		print(f"Mean in Fahrenheit: {np.mean(sensor.fahrenheit_readings()):.2f} °F")


def show_daily_averages(sensor):
	averages = sensor.daily_averages()
	normalized = sensor.normalized_readings()
	for day, average in enumerate(averages, start=1):
		deviation = np.max(np.abs(normalized[day - 1]))
		print(f"Day {day}: average={average:.2f} {sensor.unit()}, "
			  f"largest deviation from daily mean={deviation:.2f} {sensor.unit()}")


def show_alerts(sensor):
	mask = sensor.readings > sensor.alert_threshold()
	marked = np.where(mask, "ALERT", "OK")
	records = [(int(day + 1), int(hour), float(sensor.readings[day, hour]))
			   for day, hour in zip(*np.where(marked == "ALERT"))]
	print(f"{len(records)} alert reading(s) above {sensor.alert_threshold():.2f} {sensor.unit()}.")
	for day, hour, value in records:
		print(f"Day {day}, {hour:02d}:00: {value:.2f} {sensor.unit()} — ALERT")


def select_sensor(station):
	sensor_id = input("Sensor ID: ").strip()
	return station.get_sensor(sensor_id)


def main():
	station = Station()
	station.load()
	while True:
		print("\nSensor Data Analyzer")
		print("1. Add sensor (temperature / humidity)")
		print("2. Show sensor summary (min, max, mean, std)")
		print("3. Show daily averages")
		print("4. Show alerts")
		print("5. Show 3-hour moving average")
		print("6. Rank sensors by average")
		print("7. Compare two sensors (correlation)")
		print("8. Save and exit")
		choice = input("Choose an option: ").strip()

		try:
			if choice == "1":
				sensor_id = input("Sensor ID: ").strip()
				location = input("Location: ").strip()
				kind = input("Type (temperature/humidity): ").strip().lower()
				if kind not in ("temperature", "humidity"):
					raise ValueError("Type must be temperature or humidity.")
				sensor = station.create_sensor(sensor_id, location, kind)
				print(f"Added {sensor}. Readings are simulated for 7 days.")
			elif choice == "2":
				print_sensor_summary(select_sensor(station))
			elif choice == "3":
				show_daily_averages(select_sensor(station))
			elif choice == "4":
				show_alerts(select_sensor(station))
			elif choice == "5":
				sensor = select_sensor(station)
				moving = np.convolve(sensor.hourly_averages(), np.ones(3) / 3, mode="valid")
				print("3-hour moving averages:", np.round(moving, 2))
			elif choice == "6":
				sensors = list(station.sensors.values())
				if not sensors:
					print("No sensors have been added.")
					continue
				averages = np.array([np.mean(sensor.readings) for sensor in sensors])
				order = np.argsort(averages)
				for index in order:
					print(f"{sensors[index]}: {averages[index]:.2f} {sensors[index].unit()}")
			elif choice == "7":
				first = select_sensor(station)
				second = station.get_sensor(input("Second sensor ID: ").strip())
				correlation = np.corrcoef(first.readings.ravel(), second.readings.ravel())[0, 1]
				print(f"Correlation: {correlation:.2f}")
			elif choice == "8":
				station.save()
				print(f"Saved {len(station)} sensor(s) to {DATA_FILE}.")
				break
			else:
				print("Invalid menu option. Enter a number from 1 to 8.")
		except (ValueError, SensorNotFoundError) as error:
			print(f"Input error: {error}")


if __name__ == "__main__":
	main()
