import requests

from myhvac_core import cfg
from myhvac_core import system_state as sstate

import logging

LOG = logging.getLogger(__name__)

opts = [
    cfg.StrOpt('url',
                help='Url for the MyHVAC service api when use_api=True'),
    cfg.IntOpt('port', default=8080,
               help='Http port of MyHVAC service api'),
]
CONF = cfg.CONF
CONF.register_opts(opts, 'myhvac_service_api')


def build_resource_url(resource):
    base_url = CONF.myhvac_service_api.url

    if base_url.endswith('/'):
        base_url = base_url[:-1]

    if not resource.startswith('/'):
        resource = '/' + resource

    return "%s:%s%s" % (base_url, CONF.myhvac_service_api.port, resource)


def set_system_state():
    resource = build_resource_url('/system/state')

    LOG.debug('Requesting system state from service: %s', resource)

    resp = requests.get(resource)

    if resp.status_code != 200:
        LOG.error('Bad status code returned from server.  Status Code: %s, Response Body: %s',
                  resp.status_code, resp.text)
        return sstate.UNKNOWN

    data = resp.json()

    state_str = data.get('state')

    if not state_str:
        LOG.error('Invalid system state data found in json response from server.  JSON: %s', data)
        return sstate.UNKNOWN

    return sstate.system_state_from_str(state_str)
