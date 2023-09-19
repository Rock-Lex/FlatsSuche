from bs4 import BeautifulSoup
from Parse.proxy_request import proxy_request
from Parse.item import ITEM
from Parse.lists_handle import *


class IMMOSCOUT_PARSING:
    def __init__(self, context, f_logger, parse_data, if_log=False):
        self.context = context
        self.f_logger = f_logger
        self.parse_data = parse_data
        self.if_log = if_log

    def get_data(self, site, partName):
        return self.parse_data[site][partName]

    def parse(self, location, priceFrom, priceTo):
        url = self.create_url(location=location, priceFrom=priceFrom, priceTo=priceTo)
        page = proxy_request(url=url, antiblock=True)
        print(url)
        if self.if_log:
            self.f_logger.log("Immoscout::URL: " + url)
            self.f_logger.log("Immoscout::Request code: " + str(page.status_code))

        if page.status_code == 200:
            # self.get_items_in_list(page=page, location=location)
            print(page)
            pass
        else:
            print(BeautifulSoup(page.text, "html.parser").text)
            if self.if_log:
                self.f_logger.log("Immoscout::Error while parsing")
                self.f_logger.log(BeautifulSoup(page.text, "html.parser").text)

    def create_url(self, location, priceFrom=0, priceTo=100000):
        url = self.get_data('immoscout', 'base_url')
        url += self.get_data('immoscout', 'city_start')[location]
        url += self.get_data('immoscout', 'end_url')
        url = str(url).replace('PRICEFROM', str(priceFrom))
        url = url.replace('PRICETO', str(priceTo))

        return url


