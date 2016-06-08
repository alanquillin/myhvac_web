

from myhvac_web.myhvac_service import factory

import logging

LOG = logging.getLogger(__name__)


def get_system_state():
    service = factory.get_service_module()

    return service.get_system_state()