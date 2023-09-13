from bs4 import BeautifulSoup
from Parse.proxy_request import proxy_request
from Parse.item import ITEM
from Parse.lists_handle import *


class WGGESUCHT_PARSING:
    def __init__(self, context, f_logger, parse_data, if_log=False):
        self.context = context
        self.f_logger = f_logger
        self.parse_data = parse_data
        self.if_log = if_log

    def get_data(self, site, partName):
        return self.parse_data[site][partName]

    def get_list(self, location):
        self.f_logger.log_list(log_list=self.context.wg.wg_lists_old[location],
                               text=f"WgGesucht::Old list({location}):")
        self.f_logger.log_list(log_list=self.context.wg.wg_lists[location],
                               text=f"WgGesucht::New list({location}):")

        diff_items = diff_list(self.context.wg.wg_lists_old[location],
                               self.context.wg.wg_lists[location])
        return diff_items

    def parse(self, location, priceDo, swap):
        url = self.create_url(location=location, priceDo=priceDo, swap=swap)
        page = proxy_request(url=url)

        if self.if_log:
            self.f_logger.log("WgGesucht::URL: " + url)
            self.f_logger.log("WgGesucht::Request code: " + str(page.status_code))

        if page.status_code == 200:
            self.get_items_in_list(page=page, location=location)
        else:
            if self.if_log:
                self.f_logger.log("WgGesucht::Error while parsing")
                self.f_logger.log(BeautifulSoup(page.text, "html.parser").text)

    def create_url(self, location, priceDo=100000, swap=2):
        url = self.get_data('wg', 'base_url') + "/1-zimmer-wohnungen-und-wohnungen-und-haeuser-in-"
        url += self.get_data('wg', 'city_start')[location]
        url += "+3.1.0.html?csrf_token=&offer_filter=1"  # 1 Room Flat + Flats
        url += self.get_data('wg', 'city_end')[location]
        url += "&sort_column=0&noDeact=1&categories%5B%5D=1&categories%5B%5D=2&rent_types%5B%5D=2&rMax="
        url += str(priceDo)
        url += self.get_data('wg', 'swap')[swap]

        return url

    def get_items_in_list(self, page, location):
        parsed_list = []
        items_list = []
        html = page.text
        soup = BeautifulSoup(html, 'lxml')

        for item in soup.findAll("div", {"class": "wgg_card offer_list_item"}):
            parsed_list.append(item)

        for item in parsed_list[:5]:
            try:
                item_url = self.get_data('wg', 'base_url') + item.find("a", href=True)["href"]
                price = item.find("div", {"class": "col-xs-3"}).find("b").text.strip()

                address = item.find("div", {"class": "col-xs-11"}).find("span").text
                index1 = address.find("|") + 1
                address = address[index1:]
                index2 = address.find("|") + 1
                street = address[index2:].strip()
                bezirk = str(address.split("|")[0]).strip()
                bezirk = ' '.join(bezirk.split())
                address = street + ", " + bezirk

                description = item.find("a", {"class": "detailansicht"}).find("b").text
                img = item.find("a")["style"][22:-2]

                item_data = ITEM(item_url, price.split()[0], address=address, description=description, img=img)
                items_list.append(item_data)
            except Exception:
                self.f_logger.log("WgGesucht::Error: Exception during the ITEM Parsing")
                pass

        self.f_logger.log_list(log_list=items_list, text="WgGesucht::Parsed list: ")

        if items_list:
            self.context.wg.wg_lists_old[location] = self.context.wg.wg_lists[location]
            self.context.wg.wg_lists[location] = items_list
        else:
            self.f_logger.log("WgGesucht::Error: Parsed list is empty")
            self.context.wg.wg_lists_old[location] = self.context.wg.wg_lists[location]
