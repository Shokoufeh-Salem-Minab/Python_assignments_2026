import numpy as np

from temperature_sensor import TemperatureSensor
from humidity_sensor import HumiditySensor

class SensorNotFoundError(Exception):
    pass



class Station:

    def __init__(self):
        self.sensors = {}

    def add_sensor(self, sensor):
        if sensor.sensor_id in self.sensors:
            raise ValueError (
                f"Sensor ID '{sensor.sensor_id}' already exists."
            )

        self.sensors[sensor.sensor_id] = sensor

    def find_sensor_by_id(self, sensor_id):
        try:
            return self.sensors[sensor_id]
        except KeyError as error:
            raise SensorNotFoundError (
                f"Sensor '{sensor_id}' was not found."
            ) from error

    def get_unique_locations(self):
        return {
            sensor.location for sensor in self.sensors.values()
        }

    def find_shared_sensor_locations(self):
        temperature_locations = {
            sensor.location for sensor in self.sensors.values() 
            if isinstance(sensor, TemperatureSensor)
        }

        humidity_locations = {
            sensor.location for sensor in self.sensors.values()
            if isinstance(sensor, HumiditySensor)
        }

        return temperature_locations & humidity_locations

    def rank_sensors_by_average(self):
        sensors = list(self.sensors.values())

        if not sensors:
            return []

        averages = np.array([
            np.mean(sensor.readings) for sensor in sensors
        ])

        ranking = np.argsort(averages)[::-1]

        return [
            (sensors[index], float(averages[index]))
            for index in ranking
        ]

    
    def calculate_sensor_correlation(self, first_id, second_id):
        first_sensor = self.find_sensor_by_id(first_id)
        second_sensor = self.find_sensor_by_id(second_id)

        correlation = np.corrcoef(
            first_sensor.readings.ravel(),
            second_sensor.readings.ravel()
        )[0, 1]

        return float(correlation)


    def __len__(self):
        return len(self.sensors)