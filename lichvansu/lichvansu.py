# encoding: utf-8
# trumxuquang@gmail.com
import math
import re
from datetime import datetime
from datetime import date
from datetime import time
from datetime import timedelta
import datetime
import requests
import urllib3
urllib3.disable_warnings()

url_source = 'https://vansu.net/lich-van-nien.html'
vn_begin = '<div class="block-description-function change-calendar"><div class="kqua"><div class="result-change" style="margin-top:0px;"><p>'
vn_end = '<div class="lich-xem-chi-tiet" style="text-align: right; color: #d21c1b; text-decoration: underline; margin: 10px;">'
url_day = '?day='
url_mon = '&mon='
url_year = '&year='

def get_vansu():
    try:
        response = requests.get(url = url_source, verify = False).text

        #print(response)
        text_vn = response

        begin_index = text_vn.index(vn_begin)
        end_index = text_vn.index(vn_end)
        json_vn = text_vn[ begin_index + 149 : end_index - 59 ].strip()
        #print(json_vn)
        arr = json_vn.splitlines()
        
        #khai bao var
        amLich = "NA"
        saoTot = "NA"
        saoXau = "NA"
        gioTot = "NA"
        gioXau = "NA"
        truc = "NA"
        tuoiHop = "NA"
        tuoiXung = "NA"
        onlyDay = "NA"
        txt_tomo = "NA"
        ngayTotXau ="NA"
        # procesing
        saoTot = arr[3].replace('<b>', '').replace('</b>', '').replace('<br/>', '').strip()
        saoXau = arr[4].replace('<b>', '').replace('</b>', '').replace('<br/>', '').strip()
        amLich = arr[1].replace('<b>', '').replace('</b>', '').replace('<br/>', '').replace('<br>', '').strip()

        ##chia array 2
        arr2 = arr[2].split('<strong class="clr-red">')
        #print(arr2[1])
        gioTot = arr2[1].replace('</strong> <table><tbody><tr><td>', ' ').replace('</td><td>', ', ').replace('</td></tr><tr><td>', ', ').replace('</td></tr></tbody></table></p><p>', '').replace('</strong><div class="giohh-cs"> <table><tbody><tr><td>', '').replace('</td></tr></tbody></table></div></p><p>', '').strip()
        gioTot = tachhtml(gioTot)
        
        gioXau = arr2[2].replace('</strong> <table><tbody><tr><td>', ' ').replace('</td><td>', ', ').replace('</td></tr><tr><td>', ', ').replace('</td></tr></tbody></table></p><p>', '').strip()
        gioXau = tachhtml(gioXau)

        tuoiHop = arr2[3].replace('<p>', ' ').replace('</td><td>', ', ').replace('</td></tr><tr><td>', ', ').replace('</strong>', '').strip()

        tuoiXung = arr2[4].replace('<p>', ' ').replace('</td><td>', ', ').replace('</p>', ', ').replace('</strong>', '').strip()

        truc = arr2[5].replace('</strong><br>', ' ').replace('<br>', ', ').replace('</td></tr><tr><td>', ', ').replace('</p><p>', '').strip()

        ngayTotXau = arr2[0].replace('</p><p>', ' ').strip()

        # onlydate
        onlyDay = amLich.split("/")[0]
        if onlyDay.find("0") == 9:
           onlyDay = onlyDay[ -1  : ]
        else :
           onlyDay = onlyDay[ -2  : ]
        """
        print("$$$$$$$ : " + amLich)
        print("$$$$$$$ : " + saoTot)
        print("$$$$$$$ : " + saoXau)
        print("$$$$$$$ : " + gioTot)
        print("$$$$$$$ : " + gioXau)
        print("$$$$$$$ : " + ngayTotXau)
        print("$$$$$$$ : " + truc)
        print("$$$$$$$ : " + tuoiHop)
        print("$$$$$$$ : " + tuoiXung) """
        ######################
        tomorrow = datetime.date.today() + datetime.timedelta(days = 1)
        arr_tomo = tomorrow.strftime('%Y-%-m-%-d').split('-')
        url_day = '?day=' + arr_tomo[2]
        url_mon = '&mon=' + arr_tomo[1]
        url_year = '&year=' + arr_tomo[0]

        # call request tomorrow
        url_tomo = url_source + url_day + url_mon +url_year
        response_tomo = requests.get(url = url_tomo, verify = False).text
        txt_tomo = response_tomo[ response_tomo.index('<b>Âm lịch:</b> ') + 16 : response_tomo.index('<b>Âm lịch:</b> ') + 18 ].strip()
        
        if txt_tomo.find("0") == 0:
           txt_tomo = txt_tomo[ 1  : 2]
        else :
           txt_tomo = txt_tomo[ 0  : ] 

    except:
        amLich = "NA"
        saoTot = "NA"
        saoXau = "NA"
        gioTot = "NA"
        gioXau = "NA"
        truc = "NA"
        ngayTotXau = "NA"
        tuoiHop = "NA"
        tuoiXung = "NA"
        onlyDay = "NA"
        txt_tomo = "NA"

    return {'amLich': amLich, 'saoTot': saoTot ,'saoXau': saoXau, 'gioTot': gioTot, 'gioXau': gioXau ,'ngayTotXau': ngayTotXau, 'truc':truc, 'tuoiHop':tuoiHop, 'tuoiXung':tuoiXung, 'ngay_homnay':onlyDay, 'ngay_mai' :txt_tomo }
    

