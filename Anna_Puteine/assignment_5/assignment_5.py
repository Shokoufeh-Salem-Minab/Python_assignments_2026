import numpy as np

from sensor import TemperatureSensor, SensorError
from station import Station, sensor_types

station = Station()

try:
    station.loadFromStorage()
    print(f"Data loaded. Sensors in station: {len(station)}")
except FileNotFoundError:
    print("No saved data found. Starting with an empty station.")
except Exception:
    print("Error: could not read the saved file. Starting with an empty station.")
    station = Station()

def askSensor(text="Sensor id: "):
    return station.getSensor(input(text).strip())

def addSensor():
    kind = input("Sensor type (temperature/humidity): ").strip().lower()
    sensor_id = input("Sensor id: ").strip()
    location = input("Location: ").strip()

    if kind not in sensor_types:
        raise SensorError("Type must be temperature or humidity")
    if sensor_id == "" or location == "":
        raise SensorError("Sensor id and location cannot be empty")

    sensor = sensor_types[kind](sensor_id, location, seed=42 + len(station))
    station.addSensor(sensor)
    print(f"Sensor added: {sensor}")

def showSummary():
    sensor = askSensor()
    minimum, maximum, mean = sensor.summary()
    peak_day, peak_hour = sensor.peak()
    low_day, low_hour = sensor.lowest()

    print(f"\n{sensor}")
    print(f"Min: {minimum:.2f}, Max: {maximum:.2f}, Mean: {mean:.2f}, Std: {sensor.readings.std():.2f} {sensor.unit()}")
    print(f"Highest reading: day {peak_day + 1}, hour {peak_hour}")
    print(f"Lowest reading: day {low_day + 1}, hour {low_hour}")

    if isinstance(sensor, TemperatureSensor):
        print(f"Mean in Fahrenheit: {sensor.toFahrenheit().mean():.2f} F")

def showDailyAverages():
    sensor = askSensor()
    daily = sensor.readings.mean(axis=1)
    normalized = sensor.readings - daily.reshape(7, 1)

    print(f"\nDaily report for {sensor}:")
    for day in range(7):
        print(f"Day {day + 1}: average {daily[day]:.2f}, biggest change {np.abs(normalized[day]).max():.2f}")

    print("\nHourly averages:")
    print(np.round(sensor.readings.mean(axis=0), 2))

def showAlerts():
    sensor = askSensor()
    alerts = sensor.alerts()

    print(f"\nThreshold: {sensor.alert_threshold()} {sensor.unit()}, alerts: {len(alerts)}")
    for day, hour, value in alerts:
        print(f"Day {day + 1}, hour {hour}: {value:.2f} {sensor.unit()}")

def showMovingAverage():
    sensor = askSensor()
    day = int(input("Day (1-7): "))

    if day < 1 or day > 7:
        raise SensorError("Day must be between 1 and 7")

    print(np.round(sensor.movingAverage(day - 1), 2))

def showRanking():
    print("\nRanking by average:")
    for sensor, average in station.ranking():
        print(f"{sensor} - {average:.2f} {sensor.unit()}")

    print(f"Locations with both sensor types: {station.locationsWithBoth()}")

def compareSensors():
    first = askSensor("First sensor id: ")
    second = askSensor("Second sensor id: ")
    print(f"Correlation: {first.correlation(second):.2f}")

while True:
    print("\n1. Add sensor (temperature / humidity)")
    print("2. Show sensor summary (min, max, mean, std)")
    print("3. Show daily averages")
    print("4. Show alerts (readings above threshold)")
    print("5. Show 3-hour moving average")
    print("6. Rank sensors by average")
    print("7. Compare two sensors (correlation)")
    print("8. Save and exit")
    print(f"Sensors in station: {len(station)}")

    choice = input("Choose an option: ")

    try:
        if choice == "1":
            addSensor()
        elif choice == "2":
            showSummary()
        elif choice == "3":
            showDailyAverages()
        elif choice == "4":
            showAlerts()
        elif choice == "5":
            showMovingAverage()
        elif choice == "6":
            showRanking()
        elif choice == "7":
            compareSensors()
        elif choice == "8":
            station.saveToStorage()
            print("Data saved. Goodbye!")
            break
        else:
            print("Error: unknown option, choose 1-8.")

    except SensorError as ex:
        print(f"Error: {ex}")
    except ValueError:
        print("Error: please enter a valid number")
    except Exception:
        print("Something went wrong")
