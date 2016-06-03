from flask import render_template

from myhvac_core.db import api as db
from myhvac_core.db import models
from app import app

from datetime import datetime, timedelta
import logging

LOG = logging.getLogger(__name__)


@app.route('/')
def dashboard():
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

        return render_template('dashboard.html',
                               active_rooms=active_rooms,
                               inactive_rooms=inactive_rooms)
    return db.sessionize(do)


def _parse_room(session, room_model):
    room = dict(name=room_model.name,
                id=room_model.id,
                active=room_model.active)

    if room_model.sensors:
        sensors = []
        measurement_agg = 0
        measurement_cnt = 0
        current_temp_recorded_date = None

        for sensor_model in room_model.sensors:
            sensor = dict(id=sensor_model.id,
                          name=sensor_model.name,
                          manufacturer_id=sensor_model.manufacturer_id,
                          model=sensor_model.sensor_type.model,
                          manufacturer=sensor_model.sensor_type.manufacturer)

            measurement = db.get_most_recent_sensor_temperature(session,
                                                                sensor_id=sensor_model.id,
                                                                order_desc=True,
                                                                order_by=models.Measurement.recorded_date)

            if measurement and measurement.recorded_date > datetime.now() - timedelta(minutes=12):
                measurement_agg = measurement_agg + (measurement.measurement * room_model.weight)
                measurement_cnt = measurement_cnt + room_model.weight
                sensor['current_temp'] = measurement.measurement
                sensor['last_temp_recorded_date'] = measurement.recorded_date

                if not current_temp_recorded_date or measurement.recorded_date > current_temp_recorded_date:
                    current_temp_recorded_date = measurement.recorded_date

            sensors.append(sensor)

        if measurement_cnt > 0 and measurement_agg > 0:
            room['current_temp'] = measurement_agg / measurement_cnt

        room['sensors'] = sensors
        if current_temp_recorded_date:
            room['current_temp_recorded_date'] = current_temp_recorded_date.strftime('%A, %m/%d/%y')
            room['current_temp_recorded_time'] = current_temp_recorded_date.strftime('%I:%M:%S %p')
    return room
