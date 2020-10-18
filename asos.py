import csv
import datetime
import requests

import wxchal
import util


def get_observation(forecast_time: datetime.datetime,
                    station: str) -> wxchal.Forecast:
    ASOS_URL = 'https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py' \
             + '?data=all&tz=Etc%2FUTC&format=onlycomma&latlon=no&missing=M&' \
             + 'trace=0.0001&direct=no&report_type=2'

    forecast_date = forecast_time + datetime.timedelta(days=1)

    forecast_start_time = datetime.datetime(year=forecast_date.year,
                                            month=forecast_date.month,
                                            day=forecast_date.day,
                                            hour=6)

    forecast_end_time = forecast_start_time + datetime.timedelta(days=1)

    forecast_end_date = forecast_end_time.date()

    args = {
        'station': station[1:],
        'year1': forecast_date.year,
        'month1': forecast_date.month,
        'day1': forecast_date.day,
        'year2': forecast_end_date.year,
        'month2': forecast_end_date.month,
        'day2': forecast_end_date.day
    }

    args = [k + '=' + str(v) for k, v in args.items()]

    request_url = ASOS_URL + '&' + '&'.join(args)

    r = util.cached_get(request_url, datetime.timedelta(minutes=15))

    reader = csv.reader(r.text.splitlines())

    high_temperature = None
    low_temperature = None
    max_wind_speed = 0.0
    total_precip = 0.0

    last_valid = None

    first = True
    for row in reader:
        if first:
            first = False
            continue

        valid = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M')

        if valid >= forecast_start_time and valid < forecast_end_time:
            temperature = float(row[2])

            try:
                wind_speed = float(row[6])
            except ValueError:
                print('WARNING:', row[6], 'is an invalid wind speed')
                wind_speed = 0.0

            precip = float(row[7])

            if high_temperature is None or temperature > high_temperature:
                high_temperature = temperature

            if low_temperature is None or temperature < low_temperature:
                low_temperature = temperature

            if wind_speed > max_wind_speed:
                max_wind_speed = wind_speed

            total_precip += precip

            last_valid = valid

    try:
        forecast = wxchal.Forecast(forecast_date=forecast_date,
                                   high_temperature=int(high_temperature),
                                   low_temperature=int(low_temperature),
                                   peak_wind_speed=int(max_wind_speed),
                                   precip_accumulated=total_precip)
    except Exception:
        forecast = None

    return forecast, last_valid
