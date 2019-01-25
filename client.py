# @Author: Joe Iannone
# @Date:   2019-01-22T21:27:47-05:00
# @Filename: client.py
# @Last modified by:   Joe Iannone
# @Last modified time: 2019-01-24T19:53:47-05:00


class Client:

    root = 'http://swellinfo.com'
    locations = root + '/surf-forecast'
    region_url = root + '/jsmenus_json.php?js_region='
    sub_area_url = root + '/jsmenus_json.php?sub_area='
    regions = [
    {'ref': 'usa', 'display': 'United States'},
    {'ref': 'mex', 'display': 'Mexico'},
    {'ref': 'cenam', 'display': 'Central America'},
    {'ref': 'carib', 'display': 'Caribbean'}
    ]
    local_url1 = root + '/surf-forecast/fetch-timeline-data/loc/wna_nj_capemay'
    local_url2 = root + '/surf-forecast/fetch-timeline-swell-data/loc/wna_nj_capemay'

    def __init__(self, request_handler):
        self.request_handler = request_handler

    def getSubAreas(self, region):
        resp = self.request_handler.http_get(Client.region_url + region)
        return resp

    def getLocalAreas(self, subArea):
        resp = self.request_handler.http_get(Client.sub_area_url + subArea)
        return resp