''' Thuật toán tính âm lịch
(c) 2006 Ho Ngoc Duc.
Astronomical algorithms
from the book "Astronomical Algorithms" by Jean Meeus, 1998
link: https://www.informatik.uni-leipzig.de/~duc/amlich/calrules.html
'''
def jdFromDate(dd, mm, yy):
  '''def jdFromDate(dd, mm, yy): Compute the (integral) Julian day number of day dd/mm/yyyy, i.e., the number of days between 1/1/4713 BC (Julian calendar) and dd/mm/yyyy.'''
  a = int((14 - mm) / 12.)
  y = yy + 4800 - a
  m = mm + 12*a - 3
  jd = dd + int((153*m + 2) / 5.) \
        + 365*y + int(y/4.) - int(y/100.) \
        + int(y/400.) - 32045
  if (jd < 2299161):
    jd = dd + int((153*m + 2)/5.) \
          + 365*y + int(y/4.) - 32083
  return jd

def jdToDate(jd):
  '''def jdToDate(jd): Convert a Julian day number to day/month/year. jd is an integer.'''
  if (jd > 2299160):
    ## After 5/10/1582, Gregorian calendar
    a = jd + 32044
    b = int((4*a + 3) / 146097.)
    c = a - int((b*146097) / 4.)
  else:
    b = 0
    c = jd + 32082
  d = int((4*c + 3) / 1461.)
  e = c - int((1461*d) / 4.)
  m = int((5*e + 2) / 153.)
  day = e - int((153*m + 2) / 5.) + 1
  month = m + 3 - 12*int(m / 10.)
  year = b*100 + d - 4800 + int(m / 10.)
  return [day, month, year]

