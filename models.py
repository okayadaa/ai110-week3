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


def _format_item(item: FoodItem) -> str:
    return f"{item.name} — ${item.price:.2f} (rating {item.popularity_rating})"


def run_demo() -> None:
    print("=== ByteBites Demo ===\n")

    menu = create_menu()
    print(f"Full menu: {len(menu.items)} items\n")

    print("--- Filter by category ---")
    for category in CATEGORIES:
        filtered = menu.filter_by_category(category)
        names = ", ".join(item.name for item in filtered)
        print(f"  {category} ({len(filtered)}): {names}")
    print()

    unknown = menu.filter_by_category("Unknown")
    print(f'  Unknown category: {len(unknown)} items (expected 0)\n')

    print("--- Build a transaction ---")
    drinks = menu.filter_by_category("Drinks")
    burgers = menu.filter_by_category("Burgers")
    txn = Transaction()
    txn.add_item(drinks[0])
    txn.add_item(burgers[0])
    subtotal = drinks[0].price + burgers[0].price
    total = txn.compute_total()
    print(f"  Added: {_format_item(drinks[0])}")
    print(f"  Added: {_format_item(burgers[0])}")
    print(f"  Subtotal: ${subtotal:.2f}")
    print(f"  Tax ({TAX_RATE * 100:.3f}%): ${total - subtotal:.2f}")
    print(f"  Total: ${total:.2f}\n")

    print("--- Customer verification ---")
    customer = Customer("Ada", "Lovelace", "ada@example.com", "555-0100")
    good = customer.verify("Ada", "Lovelace", "555-0100")
    bad = customer.verify("Ada", "Lovelace", "555-0101")
    print(f"  Correct credentials: {'verified' if good else 'failed'}")
    print(f"  Wrong phone number: {'rejected' if not bad else 'failed'}")
    customer.add_purchase(txn)
    print(f"  Purchase history: {len(customer.purchase_history)} transaction(s)\n")


def run_checks() -> None:
    menu = create_menu()

    expected_counts = {
        "Drinks": 3,
        "Desserts": 3,
        "Burgers": 3,
        "Chicken": 3,
        "Fries": 3,
    }
    for category in CATEGORIES:
        filtered = menu.filter_by_category(category)
        assert len(filtered) == expected_counts[category], (
            f"Expected {expected_counts[category]} {category}, got {len(filtered)}"
        )
        assert all(item.category == category for item in filtered)

    assert menu.filter_by_category("Unknown") == []
    assert sum(len(menu.filter_by_category(c)) for c in CATEGORIES) == len(menu.items)

    burgers = menu.filter_by_category("Burgers")
    drinks = menu.filter_by_category("Drinks")

    assert TAX_RATE == 0.08875

    empty_txn = Transaction()
    assert empty_txn.compute_total() == 0.0

    txn = Transaction()
    txn.add_item(drinks[0])
    txn.add_item(burgers[0])
    expected_total = round((drinks[0].price + burgers[0].price) * (1 + TAX_RATE), 2)
    assert txn.compute_total() == expected_total

    customer = Customer("Ada", "Lovelace", "ada@example.com", "555-0100")
    assert customer.verify("Ada", "Lovelace", "555-0100")
    assert not customer.verify("Ada", "Lovelace", "555-0101")

    customer.add_purchase(txn)
    assert len(customer.purchase_history) == 1


def create_customers() -> list[Customer]:
    return [
        Customer("Ada", "Lovelace", "ada@example.com", "555-0100"),
        Customer("Grace", "Hopper", "grace@example.com", "555-0101"),
    ]


def find_customer(
    customers: list[Customer], first_name: str, last_name: str, phone_number: str
) -> Customer | None:
    for customer in customers:
        if customer.verify(first_name, last_name, phone_number):
            return customer
    return None


def print_menu_by_category(menu: ItemCollection) -> None:
    print("\n--- Menu by category ---")
    for category in CATEGORIES:
        filtered = menu.filter_by_category(category)
        print(f"\n{category} ({len(filtered)}):")
        for index, item in enumerate(filtered, start=1):
            print(f"  {index}. {_format_item(item)}")
    print()


