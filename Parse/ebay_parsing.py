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

    def get_last_list(self, swap, location):
        if swap == 0:
            if self.context.ebay.ebay_lists_nosw[location]:
                return self.context.ebay.ebay_lists_nosw[location]
            elif self.context.ebay.ebay_lists_old_nosw[location]:
                return self.context.ebay.ebay_lists_old_nosw[location]
            return []
        elif swap == 1:
            if self.context.ebay.ebay_lists[location]:
                return self.context.ebay.ebay_lists[location]
            elif self.context.ebay.ebay_lists_old[location]:
                return self.context.ebay.ebay_lists_old[location]
            return []
        elif swap == 2:
            if self.context.ebay.ebay_lists_both[location]:
                return self.context.ebay.ebay_lists_both[location]
            elif self.context.ebay.ebay_lists_old_both[location]:
                return self.context.ebay.ebay_lists_old_both[location]
            else:
                return []
        else:
            return []

    def parse(self, location, priceOt, priceDo, swap):
        url = self.create_url(location, priceOt, priceDo, swap)
        page = proxy_request(url=url, antiblock=False)
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
        # soup = BeautifulSoup(page.text, 'lxml')
        soup = BeautifulSoup(page.text, 'html.parser')

        for item in soup.select('li.ad-listitem:not(.badge-topad)'):
        # for item in soup.findAll('li', {'class': 'ad-listitem'}, class_=lambda x: x != 'badge-topad'):
            parsed_list.append(item)

        for item in parsed_list[:5]:
            try:
                item_url = "https://kleinanzeigen.de"  # JSON

                item_url += item.find("a", href=True)["href"]
                price = item.find("p", {"class": "aditem-main--middle--price-shipping--price"}).text.strip()
                address = item.find("div", {"class": "aditem-main--top--left"}).text.strip()
                description = item.find("a", {"class": "ellipsis"}).text.strip()

                # if item.find("div", {"class": "is-nopic"}):

                # try:
                #     sample = item.find("div")["is-nopic"]
                #     img = "https://img.freepik.com/premium-vector/no-photo-available-vector-icon-default-image-symbol-picture-coming-soon-web-site-mobile-app_87543-10615.jpg?w=2000"
                # except Exception:
                #     img = item.find("div", {"class": "imagebox srpimagebox"}).find("img")["srcset"]  # ["data-imgsrcretina"].split()[0]


                try:
                    image = soup.find('div', class_='imagebox srpimagebox')
                    if 'is-nopic' in image.get('class'):
                        img = "https://img.freepik.com/premium-vector/no-photo-available-vector-icon-default-image-symbol-picture-coming-soon-web-site-mobile-app_87543-10615.jpg?w=2000"
                    else:
                        img = item.find("div", {"class": "imagebox srpimagebox"}).find("img")["srcset"]
                except Exception:
                    img = "https://img.freepik.com/premium-vector/no-photo-available-vector-icon-default-image-symbol-picture-coming-soon-web-site-mobile-app_87543-10615.jpg?w=2000"
                    self.f_logger.log("Ebay::Error: Exception during the IMAGE Parsing")

                item_data = ITEM(url=item_url, price=price.split()[0], address=address, description=description,
                                 img=img)

                items_list.append(item_data)


            except Exception:
                self.f_logger.log("Ebay::Error: Exception during the ITEM Parsing")

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
