import datetime

import flask

import noaa
import usl

app = flask.Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/')
def wxchallenge_station():
    station_name = 'KGRR'
    today = datetime.date.today()
    
    def getdate(hour):
        return datetime.datetime(year=today.year, 
                                 month=today.month,
                                 day=today.day,
                                 hour=hour)
    ret = {}

    try:
        ret['GFS 18Z'] = noaa.get_forecast(getdate(18), 
                                           station_name, 
                                           'GFS').data_array()
    except KeyError:
        pass
    except RuntimeError:
        pass

    try:
        ret['NAM 12Z'] = noaa.get_forecast(getdate(12), 
                                           station_name, 
                                           'NAM').data_array()
    except KeyError:
        pass
    except RuntimeError:
        pass

    try:
        ret['USL 22Z'] = usl.get_forecast(getdate(22), 
                                          station_name).data_array()
    except KeyError:
        pass
    except RuntimeError:
        pass

    try:
        ret['GFS 12Z'] = noaa.get_forecast(getdate(12), 
                                           station_name, 
                                           'GFS').data_array()
    except KeyError:
        pass
    except RuntimeError:
        pass

    try:
        ret['NAM 18Z'] = noaa.get_forecast(getdate(18), 
                                           station_name, 
                                           'NAM').data_array()
    except KeyError:
        pass
    except RuntimeError:
        pass

    try:
        ret['USL 12Z'] = usl.get_forecast(getdate(12), 
                                          station_name).data_array()
    except KeyError:
        pass
    except RuntimeError:
        pass

    tomorrow = today + datetime.timedelta(days=1)
    f_start = datetime.datetime(year=tomorrow.year,
                                month=tomorrow.month,
                                day=tomorrow.day,
                                hour=6)
    f_end = f_start + datetime.timedelta(days=1)

    return flask.render_template('index.html', 
                                 data=ret, 
                                 f_date=today,
                                 f_start=f_start,
                                 f_end=f_end,
                                 station=station_name)