def print_cart(txn: Transaction) -> None:
    if not txn.selected_items:
        print("\nYour cart is empty.\n")
        return

    subtotal = sum(item.price for item in txn.selected_items)
    total = txn.compute_total()
    tax = total - subtotal

    print("\n--- Your cart ---")
    for item in txn.selected_items:
        print(f"  {_format_item(item)}")
    print(f"  Subtotal: ${subtotal:.2f}")
    print(f"  Tax ({TAX_RATE * 100:.3f}%): ${tax:.2f}")
    print(f"  Total: ${total:.2f}\n")


def _prompt_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  Please enter a value.")


def verify_customer(customers: list[Customer]) -> Customer:
    print("=== ByteBites ===\n")
    print("Please verify your account to start ordering.\n")

    while True:
        first_name = _prompt_non_empty("First name: ")
        last_name = _prompt_non_empty("Last name: ")
        phone_number = _prompt_non_empty("Phone number: ")

        customer = find_customer(customers, first_name, last_name, phone_number)
        if customer:
            print(f"\nVerified! Welcome, {customer.first_name} {customer.last_name}.\n")
            return customer

        print("\nWe could not verify those details. Please try again.\n")


def browse_category(menu: ItemCollection) -> list[FoodItem]:
    print("Categories:")
    for index, category in enumerate(CATEGORIES, start=1):
        count = len(menu.filter_by_category(category))
        print(f"  {index}. {category} ({count} items)")
    print("  Or type a category name (e.g. Drinks)")

    while True:
        choice = input("\nSelect a category: ").strip()
        if not choice:
            continue

        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(CATEGORIES):
                category = CATEGORIES[index]
                break
            print("Invalid category number.")
            continue

        matched = next((c for c in CATEGORIES if c.lower() == choice.lower()), None)
        if matched:
            category = matched
            break

        print(f"Unknown category. Choose from: {', '.join(CATEGORIES)}")

    filtered = menu.filter_by_category(category)
    print(f"\n{category}:")
    for index, item in enumerate(filtered, start=1):
        print(f"  {index}. {_format_item(item)}")
    return filtered


def select_item_from_list(items: list[FoodItem]) -> FoodItem | None:
    while True:
        choice = input("\nEnter item number to add (or 'back'): ").strip().lower()
        if choice in ("back", "b"):
            return None
        if not choice.isdigit():
            print("Enter a number from the list, or 'back'.")
            continue
        index = int(choice) - 1
        if 0 <= index < len(items):
            return items[index]
        print("Invalid item number.")


def run_interactive() -> None:
    menu = create_menu()
    customers = create_customers()
    customer = verify_customer(customers)
    txn = Transaction()

    print_menu_by_category(menu)
    print("Commands: browse | cart | checkout | quit")

    while True:
        command = input("> ").strip().lower()
        if not command:
            continue

        if command in ("quit", "q", "exit"):
            print("Goodbye!")
            break

        if command in ("browse", "b", "filter"):
            items = browse_category(menu)
            item = select_item_from_list(items)
            if item:
                txn.add_item(item)
                print(f"Added {_format_item(item)}")
                print_cart(txn)
            continue

        if command in ("cart", "c"):
            print_cart(txn)
            continue

        if command in ("checkout", "done"):
            if not txn.selected_items:
                print("Your cart is empty — browse and add items first.")
                continue

            total = txn.compute_total()
            customer.add_purchase(txn)
            print(f"Checkout complete! Total charged: ${total:.2f}")
            print(f"Thank you, {customer.first_name}! "
                  f"You have {len(customer.purchase_history)} order(s) on file.\n")

            txn = Transaction()
            print("Start a new order, or type 'quit' to leave.")
            continue

        if command == "menu":
            print_menu_by_category(menu)
            continue

        print("Unknown command. Try: browse | cart | checkout | quit")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo()
        run_checks()
        print("All checks passed.")
    else:
        run_interactive()
