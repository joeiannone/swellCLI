# @Author: Joe Iannone
# @Date:   2019-01-22T21:27:47-05:00
# @Filename: client.py
# @Last modified by:   josephiannone
# @Last modified time: 2019-01-25T22:21:05-05:00

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

    def getSwellHTML(self, localArea):
        resp = self.request_handler.http_get(Client.local_url + localArea)
        return resp
