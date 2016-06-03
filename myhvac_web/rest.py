from flask import jsonify
from flask import request

from myhvac_core.db import api as db
from myhvac_core.db import models
from myhvac_core import system_state as sstate
from app import app
from myhvac_web.myhvac_service import api as srvc_api

import logging
from datetime import datetime, timedelta

LOG = logging.getLogger(__name__)


@app.route('/api/rooms/<room_id>/temp_history')
def get_room_temp_history(room_id):
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    sort_column = request.args.get('sort_column', models.Measurement.recorded_date)
    sort_direction = request.args.get('sort_direction', 'DESC')

    LOG.debug('API call \'/api/rooms/%s/temp_history\'.  Room Id: %s, page=%s, '
              'limit: %s, sort_column: %s, sort_direction: %s',
              room_id, room_id, page, limit, sort_column, sort_direction)

    def do(session):
        room_model = db.get_room_by_id(session, room_id)
        sensors = []

        if room_model:
            for sensor_model in room_model.sensors:
                sensor = dict(name=sensor_model.name,
                              manufacturer_id=sensor_model.manufacturer_id)
                history = []
                measurement_models = db.get_sensor_temperatures(session,
                                                                sensor_id=sensor_model.id,
                                                                limit=limit,
                                                                order_desc=True if sort_direction == 'DESC' else False,
                                                                offset=(page - 1) * limit,
                                                                order_by=models.Measurement.recorded_date)

                total = db.count_sensor_temperatures(session, sensor_id=sensor_model.id)

                for measurement_model in measurement_models:
                    h = dict(id=measurement_model.id,
                             temp=measurement_model.measurement,
                             recorded_date=measurement_model.recorded_date,
                             sensor_id=measurement_model.sensor_id)
                    history.append(h)

                return jsonify(total=total, measurements=history)
                # sensor['temp_history'] = history
                # sensors.append(sensor)

    return db.sessionize(do)


@app.route('/api/system/details')
def get_system_details():
    def do(session):
        temp_agg = 0
        temp_cnt = 0

        room_models = db.get_rooms_dashboard(session)

        for room_model in room_models:
            if not room_model.active:
                continue

            room_temp = None
            measurement_agg = 0
            measurement_cnt = 0

            if room_model.sensors:
                for sensor_model in room_model.sensors:
                    measurement = db.get_most_recent_sensor_temperature(session,
                                                                        sensor_id=sensor_model.id,
                                                                        order_desc=True,
                                                                        order_by=models.Measurement.recorded_date)

                    if measurement and measurement.recorded_date > datetime.now() - timedelta(minutes=12):
                        measurement_agg = measurement.measurement
                        measurement_cnt = measurement_cnt + 1

            if measurement_cnt > 0 and measurement_agg > 0:
                room_temp = measurement_agg / measurement_cnt

            if room_temp:
                temp_agg = temp_agg + (room_temp * room_model.weight)
                temp_cnt = temp_cnt + room_model.weight

        system_state = srvc_api.set_system_state()

        if not temp_cnt and not temp_agg:
            return jsonify(error=True, error_message="No current temperature data found...")

        return jsonify(temp=temp_agg/temp_cnt,
                       state=sstate.print_state(system_state))
    return db.sessionize(do)
