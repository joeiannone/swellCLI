# @Author: Joe Iannone
# @Date:   2019-01-24T17:35:01-05:00
# @Filename: client.py
# @Last modified by:   Joe Iannone
# @Last modified time: 2019-01-24T22:36:03-05:00

import sys
import os.path
sys.path.insert(0, '..')
import random
import json
import pprint
from client import Client
from requestHandler import RequestHandler

request_handler = RequestHandler()
client = Client(request_handler)

region = client.regions[random.randint(0, len(client.regions)-1)]['ref']
sub_areas = json.loads(client.getSubAreas(region))
print(region)

sub_area = list(sub_areas.keys())[random.randint(0, len(sub_areas)-1)]
local_areas = json.loads(client.getLocalAreas(sub_area))
print(sub_area)

local_area = list(local_areas.keys())[random.randint(0, len(local_areas)-1)]
current_conditions = client.getCurrentConditions(local_area)
print(local_area)

forecast = client.getForecast(local_area)

pprint.pprint(current_conditions)

#pprint.pprint(forecast)
