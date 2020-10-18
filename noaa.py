import datetime
import requests

import wxchal
import util


def qpf_to_inches(qpf: int) -> (float, float):
    if qpf == 0:
        return (0.0, 0.0)
    elif qpf == 1:
        return (0.01, 0.09)
    elif qpf == 2:
        return (0.1, 0.24)
    elif qpf == 3:
        return (0.25, 0.49)
    elif qpf == 4:
        return (0.5, 0.99)
    elif qpf == 5:
        return (1.0, 1.99)
    elif qpf == 6:
        return (2.00, float('inf'))


def get_forecast(forecast_time: datetime.datetime,
                 station: str,
                 model: str) -> wxchal.Forecast:
    MESONET_URL = 'https://mesonet.agron.iastate.edu/api/1/mos.json?'

    args = {'station': station.upper(),
            'runtime': forecast_time.strftime('%Y-%m-%d %H:00Z'),
            'model': model.upper()}

    args = '&'.join([k + '=' + v for k, v in args.items()])

    r = util.cached_get(MESONET_URL + args,
                        datetime.timedelta(minutes=15)).json()

    fdate = forecast_time.date() + datetime.timedelta(days=1)

    wind = 0
    precip = (0.0, 0.0)

    for row in r['data']:
        ftime = datetime.datetime.strptime(row['ftime'],
                                           '%Y-%m-%dT%H:00:00.000Z')

        f_start = datetime.datetime(fdate.year, fdate.month, fdate.day, 6)
        f_stop = f_start + datetime.timedelta(days=1)

        correct_date = ftime >= f_start and ftime < f_stop

        if correct_date:
            if ftime.hour == 12:
                low = int(row['n_x'])
            if ftime.hour == 0:
                high = int(row['n_x'])
            wind = max(wind, int(row['wsp']))
            q = row['q06']
            if q is not None:
                inches = qpf_to_inches(int(q))
                precip = (precip[0] + inches[0], precip[1] + inches[1])

    forecast = wxchal.Forecast(fdate, high, low, wind, precip)

    return forecast
