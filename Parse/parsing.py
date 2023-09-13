# Scripts
from Parse.parse_context import PARSE_CONTEXT
from Parse.log_parsing import LOG_PARSING
from Parse.lists_handle import *
from Parse.ebay_parsing import EBAY_PARSING
from Parse.wg_gesucht_parsing import WGGESUCHT_PARSING
from Parse.immoscout_parsing import IMMOSCOUT_PARSING

DEBUG = False
LOG = True

if DEBUG:
    import json
    import logging
    import socket
    from logging.handlers import SysLogHandler


class PARSER:
    def __init__(self, parseData, logger):
        self.context = PARSE_CONTEXT()
        self.parseData = parseData
        self.logger = LOG_PARSING(logger)
        self.ebay_parser = EBAY_PARSING(context=self.context, f_logger=self.logger, parse_data=self.parseData, if_log=LOG)
        self.wg_parser = WGGESUCHT_PARSING(context=self.context, f_logger=self.logger, parse_data=self.parseData, if_log=LOG)
        self.immoscout_parser = IMMOSCOUT_PARSING(context=self.context, f_logger=self.logger, parse_data=self.parseData, if_log=LOG)

    def get_list(self, site, location, swap):
        if LOG:
            self.logger.getting_parsed_data()

        diff_items = []
        if site == "ebay":
            diff_items = self.ebay_parser.get_list(swap, location)
        elif site == "wggesucht":
            diff_items = self.wg_parser.get_list(location)
        elif site == "all":
            diff_items = self.wg_parser.get_list(location)
            diff_items.extend(self.ebay_parser.get_list(swap, location))

        if LOG:
            self.logger.log_list(log_list=diff_items, text="Final diff list:")

        return diff_items

    def make(self, site="all", location="", priceOt="", priceDo="", swap=2):
        if LOG:
            self.logger.log("Start parsing...")

        if site == "all":
            self.ebay_parser.parse(location, priceOt, priceDo, str(swap))
            self.wg_parser.parse(location, priceDo, str(swap))
        elif site == "ebay":
            self.ebay_parser.parse(location, priceOt, priceDo, str(swap))
        elif site == "immoscout":
            self.immoscout_parser.parse(location, priceOt, priceDo)
        elif site == "wggesucht":
            self.wg_parser.parse(location, priceDo, str(swap))


if DEBUG:
    class ContextFilter(logging.Filter):
        hostname = socket.gethostname()

        def filter(self, record):
            record.hostname = ContextFilter.hostname
            return True

    def loggerInit():
        syslog = SysLogHandler(address=('logs6.papertrailapp.com', 52605))
        syslog.addFilter(ContextFilter())
        format = '%(asctime)s %(hostname)s LOG: %(message)s'
        formatter = logging.Formatter(format, datefmt='%b %d %H:%M:%S')
        syslog.setFormatter(formatter)
        logger = logging.getLogger()
        logger.addHandler(syslog)
        logger.setLevel(logging.INFO)

        return logger

    with open('../config_parse.json') as file:
        parseData = json.load(file)

    logger = loggerInit()
    request = PARSER(parseData, logger)
    site = "wggesucht"
    location = "Berlin"
    swap = 2

    # request.make(site=site, location=location, priceDo=1500, swap=swap)
    request.make(site=site, location=location, priceOt=10, priceDo=1500, swap=swap)  # Wg gesucht - 10k geht nicht
    a = request.get_list(site=site, location=location, swap=swap)
    for item in a:
        print("ITEM")
        print("img:" + item.img)
        print("url:" + item.url)
        print("price:" + item.price)
        print("address:" + item.address)

    print("-------------------------")
    request.make(site=site, location=location, priceOt= 10, priceDo=1500, swap=swap)  # Wg gesucht - 10k geht nicht
    b = request.get_list(site=site, location=location, swap=swap)
    for item in b:
        print("ITEM")
        print("img:" + item.img)
        print("url:" + item.url)
        print("price:" + item.price)
