# @Author: Joe Iannone
# @Date:   2019-01-24T17:44:41-05:00
# @Filename: request.py
# @Last modified by:   josephiannone
# @Last modified time: 2019-01-25T22:21:02-05:00

from requests import get
from requests.exceptions import RequestException
from contextlib import closing

class RequestHandler():

    # A class for handling http requests in a general context

    def http_get(self, url):
        # http 'GET'
        try:
            with closing(get(url, stream=True)) as resp:
                if self.is_good_response(resp):
                    return resp.content
                else:
                    return None

        except RequestException as e:
            self.log_error('Error during requests to {0} : {1}'.format(url, str(e)))
            return None


    def is_good_response(self, resp):
        # Validate response code as successfull
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200 and content_type is not None)

    def log_error(self, e):
        print(e)
