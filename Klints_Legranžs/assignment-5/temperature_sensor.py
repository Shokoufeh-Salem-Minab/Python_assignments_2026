from sensor import Sensor

class TemperatureSensor(Sensor):

    def alert_threshold(self):
        return 25.0

    def unit(self):
        return "C"

    def convert_to_fahrenheit(self):
        return self.readings * 9 / 5 + 32