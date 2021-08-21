"""
A python module to the newest version number of Home Assistant.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import datetime
import logging, evncpc


_LOGGER = logging.getLogger(__name__)

class Khoitao:
    """A class for returning HA version information from different sources."""
    def __init__(self, name='evnhcm', passw='aa'):
        """Initialize the class."""
        self._state = 'n/a'
        self._name = name
        self._passw = passw
        self._attribute = {}

    @property
    def state(self):
        """Return the version."""
        return self._state

    @property
    def attribute(self):
        """Return extended version data for supported sources."""
        return self._attribute

class HassioVersion(Khoitao):
    """Hass.io version."""

    def get_evn_cpc(self):

        try:  
            api = evncpc.API(self._name , self._passw)
            data_out = api.get_evn_cpc()
            data_out['state'] = 'success'
            #print(data_out)

        except:
            print("fuck you")
            data_out ={'state': 'error', 'soNgay': 100, 'tieude': 'Từ 06/08/2021 đến 07/08/2021', 'ngay': '06/08', 'sanluong_tong': '100', 'tong_p_giao': '7,850.77'}
        
        # return data

        if  data_out['state'] in ['error']:
          self._state = '0'
          self._attribute["alert"] = "Công tơ của bạn chưa hỗ trợ đo theo ngày"
          self._attribute["state_class"] = 'measurement'
          today_date = datetime.datetime.now()
          self._attribute["last_reset"] = today_date.strftime("%Y/%m/%dT00:00:00+00:00")
          self._attribute["copyright"] = "trumxuquang@gmail.com"
        else:
          self._state = data_out['sanLuong_thangnay']
          self._attribute["ma_khachhang"] = data_out['ma_khachhang']
          self._attribute["tien_thangnay"] = data_out['tien_thangnay']
          self._attribute["tienthangtruoc"] = data_out['tienthangtruoc']
          self._attribute["ngayDo"] = data_out['chiso_date']
          self._attribute["timeDo"] = data_out['chiso_time']
          self._attribute["state_class"] = 'measurement'
          today_date = datetime.datetime.now()
          self._attribute["last_reset"] = today_date.strftime("%Y/%m/%dT00:00:00+00:00")
          self._attribute["copyright"] = "trumxuquang@gmail.com"

    def get_evncpc_solar(self):
        self._state = '0'
        self._attribute["alert"] = "Bạn không có sử dụng điện mặt trời"
        self._attribute["state_class"] = 'measurement'
        today_date = datetime.datetime.now()
        self._attribute["last_reset"] = today_date.strftime("%Y/%m/%dT00:00:00+00:00")
        self._attribute["copyright"] = "trumxuquang@gmail.com"