import pytest

from models import (
    TAX_RATE,
    FoodItem,
    ItemCollection,
    Transaction,
    create_menu,
)


@pytest.fixture
def menu():
    return create_menu()


@pytest.fixture
def sample_items():
    return [
        FoodItem("coke", 2.29, "Drinks", 4.0),
        FoodItem("cheeseburger", 5.36, "Burgers", 4.0),
        FoodItem("curly fries", 3.49, "Fries", 4.3),
    ]


class TestFilterByCategory:
    @pytest.mark.parametrize(
        "category, expected_count",
        [
            ("Drinks", 3),
            ("Desserts", 3),
            ("Burgers", 3),
            ("Chicken", 3),
            ("Fries", 3),
        ],
    )
    def test_menu_filter_returns_expected_count(self, menu, category, expected_count):
        filtered = menu.filter_by_category(category)
        assert len(filtered) == expected_count
        assert all(item.category == category for item in filtered)

    def test_filter_returns_only_matching_category(self, sample_items):
        collection = ItemCollection(sample_items)
        drinks = collection.filter_by_category("Drinks")

        assert len(drinks) == 1
        assert drinks[0].name == "coke"

    def test_filter_unknown_category_returns_empty_list(self, menu):
        assert menu.filter_by_category("Unknown") == []

    def test_filter_empty_collection_returns_empty_list(self):
        collection = ItemCollection()
        assert collection.filter_by_category("Drinks") == []

    def test_all_categories_cover_full_menu(self, menu):
        categories = ("Drinks", "Desserts", "Burgers", "Chicken", "Fries")
        total_filtered = sum(
            len(menu.filter_by_category(category)) for category in categories
        )
        assert total_filtered == len(menu.items)


class TestComputeTotal:
    def test_empty_transaction_total_is_zero(self):
        txn = Transaction()
        assert txn.compute_total() == 0.0

    def test_single_item_includes_tax(self):
        item = FoodItem("coke", 2.29, "Drinks", 4.0)
        txn = Transaction()
        txn.add_item(item)

        expected = round(item.price * (1 + TAX_RATE), 2)
        assert txn.compute_total() == expected

    def test_multiple_items_sum_prices_before_tax(self, menu):
        drinks = menu.filter_by_category("Drinks")
        burgers = menu.filter_by_category("Burgers")

        txn = Transaction()
        txn.add_item(drinks[0])
        txn.add_item(burgers[0])

        subtotal = drinks[0].price + burgers[0].price
        expected = round(subtotal * (1 + TAX_RATE), 2)
        assert txn.compute_total() == expected

    def test_tax_rate_is_8875_percent(self):
        assert TAX_RATE == 0.08875

    def test_total_rounds_to_two_decimal_places(self):
        item = FoodItem("test item", 10.01, "Burgers", 3.0)
        txn = Transaction()
        txn.add_item(item)

        total = txn.compute_total()
        assert total == round(10.01 * (1 + TAX_RATE), 2)
