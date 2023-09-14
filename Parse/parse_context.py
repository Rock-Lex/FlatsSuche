class EBAY:
    def __init__(self):
        self.ebay_lists = {
            "Berlin": [],
            "Hamburg": [],
            "Muenchen": [],
            "Frankfurt_main": [],
            "Hannover": [],
            "Leipzig": [],
            "Dresden": [],
            "Dortmund": [],
            "Koeln": [],
            "Duesseldorf": [],
            "Bremen": [],
            "Stuttgart": [],
            "Nuernberg": [],
            "Essen": [],
            "Bonn": [],
            "Kiel": [],
            "Rostock": []
        }
        self.ebay_lists_old = {
            "Berlin": [],
            "Hamburg": [],
            "Muenchen": [],
            "Frankfurt_main": [],
            "Hannover": [],
            "Leipzig": [],
            "Dresden": [],
            "Dortmund": [],
            "Koeln": [],
            "Duesseldorf": [],
            "Bremen": [],
            "Stuttgart": [],
            "Nuernberg": [],
            "Essen": [],
            "Bonn": [],
            "Kiel": [],
            "Rostock": []
        }
        self.ebay_lists_nosw = {
            "Berlin": [],
            "Hamburg": [],
            "Muenchen": [],
            "Frankfurt_main": [],
            "Hannover": [],
            "Leipzig": [],
            "Dresden": [],
            "Dortmund": [],
            "Koeln": [],
            "Duesseldorf": [],
            "Bremen": [],
            "Stuttgart": [],
            "Nuernberg": [],
            "Essen": [],
            "Bonn": [],
            "Kiel": [],
            "Rostock": []
        }
        self.ebay_lists_old_nosw = {
            "Berlin": [],
            "Hamburg": [],
            "Muenchen": [],
            "Frankfurt_main": [],
            "Hannover": [],
            "Leipzig": [],
            "Dresden": [],
            "Dortmund": [],
            "Koeln": [],
            "Duesseldorf": [],
            "Bremen": [],
            "Stuttgart": [],
            "Nuernberg": [],
            "Essen": [],
            "Bonn": [],
            "Kiel": [],
            "Rostock": []
        }
        self.ebay_lists_both = {
            "Berlin": [],
            "Hamburg": [],
            "Muenchen": [],
            "Frankfurt_main": [],
            "Hannover": [],
            "Leipzig": [],
            "Dresden": [],
            "Dortmund": [],
            "Koeln": [],
            "Duesseldorf": [],
            "Bremen": [],
            "Stuttgart": [],
            "Nuernberg": [],
            "Essen": [],
            "Bonn": [],
            "Kiel": [],
            "Rostock": []
        }
        self.ebay_lists_old_both = {
            "Berlin": [],
            "Hamburg": [],
            "Muenchen": [],
            "Frankfurt_main": [],
            "Hannover": [],
            "Leipzig": [],
            "Dresden": [],
            "Dortmund": [],
            "Koeln": [],
            "Duesseldorf": [],
            "Bremen": [],
            "Stuttgart": [],
            "Nuernberg": [],
            "Essen": [],
            "Bonn": [],
            "Kiel": [],
            "Rostock": []
        }


class WG:
    def __init__(self):
        self.wg_base_url = "https://www.wg-gesucht.de"
        self.wg_swap = {
            -1: "",
            0: "&exc=2",
            1: "&exc=1"
        }
        self.wg_lists = {
            "Berlin": [],
            "Hamburg": [],
            "Muenchen": [],
            "Frankfurt_main": [],
            "Hannover": [],
            "Leipzig": [],
            "Dresden": [],
            "Dortmund": [],
            "Koeln": [],
            "Duesseldorf": [],
            "Bremen": [],
            "Stuttgart": [],
            "Nuernberg": [],
            "Essen": [],
            "Bonn": [],
            "Kiel": [],
            "Rostock": []
        }
        self.wg_lists_old = {
            "Berlin": [],
            "Hamburg": [],
            "Muenchen": [],
            "Frankfurt_main": [],
            "Hannover": [],
            "Leipzig": [],
            "Dresden": [],
            "Dortmund": [],
            "Koeln": [],
            "Duesseldorf": [],
            "Bremen": [],
            "Stuttgart": [],
            "Nuernberg": [],
            "Essen": [],
            "Bonn": [],
            "Kiel": [],
            "Rostock": []
        }

class PARSE_CONTEXT:
    def __init__(self):
        self.locations = [
            "Berlin",
            "Hamburg",
            "Muenchen",
            "Frankfurt_main",
            "Hannover",
            "Leipzig",
            "Dresden",
            "Dortmund",
            "Koeln",
            "Duesseldorf",
            "Bremen",
            "Stuttgart",
            "Nuernberg",
            "Essen",
            "Bonn",
            "Kiel",
            "Rostock"
        ]
        self.ebay = EBAY()
        self.wg = WG()
