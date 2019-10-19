# @Author: Joe Iannone <josephiannone>
# @Date:   2019-01-26T16:56:12-05:00
# @Filename: cli.py
# @Last modified by:   josephiannone
# @Last modified time: 2019-05-14T20:28:21-04:00

import json, os, sys, pprint
from tabulate import tabulate
from bs4 import BeautifulSoup
from src.client import Client
from src.request import RequestHandler
from src.parser import swellParser
from src.colors import Colors

class swellCLI:

    def __init__(self):

        # Make sure 'user_data' directory exists, if not create
        self.user_directory = 'user_data'
        try:
            os.stat(self.user_directory)
        except:
            os.mkdir(self.user_directory)

        # Initialize data sets and swell client
        self.swellFile = self.user_directory+'/swell.json'
        self.user_data = self.read_json(self.swellFile)
        self.init_data = {'favorites': []}

        self.request_handler = RequestHandler()
        self.swell = Client(self.request_handler)

        self.nicknameList = []

        self.flags = None
        self.arg = None
        self.nickname = None

        self.args = sys.argv
        self.args.pop(0) # Remove first arg (script) for simplicity


    def run(self):

        # If user data empty initialize swellFile using init_data
        if self.user_data is None:
            self.write_json(self.swellFile, self.init_data)

        self.user_data = self.read_json(self.swellFile)

        # load spot nickname list
        for fav in self.user_data['favorites']:
            self.nicknameList.append(fav['nickname'])

        # Set flags and arg
        for arg in self.args:
            if arg in self.nicknameList:
                self.nickname = arg
            if arg[0] is '-' and self.flags is None:
                self.flags = arg.replace('-', '')
            elif self.arg is None and self.nickname is None:
                self.arg = arg

        if self.flags == 'h':
            #help
            pass

        if self.arg is None:
            self.selectAndOrDisplay()
        elif self.arg == 'add':
            self.addLocationRoutine()
        elif self.arg == 'spots':
            pass
        elif self.arg == 'help':
            #help
            pass

        sys.exit(0)


    def selectAndOrDisplay(self):

        if self.nickname is None:
            # - Allow user to select a location
            print(Colors.UNDERLINE + '\nFollow the prompts below:\n' + Colors.ENDC)
            region = self.getLocationInput(self.swell.regions, 'region')
            sub_areas = json.loads(self.swell.getSubAreas(region))
            sub_area = self.getLocationInput(sub_areas, 'sub area')
            local_areas = json.loads(self.swell.getLocalAreas(sub_area))
            local_area = self.getLocationInput(local_areas, 'local area')
        else:
            local_area = self.getLocalLinkByNickname(self, self.nickname)

        # - Display current conditions and forecast
        swell_html = self.swell.getSwellHTML(local_area)
        swell_soup = BeautifulSoup(swell_html, 'lxml')
        swell_parser = swellParser(swell_soup)

        current = self.getCurrentString(swell_parser.getCurrentConditions())
        print(current)


    def getLocalLinkByNickname(self, nickname):
        for fav in self.user_data['favorites']:
            if nickname == fav['nickname']:
                return fav['link']
        return None


    def addLocationRoutine(self):
        print(Colors.UNDERLINE + '\nFollow the prompts below:\n' + Colors.ENDC)

        region = self.getLocationInput(self.swell.regions, 'region')
        sub_areas = json.loads(self.swell.getSubAreas(region))
        sub_area = self.getLocationInput(sub_areas, 'sub area')
        local_areas = json.loads(self.swell.getLocalAreas(sub_area))
        local_area = self.getLocationInput(local_areas, 'local area')

        try:
            self.user_data['favorites'].append({'link': local_area, 'title': local_areas[local_area]['label'], 'nickname': ''})

            nickname = self.getNicknameRoutine(self.user_data['favorites'][-1])
            self.user_data['favorites'][-1]['nickname'] = nickname

            if (self.write_json(self.swellFile, self.user_data)):
                print(Colors.BOLD + '\nSpot added.' + Colors.ENDC)

        except Exception as e:
            print(e)
            return False

        print('\nYou can now easily check the conditions and forecast for ' + \
            Colors.BOLD + local_areas[local_area]['label'] + Colors.ENDC + ' using the nickname ' + \
            Colors.BOLD + nickname + Colors.ENDC + ' as a command line argument.\n')

        return True


    def getNicknameRoutine(self, spot):
        print('Add a nickname for this spot. (no spaces, limit 20 characters)')
        while 1:
            user_input = input('Nickname for ' + spot['title'] + ': ')
            if len(user_input) > 20 or ' ' in user_input:
                print('\nInvalid nickname. Try again.\n')
                continue
            if self.nicknameIsTaken(user_input):
                print('\nThat nickname is already taken. Try again\n')
                continue
            return user_input


    def getLocationInput(self, data_list, selection_str):
        while 1:
            refs = []
            for i, item in enumerate(data_list):
                refs.append(item)
                print(Colors.BOLD + '{0: <3}'.format(str(i)) + Colors.ENDC + \
                    Colors.CYAN + ' --> ' + Colors.ENDC + ' ' + data_list[item]['label'])

            user_input = input('\nSelect a ' + selection_str + ' (' + Colors.BOLD + '0-' + str(len(data_list)-1) + Colors.ENDC + ')' + ': ')

            try:
                if int(user_input) >= 0 and int(user_input) <= len(data_list)-1:
                    print('Selected ' + Colors.BOLD + data_list[refs[int(user_input)]]['label'] + Colors.ENDC + '\n')
                    return refs[int(user_input)]
            except:
                pass

            print(Colors.RED + '\nTry again. Input must be an integer from 0-' + str(len(data_list)-1) + '\n' + Colors.ENDC)


    def nicknameIsTaken(self, nickname):
        for i, spot in enumerate(self.user_data['favorites']):
            if nickname == spot['nickname']:
                return True
        return False


    def getCurrentString(self, data):
        #pprint.pprint(data)
        current = '\n'
        current += Colors.BOLD + Colors.OKYELLOW + data['location_title'] + Colors.ENDC + '\n'
        current += tabulate({
            'Air': [data['air'], data['wind']],
            'Height': [data['buoy_name'], data['wave_height']],
            'Tide': ['low: ' + data['low_tide'], 'high: ' + data['high_tide']],
            'Water': [data['water_temp'], data['wetsuit']]
        }, headers="keys", tablefmt="")
        current += '\n'
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
