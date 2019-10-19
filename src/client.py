# @Author: Joe Iannone
# @Date:   2019-01-22T21:27:47-05:00
# @Filename: client.py
# @Last modified by:   josephiannone
# @Last modified time: 2019-01-27T22:34:51-05:00

class Client:

    # This class acts as an HTTP interface for the swellinfo website

    # Some static swellinfo.com url parts
    regions = {
    'usa': {'label': 'United States'},
    'mex': {'label': 'Mexico'},
    'cenam': {'label': 'Central America'},
    'carib': {'label': 'Caribbean'},
    }
    root = 'http://swellinfo.com'
    region_url = root + '/jsmenus_json.php?js_region='
    sub_area_url = root + '/jsmenus_json.php?sub_area='
    local_url = root + '/surf-forecast/'

    def __init__(self, request_handler):
        self.request_handler = request_handler

    def getSubAreas(self, region):
        # request/retrieve swellinfo 'Sub areas'
        resp = self.request_handler.http_get(Client.region_url + region)
        return resp

    def getLocalAreas(self, subArea):
        # request/retrieve swellinfo 'Local areas'
        resp = self.request_handler.http_get(Client.sub_area_url + subArea)
        return resp

    def getSwellHTML(self, localArea):
        # request/retrieve swellinfo html of 'Local area' page
        resp = self.request_handler.http_get(Client.local_url + localArea)
        return resp
