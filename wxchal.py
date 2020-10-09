import datetime

class Forecast:
    def __init__(self,
                 forecast_date: datetime.date,
                 high_temperature: int,
                 low_temperature: int,
                 peak_wind_speed: int,
                 precip_accumulated: float) -> None:
        self.forecast_date = forecast_date
        self.high_temperature = high_temperature
        self.low_temperature = low_temperature
        self.peak_wind_speed = peak_wind_speed
        self.precip_accumulated = precip_accumulated

    def __str__(self):
        arr = [self.forecast_date.strftime('%Y%m%d'),
               self.high_temperature,
               self.low_temperature,
               self.peak_wind_speed,
               round(self.precip_accumulated, 2)]

        arr[:] = [str(x) for x in arr]

        return ' '.join(arr)
