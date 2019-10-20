# @Author: Joe Iannone <josephiannone>
# @Date:   2019-01-26T16:56:12-05:00
# @Filename: cli.py
# @Last modified by:   josephiannone
# @Last modified time: 2019-05-14T20:28:21-04:00

import json, os, sys, pprint, calendar, datetime
from bs4 import BeautifulSoup
from src.client import Client
from src.request import RequestHandler
from src.parser import swellParser
from src.colors import Colors

class swellCLI:

    def __init__(self):

        # get current day of week name
        today = datetime.date.today()
        self.today_name = calendar.day_name[today.weekday()].upper()

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
            elif arg.isdigit() and int(arg) < len(self.nicknameList):
                self.nickname = self.nicknameList[int(arg)] # use index for nickname
            if arg[0] is '-' and self.flags is None:
                self.flags = arg.replace('-', '')
            elif self.arg is None and self.nickname is None:
                self.arg = arg

        # if 'h' help flag set strictly alone
        if self.flags == 'h' or self.flags == 'help':
            exit(self.getHelpView())

        if self.arg is None:
            self.selectAndDisplay()
        if self.arg == 'add':
            self.addLocationRoutine()
        if self.arg == 'spots':
            print(self.getSpotsNicknamesView())
        if self.arg == 'help':
            print(self.getHelpView())
        if self.arg == 'remove':
            if self.nickname is not None:
                if self.removeFavoriteByNickname(self.nickname):
                    print('\n  ' + Colors.BOLD + self.nickname + ' has been removed.\n' + Colors.ENDC)
                else:
                    print(Colors.BOLD + '\n  Could not remove ' + self.nickname + ' from data store.\n' + Colors.ENDC)
            else:
                print('\n! Invalid nickname. Try again.\n')
        if self.arg == 'reset':
            if self.resetUserData():
                print('\n  ' + Colors.BOLD + 'Data has been reset.\n' + Colors.ENDC)
            else:
                print(Colors.BOLD + '\n  Could not reset data.\n' + Colors.ENDC)

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
            local_area = self.getLocalLinkByNickname(self.nickname)

        # - Display current conditions and forecast
        swell_html = self.swell.getSwellHTML(local_area)
        swell_soup = BeautifulSoup(swell_html, 'lxml')
        swell_parser = swellParser(swell_soup)

        if self.flags is None or (self.flags is not None and 'c' in self.flags):
            current = self.getCurrentView(swell_parser.getCurrentConditions())
        elif self.flags is not None and ('c' not in self.flags and 'f' not in self.flags):
            current = self.getCurrentView(swell_parser.getCurrentConditions())

        if self.flags is not None and 'f' in self.flags:
            forecast = self.getForecastView(swell_parser.getForecast())

        if current is not None:
            print(current)
        if forecast is not None:
            print(forecast)


    def resetUserData(self):
        if not self.write_json(self.swellFile, self.init_data):
            return False
        return True


    def removeFavoriteByNickname(self, nickname):
        if not self.nicknameIsTaken(nickname):
            return False
        for i, fav in enumerate(self.user_data['favorites']):
            if fav['nickname'] == nickname:
                if not self.user_data['favorites'].pop(i):
                    return False
                if not self.write_json(self.swellFile, self.user_data):
                    return False
                return True
        return False


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
                print(Colors.BOLD + '\nSpot added!' + Colors.ENDC)

        except Exception as e:
            print(e)
            return False

        print('\nYou can now easily check the conditions and forecast for ' + \
            Colors.BOLD + local_areas[local_area]['label'] + Colors.ENDC + ' using the nickname ' + \
            Colors.BOLD + nickname + Colors.ENDC + ' as a command line argument.\n')

        return True


    def getNicknameRoutine(self, spot):
        print(Colors.UNDERLINE + 'Add a nickname for this spot. (no spaces, limit 20 characters)\n' + Colors.ENDC)
        while 1:
            user_input = input(Colors.BOLD + 'Nickname for ' + spot['title'] + Colors.ENDC + ': ')
            if len(user_input) > 20 or ' ' in user_input:
                print('\n! Invalid nickname. Try again.\n')
                continue
            if self.nicknameIsTaken(user_input):
                print('\n! That nickname already exists. Try again\n')
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
        table_pad = 2
        col_w = 32
        table_w = col_w*2
        location = data['location_title'].split(',')
        city = location[0].title()
        state = location[1].upper()
        forecast_days = data['forecast']
        view = '\n'
        view += Colors.OKYELLOW + 'Long range forecast for ' + Colors.BOLD + city + ',' + state + Colors.ENDC + '\n\n'

        for i, day in enumerate(forecast_days):

            day_str = Colors.BOLD + day['day_of_week'] + Colors.ENDC
            if day['day_of_week'] == self.today_name:
                day_str += ' (' + Colors.OKYELLOW + 'TODAY' + Colors.ENDC + ')'

            am_color = Colors.WHITE
            pm_color = Colors.WHITE
            if 'FAIR' in day['am_conditions']:
                am_color = Colors.OKBLUE
            elif 'CHOPPY' in day['am_conditions']:
                am_color = Colors.RED
            elif 'CLEAN' in day['am_conditions']:
                am_color = Colors.OKGREEN
            if 'FAIR' in day['pm_conditions']:
                pm_color = Colors.OKBLUE
            elif 'CHOPPY' in day['pm_conditions']:
                pm_color = Colors.RED
            elif 'CLEAN' in day['pm_conditions']:
                pm_color = Colors.OKGREEN

            #print(self.breakDownLongText(day['conditions_long_text'], table_w))

            am_str = str(am_color + 'AM: ' +  day['am_height'] + Colors.ENDC).ljust(col_w)
            pm_str = str(pm_color + 'AM: ' +  day['pm_height'] + Colors.ENDC).ljust(col_w)

            view += ''.ljust(table_pad) + day_str + '\n'
            view += ''.ljust(table_pad) + am_str
            view += ''.ljust(table_pad) + pm_str
            view += '\n'
            if len(day['conditions_long_text']) > 4:
                for line in self.breakDownLongText(day['conditions_long_text'], table_w):
                    view += ''.ljust(table_pad) + line + '\n'
                view += '\n'
            if len(day['surf']) > 4:
                for line in self.breakDownLongText(day['surf'], table_w):
                    view += ''.ljust(table_pad) + line + '\n'
                view += '\n'


            view += '\n'
        return view


    def getSpotsNicknamesView(self):
        view = '\n'
        view += Colors.BOLD + 'Your Saved Spots' + Colors.ENDC + ':\n\n'

        no_spots = False
        try:
            if len(self.user_data['favorites']) == 0:
                no_spots = True
        except IndexError:
            no_spots = True

        if no_spots:
            view += '    -- None available --\n\n'
            return view

        for i, fav in enumerate(self.user_data['favorites']):
            view += '  ' + Colors.CYAN + Colors.BOLD + '{0: <20}'.format(fav['nickname']) + Colors.ENDC + ' (' + str(i) + ' - ' + fav['title'] + ')\n'
        view += '\n'
        view += '  * Use these nicknames or indexes as a command line argument to quickly retrieve the surf report.\n'
        return view


    def getHelpView(self):
        table_pad = 2
        col_pad = 20
        view = '\n'
        view += Colors.BOLD + 'MANUAL:' + Colors.ENDC + '\n\n'
        view += ''.ljust(table_pad) + Colors.UNDERLINE + Colors.OKYELLOW + 'COMMANDS:' + Colors.ENDC + '\n'
        view += ''.ljust(table_pad) + Colors.BOLD + '[no argument]'.ljust(col_pad) + Colors.ENDC + \
            '- Prompts user to select a location and by default will display \n' + ''.ljust(col_pad+4) + 'the current conditions (unless other flags are specified).\n'
        view += ''.ljust(table_pad) + Colors.BOLD + '[nickname]'.ljust(col_pad) + Colors.ENDC + \
            '- Will display either the current conditions, forecast, or both \n' + ''.ljust(col_pad+4) + '(depending on specified flags) for the given nickname.\n'
        view += ''.ljust(table_pad) + Colors.BOLD + 'spots'.ljust(col_pad) + Colors.ENDC + \
            '- Displays users saved spots by nickname.\n'
        view += ''.ljust(table_pad) + Colors.BOLD + 'add'.ljust(col_pad) + Colors.ENDC + \
            '- Prompts user to add/save a new spot to user data store.\n'
        view += ''.ljust(table_pad) + Colors.BOLD + 'remove [nickname]'.ljust(col_pad) + Colors.ENDC + \
            '- Removes saved spot from user data store if [nickname] is a \n' + ''.ljust(col_pad+4) + 'valid nickname or spot index.\n'
        view += ''.ljust(table_pad) + Colors.BOLD + 'reset'.ljust(col_pad) + Colors.ENDC + \
            '- Resets user data store to original state.\n\n'
        view += ''.ljust(table_pad) + Colors.UNDERLINE + Colors.OKYELLOW + 'FLAGS:' + Colors.ENDC + '\n'
        view += ''.ljust(table_pad) + Colors.BOLD + '-c'.ljust(col_pad) + Colors.ENDC + \
            '- Current conditions\n'
        view += ''.ljust(table_pad) + Colors.BOLD + '-f'.ljust(col_pad) + Colors.ENDC + \
            '- Forecast\n'
        view += ''.ljust(table_pad) + Colors.BOLD + '-h, --help'.ljust(col_pad) + Colors.ENDC + '- Displays manual\n'
        view += '\n'
        view += ''.ljust(table_pad) + Colors.BOLD + "*" + Colors.ENDC + " '-h' and '--help' are only interpreted if used exclusively.\n"
        view += ''.ljust(table_pad) + Colors.BOLD + "*" + Colors.ENDC + " Other flags can be used in combination i.e. -fc, -cf.\n\n"
        return view


    def breakDownLongText(self, text, chunk_size):
        if len(text) == 0:
            return []
        elif len(text) <= chunk_size:
            return [text]
        s = text.split(' ')
        line = ''
        text_chunks = []
        for  i, word in enumerate(s):
            redo = True
            while redo:
                if (len(line) + len(word) + len(' ')) < chunk_size:
                    line += str(word + ' ')
                    redo = False
                else:
                    text_chunks.append(line)
                    line = ''
                if i == len(s)-1:
                    text_chunks.append(line)
        return text_chunks


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
