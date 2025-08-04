import json # simple database for storing orders
from datetime import datetime # for timestamping orders
import os # for checking if the order file exists
from collections import Counter



# Pizza Information
pizza_data = {
    "1": {"name": "Classic", "price": 3.4},
    "2": {"name": "Chicken", "price": 4.5},
    "3": {"name": "Pepperoni", "price": 4.0},
    "4": {"name": "Deluxe", "price": 6.0},
    "5": {"name": "Vegetable", "price": 4.0},
    "6": {"name": "Chocolate", "price": 12.0},
    "7": {"name": "Cheese", "price": 5.0},
    "8": {"name": "BBQ Beef", "price": 5.5} #TASK 1
}

ORDER_DB_FILE = "pizza_orders.json"

def save_order_to_json(customer_name, pizza_name, quantity, total_price, order_type, discount_applied):
    """
    Append a new order to the JSON 'database' file.
    If the file does not exist, it creates a new one.
    :param pizza_name: Name of the pizza ordered
    :param quantity: Number of pizzas or slices ordered
    :param total_price: Total price of the order
    :param order_type: Type of order ('box' or 'slice')
    :param discount_applied: Boolean indicating if a discount was applied
    :return: None
    """
    order = {
        "orderdatetime": datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),
        "pizza_type": pizza_name,
        "order_type": order_type,
        "quantity": quantity,
        "total_price": round(total_price, 2),
        "discount_applied": discount_applied,
        "customer_name": customer_name
    }

    if os.path.exists(ORDER_DB_FILE):
        with open(ORDER_DB_FILE, "r+", encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
            data.append(order)
            file.seek(0) # Move the cursor to the beginning of the file
            json.dump(data, file, indent=4) # Write the updated data back to the file
    else:
        with open(ORDER_DB_FILE, "w", encoding='utf-8') as file:
            json.dump([order], file, indent=4)


# Calculate total payment with optional discount
def calculate_payment(price, quantity, discount_rate=0.0):
    """
    Calculate total payment with optional discount.
    :param price: Price per pizza box or slice
    :param quantity: Number of pizzas or slices ordered
    :param discount_rate: Discount rate as a decimal (e.g., 0.20 for 20%)
    :return: Total payment after discount
    """
    total = price * quantity
    discount = total * discount_rate
    return total - discount


# Handle box and slice orders with discounts
def handle_box_order(pizza_name, price):
    """
    Process box order with possible discounts.
    """
    while True:
        qty_input = input("How many boxes do you want? (or type 'q' to cancel): ").strip()
        if qty_input.lower() == 'q':
            print("Cancelled box order.")
            return
        if qty_input.isdigit():
            quantity = int(qty_input)
            break
        else:
            print("Please enter a valid number.")

    discount_rate = 0.0
    if quantity >= 10:
        discount_rate = 0.20 # 20% discount for 10 or more boxes
    elif quantity >= 5:
        discount_rate = 0.10 # 10% discount for 5 or more boxes

    discount_applied = True if discount_rate > 0.0 else False
    if discount_applied:
        total = calculate_payment(price, quantity, discount_rate)
        # TASK 2: Apply 7.5% tax
        tax_amount = round((7.5/100)*total, 2)
        taxed_total = tax_amount + total
        print(f"Total before tax is: {total}")
        print(f"A tax of {tax_amount} was applied")
        print(f"Your total with tax is {taxed_total:.2f}")

#    print(f"Your payment is ${total:.2f} for {quantity} box(es).")
#   if discount_applied:
#      print(f"A discount of {int(discount_rate * 100)}% was applied")

# TASK 4: Ask for customer name
    customer_name = input("Great, please what's your name?: ")

# TASK 3
    print(f"""
--Your order is successful--
-----ORDER SUMMARY-----
Customer   --- {customer_name}
Pizza Name --- {pizza_name}
Quantity   --- {quantity}
Discount:  --- {discount_rate}
Tax Applied--- {tax_amount}
Total to pay-- {taxed_total:.2f}
            """)

    save_order_to_json(customer_name, pizza_name, quantity, total, "box", discount_applied)


def handle_slice_order(pizza_name, slice_price):
    """Process slice order without discounts.
    """
    while True:
        qty_input = input("How many slices do you want? (or type 'q' to cancel): ").strip()
        if qty_input.lower() == 'q':
            print("Cancelled slice order.")
            return
        if qty_input.isdigit(): # Check if input is a digit
            quantity = int(qty_input) # Ensure it's an integer
            break
        else:
            print("Please enter a valid number.")

    total = calculate_payment(slice_price, quantity)
    print(f"Your payment is ${total:.2f} for {quantity} slice(s).")

    save_order_to_json(pizza_name, quantity, total, "slice", False)


# Order Pizza Function
def order_pizza(pizza_type):
    """
    Handle the pizza order process.
    """
    if pizza_type in pizza_data:
        pizza = pizza_data[pizza_type]
        price = pizza["price"]
        name = pizza["name"]
        slice_price = round(price / 8, 2)

        print(
            f"You selected {name}!\n"
            f"Price - ${price:.2f} per box\n"
            f"Per Slice - ${slice_price:.2f}"
        )

        while True:
            choice = input("Select 'B' for Box or 'S' for Slice (or 'q' to cancel): ").strip().upper()
            if choice == "B":
                handle_box_order(name, price)
                break
            elif choice == "S":
                handle_slice_order(name, slice_price)
                break
            elif choice == "Q":
                print("Cancelled selection.")
                break
            else:
                print("Invalid choice. Please select 'B', 'S', or 'q'.")
    else:
        print("We do not have this type of pizza for now, maybe later!")

# Main function to run the pizza ordering system
def main():
    while True:
        print("\nWelcome to RushMore Pizza!")
        print("Menu:")
        for key, value in pizza_data.items():
            print(f"{key}: {value['name']} - ${value['price']:.2f}")

        print("\nOptions:")
        print("Enter the number to order a pizza")
        print("Type 'q' to quit")
        print("Type s to view stats")

        choice = input("What would you like to do? ").strip().lower()

        if choice == 'q':
            print("Goodbye from RushMore Pizza!")
            break
        elif choice == 'v':
            view_orders()
        elif choice in pizza_data:
            order_pizza(choice)
        elif choice == 's':
            view_stats()
        else:
            print("Invalid input. Please try again.")

def view_stats():
    """View order statistics"""
    if os.path.exists(ORDER_DB_FILE):
        with open(ORDER_DB_FILE, "r", encoding='utf-8') as file:
            try:
                orders = json.load(file)
                if not orders:
                    print("Hey!, no orders yet")
                else:
                    # TOTAL ORDERS
                    total_orders = len(orders)

                    # TOTAL PIZZA COUNT
                    pizza_counts = {}
                    for order in orders:
                        pizza = order["pizza_type"]
                        if pizza in pizza_counts:
                            pizza_counts[pizza] += 1
                        else:
                            pizza_counts[pizza] = 1

                    most_frequent_pizza = None
                    max_count = 0
                    for pizza, count in pizza_counts.items():
                        if count > max_count:
                            max_count = count
                            most_frequent_pizza = pizza

                    # TOTAL REVENUE
                    total_revenue = sum(order["total_price"] for order in orders)

                    print(f"""
-----ORDER STATISTICS-----
Total Orders    --- {total_orders}
Frequent Orders --- {most_frequent_pizza}
total_revenue   --- {total_revenue}
                          """
                    )

            except json.JSONEncoder:
                print("Error reading the order database")
    else:
        print("No orders yet")

def view_orders():
    """
    View all orders from the JSON database.
    """
    if os.path.exists(ORDER_DB_FILE):
        with open(ORDER_DB_FILE, "r", encoding='utf-8') as file:
            try:
                orders = json.load(file)
                if not orders:
                    print("No orders found.")
                else:
                    for order in orders:
                        print(f"Order at {order['orderdatetime']}: {order['quantity']} {order['pizza_type']} ({order['order_type']}) - ${order['total_price']}")
            except json.JSONDecodeError:
                print("Error reading the order database.")
    else:
        print("No orders have been placed yet.")

if __name__ == "__main__":
    main()
