from math import inf


def is_int(string):
    try:
        int(string)
        return True
    except:
        return False


def is_float(value):
    try:
        float(value)
        return True
    except:
        return False


def extract_float_from_string(string):
    string = string.replace(',', '.')
    string = string.replace('(', '')
    string = string.replace(')', '')
    array = string.split(' ')
    for element in array:
        if is_float(element):
            return float(element)
    return -inf


class Beer:
    brand = "brand"
    name = "name"
    has_offer = "has_offer"
    alc_percent = "alc_percent"
    bottles = "bottles"
    bottle_size = "bottle_size"
    price = "price"
    ppl = "ppl"

    def __init__(self, brand, name, has_offer, alc_percent, bottle_info, price, ppl):
        self.brand = brand
        self.name = name
        self.has_offer = True if has_offer.lower() == "true" else False
        self.alc_percent = extract_float_from_string(alc_percent)
        # parse bottle info, usually provided as "00 x 0.00L (Glas)"
        bottle_info = bottle_info.replace(",", ".")
        bottle_info = bottle_info.replace("L", "")
        bottle_info = bottle_info.replace("l", "")
        bottle_info = bottle_info.replace("ML", "")
        bottle_info = bottle_info.replace("ml", "")
        arr = bottle_info.split(" x ")
        if len(arr) > 2:
            self.bottles = 1
            for i in range(len(arr)-1):
                self.bottles *= int(arr[i])
        else:
            if is_int(arr[0]):
                self.bottles = int(arr[0])
        if is_float(len(arr)):
            self.bottle_size = float(len(arr))

        # parse price, usually provided as "00,00 €"
        price = price.replace("€", "")
        price = extract_float_from_string(price)

        self.price = price
        self.ppl = extract_float_from_string(ppl)

    def print(self):
        print(self.brand, self.name, self.has_offer, self.alc_percent, self.bottles, self.bottle_size, self.price,
              self.ppl)

    def print_fancy(self):
        print("brand: ", self.brand)
        print("\tname:\t\t\t", self.name)
        print("\thas_offer:\t\t", self.has_offer)
        print("\talc_percent:\t", self.alc_percent, "%")
        print("\tbottles:\t\t", self.bottles)
        print("\tbottle_size:\t", self.bottle_size, "L")
        print("\tprice:\t\t\t", self.price, "€")
        print("\tppl:\t\t\t", self.ppl, "€/L")

    def __cmp__(self, other):
        return self.ppl > other.ppl