def NewMoon(k):
  '''def NewMoon(k): Compute the time of the k-th new moon after the new moon of 1/1/1900 13:52 UCT (measured as the number of days since 1/1/4713 BC noon UCT, e.g., 2451545.125 is 1/1/2000 15:00 UTC. Returns a floating number, e.g., 2415079.9758617813 for k=2 or 2414961.935157746 for k=-2.'''
  ## Time in Julian centuries from 1900 January 0.5
  T = k / 1236.85
  T2 = T * T
  T3 = T2 * T
  dr = math.pi / 180.
  Jd1 = 2415020.75933 + 29.53058868*k \
          + 0.0001178*T2 - 0.000000155*T3
  Jd1 = Jd1 + 0.00033*math.sin( \
            (166.56 + 132.87*T - 0.009173*T2)*dr)
  ## Mean new moon
  M = 359.2242 + 29.10535608*k \
      - 0.0000333*T2 - 0.00000347*T3
  ## Sun's mean anomaly
  Mpr = 306.0253 + 385.81691806*k \
          + 0.0107306*T2 + 0.00001236*T3
  ## Moon's mean anomaly
  F = 21.2964 + 390.67050646*k - 0.0016528*T2 \
        - 0.00000239*T3
  ## Moon's argument of latitude
  C1 = (0.1734 - 0.000393*T)*math.sin(M*dr) \
        + 0.0021*math.sin(2*dr*M)
  C1 = C1 - 0.4068*math.sin(Mpr*dr) \
        + 0.0161*math.sin(dr*2*Mpr)
  C1 = C1 - 0.0004*math.sin(dr*3*Mpr)
  C1 = C1 + 0.0104*math.sin(dr*2*F) \
        - 0.0051*math.sin(dr*(M + Mpr))
  C1 = C1 - 0.0074*math.sin(dr*(M - Mpr)) \
        + 0.0004*math.sin(dr*(2*F + M))
  C1 = C1 - 0.0004*math.sin(dr*(2*F - M)) \
        - 0.0006*math.sin(dr*(2*F + Mpr))
  C1 = C1 + 0.0010*math.sin(dr*(2*F - Mpr)) \
        + 0.0005*math.sin(dr*(2*Mpr + M))
  if (T < -11):
    deltat= 0.001 + 0.000839*T + 0.0002261*T2 \
                - 0.00000845*T3 - 0.000000081*T*T3
  else:
    deltat= -0.000278 + 0.000265*T + 0.000262*T2
  JdNew = Jd1 + C1 - deltat
  return JdNew

def SunLongitude(jdn):
  '''def SunLongitude(jdn): Compute the longitude of the sun at any time. Parameter: floating number jdn, the number of days since 1/1/4713 BC noon.'''
  T = (jdn - 2451545.0 ) / 36525.
  ## Time in Julian centuries
  ## from 2000-01-01 12:00:00 GMT
  T2 = T * T
  dr = math.pi / 180.  ## degree to radian
  M = 357.52910 + 35999.05030*T \
      - 0.0001559*T2 - 0.00000048*T*T2
  ## mean anomaly, degree
  L0 = 280.46645 + 36000.76983*T + 0.0003032*T2
  ## mean longitude, degree
  DL = (1.914600 - 0.004817*T - 0.000014*T2) \
          * math.sin(dr*M)
  DL += (0.019993 - 0.000101*T) *math.sin(dr*2*M) \
            + 0.000290*math.sin(dr*3*M)
  L = L0 + DL  ## true longitude, degree
  L = L * dr
  L = L - math.pi*2*(int(L / (math.pi*2)))
  #### Normalize to (0, 2*math.pi)
  return L

def getSunLongitude(dayNumber, timeZone):
  '''def getSunLongitude(dayNumber, timeZone):  Compute sun position at midnight of the day with the given Julian day number. The time zone if the time difference between local time and UTC: 7.0 for UTC+7:00. The function returns a number between 0 and 11.  From the day after March equinox and the 1st major term after March equinox, 0 is returned. After that, return 1, 2, 3 ...'''
  return int( \
    SunLongitude(dayNumber - 0.5 - timeZone/24.) \
    / math.pi*6)

def getNewMoonDay(k, timeZone):
  '''def getNewMoonDay(k, timeZone): Compute the day of the k-th new moon in the given time zone. The time zone if the time difference between local time and UTC: 7.0 for UTC+7:00.'''
  return int(NewMoon(k) + 0.5 + timeZone / 24.)

