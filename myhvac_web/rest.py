from flask import jsonify
from flask import request

from myhvac_core.db import api as db
from myhvac_core.db import models
from app import app

import logging

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
