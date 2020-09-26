import requests,json,os
import pyutil

def _getketqua_last(json_):
    #print(json_)
    tournament = json_['tournament']
    giaidau = pyutil._extract_values_json(tournament, 'name')

    events = json_['events']
    
    #luotdau
    luotdau='N/a'
    try:
        tmp = events[0]['roundInfo']
        luotdau = pyutil._extract_values_json(tmp, 'name')

        if len(luotdau) == 0:
            luotdau = str(pyutil._extract_values_json(tmp, 'round')[0])
    except :
        luotdau='N/a'

    #tran_dau
    tmp = events[0]['homeTeam']
    tran_dau1 = pyutil._extract_values_json(tmp, 'name')
    tmp2 = events[0]['awayTeam']
    tran_dau2 = pyutil._extract_values_json(tmp2, 'name')

    #ket_qua
    ketqua = pyutil._extract_values_json(events, 'current')
    sport = pyutil._extract_values_json(json_, 'statusDescription')
    startTimestamp = pyutil._extract_values_json(json_, 'startTimestamp')
    datee = pyutil._linux2time(startTimestamp[0])

    if sport[0] == 'FT':
        rs ={
            'code':'last',
            'luotdau':luotdau[0],
            'giaidau':giaidau[0],
            'tran_dau':f"{tran_dau1[0]} - {tran_dau2[0]}",
            'ket_qua':f"{ketqua[0]} - {ketqua[1]}",
            'date':datee['date'],
            'time':datee['time']
        }
        print(rs)
        return rs
    else:
        rs ={
            'code':'last',
            'msg':'Eror',
        }
        print(rs)
        return rs

def _getketqua_next(json_):

    tournament = json_['tournament']
    giaidau = pyutil._extract_values_json(tournament, 'name')

    events = json_['events']
    
    #luotdau
    luotdau='N/a'
    try:
        tmp = events[0]['roundInfo']
        luotdau = pyutil._extract_values_json(tmp, 'name')

        if len(luotdau) == 0:
            luotdau = str(pyutil._extract_values_json(tmp, 'round')[0])
    except :
        luotdau='N/a'

    #tran_dau
    tmp = events[0]['homeTeam']
    tran_dau1 = pyutil._extract_values_json(tmp, 'name')
    tmp2 = events[0]['awayTeam']
    tran_dau2 = pyutil._extract_values_json(tmp2, 'name')

    #ket_qua
    startTimestamp = pyutil._extract_values_json(json_, 'startTimestamp')
    datee = pyutil._linux2time(startTimestamp[0])

    rs ={
        'code':'next',
        'luotdau':luotdau,
        'giaidau':giaidau[0],
        'tran_dau':f"{tran_dau1[0]} - {tran_dau2[0]}",
        'ket_qua': "N/A",
        'date':datee['date'],
        'time':datee['time']
    }
    print(rs)
    return rs


def _getjsonlocal(jsonfile):
    path = pyutil._getpath() + f"/data/{jsonfile}"
    jsondata = pyutil._get_json(path)
 
    
    jsonlast1 = jsondata['last']['tournaments'][0]
    jsonlast2 = jsondata['last']['tournaments'][1]
    jsonlast3 = jsondata['last']['tournaments'][2]

    
    jsonnext1 = jsondata['next']['tournaments'][0]
    jsonnext2 = jsondata['next']['tournaments'][1]
    jsonnext3 = jsondata['next']['tournaments'][2]

    rslast1 = _getketqua_last(jsonlast1)
    rslast2 = _getketqua_last(jsonlast2)
    rslast3 = _getketqua_last(jsonlast3)

    rsnext1 = _getketqua_next(jsonnext1)
    rsnext2 = _getketqua_next(jsonnext2)
    rsnext3 = _getketqua_next(jsonnext3)

    lst ={'last1':rslast1, 'last2':rslast2, 'last3':rslast3, 'next1':rsnext1, 'next3':rsnext2, 'next3':rsnext3}

    return lst

def _gettrandau(idteam):

    url = f"https://api.sofascore.com/mobile/v4/team/{idteam}/lastnext"
    #url ="https://api.sofascore.com/api/v1/tournament/1/season/29415/standings/total"
    headers = {
        'authority': 'api.sofascore.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-language': 'vi-VN,vi;q=0.9,en;q=0.8',
        'cookie': '__cfduid=d5e9f131206588de0c1a08b7470a544001600777701; _ga=GA1.2.1570948191.1600777704; _ym_d=1600777705; _ym_uid=1600777705602763648; __gads=ID=0d161b238d418c95:T=1600777704:S=ALNI_MZOjokL1F480r-Vq61VXJQgp6SSEA; sc_is_visitor_unique=rx10558723.1600778005.71A1EADCEE3C4F127469977868655D5B.1.1.1.1.1.1.1.1.1-9655907.1600777998.1.1.1.1.1.1.1.1.1',
        'if-none-match': 'W/"1841495c72"',
    }

    response = requests.get(url, headers=headers)
    print(response.text)

lst = _getjsonlocal('lastnext.json')

print(lst)