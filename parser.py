# @Author: Joe Iannone <josephiannone>
# @Date:   2019-01-25T17:25:40-05:00
# @Filename: parser.py
# @Last modified by:   josephiannone
# @Last modified time: 2019-01-25T22:26:21-05:00

class swellParser():

    def __init__(self, html):
        self.html = html

    def getCurrentConditions(self):

        current_buoy = self.html.find("div", {'class': 'wx-icon-buoy-data'})
        current_tide = self.html.find("div", {'class': 'wx-icon-tide-data'}).find_all('div', attrs={'class': None})
        current_water = self.html.find("div", {'class': 'wx-icon-water-data'})

        current = {}
        current['location_title'] = self.html.find('h1', {'class': 'fcst-loc-name-label'}).text.strip()
        current['air'] = self.html.find("div", {'class': 'wx-icon-temp'}).string.strip()
        current['wind'] = self.html.find("div", {'class': 'wx-icons-wind-desc'}).string.strip()
        current['buoy_name'] = current_buoy.find('div', {'class': 'wx-icon-buoy-name'}).string.strip()
        current['wave_height'] = current_buoy.find(attrs={'class': None}).string.strip()
        current['low_tide'] = current_tide[0].getText()[3:]
        current['high_tide'] = current_tide[1].getText()[4:]
        current['water_temp'] = current_water.find('div', attrs={'class': None}).text.strip()
        current['wetsuit'] = current_water.find('div', {'class': 'wx-icon-wetsuit'}).text.strip()

        return current

    def getForecast(self):

        forecast_days = self.html.find_all('li', {'class': 'fcst-day'})

        forecast = []
        for day in forecast_days:
            forecast_height_cond_am = day.find('div', {'class': 'fcst-day-am'})
            forecast_height_cond_pm = day.find('div', {'class': 'fcst-day-pm'})
            forecast_day_tide_am = day.find('div', {'class': 'fcst-day-tide-am'})
            forecast_day_tide_pm = day.find('div', {'class': 'fcst-day-tide-pm'})
            day_dict = {}
            day_dict['day_of_week'] = day.find("div", {'class': 'fcst-day-summary-name'}).text.strip()
            day_dict['am_height'] = forecast_height_cond_am.find('div', {'class': 'fcst-day-wvht'}).text.strip()
            day_dict['am_conditions'] = forecast_height_cond_am.find('div', {'class': 'fcst-day-cond'}).text.strip()
            day_dict['pm_height'] = forecast_height_cond_pm.find('div', {'class': 'fcst-day-wvht'}).text.strip()
            day_dict['pm_conditions'] = forecast_height_cond_pm.find('div', {'class': 'fcst-day-cond'}).text.strip()
            day_dict['surf'] = day.find('div', {'class': 'fcst-day-surf-text'}).text.strip()
            day_dict['conditions_long_text'] = day.find('div', {'class': 'fcst-day-cond-text'}).text.strip()
            day_dict['am_low'] = forecast_day_tide_am.find('div', {'class': 'fcst-day-tide-low'}).find('span', {'class': 'fcst-tide-lowhigh-data'}).text.strip()
            day_dict['am_high'] = forecast_day_tide_am.find('div', {'class': 'fcst-day-tide-high'}).find('span', {'class': 'fcst-tide-lowhigh-data'}).text.strip()
            day_dict['sunrise'] = forecast_day_tide_am.find('div', {'class': 'fcst-day-sunrise'}).find('span', {'class': 'fcst-tide-lowhigh-data'}).text.strip()
            day_dict['pm_low'] = forecast_day_tide_pm.find('div', {'class': 'fcst-day-tide-low'}).find('span', {'class': 'fcst-tide-lowhigh-data'}).text.strip()
            day_dict['pm_high'] = forecast_day_tide_pm.find('div', {'class': 'fcst-day-tide-high'}).find('span', {'class': 'fcst-tide-lowhigh-data'}).text.strip()
            day_dict['sunset'] = forecast_day_tide_pm.find('div', {'class': 'fcst-day-sunset'}).find('span', {'class': 'fcst-tide-lowhigh-data'}).text.strip()

            hourly_title = day.find_all('div', {'class': 'fcst-day-hourly-time'})
            hourly_wind = day.find_all('div', {'class': 'fcst-day-hourly-wind'})
            hourly_swell = day.find_all('div', {'class': 'fcst-day-hourly-swell'})
            hourly_weather = day.find_all('div', {'class': 'fcst-day-hourly-wx-text'})

            day_dict['hourly_title'] = []
            day_dict['hourly_wind'] = []
            day_dict['hourly_swell'] = []
            day_dict['hourly_weather'] = []
            for i, title in enumerate(hourly_title):
                day_dict['hourly_title'].append(title.string.strip())
                try:
                    day_dict['hourly_wind'].append(hourly_wind[i].find('div', attrs={'class': None}).text.strip())
                except IndexError:
                    day_dict['hourly_wind'].append('')
                try:
                    day_dict['hourly_swell'].append(hourly_swell[i].find_all('span', {'class': 'hourly-swell-data'})[0].text.strip())
                except IndexError:
                    day_dict['hourly_swell'].append('')
                try:
                    day_dict['hourly_weather'].append(hourly_weather[i].text.strip())
                except IndexError:
                    day_dict['hourly_weather'].append('')

            forecast.append(day_dict)

        return forecast
