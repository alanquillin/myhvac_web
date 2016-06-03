from myhvac_core import cfg

from myhvac_web.myhvac_service import web

import logging

LOG = logging.getLogger(__name__)

opts = [
    cfg.BoolOpt('use_api', default=True,
                help='When true, the data will be retrieved from the MyHVAC service\'s rest api, else '
                     'data will be retrieved directly from the systm.  '
                     'This should only be false when the web server is running on the same system')
]
CONF = cfg.CONF
CONF.register_opts(opts, 'myhvac_service_api')


service_module = None


def get_service_module():
    global service_module

    if service_module:
        return service_module

    if CONF.myhvac_service_api.use_api:
        service_module = web
        return web

    # only import this module if you are going to use it as it has
    # dependecies that system NOT runnig the service may not have
    import myhvac_web.myhvac_service.system as sys
    service_module = sys
    return sys