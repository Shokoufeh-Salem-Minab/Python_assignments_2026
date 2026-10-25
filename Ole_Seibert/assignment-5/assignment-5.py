# Homework 5 - Sensor Data Analyzer

import numpy as np

FILE_NAME = 'sensors.npz'
SEED = 42
DAYS = 7
HOURS = 24


# my own exceptions
class SensorNotFoundError(Exception):
    pass


class InvalidInputError(Exception):
    pass


def generate_readings(base, amplitude, noise, seed):
    # 7 days x 24 hours: a daily curve (warmest in the afternoon) plus random noise
    rng = np.random.default_rng(seed)
    hours = np.arange(HOURS)
    day_curve = base + amplitude * np.sin((hours - 9) / HOURS * 2 * np.pi)
    noise_values = rng.normal(0, noise, DAYS * HOURS).reshape(DAYS, HOURS)
    return noise_values + day_curve  # broadcasting: (7, 24) + (24,)


class Sensor:
    def __init__(self, sensor_id, location, readings):
        self.sensor_id = sensor_id
        self.location = location
        self.readings = np.array(readings).reshape(DAYS, HOURS)

    def sensor_type(self):
        return 'sensor'

    def unit(self):
        return ''

    def alert_threshold(self):
        return 0

    def summary(self):
        # returns a tuple (min, max, mean)
        return (self.readings.min(), self.readings.max(), self.readings.mean())

    def peak_time(self):
        # returns a tuple (day, hour) of the highest reading
        index = self.readings.argmax()
        return (index // HOURS + 1, index % HOURS)

    def lowest_time(self):
        index = self.readings.argmin()
        return (index // HOURS + 1, index % HOURS)

    def daily_averages(self):
        return self.readings.mean(axis=1)

    def hourly_averages(self):
        return self.readings.mean(axis=0)

    def normalized(self):
        # subtract the average of each day from the readings of that day
        return self.readings - self.daily_averages().reshape(DAYS, 1)

    def alert_mask(self, threshold):
        return self.readings > threshold

    def alerts(self, threshold):
        # list of tuples (day, hour, value)
        days, hours = np.where(self.alert_mask(threshold))
        return [(d + 1, h, self.readings[d, h]) for d, h in zip(days, hours)]

    def moving_average(self, day):
        # 3-hour moving average for one day
        return np.convolve(self.readings[day - 1], np.ones(3) / 3, mode='valid')

    def __str__(self):
        return f'{self.sensor_id}: {self.sensor_type()} sensor in {self.location}'


class TemperatureSensor(Sensor):
    def sensor_type(self):
        return 'temperature'

    def unit(self):
        return '°C'

    def alert_threshold(self):
        return 25

    def to_fahrenheit(self):
        return self.readings * 9 / 5 + 32


class HumiditySensor(Sensor):
    def sensor_type(self):
        return 'humidity'

    def unit(self):
        return '%'

    def alert_threshold(self):
        return 70


def create_sensor(sensor_type, sensor_id, location, seed):
    if sensor_type == 'temperature':
        return TemperatureSensor(sensor_id, location, generate_readings(21, 4, 1.5, seed))
    # humidity goes down when it gets warm, so the curve is the other way around
    return HumiditySensor(sensor_id, location, generate_readings(60, -10, 4, seed))


class Station:
    def __init__(self):
        self.sensors = {}  # {sensor_id: Sensor}

    def __len__(self):
        return len(self.sensors)

    def add_sensor(self, sensor):
        if sensor.sensor_id in self.sensors:
            raise ValueError('this sensor ID already exists')
        self.sensors[sensor.sensor_id] = sensor

    def get_sensor(self, sensor_id):
        if sensor_id not in self.sensors:
            raise SensorNotFoundError(f'no sensor with ID {sensor_id}')
        return self.sensors[sensor_id]

    def all_locations(self):
        return {s.location for s in self.sensors.values()}

    def locations_with_both(self):
        temperature = set()
        humidity = set()
        for sensor in self.sensors.values():
            if sensor.sensor_type() == 'temperature':
                temperature.add(sensor.location)
            else:
                humidity.add(sensor.location)
        return temperature & humidity

    def ranking(self, sensor_type):
        sensors = [s for s in self.sensors.values() if s.sensor_type() == sensor_type]
        averages = np.array([s.readings.mean() for s in sensors])
        order = np.argsort(averages)[::-1]  # highest average first
        return [sensors[i] for i in order]

    def save(self):
        sensors = list(self.sensors.values())
        np.savez(FILE_NAME,
                 ids=np.array([s.sensor_id for s in sensors]),
                 types=np.array([s.sensor_type() for s in sensors]),
                 locations=np.array([s.location for s in sensors]),
                 readings=np.array([s.readings for s in sensors]))

    def load(self):
        try:
            data = np.load(FILE_NAME)
            ids = data['ids']
            types = data['types']
            locations = data['locations']
            readings = data['readings']
        except FileNotFoundError:
            print('No saved file found, starting with an empty station.')
            return
        except (OSError, ValueError, KeyError):
            print('Saved file is broken, starting with an empty station.')
            return
        for i in range(len(ids)):
            if types[i] == 'temperature':
                sensor = TemperatureSensor(str(ids[i]), str(locations[i]), readings[i])
            else:
                sensor = HumiditySensor(str(ids[i]), str(locations[i]), readings[i])
            self.add_sensor(sensor)
        print(f'Loaded {len(self)} sensors from {FILE_NAME}.')


def read_sensor(station, text='Sensor ID: '):
    if len(station) == 0:
        raise SensorNotFoundError('there are no sensors yet, add one first')
    print('Sensors:', ', '.join(station.sensors))
    return station.get_sensor(input(text).strip().upper())


def read_day():
    text = input('Day (1-7): ').strip()
    if not text.isdigit() or not (1 <= int(text) <= DAYS):
        raise InvalidInputError(f'"{text}" is not a day between 1 and 7')
    return int(text)


def read_threshold(default):
    text = input(f'Threshold (press Enter for {default}): ').strip()
    if text == '':
        return default
    try:
        return float(text)
    except ValueError:
        raise InvalidInputError(f'"{text}" is not a number')


def add_sensor_menu(station):
    sensor_type = input('Temperature or humidity sensor? (t/h): ').strip().lower()
    if sensor_type != 't' and sensor_type != 'h':
        print('Please enter t or h.')
        return
    sensor_id = input('Sensor ID: ').strip().upper()
    location = input('Location: ').strip()
    if sensor_id == '' or location == '':
        print('ID and location cannot be empty.')
        return
    if sensor_type == 't':
        sensor_type = 'temperature'
    else:
        sensor_type = 'humidity'
    seed = SEED + len(station)  # every sensor gets different, but repeatable data
    sensor = create_sensor(sensor_type, sensor_id, location, seed)
    station.add_sensor(sensor)
    print(f'{sensor} was added.')


def summary_menu(station):
    sensor = read_sensor(station)
    unit = sensor.unit()
    low, high, mean = sensor.summary()
    peak_day, peak_hour = sensor.peak_time()
    low_day, low_hour = sensor.lowest_time()
    print(sensor)
    print(f'Min:  {low:.2f} {unit} (day {low_day}, {low_hour}:00)')
    print(f'Max:  {high:.2f} {unit} (day {peak_day}, {peak_hour}:00)')
    print(f'Mean: {mean:.2f} {unit}')
    print(f'Std:  {sensor.readings.std():.2f} {unit}')
    if isinstance(sensor, TemperatureSensor):
        fahrenheit = sensor.to_fahrenheit()
        print(f'In Fahrenheit: min {fahrenheit.min():.2f}, max {fahrenheit.max():.2f}, '
              f'mean {fahrenheit.mean():.2f}')


def daily_averages_menu(station):
    sensor = read_sensor(station)
    averages = sensor.daily_averages()
    above_average = sensor.normalized().max(axis=1)
    print(f'Daily report for {sensor}:')
    for i in range(DAYS):
        print(f'Day {i + 1}: average {averages[i]:.2f} {sensor.unit()}, '
              f'highest reading {above_average[i]:.2f} above the day average')
    best_hour = sensor.hourly_averages().argmax()
    print(f'On average the highest values are at {best_hour}:00')


def alerts_menu(station):
    sensor = read_sensor(station)
    threshold = read_threshold(sensor.alert_threshold())
    mask = sensor.alert_mask(threshold)
    print(f'{mask.sum()} of {mask.size} readings are above {threshold} {sensor.unit()}')
    marked = np.where(mask, '!', '.')  # ! = alert
    for i in range(DAYS):
        print(f'Day {i + 1}: ' + ''.join(marked[i]))
    for day, hour, value in sensor.alerts(threshold):
        print(f'ALERT: day {day}, {hour}:00 -> {value:.2f} {sensor.unit()}')


def moving_average_menu(station):
    sensor = read_sensor(station)
    day = read_day()
    averages = sensor.moving_average(day)
    print(f'3-hour moving average for day {day}:')
    for hour in range(len(averages)):
        print(f'{hour}:00 - {hour + 2}:00   {averages[hour]:.2f} {sensor.unit()}')


def ranking_menu(station):
    if len(station) == 0:
        print('No sensors yet.')
        return
    for sensor_type in ['temperature', 'humidity']:
        ranking = station.ranking(sensor_type)
        if len(ranking) == 0:
            continue
        print(f'{sensor_type.capitalize()} sensors:')
        place = 1
        for sensor in ranking:
            print(f'{place}. {sensor.sensor_id} ({sensor.location}) - '
                  f'average {sensor.readings.mean():.2f} {sensor.unit()}')
            place += 1
    print('All locations:', ', '.join(sorted(station.all_locations())))
    both = station.locations_with_both()
    if len(both) > 0:
        print('Locations with both sensor types:', ', '.join(sorted(both)))


def compare_menu(station):
    sensor1 = read_sensor(station, 'First sensor ID: ')
    sensor2 = read_sensor(station, 'Second sensor ID: ')
    if sensor1 == sensor2:
        print('Please choose two different sensors.')
        return
    correlation = np.corrcoef(sensor1.readings.flatten(), sensor2.readings.flatten())[0, 1]
    print(f'Correlation between {sensor1.sensor_id} and {sensor2.sensor_id}: {correlation:.2f}')


def print_menu():
    print('\n--- Sensor Data Analyzer ---')
    print('1. Add sensor (temperature / humidity)')
    print('2. Show sensor summary (min, max, mean, std)')
    print('3. Show daily averages')
    print('4. Show alerts (readings above threshold)')
    print('5. Show 3-hour moving average')
    print('6. Rank sensors by average')
    print('7. Compare two sensors (correlation)')
    print('8. Save and exit')


def handle_choice(station, choice):
    # returns False when the program should stop
    if choice == '1':
        add_sensor_menu(station)
    elif choice == '2':
        summary_menu(station)
    elif choice == '3':
        daily_averages_menu(station)
    elif choice == '4':
        alerts_menu(station)
    elif choice == '5':
        moving_average_menu(station)
    elif choice == '6':
        ranking_menu(station)
    elif choice == '7':
        compare_menu(station)
    elif choice == '8':
        station.save()
        print('Data saved. Bye!')
        return False
    else:
        print('Invalid option, please choose 1-8.')
    return True


def main():
    station = Station()
    station.load()
    running = True
    while running:
        print_menu()
        choice = input('Choose an option: ').strip()
        try:
            running = handle_choice(station, choice)
        except SensorNotFoundError as e:
            print('Error:', e)
        except InvalidInputError as e:
            print('Invalid input:', e)
        except ValueError as e:
            print('Error:', e)


main()
