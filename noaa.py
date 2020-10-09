import datetime
import requests

import wxchal

def get_forecast(forecast_time: datetime.datetime, 
                 station: str, 
                 model: str) -> wxchal.Forecast:
    MESONET_URL = 'https://mesonet.agron.iastate.edu/api/1/mos.json?'
    
    args = {'station': station.upper(),
            'runtime': forecast_time.strftime('%Y-%m-%d %H:00Z'),
            'model': model.upper()}

    args = '&'.join([k + '=' + v for k, v in args.items()])

    r = requests.get(MESONET_URL + args).json()

    fdate = forecast_time.date() + datetime.timedelta(days=1)

    wind = 0
    precip = 0.0

    for row in r['data']:
        ftime = datetime.datetime.strptime(row['ftime'], 
                                           '%Y-%m-%dT%H:00:00.000Z')
        
        f_start = datetime.datetime(fdate.year, fdate.month, fdate.day, 6)
        f_stop = f_start + datetime.timedelta(days=1)
        
        correct_date = ftime >= f_start and ftime < f_stop

        if correct_date:
            if ftime.hour == 12:
                low = row['n_x']
            if ftime.hour == 0:
                high = row['n_x']
            wind = max(wind, row['wsp'])
            q = row['q06']
            if q is not None:
                precip += q 

    forecast = wxchal.Forecast(fdate, high, low, wind, precip)

    return forecast
