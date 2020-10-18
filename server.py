import datetime

import flask

import noaa
import usl
import asos

app = flask.Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/')
def wxchallenge_station():
    date = flask.request.args.get('date')

    if date is None:
        date = datetime.date.today()
    else:
        date = datetime.datetime.strptime(date, '%Y%m%d').date()

    station_name = 'KGFL'

    def getdate(hour):
        return datetime.datetime(year=date.year,
                                 month=date.month,
                                 day=date.day,
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
        ret['USL 12Z'] = usl.get_forecast(getdate(12),
                                          station_name).data_array()
    except KeyError:
        pass
    except RuntimeError:
        pass

    for k, v in ret.items():
        if isinstance(v[3], tuple):
            ret[k][3] = '-'.join([str(round(x, 2)) for x in v[3]])

    tomorrow = date + datetime.timedelta(days=1)
    f_start = datetime.datetime(year=tomorrow.year,
                                month=tomorrow.month,
                                day=tomorrow.day,
                                hour=6)
    f_end = f_start + datetime.timedelta(days=1)

    yesterday = date - datetime.timedelta(days=1)

    verification, last_valid = asos.get_observation(yesterday,
                                                    station_name)

    return flask.render_template('index.html',
                                 data=ret,
                                 f_date=date,
                                 f_tomorrow=tomorrow,
                                 f_start=f_start,
                                 f_end=f_end,
                                 station=station_name,
                                 ver=verification.data_array(),
                                 last_valid=last_valid)
