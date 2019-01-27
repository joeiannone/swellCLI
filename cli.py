# @Author: Joe Iannone <josephiannone>
# @Date:   2019-01-26T16:56:12-05:00
# @Filename: cli.py
# @Last modified by:   josephiannone
# @Last modified time: 2019-01-27T01:00:59-05:00

import json
import pprint
from bs4 import BeautifulSoup
from tabulate import tabulate
from client import Client
from request import RequestHandler
from parser import swellParser

class swellCLI:

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    OKYELLOW = '\033[93m'
    WHITE = '\033[97m'
    BLUE = '\033[34m'
    RED = '\033[31m'
    DEFAULT = '\033[30m'
    CYAN = '\033[36m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self):
        self.run()

    def run(self):

        request_handler = RequestHandler()
        swell = Client(request_handler)

        print('')
        for i, region in enumerate(swell.regions):
            print(swellCLI.BOLD + str(i) + swellCLI.ENDC + ' --> ' + region['display'])

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
        swell_soup = BeautifulSoup(swell_html, 'lxml')
        swell_parser = swellParser(swell_soup)

        if foc is 'f':
            forecast = swell_parser.getForecast()
            pprint.pprint(forecast)

        elif foc is 'c':
            current = swell_parser.getCurrentConditions()
            pprint.pprint(current)

    def input(self, data_options):
        pass
