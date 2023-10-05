import json


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "type": "product"
        }


class Service(Product):
    def __init__(self, name, duration, price):
        super().__init__(name, price)
        self.duration = duration

    def get_info(self):
        return f"Service name: {self.name},\nDuration: {self.duration}, \nPrice: {self.price}\n"

    def to_dict(self):
        return {
            "name": self.name,
            "duration": self.duration,
            "price": self.price,
            "type": "service"
        }


class Item(Product):
    def __init__(self, name, price):
        super().__init__(name, price)

    def get_info(self):
        return f"Item name: {self.name}, \nPrice: {self.price}\n"

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "type": "item"
        }


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

bask.save_to_file("bask.json")