def getLunarMonth11(yy, timeZone):
  '''def getLunarMonth11(yy, timeZone):  Find the day that starts the luner month 11of the given year for the given time zone.'''
  # off = jdFromDate(31, 12, yy) \
  #            - 2415021.076998695
  off = jdFromDate(31, 12, yy) - 2415021.
  k = int(off / 29.530588853)
  nm = getNewMoonDay(k, timeZone)
  sunLong = getSunLongitude(nm, timeZone)
  #### sun longitude at local midnight
  if (sunLong >= 9):
    nm = getNewMoonDay(k - 1, timeZone)
  return nm

def getLeapMonthOffset(a11, timeZone):
  '''def getLeapMonthOffset(a11, timeZone): Find the index of the leap month after the month starting on the day a11.'''
  k = int((a11 - 2415021.076998695) \
              / 29.530588853 + 0.5)
  last = 0
  i = 1  ## start with month following lunar month 11
  arc = getSunLongitude( \
                getNewMoonDay(k + i, timeZone), timeZone)
  while True:
    last = arc
    i += 1
    arc = getSunLongitude( \
                      getNewMoonDay(k + i, timeZone), \
                      timeZone)
    if  not (arc != last and i < 14):
      break
  return i - 1

def S2L(dd, mm, yy, timeZone = 7):
  '''def S2L(dd, mm, yy, timeZone = 7): Convert solar date dd/mm/yyyy to the corresponding lunar date.'''
  dayNumber = jdFromDate(dd, mm, yy)
  k = int((dayNumber - 2415021.076998695) \
                / 29.530588853)
  monthStart = getNewMoonDay(k + 1, timeZone)
  if (monthStart > dayNumber):
    monthStart = getNewMoonDay(k, timeZone)
  # alert(dayNumber + " -> " + monthStart)
  a11 = getLunarMonth11(yy, timeZone)
  b11 = a11
  if (a11 >= monthStart):
    lunarYear = yy
    a11 = getLunarMonth11(yy - 1, timeZone)
  else:
    lunarYear = yy + 1
    b11 = getLunarMonth11(yy + 1, timeZone)
  lunarDay = dayNumber - monthStart + 1
  diff = int((monthStart - a11) / 29.)
  lunarLeap = 0
  lunarMonth = diff + 11
  if (b11 - a11 > 365):
    leapMonthDiff = \
        getLeapMonthOffset(a11, timeZone)
    if (diff >= leapMonthDiff):
      lunarMonth = diff + 10
      if (diff == leapMonthDiff):
        lunarLeap = 1
  if (lunarMonth > 12):
    lunarMonth = lunarMonth - 12
  if (lunarMonth >= 11 and diff < 4):
    lunarYear -= 1
  return \
      [ lunarDay, lunarMonth, lunarYear, lunarLeap ]

def L2S(lunarD, lunarM, lunarY, lunarLeap, tZ = 7):
  '''def L2S(lunarD, lunarM, lunarY, lunarLeap, tZ = 7): Convert a lunar date to the corresponding solar date.'''
  if (lunarM < 11):
    a11 = getLunarMonth11(lunarY - 1, tZ)
    b11 = getLunarMonth11(lunarY, tZ)
  else:
    a11 = getLunarMonth11(lunarY, tZ)
    b11 = getLunarMonth11(lunarY + 1, tZ)
  k = int(0.5 + \
              (a11 - 2415021.076998695) / 29.530588853)
  off = lunarM - 11
  if (off < 0):
    off += 12
  if (b11 - a11 > 365):
    leapOff = getLeapMonthOffset(a11, tZ)
    leapM = leapOff - 2
    if (leapM < 0):
      leapM += 12
    if (lunarLeap != 0 and lunarM != leapM):
      return [0, 0, 0]
    elif (lunarLeap != 0 or off >= leapOff):
      off += 1
  monthStart = getNewMoonDay(k + off, tZ)
  return jdToDate(monthStart + lunarD - 1)

