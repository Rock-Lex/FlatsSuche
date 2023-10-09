class ITEM:
    def __init__(self, url="", price="", address="-", description="-", img="-"):
        price = str(price).replace(".", "")
        self.url = url
        self.price = price
        self.address = address
        self.description = description
        self.img = img