## Run in Python 3
## Import dependencies

from datetime import datetime
from dateutil.parser import parse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import json
from xml.etree import ElementTree as ET
from geopy.geocoders import Nominatim

Canada = {
'Alberta' : 'AB', 'British Columbia' : 'BC', 'Manitoba' : 'MB',
'New Brunswick' : 'NB','Newfoundland and Labrador' : 'NL',
'Northwest Territories' : 'NT', 'Nova Scotia' : 'NS','Nunavut' : 'NU',
 'Ontario' : 'ON','Prince Edward Island' : 'PE','Quebec' : 'QC',
 'Saskatchewan' : 'SK','Yukon' : 'YT'}

Australia = {'New South Wales':'NSW','Queensland':'QLD','South Australia':'SA',
'Tasmania':'TAS','Victoria':'VIC','Western Australia':'WA',
'Australian Capital Territory':'ACT','Northern Territory':'NT'}

geolocator = Nominatim(user_agent="RoadGoat")

finName = 'query_result_2019-04-15T18_54_31.744Z.csv'
foutName = 'Citywalkscores2.csv'
#fout2Name = 'RGNotCities.csv'

fout=open(foutName,'w')
fout.write('id,name,state/province,country,walk_score,bike_score,transit_score,visits,url\n')

#fout_nones =open(fout2Name,'w')
#fout_nones.write('id,name,state/province,country,visits,url')

with open(finName, 'r') as fi:
    reader = enumerate(csv.DictReader(fi))
    for rId, record in reader:
        cityId = record['id']
        name = record['name']
        state = 'N'
        visits = record['visits_counter_cache']
        if record['autocomplete_title'][-2:]  =='US':
            cc = 'US'
            state = record['location_title'][-2:]
            url = 'https://www.walkscore.com/%s/%s'%(state,name.replace(" ", "_"))

        elif record['location_title'][-6:]  =='Canada':
            cc = 'CA'
            a = record['twofishes_profile']
            if '\\"' in a:
                state = a.split(name)[2][2:4]
            else:
                try:
                    d = json.loads(a.replace("'", "\""))
                    state = d['displayName'][-10:-8]
                except:
                    location = geolocator.geocode(name + ' Canada')
                    for a in location.address.split(', '):
                        if a in Canada:
                            state = Canada[a]

            url = 'https://www.walkscore.com/%s-%s/%s'%(cc,state,name.replace(" ", "_"))


        elif record['location_title'][-9:]  == 'Australia':
            cc = 'AU'
            a = record['twofishes_profile']
            if '\\"'in a:
                state = a.split(name)[2].split(', ')[1]
            else:
                try:
                    d = json.loads(a.replace("'", "\""))
                    state = d['displayName'].split(', ')[1]
                except:
                    try:
                        location = geolocator.geocode(name + ' Australia')
                        for a in location.address.split(', '):
                            if a in Australia:
                                state = Australia[a]
                    except:
                        print('AUS FAIL', name)
                        continue

            url = 'https://www.walkscore.com/%s-%s/%s'%(cc,state,name.replace(" ", "_"))

        else:
            continue

        ws, ts, bs = 'N','N','N'

        try:
            html_content = requests.get(url).text
            soup = BeautifulSoup(html_content, 'lxml')
            if '<h2>About this Location</h2>' in str(soup):
                #fout_nones.write('{},{},{},{},{},{}\n'.format(cityId, name, state, cc, visits, url))
        #        print('Coordinate Fail')
                continue
            if 'pp.walk.sc/badge/walk/score' in str(soup):
                ws = str(soup).split('pp.walk.sc/badge/walk/score/')[1][:2]
            if 'pp.walk.sc/badge/bike/score' in str(soup):
                bs = str(soup).split('pp.walk.sc/badge/bike/score/')[1][:2]
            if 'pp.walk.sc/badge/transit/score' in str(soup):
                ts = str(soup).split('pp.walk.sc/badge/transit/score/')[1][:2]
            fout.write('{},{},{},{},{},{},{},{},{}\n'.format(
            cityId, name, state, cc, ws, bs, ts, visits, url))
        except:
            fout.write('{},{},{},{},{},{},{},{}, Abnormal URL Format\n'.format(
            cityId, name, state, cc, ws, bs, ts, visits))