''' end function calendar '''    
# Chữ sang số
def ngaymai():
    print ('Âm lịch ngày mai')
    a = 'Ngày mai'
    ngay = datetime.date.today() + timedelta(1)
    yy =  ngay.year
    mm = ngay.month
    dd = ngay.day
    return a,ngay,yy,mm,dd
def ngaymot():
    print ('Âm lịch ngày mốt')
    a = 'ngày mốt'
    ngay = datetime.date.today() + timedelta(2)
    yy = ngay.year
    mm = ngay.month
    dd = ngay.day
    return a,ngay,yy,mm,dd
def homqua():
    print ('Âm lịch hôm qua')
    a = 'hôm qua'
    ngay = datetime.date.today() - timedelta(1)
    yy =  ngay.year
    mm = ngay.month
    dd = ngay.day
    return a,ngay,yy,mm,dd
def homnay():
    a = 'hôm nay'
    print ('âm lịch hôm nay')
    ngay = datetime.date.today()
    yy =  ngay.year
    mm = ngay.month
    dd = ngay.day
    return a,ngay,yy,mm,dd

def ngaykhac(data):
    today=datetime.date.today()
    print ('Âm lịch ngày')
    if 'NGÀY' in data:
        ngay = re.search('NGÀY (.+?)(.+?)', data)
        dd = int(ngay.group(1)+ngay.group(2))
    else: 
        dd = today.day
    if 'THÁNG' in data:
        thang = re.search('THÁNG (.+?)(.+?)', data)
        mm = int(thang.group(1)+thang.group(2))    
    else:
        mm = today.month    
    yy = today.year        
    a = 'Ngày '+str(dd)+ 'tháng '+str(mm)
    daa = str(yy)+'-'+str(mm)+'-'+str(dd)
    ngay = datetime.datetime.strptime(daa, '%Y-%m-%d')
    a = 'Ngày '+str(dd)+ 'tháng '+str(mm)+' năm nay'
    return a,ngay,yy,mm,dd

def from_to_day(yy1,mm1,dd1,yy2,mm2,dd2):
    ''' format yyyy mm dd'''
    from_day = date(yy1, mm1, dd1)
    to_day = date(yy2, mm2, dd2)
    delta = (from_day - to_day)
    return delta.days 

