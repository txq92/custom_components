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
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

CONF_PASS = "passwd"

CONF_DATE = "day"

ICON = "mdi:fingerprint"

TIME_BETWEEN_UPDATES = timedelta(minutes=58)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default="evnhcm"): cv.string,
        vol.Optional(CONF_PASS, default='1234567890'): cv.string,
        vol.Optional(CONF_DATE, default='1'): cv.string,
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Version sensor platform."""

    name = config.get(CONF_NAME)
    passwd = config.get(CONF_PASS)
    date = config.get(CONF_DATE)

    #get session HA
    session = async_get_clientsession(hass)

    #call xu ly data
    haversion = VersionData(vnhass_util.HassioVersion(hass.loop, session, name, passwd, date))

    if not name:
        name = 'evnhcm'
    if not passwd:
        passwd = '1234567890'
    async_add_entities([VersionSensor(haversion, name)], True)


class VersionSensor(Entity):
    """Representation of a Home Assistant version sensor."""

    def __init__(self, haversion, name):
        """Initialize the Version sensor."""
        self.haversion = haversion
        self._name = name
        self._state = None

    async def async_update(self):
        """Get the latest version information."""
        await self.haversion.async_update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'nct evnhcm sanluong'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.haversion.api.version

    @property
    def device_state_attributes(self):
        """Return attributes for the sensor."""
        return self.haversion.api.version_data

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return ICON

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return 'kwh'

class VersionData:
    """Get the latest data and update the states."""

    def __init__(self, api):
        """Initialize the data object."""
        self.api = api

    @Throttle(TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Get the latest version information."""
        await self.api.get_version()