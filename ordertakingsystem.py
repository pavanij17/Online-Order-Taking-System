import mysql.connector
import random
import string
from datetime import date
from prettytable import PrettyTable

def connection():
    con = mysql.connector.connect(host="localhost", user="root", password="1234", database="indian_restruant")
    self = con.cursor()

    self.execute("CREATE TABLE IF NOT EXISTS _fooditems (item_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), price DECIMAL(10, 2))")
    self.execute("CREATE TABLE IF NOT EXISTS _order (custname VARCHAR(255), custph INT, order_id INT AUTO_INCREMENT PRIMARY KEY, item_id INT, quantity INT)")
    self.execute("CREATE TABLE IF NOT EXISTS _sales (date DATE, bill_no VARCHAR(10), net_amount DECIMAL(10, 2), gst DECIMAL(10, 2), gross_amount DECIMAL(10, 2))")

def create_sales_table():
    con = mysql.connector.connect(host="localhost", user="root", password="1234", database="indian_restruant")
    self = con.cursor()

    self.execute("CREATE TABLE IF NOT EXISTS _sales (date DATE, bill_no VARCHAR(10), net_amount DECIMAL(10, 2), gst DECIMAL(10, 2), gross_amount DECIMAL(10, 2))")

def generate_bill_no():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def fooditemto_menu(name, price):
    
    con = mysql.connector.connect(host="localhost", user="root", password="1234", database="indian_restruant")
    self = con.cursor()

    query = "INSERT INTO _fooditems (name, price) VALUES (%s, %s)"
    data = (name, price)
    self.execute(query, data)
    con.commit()
    print("ADDED DISH:", name, "PRICE", "   " "₹", price)

def display_menu():
    con = mysql.connector.connect(host="localhost", user="root", password="1234", database="indian_restruant")
    self = con.cursor()
    global menu
    menu = []

    self.execute("SELECT * FROM _fooditems")
    data = self.fetchall()
    for i in data:
        food_item = (i[0], i[1], i[2])
        print("  ", i[0], "  ", i[1], " ", i[2], "(₹)/per plate")
        menu.append(food_item)

def take_orders():
    con = mysql.connector.connect(host="localhost", user="root", password="1234", database="indian_restruant")
    self = con.cursor()
    display_menu()
    
    order_id = 1
    custname = input("enter your name")
    custph = int(input("enter phone no."))
    item_id = int(input("Enter the item ID to order: "))
    quantity = int(input("Enter the quantity:"))
    query = "insert into _order (custname,custph,item_id,quantity) values(%s,%s,%s,%s)"
    data = (custname, custph, item_id, quantity)
    self.execute(query, data)
    con.commit()
    query2 = "select order_id from _order where custph={}".format(custph)
    self.execute(query2)
    data = self.fetchall()
    a = data[0]
    if item_id < 1 or item_id > len(menu):
        print("Invalid item ID.")
        return
    print("==ordered successfully==", "please wait your order id is:", a)

def _totalcost():
    con = mysql.connector.connect(host="localhost", user="root", password="1234", database="indian_restruant")
    self = con.cursor()

    print("==BILLING==")
    userid = int(input("enter   your order id"))
    query1 = ("select quantity from _order where order_id={}".format(userid))
    self.execute(query1)
    data1 = self.fetchall()

    query2 = ("select price from _order,_fooditems where _order.item_id=_fooditems.item_id")
    self.execute(query2)
    data2 = self.fetchall()

    gst = 0.09
    calc = int(data1[0][0]) * int(data2[0][0])
    billprice = calc + calc * 0.09

    bill_no = generate_bill_no()
    date_today = date.today()
    query3 = "INSERT INTO _sales (date, bill_no, net_amount, gst, gross_amount) VALUES (%s, %s, %s, %s, %s)"
    data3 = (date_today, bill_no, calc, calc * 0.09, billprice)
    self.execute(query3, data3)

   
    con.commit()

    print("you have to pay", billprice, "including 9% GST")
    print("=======HAVE A NICE DAY!!========")

def orderhistory():
    passcode = input("enter pass code")
    if passcode == "dav":
        con = mysql.connector.connect(host="localhost", user="root", password="1234", database="indian_restruant")
        self = con.cursor()
        query = "select * from _order"
        self.execute(query)
        data = self.fetchall()
        count = 1
        for j in data:
            custname, custph, order_id, item_id, quantity = j
            print("=====customer", count, "======")
            print("customer name:", custname)
            print("customer contact:", custph)
            print("order id:", order_id)
            print("item id:", item_id)
            print("quantity bought:", quantity)
            count += 1
    else:
        print("unauthorized access!!")

def display_total_sales_from_db():
    con = mysql.connector.connect(host="localhost", user="root", password="1234", database="indian_restruant")
    self = con.cursor()

    self.execute("SELECT * FROM _sales")
    data = self.fetchall()

    if not data:
        print("No sales data available.")
        return

    table = PrettyTable()
    table.field_names = ["Date", "Bill No", "Net Amount", "GST", "Gross Amount"]

    for sale in data:
        table.add_row(sale)

    print(table)

create_sales_table()
connection()
while True:
    print("\nOnline Food Order System Menu:")
    print("1. Add Food Item to Menu")
    print("2. Display Menu")
    print("3. Take Order")
    print("4. Calculate Total Cost")
    print("5. Display order history")
    print("6. Display Total Sales")
    print("7. Quit")

    choice = input("Enter your choice: ")

    if choice == "1":
        passcode = input("enter pass code")
        if passcode == "dav":
            name = input("Enter food item name: ")
            price = float(input("Enter food item price: "))
            fooditemto_menu(name, price)
        else:
            print("unauthorized access!!")

    if choice == "2":
        display_menu()
    if choice == "3":
        take_orders()
    if choice == "4":
        _totalcost()
    if choice == "5":
        orderhistory()
    if choice == "6":
        display_total_sales_from_db()
    if choice == "7":
        break
