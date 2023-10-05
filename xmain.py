import xml.etree.ElementTree as ET


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def get_info(self):
        return f"Product name: {self.name}"

    def to_xml(self):
        product_element = ET.Element("Product")
        name_element = ET.SubElement(product_element, "Name")
        name_element.text = self.name
        return product_element


class Service(Product):
    def __init__(self, name, duration, price):
        super().__init__(name, price)
        self.duration = duration

    def get_info(self):
        return f"Service name: {self.name}, \nDuration: {self.duration}, \nPrice: {self.price}\n"

    def to_xml(self):
        service_element = ET.Element("Service")
        name_element = ET.SubElement(service_element, "Name")
        name_element.text = self.name
        duration_element = ET.SubElement(service_element, "Duration")
        duration_element.text = self.duration
        price_element = ET.SubElement(service_element, "Price")
        price_element.text = str(self.price)
        return service_element


class Item(Product):
    def __init__(self, name, price):
        super().__init__(name, price)

    def get_info(self):
        return f"Item name: {self.name}, \nPrice: {self.price}\n"

    def to_xml(self):
        item_element = ET.Element("Item")
        name_element = ET.SubElement(item_element, "Name")
        name_element.text = self.name
        price_element = ET.SubElement(item_element, "Price")
        price_element.text = str(self.price)
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
            if isinstance(product, Item):
                try:
                    if type(product.price) == str:

                        raise ValueError
                    else:
                        total_price += product.price
                except ValueError:
                    print("It's over...")
                    quit()
        try:
            if total_price > 0:
                return f"Your final price will be: {total_price}"
            else:
                raise Low
        except Low:
            return "Your basket is empty"

    def to_xml(self):
        bask_element = ET.Element("Cart")
        for product in self.products:
            product_element = product.to_xml()
            bask_element.append(product_element)
        return bask_element


class Low(Exception):
    pass


service = Service("Cleaning", "1 hour", 20)
print(service.get_info())

item = Item("Shirt", 20)
print(item.get_info())

bask = Basket()
bask.add_product(service)
bask.add_product(item)
print(bask.get_total_price())

# Запись в XML файл
bask_element = bask.to_xml()
tree = ET.ElementTree(bask_element)
tree.write("bask.xml")

# Считывание из XML файла
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