def kiemtra_amlich(a,yy,mm,dd):
    left_01 = 0
    left_15 = 15
    lunar_date = S2L(dd, mm, yy)
    ngay_am = str(lunar_date[0])
    list_thang = ["tháng Giêng","tháng Hai","tháng Ba","tháng Tư","tháng Năm","tháng Sáu","tháng Bảy","tháng Tám","tháng Chín","tháng Mười","tháng Mười một","tháng Chạp"]
    #thang_am = int(str(lunar_date[1]))-1
    thang_am = int(str(lunar_date[1]))
    thang_am1 = list_thang[int(str(lunar_date[1]))-1]
    can = ['Canh ', 'Tân ', 'Nhâm ', 'Quý ', 'Giáp ', 'Ất ', 'Bính ', 'Đinh ','Mậu ','Kỷ ']
    chi = ['Thân', 'Dậu', 'Tuất', 'Hợi','Tí','Sửu','Dần', 'Mão', 'Thìn', 'Tị', 'Ngọ', "Mùi"]
    nam = int(str(lunar_date[2]))
    vitri_can = nam % 10
    vitri_chi = nam % 12
    nam_am = str(lunar_date[2])
    # lunar_text2 = 'Ngày: ' + str(lunar_date[0]) + ' - ' + thang_am1  + ' năm '  + can[vitri_can] + chi[vitri_chi] + ' (' +  str(lunar_date[2]) +')'
    ss = int(ngay_am)
    nam_nhuan = int(str(lunar_date[3]))
    if ss == 15:
        left_15 = 0
        speaking = a+" là ngày rằm "+ thang_am1 + ' năm ' + can[vitri_can] +' '+ chi[vitri_chi]+' ' + ' ' + nam_am
    elif ss == 1:
        left_01 = 0
        speaking = a+" là ngày mùng một "+ thang_am1 + ' năm ' + can[vitri_can] +' '+ chi[vitri_chi]+ ' ' + nam_am
    elif ss>1 and ss<15:
        days_left = 15 - ss
        left_15 = days_left
        speaking = a+" là ngày " + ngay_am +' '+ thang_am1 + ' năm ' + can[vitri_can] +' '+ chi[vitri_chi] +' ('+ nam_am  + "). Còn " + str(days_left) + " ngày nữa là đến rằm"
    elif ss>15 and ss<31:
        thang_sau = thang_am + 1
        if thang_am <= 12:
            nam_a = nam_am 
        else:
            nam_a = nam_am + 1
            # ny = yy + 1
            a2d = L2S(28,12,yy,nam_nhuan)
            nd = a2d[0]
            td = a2d[1]
            nmd = a2d[2]
            daa = str(nd)+'-'+str(td)+'-'+str(nmd)
            a2dnew = datetime.datetime.strptime(daa, '%d-%m-%Y')
            ngaytet = a2dnew.day
            thangtet = a2dnew.month
            namtet = a2dnew.year
            nammoi = S2L(ngaytet,thangtet,namtet)
            nam_nhuan = int(str(nammoi[3]))
        next = L2S(1,thang_sau,int(nam_a), nam_nhuan)
        print(next)
        nd = next[0]
        td = next[1]
        nmd = next[2]
        days_left = from_to_day(nmd,td ,nd , yy, mm, dd)
        left_01 = days_left

        '''daa = str(nd)+'-'+str(td)+'-'+str(nmd)
        a2dnew = datetime.datetime.strptime(daa, '%d-%m-%Y')
        delta = a2dnew - datetime.datetime.today()
        days_left = delta.days'''
        thang_am = list_thang[thang_am -1]
        ngay_am =str(lunar_date[0])
        speaking = a+' là ngày ' + ngay_am +' '+ thang_am + ' năm ' + can[vitri_can]+' ' + chi[vitri_chi]+' ' + nam_am + ". Còn " + str(days_left) + " ngày nữa là đến mùng một"
    else:
        print("Error")
    return {"speaking" : speaking , "left_01" : left_01 , "left_15" : left_15 }

def kiemtra_amlich1(a,yy,mm,dd):
    left_01 = 0
    left_15 = 0
    #chuyen sang ngay am lich
    lunar_date = S2L(dd, mm, yy)
    ngay_am = int(str(lunar_date[0]))
    thang_am = int(str(lunar_date[1]))
    nam = int(str(lunar_date[2]))
    nam_nhuan = int(str(lunar_date[3]))
    thang_amc01 = thang_am
    thang_amc15 = thang_am
    nam_a = nam

    if ngay_am>1 and ngay_am<15:
        thang_amc01 = thang_am + 1
        thang_amc15 = thang_am
        nam_a = nam

    if ngay_am>15 and ngay_am<31:
        thang_amc01 = thang_am + 1
        thang_amc15 = thang_am + 1
        if thang_am <= 12:
            nam_a = nam 
        else:
            nam_a = nam + 1
            a2d = L2S(28,12,yy,nam_nhuan)
            nd = a2d[0]
            td = a2d[1]
            nmd = a2d[2]
            daa = str(nd)+'-'+str(td)+'-'+str(nmd)
            a2dnew = datetime.datetime.strptime(daa, '%d-%m-%Y')
            ngaytet = a2dnew.day
            thangtet = a2dnew.month
            namtet = a2dnew.year
            nammoi = S2L(ngaytet,thangtet,namtet)
            nam_nhuan = int(str(nammoi[3]))
    #chuyen ngay am sang duong
    a2d1 = L2S(15, thang_amc15, nam_a, nam_nhuan)
    a2d2 = L2S(1, thang_amc01 , nam_a, nam_nhuan)
    print( thang_amc01 )
    print( nam_a )
    print( nam_nhuan )

    print( a2d2 )
    if ngay_am == 15:
        left_15 = 0
    else:
        left_15 = from_to_day(a2d1[2],a2d1[1] ,a2d1[0] , yy, mm, dd)
    if ngay_am == 1:
        left_01 = 0
    else:
        left_01 = from_to_day(a2d2[2],a2d2[1] ,a2d2[0] , yy, mm, dd)
    
    return {"amlich": lunar_date ,"left_01" : left_01 , "left_15" : left_15 }

