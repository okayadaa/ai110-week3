classDiagram
    class Customer {
        - String firstName
        - String lastName
        - String email
        - String phoneNumber
        - List~Transaction~ purchaseHistory
        + verify(firstName, lastName, phoneNumber) bool
        + addPurchase(transaction) void
    }

    class FoodItem {
        - String name
        - float price
        - String category
        - float rating
        + getName() String
        + getPrice() float
        + getCategory() String
        + getRating() float
    }

    class ItemCollection {
        - List~FoodItem~ items
        + addItem(item) void
        + removeItem(item) void
        + filterByCategory(category) List~FoodItem~
        + getAllItems() List~FoodItem~
    }

    class Transaction {
        - Customer customer
        - List~FoodItem~ selectedItems
        - float TAX_RATE
        + addItem(item) void
        + computeSubtotal() float
        + computeTotal() float
    }

    Customer "1" --> "*" Transaction : has history
    Transaction "*" --> "*" FoodItem : contains
    ItemCollection "1" o-- "*" FoodItem : holds
    Transaction "*" --> "1" Customer : belongs to

