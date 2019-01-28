# @Author: Joe Iannone <josephiannone>
# @Date:   2019-01-26T16:56:12-05:00
# @Filename: cli.py
# @Last modified by:   josephiannone
# @Last modified time: 2019-01-27T22:34:24-05:00

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

    def run(self):

        request_handler = RequestHandler()

        swell = Client(request_handler)

        print('')

        region = self.getLocationInput(swell.regions, 'region')

        sub_areas = json.loads(swell.getSubAreas(region))

        sub_area = self.getLocationInput(sub_areas, 'sub area')

        local_areas = json.loads(swell.getLocalAreas(sub_area))

        local_area = self.getLocationInput(local_areas, 'local area')


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



    def getLocationInput(self, data_list, selection_str):

        while 1:
            refs = []
            for i, item in enumerate(data_list):
                refs.append(item)
                print(swellCLI.BOLD + str(i) + swellCLI.ENDC + ' --> ' + data_list[item]['label'])

            print('')
            user_input = input('Select a ' + selection_str + ' (0-' + str(len(data_list)-1) + '): ')
            try:
                if int(user_input) >= 0 and int(user_input) <= len(data_list)-1:
                    print('\nSelected ' + swellCLI.BOLD + data_list[refs[int(user_input)]]['label'] + swellCLI.ENDC + '\n')
                    return refs[int(user_input)]
            except:
                pass

            print(swellCLI.RED + '\nTry again. Input must be an integer from 0-' + str(len(data_list)-1) + '\n' + swellCLI.ENDC)
