from bs4 import BeautifulSoup
from Parse.proxy_request import proxy_request
from Parse.item import ITEM
from Parse.lists_handle import *


class EBAY_PARSING:
    def __init__(self, context, f_logger, parse_data, if_log=False):
        self.context = context
        self.f_logger = f_logger
        self.parse_data = parse_data
        self.if_log = if_log

    def get_data(self, site, partName):
        return self.parse_data[site][partName]

    def parse(self, location, priceOt, priceDo, swap):
        url = self.create_url(location, priceOt, priceDo, swap)
        page = proxy_request(url=url)
        # print(page.text)

        if self.if_log:
            self.f_logger.log("Ebay::URL: " + url)
            self.f_logger.log("Ebay::Request code: " + str(page.status_code))

        if page.status_code == 200:
            self.get_items_in_list(page=page, location=location, swap=swap)
        else:
            if self.if_log:
                self.f_logger.log("Ebay::Error while parsing")
                self.f_logger.log(BeautifulSoup(page.text, "html.parser").text)

    def get_list(self, swap, location):
        if swap == 0:
            self.f_logger.log_list(log_list=self.context.ebay.ebay_lists_old_nosw[location],
                                   text=f"Ebay::Old list(swap={swap}, {location}):")
            self.f_logger.log_list(log_list=self.context.ebay.ebay_lists_nosw[location],
                                   text=f"Ebay::New list(swap={swap}, {location}):")

            diff_items = diff_list(self.context.ebay.ebay_lists_old_nosw[location],
                                   self.context.ebay.ebay_lists_nosw[location])
            return diff_items
        elif swap == 1:
            self.f_logger.log_list(log_list=self.context.ebay.ebay_lists_old[location],
                                   text=f"Ebay::Old list(swap={swap}, {location}):")
            self.f_logger.log_list(log_list=self.context.ebay.ebay_lists[location],
                                   text=f"Ebay::New list(swap={swap}, {location}):")

            diff_items = diff_list(self.context.ebay.ebay_lists_old[location],
                                   self.context.ebay.ebay_lists[location])
            return diff_items
        elif swap == 2:
            self.f_logger.log_list(log_list=self.context.ebay.ebay_lists_old_both[location],
                                   text=f"Ebay::Old list(swap={swap}, {location}):")
            self.f_logger.log_list(log_list=self.context.ebay.ebay_lists_both[location],
                                   text=f"Ebay::New list(swap={swap}, {location}):")

            diff_items = diff_list(self.context.ebay.ebay_lists_old_both[location],
                                   self.context.ebay.ebay_lists_both[location])
            return diff_items
        else:
            self.f_logger.log("Ebay::Error: Wrong SWAP parameter in method parse.make()")
            return []

    def create_url(self, location, priceOt, priceDo, swap):
        url = self.get_data('ebay', 'base_url')

        if location != "":
            url += self.get_data('ebay', 'city_start')[location]

        url += self.get_data('ebay', 'price_base_url') + str(priceOt) + ":" + str(priceDo)

        if location != "":
            url += self.get_data('ebay', 'city_end')[location]
        else:
            url += "/c203"

        url += self.get_data('ebay', 'swap')[swap]

        return url

    def get_items_in_list(self, page, location, swap):
        parsed_list = []
        items_list = []
        soup = BeautifulSoup(page.text, 'lxml')

        for item in soup.select('li.ad-listitem:not(.badge-topad)'):
            parsed_list.append(item)

        for item in parsed_list[:5]:
            try:
                item_url = "https://kleinanzeigen.de"  # JSON

                item_url += item.find("a", href=True)["href"]
                price = item.find("p", {"class": "aditem-main--middle--price-shipping--price"}).text.strip()
                address = item.find("div", {"class": "aditem-main--top--left"}).text.strip()
                description = item.find("a", {"class": "ellipsis"}).text.strip()
                img = item.find("div", {"class": "imagebox srpimagebox"}).find("img")[
                    "srcset"]  # ["data-imgsrcretina"].split()[0]

                item_data = ITEM(url=item_url, price=price.split()[0], address=address, description=description,
                                 img=img)

                items_list.append(item_data)
            except Exception:
                pass

        self.f_logger.log_list(log_list=items_list, text="Ebay::Parsed list: ")

        if items_list:
            if swap == "0":
                self.context.ebay.ebay_lists_old_nosw[location] = self.context.ebay.ebay_lists_nosw[location]
                self.context.ebay.ebay_lists_nosw[location] = items_list
            elif swap == "1":
                self.context.ebay.ebay_lists_old[location] = self.context.ebay.ebay_lists[location]
                self.context.ebay.ebay_lists[location] = items_list
            elif swap == "2":
                self.context.ebay.ebay_lists_old_both[location] = self.context.ebay.ebay_lists_both[location]
                self.context.ebay.ebay_lists_both[location] = items_list
            else:
                self.f_logger.log("Ebay::Error: Wrong SWAP parameter in method parse.make()")
        else:
            self.f_logger.log("Ebay::Error: Parsed list is empty")
            if swap == "0":
                self.context.ebay.ebay_lists_old_nosw[location] = self.context.ebay.ebay_lists_nosw[location]
            elif swap == "1":
                self.context.ebay.ebay_lists_old[location] = self.context.ebay.ebay_lists[location]
            elif swap == "2":
                self.context.ebay.ebay_lists_old_both[location] = self.context.ebay.ebay_lists_both[location]
            else:
                self.f_logger.log("Ebay::Error: Wrong SWAP parameter in method parse.make()")
