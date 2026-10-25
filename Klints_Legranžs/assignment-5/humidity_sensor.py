from sensor import Sensor

class HumiditySensor(Sensor):

    def alert_threshold(self):
        return 70.0

    def unit(self):
        return "%"