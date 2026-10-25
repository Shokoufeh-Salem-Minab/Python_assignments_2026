import zipfile
import numpy as np

from temperature_sensor import TemperatureSensor
from humidity_sensor import HumiditySensor
from station import Station, SensorNotFoundError

DATA_FILE = "sensor_data.npz"



def generate_sensor_readings(sensor_type, rng):
    hours = np.arange(168)

    if sensor_type == "temperature":
        baseline = 18 + 4 * np.sin(
            2 * np.pi * (hours % 24) / 24
        )
        readings = rng.normal(
            loc = baseline,
            scale = 2,
            size = 168
        )

    else:
        baseline = 60 - 8 * np.sin(
            2 * np.pi * (hours % 24) / 24
        )
        readings = rng.normal(
            loc = baseline,
            scale = 5,
            size = 168
        )

    return np.array(readings).reshape(7, 24)


def save_station_data(station):
    sensors = list(station.sensors.values())

    sensor_ids = np.array(
        [sensor.sensor_id for sensor in sensors],
        dtype = str
    )

    locations = np.array(
        [sensor.location for sensor in sensors],
        dtype = str
    )

    sensor_types = []

    for sensor in sensors:
        if isinstance(sensor, TemperatureSensor):
            sensor_types.append("temperature")
        elif isinstance(sensor, HumiditySensor):
            sensor_types.append("humidity")
        else:
            raise ValueError (
                f"Unsupported sensor type: {type(sensor).__name__}"
            )

    sensor_types = np.array(sensor_types, dtype = str)

    if sensors:
        readings = np.stack([
            sensor.readings for sensor in sensors
        ])
    else:
        readings = np.empty((0, 7, 24), dtype = float)

    np.savez(
        DATA_FILE,
        sensor_ids = sensor_ids,
        locations = locations,
        sensor_types = sensor_types,
        readings = readings
    )

def load_station_data():
    station = Station()

    try:
        with np.load(DATA_FILE, allow_pickle = False) as saved:
            sensor_ids = saved["sensor_ids"]
            locations = saved["locations"]
            sensor_types = saved["sensor_types"]
            readings = saved["readings"]

            metadata_lengths = {
                len(sensor_ids),
                len(locations),
                len(sensor_types)
            }

            if len(metadata_lengths) != 1:
                raise ValueError("Saved sensor metadata is inconsistent.")

            expected_shape = (len(sensor_ids), 7, 24)

            if readings.shape != expected_shape:
                raise ValueError("Saved readings have an invalid shape.")

            if len(set(str(sensor_id) for sensor_id in sensor_ids)) != len(sensor_ids):
                raise ValueError("Saved data contains duplicate sensor IDs.")

            restored_sensors = []

            for index in range(len(sensor_ids)):
                sensor_id = str(sensor_ids[index])
                location = str(locations[index])
                sensor_types = str(sensor_types[index])

                if sensor_types == "temperature":
                    sensor = TemperatureSensor(
                        sensor_id,
                        location,
                        readings[index]
                    )

                elif sensor_types == "humidity":
                    sensor = HumiditySensor(
                        sensor_id,
                        location,
                        readings[index]
                    )

                else:
                    raise ValueError(
                        f"Unknown saved sensor type: {sensor_types}"
                    )

                restored_sensors.append(sensor)

    except FileNotFoundError:
        print("No saved data found. Starting with an empty station.")
        return station

    except (
        OSError,
        ValueError,
        KeyError,
        EOFError,
        zipfile.BadZipFile
    ) as error:
        print(f"Could not load saved data: {error}")
        print("Starting with an empty station.")
        return station

    for sensor in restored_sensors:
        station.add_sensor(sensor)

    print(f"Loaded {len(station)} sensor(s).")

    return station


def handle_add_sensor(station, rng):
    sensor_type = input(
        "Enter sensor type (temperature/humidity): "
    ).strip().lower()

    if sensor_type not in ("temperature", "humidity"):
        print("Invalid sensor type.")
        return

    sensor_id = input("Enter sensor ID: ").strip()
    location = input("Enter sensor location: ").strip()

    if not sensor_id:
        print("Sensor ID cannot be empty.")
        return

    if not location:
        print("Sensor location cannot be empty.")
        return

    try:
        readings = generate_sensor_readings(sensor_type, rng)

        if sensor_type == "temperature":
            sensor = TemperatureSensor(
                sensor_id,
                location,
                readings
            )
        else:
            sensor = HumiditySensor(
                sensor_id,
                location,
                readings
            )

        station.add_sensor(sensor)

    except ValueError as error:
        print(f"Could not add sensor: {error}")
        return

    print(f"Sensor added successfully: {sensor}")


def prompt_for_sensor(station):
    if len(station) == 0:
        print("There are no sensors registered.")
        return None

    sensor_id = input("Enter sensor ID: ").strip()

    try:
        return station.find_sensor_by_id(sensor_id)

    except SensorNotFoundError as error:
        print(error)
        return None


