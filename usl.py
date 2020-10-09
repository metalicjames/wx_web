import datetime
import requests

import bs4

import wxchal

def get_forecast(forecast_time: datetime.datetime, 
                 station: str) -> wxchal.Forecast:
    USL_URL = 'http://microclimates.org/forecast/'

    if forecast_time.hour not in [12, 22]:
        raise ValueError('USL only has 12z and 22z forecasts')

    request_url = '/'.join([USL_URL, 
                            station.upper(), 
                            forecast_time.strftime('%Y%m%d_%H')])

    request_url += '.html'

    resp = requests.get(request_url)

    if resp.status_code != 200:
        raise RuntimeError('Forecast unavailable for station and time')

    soup = bs4.BeautifulSoup(resp.text, 'html.parser')

    cols = soup.find(id='stats').find_all('tr')[1].find_all('td')

    cols[:] = [c.string for c in cols]
        
    high = int(cols[0].split('°')[0])
    low = int(cols[1].split('°')[0])
    wind = int(cols[2].split(' ')[0])
    precip = float(cols[3][:-1])

    forecast = wxchal.Forecast(forecast_time.date() + 
                               datetime.timedelta(days=1), 
                               high, 
                               low, 
                               wind, 
                               precip)

    return forecast
