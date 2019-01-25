# @Author: Joe Iannone
# @Date:   2019-01-22T21:27:47-05:00
# @Filename: client.py
# @Last modified by:   Joe Iannone
# @Last modified time: 2019-01-24T22:36:24-05:00

from bs4 import BeautifulSoup

class Client:

    regions = [
    {'ref': 'usa', 'display': 'United States'},
    {'ref': 'mex', 'display': 'Mexico'},
    {'ref': 'cenam', 'display': 'Central America'},
    {'ref': 'carib', 'display': 'Caribbean'}
    ]
    root = 'http://swellinfo.com'
    region_url = root + '/jsmenus_json.php?js_region='
    sub_area_url = root + '/jsmenus_json.php?sub_area='
    local_url = root + '/surf-forecast/'

    def __init__(self, request_handler):
        self.request_handler = request_handler

    def getSubAreas(self, region):
        resp = self.request_handler.http_get(Client.region_url + region)
        return resp

    def getLocalAreas(self, subArea):
        resp = self.request_handler.http_get(Client.sub_area_url + subArea)
        return resp

    def getLocalData(self, localArea):
        resp = self.request_handler.http_get(Client.local_url + localArea)
        return resp

    def getCurrentConditions(self, localArea):
        resp = self.getLocalData(localArea)
        html = BeautifulSoup(resp, 'html.parser')

        current = html.find_all("ul", {'class': 'wx-icons'})
        current_buoy = html.find("div", {'class': 'wx-icon-buoy-data'})
        current_tide = html.find("div", {'class': 'wx-icon-tide-data'}).find_all('div', attrs={'class': None})
        current_water = html.find("div", {'class': 'wx-icon-water-data'})

        current_dict = {}
        current_dict['location_title'] = html.find('h1', {'class': 'fcst-loc-name-label'}).text
        current_dict['air'] = html.find("div", {'class': 'wx-icon-temp'}).string
        current_dict['wind'] = html.find("div", {'class': 'wx-icons-wind-desc'}).string
        current_dict['buoy_name'] = current_buoy.find('div', {'class': 'wx-icon-buoy-name'}).string
        current_dict['wave_height'] = current_buoy.find(attrs={'class': None}).string
        current_dict['low_tide'] = current_tide[0].getText()[3:]
        current_dict['high_tide'] = current_tide[1].getText()[4:]
        current_dict['water_temp'] = current_water.find('div', attrs={'class': None}).text
        current_dict['wetsuit'] = current_water.find('div', {'class': 'wx-icon-wetsuit'}).text

        return current_dict

    def getForecast(self, localArea):
        resp = self.getLocalData(localArea)
        html = BeautifulSoup(resp, 'html.parser')

        forecast_days = html.find_all('li', {'class': 'fcst-day'})

        forecast = []
        for day in forecast_days:
            forecast_height_cond_am = day.find('div', {'class': 'fcst-day-am'})
            forecast_height_cond_pm = day.find('div', {'class': 'fcst-day-pm'})
            forecast_day_tide_am = day.find('div', {'class': 'fcst-day-tide-am'})
            forecast_day_tide_pm = day.find('div', {'class': 'fcst-day-tide-pm'})
            day_dict = {}
            day_dict['day_of_week'] = day.find("div", {'class': 'fcst-day-summary-name'}).text
            day_dict['am_height'] = forecast_height_cond_am.find('div', {'class': 'fcst-day-wvht'}).text
            day_dict['am_conditions'] = forecast_height_cond_am.find('div', {'class': 'fcst-day-cond'}).text
            day_dict['pm_height'] = forecast_height_cond_pm.find('div', {'class': 'fcst-day-wvht'}).text
            day_dict['pm_conditions'] = forecast_height_cond_pm.find('div', {'class': 'fcst-day-cond'}).text
            day_dict['surf'] = day.find('div', {'class': 'fcst-day-surf-text'}).text
            day_dict['conditions_long_text'] = day.find('div', {'class': 'fcst-day-cond-text'}).text
            day_dict['am_low'] = forecast_day_tide_am.find('div', {'class': 'fcst-day-tide-low'}).find('span', {'class': 'fcst-tide-lowhigh-data'}).text
            day_dict['am_high'] = forecast_day_tide_am.find('div', {'class': 'fcst-day-tide-high'}).find('span', {'class': 'fcst-tide-lowhigh-data'}).text
            day_dict['sunrise'] = forecast_day_tide_am.find('div', {'class': 'fcst-day-sunrise'}).find('span', {'class': 'fcst-tide-lowhigh-data'}).text
            day_dict['pm_low'] = forecast_day_tide_pm.find('div', {'class': 'fcst-day-tide-low'}).find('span', {'class': 'fcst-tide-lowhigh-data'}).text
            day_dict['pm_high'] = forecast_day_tide_pm.find('div', {'class': 'fcst-day-tide-high'}).find('span', {'class': 'fcst-tide-lowhigh-data'}).text
            day_dict['sunset'] = forecast_day_tide_pm.find('div', {'class': 'fcst-day-sunset'}).find('span', {'class': 'fcst-tide-lowhigh-data'}).text

            forecast.append(day_dict)

        return forecast
