from app import app

import routes
import rest

from myhvac_core import cfg
from myhvac_core.db import api as db
from myhvac_core import log

import logging

LOG = logging.getLogger(__name__)

opts = [
    cfg.BoolOpt('debug', default=False,
                help='Enables debug mode for the flask rest api'),
    cfg.IntOpt('port', default=8081, help='Http port of the webserver')
]
CONF = cfg.CONF
CONF.register_opts(opts, 'rest_api')
CONF = cfg.CONF


def init():
    try:
        CONF(project='myhvac_service')
    except cfg.RequiredOptError:
        CONF.print_help()
        raise SystemExit(1)

    log.init_log()
    db.init_db()


if __name__ == '__main__':
    init()
    app.run()
