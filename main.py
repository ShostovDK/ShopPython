import json
import xml.etree.ElementTree as ET

class Product:
    def __init__(self, name, price):
        self._name = name
        self._price = price

    def get_info(self):
        return f"Product name: {self._name}"

    def to_dict(self):
        return {
            "name": self._name,
            "price": self._price,
            "type": "product"
        }

    def to_xml(self):
        product_element = ET.Element("Product")
        name_element = ET.SubElement(product_element, "Name")
        name_element.text = self._name
        return product_element


class Service(Product):
    def __init__(self, name, duration, price):
        super().__init__(name, price)
        self.duration = duration

    def get_info(self):
        return f"Service name: {self._name},\nDuration: {self.duration}, \nPrice: {self._price}\n"

    def to_dict(self):
        return {
            "name": self._name,
            "duration": self.duration,
            "price": self._price,
            "type": "service"
        }

    def to_xml(self):
        service_element = ET.Element("Service")
        name_element = ET.SubElement(service_element, "Name")
        name_element.text = self._name
        duration_element = ET.SubElement(service_element, "Duration")
        duration_element.text = self.duration
        price_element = ET.SubElement(service_element, "Price")
        price_element.text = str(self._price)
        return service_element


class Item(Product):
    def __init__(self, name, price):
        super().__init__(name, price)

    def get_info(self):
        return f"Item name: {self._name}, \nPrice: {self._price}\n"

    def to_dict(self):
        return {
            "name": self._name,
            "price": self._price,
            "type": "item"
        }

    def to_xml(self):
        item_element = ET.Element("Item")
        name_element = ET.SubElement(item_element, "Name")
        name_element.text = self._name
        price_element = ET.SubElement(item_element, "Price")
        price_element.text = str(self._price)
        return item_element


class Basket:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product):
        self.products.remove(product)

    def get_total_price(self):
        total_price = 0
        for product in self.products:
            try:
                if type(product._price) == str:
                    raise ValueError
                else:
                    total_price += product._price
            except ValueError:
                print("It's over...")
                quit()
        try:
            if total_price > 0:
                return f"Your total price will be: {total_price}"
            else:
                raise Low
        except Low:
            return "Your basket is empty"



    def to_dict(self):
        product_list = [product.to_dict() for product in self.products]
        return {
            "products": product_list
        }

    def save_to_file(self, filename):
        bask_data = self.to_dict()
        with open(filename, "w") as file:
            json.dump(bask_data, file)

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, "r") as file:
            bask_data = json.load(file)

        wow = Basket()
        for item_data in bask_data["products"]:
            if item_data["type"] == "service":
                wow.add_product(Service(item_data["name"], item_data["duration"], item_data["price"]))
            elif item_data["type"] == "item":
                wow.add_product(Item(item_data["name"], item_data["price"]))

        return wow

    def to_xml(self):
        bask_element = ET.Element("Cart")
        for product in self.products:
            product_element = product.to_xml()
            bask_element.append(product_element)
        return bask_element


class Low(Exception):
    pass




service = Service("Cleaning", "1 hour", 5)
print(service.get_info())

item = Item("Shirt", -10)
print(item.get_info())

bask = Basket()
bask.add_product(service)
bask.add_product(item)

print(bask.get_total_price())

bask.save_to_file("bask.json")
print("\nSaved in bask.json")

#----------------------------------------------------XML----------------------------------------------------------------

bask_element = bask.to_xml()
tree = ET.ElementTree(bask_element)
tree.write("bask.xml")

tree = ET.parse("bask.xml")
root = tree.getroot()

for product_element in root:
    product_type = product_element.tag
    if product_type == "Product":
        name = product_element.find("Name").text
        price = float(product_element.find("Price").text)
        product = Product(name, price)
    elif product_type == "Service":
        name = product_element.find("Name").text
        duration = product_element.find("Duration").text
        price = float(product_element.find("Price").text)
        product = Service(name, duration, price)
    elif product_type == "Item":
        name = product_element.find("Name").text
        price = float(product_element.find("Price").text)
        product = Item(name, price)
print("Saved in bask.xml")

print("\nDo you want to clean your basket? \n Y/N")
if input() == "Y":
    with open("bask.json", "w") as file:
        pass
    for element in root.findall(".//*"):
        element.clear()
    for element in root.iter():
        element.attrib.clear()
    tree.write("bask.xml")
    print("Basket is empty")

