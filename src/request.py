# @Author: Joe Iannone
# @Date:   2019-01-24T17:44:41-05:00
# @Filename: request.py
# @Last modified by:   josephiannone
# @Last modified time: 2019-01-25T22:21:02-05:00


from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from yaspin import yaspin, Spinner
from src.spinners import Spinners

class RequestHandler():

    # A class for handling http requests in a general context

    def http_get(self, url):
        # http 'GET'

        # set spinner
        if url.find('surf-forecast') is not -1:
            self.loader = yaspin(Spinner(Spinners.shark, 100)).white.bold.on_blue
        else:
            self.loader = yaspin(Spinner(Spinners.earth, 180))

        # start loader to anticipate a possible slow request
        self.loader.start()

        try:
            with closing(get(url, stream=True)) as resp:
                if self.is_good_response(resp):
                    self.loader.stop() # stop loader
                    return resp.content
                else:
                    self.loader.stop() # stop loader
                    return None

        except RequestException as e:
            self.log_error('Error during requests to {0} : {1}'.format(url, str(e)))
            self.loader.stop() # stop loader
            return None


    def is_good_response(self, resp):
        # Validate response code as successfull
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200 and content_type is not None)

    def log_error(self, e):
        print(e)
