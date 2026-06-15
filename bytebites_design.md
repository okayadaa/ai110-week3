classDiagram
    class Customer {
        -String firstName
        -String lastName
        -String email
        -String phoneNumber
        -List~Transaction~ purchaseHistory
        +verify(firstName, lastName, phoneNumber) bool
        +addPurchase(transaction) void
    }

    class FoodItem {
        -String name
        -float price
        -String category
        -float popularityRating
    }

    class ItemCollection {
        -List~FoodItem~ items
        +__init__(items) void
        +filterByCategory(category) List~FoodItem~
    }

    class Transaction {
        -List~FoodItem~ selectedItems
        +addItem(item) void
        +computeTotal() float
    }

    note for Transaction "subtotal + 8.875% tax, rounded to 2 dp"

    Customer "1" --> "*" Transaction : purchase history
    ItemCollection "1" o-- "*" FoodItem : holds
    Transaction "*" o-- "*" FoodItem : selected items
