
class LOG_PARSING:
    def __init__(self, logger):
        self.logger = logger

    def log(self, text):
        self.logger.info(f"\n {text} \n")

    # PASS A LIST AS A PARAMETR
    # def print_list(self):
    #     for item in self.itemsList:
    #         print(item.price, item.url)

    def log_list(self, log_list, text=""):
        self.logger.info("--")

        if len(text) != 0:
            self.logger.info(text)

        for item in log_list:
            string = "      " + item.price + ", " + item.address
            self.logger.info(string)
            self.logger.info(item.url)
            self.logger.info("foto: " + item.img)
            self.logger.info("-")

    def getting_parsed_data(self):
        self.logger.info("#")
        self.logger.info("#")
        self.logger.info("#")
        self.logger.info("getting parsed data...")