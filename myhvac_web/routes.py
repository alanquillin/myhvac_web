from flask import render_template

from myhvac_core.db import api as db
from myhvac_core.db import models
from app import app

import logging

LOG = logging.getLogger(__name__)


def sessionize(f, *args, **kwargs):
    session = db.Session()

    ret = None
    try:
        ret = f(session, *args, **kwargs)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    return ret


@app.route('/')
def index():
    def do(session):
        rooms = db.get_rooms_dashboard(session)

        active_rooms = []
        inactive_rooms = []
        for room_model in rooms:
            room = _parse_room(session, room_model)
            if room_model.active:
                active_rooms.append(room)
            else:
                inactive_rooms.append(room)

        temp_agg = 0
        temp_cnt = 0
        for room in active_rooms:
            temp = room.get('current_temp')
            if temp:
                temp_agg = temp_agg + temp
                temp_cnt = temp_cnt + 1

        if temp_agg > 0 and temp_cnt > 0:
            current_temp = temp_agg / temp_cnt

        return render_template('main.html',
                               active_rooms=active_rooms,
                               inactive_rooms=inactive_rooms,
                               current_temp=current_temp)
    return sessionize(do)


def _parse_room(session, room_model):
    room = dict(name=room_model.name, id=room_model.id, active=room_model.active)

    if room_model.sensors:
        LOG.debug('Room: %s, %s, %s', room_model.id, room_model.name, room_model.active)
        sensors = []
        measurement_agg = 0
        measurement_cnt = 0

        for sensor_model in room_model.sensors:
            LOG.debug('\t\tSensor: %s, %s, %s, %s, %s', sensor_model.id, sensor_model.name,
                      sensor_model.manufacturer_id, sensor_model.sensor_type.model, sensor_model.sensor_type.manufacturer)
            sensor = dict(id=sensor_model.id, name=sensor_model.name, manufacturer_id=sensor_model.manufacturer_id,
                          model=sensor_model.sensor_type.model, manufacturer=sensor_model.sensor_type.manufacturer)

            measurements = db.get_sensor_temperatures(session, sensor_id=sensor_model.id, order_desc=True, limit=1,
                                                      order_by=models.Measurement.recorded_date)
            if measurements:
                LOG.debug('Measurement list length: %s', len(measurements))
                m = measurements[-1]
                LOG.debug('\t\t\tMeasurement: %s, %s', m.measurement, m.recorded_date)
                measurement_agg = measurement_agg + m.measurement
                measurement_cnt = measurement_cnt + 1
                sensor['current_temp'] = m.measurement
                sensor['last_temp_recorded_date'] = m.recorded_date

            sensors.append(sensor)

        if measurement_cnt > 0 and measurement_agg > 0:
            room['current_temp'] = measurement_agg / measurement_cnt


        room['sensors'] = sensors
    return room

@app.route('/room/<room>')
def getRoomDetails(room):
    return 'Details for room: %s' % room