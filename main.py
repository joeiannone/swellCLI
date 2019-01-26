# @Author: Joe Iannone <josephiannone>
# @Date:   2019-01-22T21:22:57-05:00
# @Filename: main.py
# @Last modified by:   josephiannone
# @Last modified time: 2019-01-25T23:35:09-05:00

import sys
import json
import pprint
from bs4 import BeautifulSoup
from tabulate import tabulate
from client import Client
from request import RequestHandler
from parser import swellParser

request_handler = RequestHandler()
swell = Client(request_handler)

print('')
for i, region in enumerate(swell.regions):
    print(str(i) + ' --> ' + region['display'])

print('')
region_input = input('Select a region: ')
region = swell.regions[int(region_input)]['ref']

sub_areas = json.loads(swell.getSubAreas(region))

print('')
sub_area_refs = []
for i, sub_area in enumerate(sub_areas):
    sub_area_refs.append(sub_area)
    print(str(i) + ' --> ' + sub_areas[sub_area]['label'])

print('')
sub_area_input = input('Select a sub area: ')
sub_area = sub_area_refs[int(sub_area_input)]

local_areas = json.loads(swell.getLocalAreas(sub_area))
print('')
local_area_refs = []
for i, local_area in enumerate(local_areas):
    local_area_refs.append(local_area)
    print(str(i) + ' --> ' + local_areas[local_area]['label'])

print('')
local_area_input = input('Select a local area: ')
local_area = local_area_refs[int(local_area_input)]

print('')
foc = input('forecast or current? (f | c): ')
print('...\n')

swell_html = swell.getSwellHTML(local_area)
swell_soup = BeautifulSoup(swell_html, 'html5lib')
swell_parser = swellParser(swell_soup)

if foc is 'f':
    forecast = swell_parser.getForecast()
    pprint.pprint(forecast)

elif foc is 'c':
    current = swell_parser.getCurrentConditions()
    pprint.pprint(current)


#data = tabulate([['sex', 'age'], ['Joe', 'M', 29], ['Alice', 'F', 24], ['Bob', 'M', 31]], headers='firstrow')
#print(data)