def calcDayto01(yyyy, mm, dd):

    to_mung1 = 0
    #convert to duong lich
    lunar_date = S2L(dd, mm, yyyy)
    ngay_am = int(str(lunar_date[0]))

    to_mung1 = 31 - ngay_am
    x = datetime.date(yyyy, mm, dd)
    x = x + datetime.timedelta(days=to_mung1)
    #convert to duong lich
    lunar_date1 = S2L(x.day, x.month, x.year)
    ngay_am = int(str(lunar_date1[0]))

    left_01 = 0
    if ngay_am == 1:
       left_01 = to_mung1
    elif ngay_am == 2:
       left_01 = to_mung1 - 1
    elif ngay_am == 3:
       left_01 = to_mung1 -2

    return left_01

def checkYear(year): 
  
    # Return true if year is a multiple 
    # of 4 and not multiple of 100. 
    # OR year is multiple of 400. 
    return (((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0))

def kiemtra_amlich2():
    
    today = date.today()
    yy = today.year
    mm = today.month
    dd = today.day

    #chuyen sang ngay am lich
    lunar_date = S2L(dd, mm, yy)

    ngay_am = int(str(lunar_date[0]))

    days_left15 = 0
    days_left01 = 0

    if ngay_am == 1:
       days_left15 = 15
       days_left01 = 0

    if ngay_am>1 and ngay_am<16:
       days_left15 = 15 - ngay_am
       days_left01 = calcDayto01(yy,mm,dd)

    if ngay_am>15 and ngay_am<31:
       days_left01 = calcDayto01(yy,mm,dd)
       days_left15 = days_left01 + 14

    return {"lunar_date" : lunar_date , "days_left01" : days_left01 , "days_left15" : days_left15 }

def khoang_cach_AL(mm = 3, dd =10):
    ''' ngay am lich -> con bao nhieu ngay 
    '''
    today = date.today()
    yyyy = today.year
    ngay_duong = 0
    thang_duong = 0
    nam_duong = 0

    lu_date = S2L(today.day, today.month, today.year)
    thang_nhuan = int(str(lu_date[3]))

    sun_date = L2S(dd, mm, yyyy, 0)
    ngay_duong = int(str(sun_date[0]))
    thang_duong = int(str(sun_date[1]))
    nam_duong = int(str(sun_date[2]))
    
    sun_date_n = L2S(dd, mm, yyyy, 1)
    ngay_duong_n = int(str(sun_date_n[0]))

    if ngay_duong > 0 and ngay_duong_n > 0 and thang_nhuan ==1:
        sun_date = L2S(dd, mm, yyyy, 1)
        ngay_duong = int(str(sun_date[0]))
        thang_duong = int(str(sun_date[1]))
        nam_duong = int(str(sun_date[2]))

    dayxx = from_to_day(nam_duong, thang_duong, ngay_duong , today.year, today.month, today.day)
    if dayxx < 0 :
        dayxx = 365 + dayxx

    return dayxx

def tachhtml(str):
    str = str.replace('</td></tr></tbody></table></div></p><p>','').replace('</strong><div class="giohh-cs"> <table><tbody><tr><td>','')
    return str.strip()
  

####
print(get_vansu())
print(kiemtra_amlich2())
print(khoang_cach_AL(6, 17))