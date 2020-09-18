""" @trumxuquang@gmail.com
# Config in configuration.yaml file for Home Assistant
sensor:
  - platform: lichvansu
    display_options:
      - 'amLich'
"""
"""
Them ngay dam gio tại #denNgayGio = lichvansu.khoang_cach_AL(6, 17)
"""

from . import lichvansu
from . import lunar

from datetime import timedelta

import logging
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_DISPLAY_OPTIONS
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=58)

OPTION_TYPES = {
    "amLich": "vansu amlich",
    "damgio": "vansu damgio",
}
OPTION_ATT = {
    "truc": 'N/A',
    "saoTot": 'N/A',
    "saoXau": 'N/A',
    "gioTot": 'N/A',
    "gioXau": 'N/A',
    "ngayTotXau": 'N/A',
    "tuoiHop": 'N/A',
    "tuoiXung": 'N/A',
    "onlyDay": 'N/A',
    "denMungMot": 'N/A',
    "denNgayRam": 'N/A',
    "denNgayGio01": 'N/A',
    "denNgayGio02": 'N/A',
    "Copyright": "@TrumXuQuang",
}

OPTION_DEFAULT_ = "amLich"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_DISPLAY_OPTIONS, default=["amLich"]): vol.All(
            cv.ensure_list, [vol.In(OPTION_TYPES)]
        )
    }
)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):

    async_add_entities(
        [vansu_class(hass, variable) for variable in config[CONF_DISPLAY_OPTIONS]]
    )


class vansu_class(Entity):

    def __initXXXX__(self, option_type):
        """Initialize the sensor."""
        self._name = OPTION_TYPES[option_type]
        self.type = option_type
        self._state = None
        self._author = '@trumxuquang'
        self._description = 'lich van su Viet Nam'
        self._attrs = OPTION_ATT
        self.update()

    def __init__(self, hass, option_type):
        """Initialize the sensor."""
        self._name = OPTION_TYPES[option_type]
        self.type = option_type
        self._state = None
        self.hass = hass
        self._author = '@trumxuquang'
        self._description = 'lich van su Viet Nam'
        self._attrs = OPTION_ATT
        self.unsub = None

        self.update()


    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor"""
        return 'mdi:atom'

    @property
    def device_state_attributes(self):
        return self._attrs
    
    @Throttle(SCAN_INTERVAL)
    def update(self):
        data = lichvansu.get_vansu()
        demngay = lichvansu.kiemtra_amlich2()
        denNgayGio01x = lichvansu.khoang_cach_AL(6, 17)
        denNgayGio02x = lichvansu.khoang_cach_AL(8, 20)
        if self.type == "amLich":
            self._state = data['amLich']
            self._attrs['truc'] = data['truc']
            self._attrs['saoTot'] = data['saoTot']
            self._attrs['saoXau'] = data['saoXau']
            self._attrs['gioTot'] = data['gioTot']