import sys

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

    def __init__(self):
        pass

    def getRegions():
        pass

    def getSubAreas(region):
        pass

    def getLocalData(subArea):
        pass
