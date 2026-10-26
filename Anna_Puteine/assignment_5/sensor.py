import numpy as np

class SensorError(Exception):
    pass

class Sensor:
    kind = "sensor"
    base_value = 0
    spread = 1

    def __init__(self, sensor_id, location, readings=None, seed=0):
        self.sensor_id = sensor_id
        self.location = location

        if readings is None:
            rng = np.random.default_rng(seed)
            daily_curve = 2 * self.spread * np.sin(np.linspace(0, 2 * np.pi, 24))
            readings = rng.normal(self.base_value, self.spread, 7 * 24).reshape(7, 24) + daily_curve

        self.readings = np.array(readings).reshape(7, 24)

    def __str__(self):
        return f"{self.sensor_id} ({self.kind}) at {self.location}"

    def unit(self):
        return ""

    def alert_threshold(self):
        return 0

    def summary(self):
        return (self.readings.min(), self.readings.max(), self.readings.mean())

    def peak(self):
        return np.unravel_index(self.readings.argmax(), self.readings.shape)

    def lowest(self):
        return np.unravel_index(self.readings.argmin(), self.readings.shape)

    def alerts(self):
        mask = self.readings > self.alert_threshold()
        days, hours = np.where(mask)
        return [(day, hour, value) for day, hour, value in zip(days, hours, self.readings[mask])]

    def movingAverage(self, day):
        return np.convolve(self.readings[day], np.ones(3) / 3, mode="valid")

    def correlation(self, other):
        return np.corrcoef(self.readings.flatten(), other.readings.flatten())[0, 1]

class TemperatureSensor(Sensor):
    kind = "temperature"
    base_value = 20
    spread = 2

    def unit(self):
        return "C"

    def alert_threshold(self):
        return 25

    def toFahrenheit(self):
        return self.readings * 9 / 5 + 32

class HumiditySensor(Sensor):
    kind = "humidity"
    base_value = 55
    spread = 5

    def unit(self):
        return "%"

    def alert_threshold(self):
        return 70
