from myhvac_core import hvac

import logging

LOG = logging.getLogger(__name__)


def set_system_state():
    return hvac.get_system_state()
