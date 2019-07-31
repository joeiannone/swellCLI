# @Author: Joe Iannone <josephiannone>
# @Date:   2019-01-26T16:56:12-05:00
# @Filename: cli.py
# @Last modified by:   josephiannone
# @Last modified time: 2019-05-14T20:28:21-04:00

import json, os, sys
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

        self.user_directory = 'user_data'
        try:
            os.stat(self.user_directory)
        except:
            os.mkdir(self.user_directory)

        self.swellFile = self.user_directory+'/swell.json'
        self.user_data = self.read_json(self.swellFile)
        self.init_data = {'defaultKey': 0, 'favorites': []}

        self.request_handler = RequestHandler()
        self.swell = Client(self.request_handler)

        self.run()


    def run(self):

        if self.user_data is None:
            self.write_json(self.swellFile, self.init_data)
            self.user_data = self.read_json(self.swellFile)

        if not self.user_data['favorites'] or not self.user_data['favorites'][self.user_data['defaultKey']]:
            print('\nFollow the prompts below to setup your default location.\n')
            print('')

            if self.addLocationRoutine():
                print('\nDefault spot created. \nYou can now easily check the conditions and forecast for ' + self.user_data['favorites'][self.user_data['defaultKey']]['title'] + '.\n')
            else:
                print('')
        else:

            ###############################
            # Now check args
            ###############################

            self.args = sys.argv
            self.args.pop(0) # remove first arg

            self.default_location = self.user_data['favorites'][self.user_data['defaultKey']]

            if len(self.args) is 0:
                swell_html = self.swell.getSwellHTML(self.default_location['link'])
                swell_soup = BeautifulSoup(swell_html, 'lxml')
                swell_parser = swellParser(swell_soup)
                current = self.getCurrentString(swell_parser.getCurrentConditions())
                print(current)

            else:

                self.cmd = {'subargs': [], 'nickname': ''}

                # loop through args
                for i, arg in enumerate(self.args):

                    if arg[0] is '-':
                        # sub args
                        subargs = list(arg)

                        subargs.pop(0) # remove '-'
                        self.cmd['subargs'] = subargs

                        if i is 0 and len(self.args) > 1:
                            self.cmd['nickname'] = self.args[1]
                        elif i is not 0:
                            self.cmd['nickname'] = self.args[0]

                    elif arg == 'add':
                        print('\nFollow the prompts below to add a new location.\n')
                        print('')

                        if self.addLocationRoutine():
                            print('\nSpot added. \nYou can now easily check the conditions and forecast for ' + self.user_data['favorites'][self.user_data['defaultKey']]['title'] + '.\n')

                    elif arg is 'spots':

                        pass

                    else:

                        pass

                    #print(arg)

        sys.exit(0)

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
            current = self.getCurrentString(swell_parser.getCurrentConditions())
            #pprint.pprint(current)
            print(current)


    def addLocationRoutine(self):
        try:
            region = self.getLocationInput(self.swell.regions, 'region')
            sub_areas = json.loads(self.swell.getSubAreas(region))
            sub_area = self.getLocationInput(sub_areas, 'sub area')
            local_areas = json.loads(self.swell.getLocalAreas(sub_area))
            local_area = self.getLocationInput(local_areas, 'local area')
            self.user_data['favorites'].append({'link': local_area, 'title': local_areas[local_area]['label']})

            self.write_json(self.swellFile, self.user_data)
        except Exception as e:
            print(e)
            return False

        return True

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


    def getCurrentString(self, data):
        current = self.BOLD + self.OKYELLOW + data['location_title'] + self.ENDC + '\n'
        current += tabulate({
            'Air': [data['air'], data['wind']],
            'Height': [data['buoy_name'], data['wave_height']],
            'Tide': ['low: ' + data['low_tide'], 'high: ' + data['high_tide']],
            'Water': [data['water_temp'], data['wetsuit']]
        }, headers="keys", tablefmt="rst")
        return current


    def getForecastString(self, data):
        forecast = ''
        return forecast


    def write_json(self, filename, data):
      try:
        with open(filename, 'w+') as outfile:
          json.dump(data, outfile)
        outfile.close()
        return True
      except:
        return False


    def read_json(self, filename):
      try:
        with open(filename) as json_data:
          d = json.load(json_data)
        json_data.close()
        return d
      except json.JSONDecodeError:
        return None
      except FileNotFoundError:
        return None
