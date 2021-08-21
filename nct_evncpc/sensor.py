"""Sensor that can display the current Home Assistant versions."""
from datetime import timedelta
import logging

from . import vnhass_util
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, CONF_SOURCE
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle, dt

from datetime import datetime, timedelta

_LOGGER = logging.getLogger(__name__)

CONF_PASS = "passwd"
CONF_MA = "makhach"
CONF_DATE = "day"

ICON = "mdi:fingerprint"

TIME_BETWEEN_UPDATES = timedelta(minutes=50)
TIME_BETWEEN_UPDATES_SOLAR = timedelta(minutes=58)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default="evnhcm"): cv.string,
        vol.Optional(CONF_PASS, default='1234567890'): cv.string,
        vol.Optional(CONF_MA, default='xxx'): cv.string,
        vol.Optional(CONF_DATE, default='1'): cv.string,
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Version sensor platform."""

    name = config.get(CONF_NAME)
    passwd = config.get(CONF_PASS)
    makhach = config.get(CONF_MA)
    date = config.get(CONF_DATE)

    #get session HA
    #session = async_get_clientsession(hass)

    #call xu ly data
    evncpc_grid = EvnCPC(vnhass_util.HassioVersion(name, passwd))
    
    evncpc_solar = Solar(vnhass_util.HassioVersion(name, passwd))

    async_add_entities([VersionSensor(evncpc_grid, 'nct_evncpc'), VersionSensor(evncpc_solar, 'evncpc_solar')], True)
    #async_add_entities([VersionSensor(evncpc_grid, 'nct_evncpc')], True)

class Solar:
    """Get the latest data and update the states."""

    def __init__(self, vnhass):
        """Initialize the data object."""
        self.vnhass = vnhass

    @Throttle(TIME_BETWEEN_UPDATES_SOLAR)
    def update(self):
        """Get the latest version information."""
        self.vnhass.get_evncpc_solar()

class EvnCPC:
    """Get the latest data and update the states."""

    def __init__(self, vnhass):
        """Initialize the data object."""
        self.vnhass = vnhass

    @Throttle(TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest version information."""
        self.vnhass.get_evn_cpc()

class VersionSensor(Entity):
    """Representation of a Home Assistant version sensor."""

    def __init__(self, haversion, name):
        """Initialize the Version sensor."""
        self.haversion = haversion
        self._name = name
        self._state = None

    def update(self):
        """Get the latest version information."""
        self.haversion.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def device_class(self):
        """Return the name of the sensor."""
        return 'energy'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.haversion.vnhass.state

    @property
    def device_state_attributes(self):
        """Return attributes for the sensor."""
        return self.haversion.vnhass.attribute

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return ICON

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return 'kWh'

