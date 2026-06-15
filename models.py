from __future__ import annotations

from typing import Optional

TAX_RATE = 0.08875  # 8.875%
CATEGORIES = ("Drinks", "Desserts", "Burgers", "Chicken", "Fries")
# Category strings use Title Case to match spec filter examples.


class FoodItem:
    def __init__(self, name: str, price: float, category: str, popularity_rating: float):
        self.name = name
        self.price = price
        self.category = category
        self.popularity_rating = popularity_rating


class ItemCollection:
    def __init__(self, items: Optional[list[FoodItem]] = None):
        self.items = list(items) if items else []

    def filter_by_category(self, category: str) -> list[FoodItem]:
        return [item for item in self.items if item.category == category]


class Transaction:
    def __init__(self):
        self.selected_items: list[FoodItem] = []

    def add_item(self, item: FoodItem) -> None:
        self.selected_items.append(item)

    def compute_total(self) -> float:
        subtotal = sum(item.price for item in self.selected_items)
        return round(subtotal * (1 + TAX_RATE), 2)


class Customer:
    def __init__(self, first_name: str, last_name: str, email: str, phone_number: str):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.purchase_history: list[Transaction] = []

    def verify(self, first_name: str, last_name: str, phone_number: str) -> bool:
        return (
            self.first_name == first_name
            and self.last_name == last_name
            and self.phone_number == phone_number
        )

    def add_purchase(self, transaction: Transaction) -> None:
        self.purchase_history.append(transaction)


def create_menu() -> ItemCollection:
    # Prices and ratings are illustrative; cheeseburger matches spec example.
    items = [
        FoodItem("cheeseburger", 5.36, "Burgers", 4.0),
        FoodItem("bacon cheeseburger", 6.49, "Burgers", 4.5),
        FoodItem("chicken burger", 5.99, "Burgers", 4.2),
        FoodItem("curly fries", 3.49, "Fries", 4.3),
        FoodItem("regular fries", 2.99, "Fries", 3.8),
        FoodItem("waffle fries", 3.79, "Fries", 4.6),
        FoodItem("chocolate cake", 4.99, "Desserts", 4.7),
        FoodItem("vanilla ice cream", 3.49, "Desserts", 4.1),
        FoodItem("cookie sandwich", 3.99, "Desserts", 4.4),
        FoodItem("coke", 2.29, "Drinks", 4.0),
        FoodItem("sprite", 2.29, "Drinks", 3.9),
        FoodItem("ginger soda", 2.49, "Drinks", 3.7),
        FoodItem("chicken tenders", 5.99, "Chicken", 4.5),
        FoodItem("chicken nuggets", 4.99, "Chicken", 4.3),
        FoodItem("spicy nuggets", 5.49, "Chicken", 4.6),
    ]
    return ItemCollection(items)


if __name__ == "__main__":
    menu = create_menu()
    burgers = menu.filter_by_category("Burgers")
    assert len(burgers) == 3, f"Expected 3 burgers, got {len(burgers)}"

    customer = Customer("Ada", "Lovelace", "ada@example.com", "555-0100")
    assert customer.verify("Ada", "Lovelace", "555-0100")
    assert not customer.verify("Ada", "Lovelace", "555-0101")

    drinks = menu.filter_by_category("Drinks")
    txn = Transaction()
    txn.add_item(drinks[0])  # coke
    txn.add_item(burgers[0])  # cheeseburger
    expected_total = round((drinks[0].price + burgers[0].price) * (1 + TAX_RATE), 2)
    assert txn.compute_total() == expected_total

    customer.add_purchase(txn)
    assert len(customer.purchase_history) == 1

    print("All smoke tests passed.")
