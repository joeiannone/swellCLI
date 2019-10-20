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

        self.root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Make sure 'user_data' directory exists, if not create
        self.user_directory = self.root_path + '/user_data'
        try:
            os.stat(self.user_directory)
        except:
            os.mkdir(self.user_directory)

        # Initialize data sets and swell client
        self.swellFile = self.user_directory + '/swell.json'
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
            self.selectAndDisplay()
        elif self.arg == 'add':
            self.addLocationRoutine()
        elif self.arg == 'spots':
            print(self.getSpotsNicknamesView())

        elif self.arg == 'help':
            #help
            pass

        sys.exit(0)


    def selectAndDisplay(self):

        current = None
        forecast = None

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

        if self.flags is None or (self.flags is not None and 'c' in self.flags):
            current = self.getCurrentView(swell_parser.getCurrentConditions())

        if self.flags is not None and 'f' in self.flags:
            forecast = self.getForecastView(swell_parser.getForecast())

        if current is not None:
            print(current)
        if forecast is not None:
            print(forecast)



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
                print('  ' + Colors.BOLD + '{0: <3}'.format(str(i)) + Colors.ENDC + \
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


    def getCurrentView(self, data):
        #pprint.pprint(data)
        col_pad = 4
        table_pad = 2
        location = data['location_title'].split(',')
        city = location[0].title()
        state = location[1].upper()
        air = ['Air', data['air'], data['wind']]
        swell = ['Swell', data['buoy_name'], data['wave_height']]
        tide = ['Tide', str('low: ' + data['low_tide']), str('high: ' + data['high_tide'])]
        water = ['Water', data['water_temp'], data['wetsuit']]
        air_w = len(max(air, key=len)) + col_pad
        swell_w = len(max(swell, key=len)) + col_pad
        tide_w = len(max(tide, key=len)) + col_pad
        water_w = len(max(water, key=len)) + col_pad
        table_w = air_w + swell_w + tide_w + water_w + col_pad
        view = '\n'
        view += Colors.OKYELLOW + str('Current conditions for ' + Colors.BOLD + city + ',' + state).ljust(table_w) + Colors.ENDC + '\n\n'
        view += ''.ljust(table_pad) + Colors.CYAN + Colors.BOLD + air[0].ljust(air_w) + swell[0].ljust(swell_w) + tide[0].ljust(tide_w) + water[0].ljust(water_w) + Colors.ENDC + '\n'
        view += ''.ljust(table_pad) + air[1].ljust(air_w) + swell[1].ljust(swell_w) + tide[1].ljust(tide_w) + water[1].ljust(water_w) + '\n'
        view += ''.ljust(table_pad) + air[2].ljust(air_w) + swell[2].ljust(swell_w) + tide[2].ljust(tide_w) + water[2].ljust(water_w) + '\n'
        view += '\n'
        return view


    def getForecastView(self, data):
        pprint.pprint(data)
        forecast = ''
        return forecast


    def getSpotsNicknamesView(self):
        view = '\n'
        view += Colors.BOLD + 'Your Saved Spots' + Colors.ENDC + ':\n\n'
        for i, fav in enumerate(self.user_data['favorites']):
            view += '  ' + Colors.CYAN + Colors.BOLD + '{0: <20}'.format(fav['nickname']) + Colors.ENDC + ' (' + str(i) + ' - ' + fav['title'] + ')\n'
        view += '\n'
        view += 'Pass one of these nicknames or indexes as a command line argument to quickly retrieve the surf report.\n'
        return view


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
