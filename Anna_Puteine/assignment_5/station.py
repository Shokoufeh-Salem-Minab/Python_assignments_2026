import numpy as np

from sensor import TemperatureSensor, HumiditySensor, SensorError

sensor_types = {"temperature": TemperatureSensor, "humidity": HumiditySensor}

class Station:
    filename = "station_data.npz"

    def __init__(self):
        self.sensors = {}
        self.locations = set()

    def __len__(self):
        return len(self.sensors)

    def saveToStorage(self):
        sensors = list(self.sensors.values())
        info = np.array([[s.sensor_id, s.kind, s.location] for s in sensors])
        readings = np.array([s.readings for s in sensors])
        np.savez(self.filename, info=info, readings=readings)

    def loadFromStorage(self):
        data = np.load(self.filename)

        for (sensor_id, kind, location), readings in zip(data["info"], data["readings"]):
            self.addSensor(sensor_types[kind](str(sensor_id), str(location), readings))

    def addSensor(self, sensor):
        if sensor.sensor_id in self.sensors:
            raise SensorError("A sensor with this id already exists")

        self.sensors[sensor.sensor_id] = sensor
        self.locations.add(sensor.location)

    def getSensor(self, sensor_id):
        if sensor_id not in self.sensors:
            raise SensorError(f"No sensor with id {sensor_id}")

        return self.sensors[sensor_id]

    def locationsWithBoth(self):
        temperature = {s.location for s in self.sensors.values() if s.kind == "temperature"}
        humidity = {s.location for s in self.sensors.values() if s.kind == "humidity"}
        return temperature & humidity

    def ranking(self):
        sensors = list(self.sensors.values())
        averages = np.array([s.readings.mean() for s in sensors])
        order = np.argsort(averages)[::-1]
        return [(sensors[i], averages[i]) for i in order]