def display_sensor_summary(station):
    sensor = prompt_for_sensor(station)

    if sensor is None:
        return

    minimum, maximum, mean = sensor.summary()
    standard_deviation = np.std(sensor.readings)

    peak_day, peak_hour = sensor.peak_reading_time()
    lowest_day, lowest_hour = sensor.lowest_reading_time()

    print(f"\nSummary for {sensor}")
    print(f"Minimum: {minimum:.2f} {sensor.unit()}")
    print(f"Maximum: {maximum:.2f} {sensor.unit()}")
    print(f"Mean: {mean:.2f} {sensor.unit()}")
    print(f"Standard deviation: {standard_deviation:.2f}")

    peak_value = sensor.readings[peak_day - 1, peak_hour]
    lowest_value = sensor.readings[lowest_day - 1, lowest_hour]

    print(
        f"Highest reading: {peak_value:.2f} {sensor.unit()}, "
        f"day {peak_day}, hour {peak_hour:02d}:00"
    )

    print(
        f"Lowest reading: {lowest_value:.2f} {sensor.unit()}, "
        f"day {lowest_day}, hour {lowest_hour:02d}:00"
    )

    if isinstance(sensor, TemperatureSensor):
        fahrenheit_readings = sensor.convert_to_fahrenheit()

        print(
            f"Mean in Fahrenheit: "
            f"{np.mean(fahrenheit_readings):.2f} °F"
        )


def display_daily_averages(station):
    sensor = prompt_for_sensor(station)

    if sensor is None:
        return

    daily_means = sensor.daily_mean()

    print(f"\nDaily averages for {sensor.sensor_id}:")

    for day, average in enumerate(daily_means, start=1):
        print(f"Day {day}: {average:.2f} {sensor.unit()}")

    hourly_means = sensor.hourly_mean()

    print("\nHourly averages (hours 00–23):")
    print(np.round(hourly_means, 2))

    normalized = sensor.daily_normalised_readings()

    print("\nNormalized readings (each reading minus its day's mean):")

    for day, readings in enumerate(normalized, start=1):
        print(f"Day {day}: {np.round(readings, 2)}")


def display_alerts(station):
    sensor = prompt_for_sensor(station)

    if sensor is None:
        return

    mask = sensor.readings > sensor.alert_threshold()
    alert_count = np.count_nonzero(mask)

    alert_records = sensor.show_alerts()

    print(
        f"\nFound {alert_count} alert reading(s) "
        f"for sensor {sensor.sensor_id}."
    )

    if not alert_records:
        print("No readings exceeded the threshold.")
        return

    print(f"Alert threshold: {sensor.alert_threshold()} {sensor.unit()}")

    for day, hour, reading, status in alert_records:
        print(
            f"Day {day}, hour {hour:02d}:00: "
            f"{reading:.2f} {sensor.unit()} [{status}]"
        )


def display_three_hour_average(station):
    sensor = prompt_for_sensor(station)

    if sensor is None:
        return

    averages = sensor.show_3_hour_average()

    print(
        f"\nThree-hour moving averages for sensor {sensor.sensor_id}:"
    )
    print(np.round(averages, 2))
    print(f"Number of averages: {len(averages)}")


def display_sensor_ranking(station):
    ranking = station.rank_sensors_by_average()

    if not ranking:
        print("There are no sensors to rank.")
        return

    print("\nSensors ranked by average reading (highest first):")

    for rank, (sensor, average) in enumerate(ranking, start=1):
        print(
            f"{rank}. {sensor.sensor_id} at {sensor.location}: "
            f"{average:.2f} {sensor.unit()}"
        )

    locations = station.get_unique_locations()
    shared_locations = station.find_shared_sensor_locations()

    print("\nUnique sensor locations:")
    print(", ".join(sorted(locations)) if locations else "None")

    print("\nLocations with both temperature and humidity sensors:")
    print(
        ", ".join(sorted(shared_locations))
        if shared_locations
        else "None"
    )


def compare_two_sensors(station):
    if len(station) < 2:
        print("At least two sensors are needed for comparison.")
        return

    first_id = input("Enter the first sensor ID: ").strip()
    second_id = input("Enter the second sensor ID: ").strip()

    try:
        correlation = station.calculate_sensor_correlation(
            first_id,
            second_id
        )

        if np.isnan(correlation):
            print("Correlation cannot be calculated for these readings.")
        else:
            print(
                f"Correlation between {first_id} and {second_id}: "
                f"{correlation:.2f}"
            )

    except SensorNotFoundError as error:
        print(error)




def main():

    rng = np.random.default_rng(42)
    station = load_station_data()

    while True:
        print("\n1. Add sensor (temperature or humidity)")
        print("2. Show sensor summary (min|max|mean|std)")
        print("3. Show daily averages")
        print("4. Show alerts (readings above threshold)")
        print("5. Show 3-hour moving average")
        print("6. Rank sensors by average")
        print("7. Compare two sensors (correlation)")
        print("8. Save and exit")

        try:
            choice = int(input("Choose an option: "))
        except ValueError:
            print("Invalid input. Enter a number from 1 - 8.")
            continue

        match choice:
            case 1:
                handle_add_sensor(station, rng)

            case 2:
                display_sensor_summary(station)

            case 3:
                display_daily_averages(station)

            case 4:
                display_alerts(station)

            case 5:
                display_three_hour_average(station)

            case 6:
                display_sensor_ranking(station)

            case 7:
                compare_two_sensors(station)

            case 8:
                try:
                    save_station_data(station)
                    print("Data saved successfully.")
                    break

                except (OSError, ValueError) as error:
                    print(f"Could not save the data: {error}")

            case _:
                print("Invalid menu choice. Choose a number from 1 to 8.")


if __name__ == "__main__":
    main()  