# @Author: Joe Iannone
# @Date:   2019-01-24T17:35:01-05:00
# @Filename: client.py
# @Last modified by:   Joe Iannone
# @Last modified time: 2019-01-24T19:53:03-05:00
import sys
import os.path
sys.path.insert(0, '..')
import random
import json
from client import Client
from requestHandler import RequestHandler

request_handler = RequestHandler()
client = Client(request_handler)

sub_areas = json.loads(client.getSubAreas(client.regions[random.randint(0, len(client.regions)-1)]['ref']))

local = json.loads(client.getLocalAreas(list(sub_areas.keys())[random.randint(0, len(sub_areas)-1)]));

print(json.dumps(local, indent=4, sort_keys=True))
