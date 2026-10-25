import numpy as np

class Sensor:

    def __init__(self, sensor_id, location, readings):
        self.sensor_id = sensor_id
        self.location = location
        readings = np.asarray(readings, dtype = float)

        if readings.size != 168:
            raise ValueError("A sensor must have exactly 168 readings.")

        self.readings = readings.reshape(7, 24)


    def alert_threshold(self):
        raise NotImplementedError

    def unit(self):
        raise NotImplementedError

    def summary(self):
        return (
            float(np.min(self.readings)),
            float(np.max(self.readings)),
            float(np.mean(self.readings)),
        )


    def daily_mean(self):
        return np.mean(self.readings, axis = 1)

    def hourly_mean(self):
        return np.mean(self.readings, axis = 0)

    def peak_reading_time(self):
        index = np.argmax(self.readings)
        day, hour = np.unravel_index(index, self.readings.shape)

        return int(day) + 1, int(hour)

    def lowest_reading_time(self):
        index = np.argmin(self.readings)
        day, hour = np.unravel_index(index, self.readings.shape)

        return int(day) + 1, int(hour)

    def show_alerts(self):
        mask = self.readings > self.alert_threshold()

        statuses = np.where(mask, "ALERT", "OK")

        day_indices, hour_indices = np.where(mask)

        return [
            (
                int(day) + 1,
                int(hour),
                float(self.readings[day, hour]),
                str(statuses[day, hour])
            )
            for day, hour in zip(day_indices, hour_indices)
        ]

    def show_3_hour_average(self):
        readings = self.readings.ravel()
        window = np.ones(3) / 3

        return np.convolve(readings, window, mode = "valid")

    def daily_normalised_readings(self):
        daily_means = self.daily_mean()

        return self.readings - daily_means[:, np.newaxis]

    def __str__(self):
        return (
            f"Sensor ID: {self.sensor_id},"
            f"Location: {self.location},"
            f"Unit: {self.unit()},"
        )
