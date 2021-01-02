"""
A python module to the newest version number of Home Assistant.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import asyncio
import logging
import socket
import re
import random

import aiohttp
import async_timeout

_LOGGER = logging.getLogger(__name__)


class Version:
    """A class for returning HA version information from different sources."""

    def __init__(self, loop, session, name='evncpc', passwd='1234567890', date='1'):
        """Initialize the class."""
        self.loop = loop
        self.session = session
        self._version = None
        self._name = name
        self._passwd = passwd
        self._date = date
        self._version_data = {}

    @property
    def version(self):
        """Return the version."""
        return self._version

    @property
    def version_data(self):
        """Return extended version data for supported sources."""
        return self._version_data

class HassioVersion(Version):
    """Hass.io version."""

    async def get_version(self):

        self._version_data["copyright"] = "trumxuquang@gmail.com"
        lst_url = ['https://protected-ocean-21066.herokuapp.com','https://mysterious-crag-20408.herokuapp.com']
        choice_url = random.choice(lst_url)

        url = f'{choice_url}/evnhcm/{self._name}/data/{self._passwd}/date/{self._date}'

        try:
            async with async_timeout.timeout(600, loop=self.loop):
                response = await self.session.get(url)
                data = await response.json()

                self._version = data['sanluong_day']
                self._version_data["ma_khachhang"] = data['makh']
                self._version_data["time_month"] = data['time_month']
                self._version_data["sanluong_month"] = data['sanluong_month']
                self._version_data["time_day"] = data['time_day']
                self._version_data["sanluong_day"] = data['sanluong_day']
                self._version_data["tienthangnay"] = data['tienthangnay']
                self._version_data["tienthangtruoc"] = 'đang coding...'
                self._version_data["tienhomqua"] = 'đang coding...'
                self._version_data["ngaycupdien"] = 'đang coding...'


            _LOGGER.debug("Version: %s", self.version)
            _LOGGER.debug("Version data: %s", self.version_data)

        except asyncio.TimeoutError as error:
            _LOGGER.error(
                "Timeout error fetching version information from %s, %s",
                self._version_data["ma_khachhang"],
                error,
            )
        except (KeyError, TypeError) as error:
            _LOGGER.error(
                "Error parsing version information from %s, %s",
                self._version_data["ma_khachhang"],
                error,
            )
        except (aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error(
                "Error fetching version information from %s, %s",
                self._version_data["ma_khachhang"],
                error,
            )
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.critical("loi toi khong biet! - %s", error)


def extract_data(datajson):

  print(datajson)
  time = datajson['labels'].split(",")
  value = datajson['value'].split(",")

  time_asis = time[len(time) - 1]
  data_asis = value[len(value) - 1]

  time_before = time[len(time) - 2]
  data_before = value[len(value) - 2]

  try:
    total_rain = rm_html(datajson['total_rain'])
    total_rain = total_rain.split(",")
  
    total_rain_1day =total_rain[0]
    total_rain_3day =total_rain[1]
    total_rain_7day =total_rain[2]

  except :
    total_rain_1day = 'None'
    total_rain_3day ='None'
    total_rain_7day ='None'
  #nuoc song
  try:
    bao_dong1 = datajson['bao_dong1'].split(",")[1]
    bao_dong2 = datajson['bao_dong2'].split(",")[1]
    bao_dong3 = datajson['bao_dong3'].split(",")[1]
  except :
    bao_dong1 ='None'
    bao_dong2 ='None'
    bao_dong3 ='None'

  return {'time_asis' : time_asis,
  'data_asis':data_asis, 
  'time_before':time_before, 
  'data_before':data_before,
  'total_rain_1day':total_rain_1day,
  'total_rain_3day':total_rain_3day,
  'total_rain_7day':total_rain_7day,
  'bao_dong1':bao_dong1,
  'bao_dong2':bao_dong2,
  'bao_dong3':bao_dong3
  }

def rm_html(string):

  string = string.replace('<b>','')
  string = string.replace('mm (24)','')
  string = string.replace('mm (3 ngày)','')
  string = string.replace('mm (7 ngày)</b>','')
  return string
