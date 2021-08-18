"""
A python module to the newest version number of Home Assistant.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import datetime
import logging, evnhassio


_LOGGER = logging.getLogger(__name__)

class Khoitao:
    """A class for returning HA version information from different sources."""
    def __init__(self, name='evnhcm', passw='aa' , makhach='xxx', numday='1'):
        """Initialize the class."""
        self._state = 'n/a'
        self._name = name
        self._passw = passw
        self._makhach = makhach
        self._numday = numday
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

    def get_evnhcm(self):

        try:  
            api = evnhassio.API(self._name , self._passw)
            data_out = api.get_evn_hcm(self._makhach)
            #print(data_out)
            #{'state': 'success', 'soNgay': 2, 'tieude': 'Từ 06/08/2021 đến 07/08/2021', 'ngay': '06/08', 'sanluong_tong': '22.57', 'tong_p_giao': '7,850.77'}
            
        except:
            print("fuck you")
            data_out ={'state': 'error', 'soNgay': 100, 'tieude': 'Từ 06/08/2021 đến 07/08/2021', 'ngay': '06/08', 'sanluong_tong': '100', 'tong_p_giao': '7,850.77'}
        
        # return data
        #print(data_out)
        tiendien = 0
        try:
          tiendien = float(data_out['sanluong_tong']) * 2014
        except:
          tiendien = 0

        if  data_out['state'] in ['error']:
          self._state = '0'
          self._attribute["alert"] = "Công tơ của bạn chưa hỗ trợ đo theo ngày"
          self._attribute["state_class"] = 'measurement'
          today_date = datetime.datetime.now()
          self._attribute["last_reset"] = today_date.strftime("%Y/%m/%dT00:00:00+00:00")
          self._attribute["copyright"] = "trumxuquang@gmail.com"
        else:
          self._state = data_out['sanluong_tong']
          self._attribute["alert"] = data_out['alert']
          self._attribute["tong_p_giao"] = data_out['tong_p_giao']
          self._attribute["tientamtinh"] = str(round(tiendien, 2)) + ' vnd'
          self._attribute["ngayDo"] = data_out['ngayFull']
          self._attribute["state_class"] = 'measurement'
          today_date = datetime.datetime.now()
          self._attribute["last_reset"] = today_date.strftime("%Y/%m/%dT00:00:00+00:00")
          self._attribute["copyright"] = "trumxuquang@gmail.com"
        #return datajson

    def get_evnhcm_solar(self):

        try:
            api = evnhassio.API(self._name , self._passw)
            data_out = api.get_evn_hcm_solar(self._makhach)
            #print(data_out)
            #{'state': 'success', 'soNgay': 2, 'tieude': 'Từ 06/08/2021 đến 07/08/2021', 'ngay': '06/08', 'sanluong_tong': '22.57', 'tong_p_giao': '7,850.77'}
            
        except:
            print("fuck you")
            data_out = {'state': 'error', 'soNgay': 100, 'tieude': 'Từ 06/08/2021 đến 07/08/2021', 'ngay': '06/08', 'sanluong_tong': '100', 'tong_p_nhan': '7,850.77'}
        
        ######
        if  data_out['state'] in ['error']:
          self._state = '0'
          self._attribute["alert"] = "Bạn không có sử dụng điện mặt trời"
          self._attribute["state_class"] = 'measurement'
          today_date = datetime.datetime.now()
          self._attribute["last_reset"] = today_date.strftime("%Y/%m/%dT00:00:00+00:00")
          self._attribute["copyright"] = "trumxuquang@gmail.com"
        else:
          self._state = data_out['sanluong_tong']
          self._attribute["alert"] = data_out['alert']
          self._attribute["tong_p_nhan"] = data_out['tong_p_nhan']
          self._attribute["ngayDo"] = data_out['ngayFull']
          self._attribute["sanluong_TD"] = data_out['sanluong_TD']
          self._attribute["sanluong_BT"] = data_out['sanluong_BT']
          self._attribute["sanluong_CD"] = data_out['sanluong_CD']
          self._attribute["state_class"] = 'measurement'
          today_date = datetime.datetime.now()
          self._attribute["last_reset"] = today_date.strftime("%Y/%m/%dT00:00:00+00:00")
          self._attribute["copyright"] = "trumxuquang@gmail.com"
        #return datajson


##########################################################################################
'''
def kc_date(kc=1):
    import datetime 
    today = datetime.date.today()
    today_date = today - datetime.timedelta(days = kc)

    return {"kc_date":today_date.strftime("%d/%m/%Y"),"today":today.strftime("%d/%m/%Y"), 
    }

def getdata_extr(txt):

    data_raw = txt.split("$('.text_result_tungaydenngay').html(\"")
    try:
        data=data_raw[1].split('\r\n')
        time_do = data[0].replace('");','').strip()
        sanluong = data[4].replace("$('.tong_cackhunggio').html(\"",'').strip()
        sanluong = sanluong.replace('");','').strip()

        input_makh ="hhh"
        input_makh = data[19].strip().replace("input_makh: \"",'').strip()
        input_makh = input_makh.replace('",','').strip()
        #print(input_makh)
        print()
        #print(data[19])

    except :
        time_do ='None'
        sanluong ='None'
        input_makh = 'None'
    return {"makh":input_makh, "time_do":time_do, "sanluong":sanluong}

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
'''