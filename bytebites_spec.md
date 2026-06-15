We need to build the backend logic for the ByteBites app. The system needs to manage our customers, tracking their names and their past purchase history so the system can verify they are real users.

These customers need to browse specific food items (like a "Spicy Burger" or "Large Soda"), so we must track the name, price, category, and popularity rating for every item we sell.

We also need a way to manage the full collection of items — a digital list that holds all items and lets us filter by category such as "Drinks" or "Desserts".

Finally, when a user picks items, we need to group them into a single transaction. This transaction object should store the selected items and compute the total cost.

Candidate Classes:
1. Customers - Managing customers info such as first name, last name, email, phone number. It's should be also a way that the system can vertify the real users by having user inputting their first name, last name, and phone number 
2. Food Items - Tracking food items such as name, price, categories, and popularity rating (Ex: cheeseburger, $5.36, category: burgers, rating: 4.0). The following of food items that should be displayed is "cheeseburger", "bacon cheeseburger", "chicken burger", "curly fries", regular fries", "waffle fries", "chocolate cake", "vanilla ice cream", "cookie sandwich", "coke", "sprite", "ginger soda", "chicken tenders", "chicken nuggets", "spicy nuggets".  
3. Item Collection - Managing the full collection of food items. Must filter by category such as "Drinks", "Desserts", "Burgers", "Chicken", and "Fries"
4. Transaction - All the items that the user selected should be grouped into a singular transaction. Compute the total cost including tax which is 8.875%