from myhvac_core import hvac

import logging

LOG = logging.getLogger(__name__)


def get_system_state():
    rs, es = hvac.get_system_state()
    return rs
