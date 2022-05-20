# tkinter imports
from ctypes import alignment
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from query import query
from database import database

import sys
import time
import csv

root = Tk()
root.title("Z41 Demo")
root.geometry("950x600")

# clear frame
def clear_frame():
   for widgets in frame.winfo_children():
      widgets.destroy()

# returns current datetime in sql format
def get_curr_datetime():
    return time.strftime('%Y-%m-%d %H:%M:%S')

# helper function for initializing trees
def get_initialized_tree(tree_frame):
    # Create treeview scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # Create treeview
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")

    # Configure Scrollbar
    tree_scroll.config(command=my_tree.yview)

    return my_tree

# writes data to csv file with given title name
def write_csv(file_name, data):
        csv.writer(open(file_name, 'w')).writerows(data)

##### ----------------- WELCOME -----------------
class Welcome:
    # clears frame and populates
    def welcome():
        clear_frame()
        account_frame = LabelFrame(frame, text="Select an Account Type")
        account_frame.grid(row=0,column=0, sticky="NESW", padx=50, pady=5)
        Label(account_frame, text="Are you a Developer or a Customer?").grid(row=0, column=0, columnspan=2)
        Button(account_frame, text="Developer", command=Welcome.developer).grid(row=1, column=0)
        Button(account_frame, text="Customer", command=Welcome.customer).grid(row=1, column=1)

        # View Premium Customers (Premium is purchase total of > $100)
        special_frame = LabelFrame(frame, text="Special Options")
        special_frame.grid(row=0,column=1, sticky="NESW", padx=50, pady=5)
        Button(special_frame, text="View Premium Customers", command=Welcome.view_premium_customers).grid(row=0, column=0)

        # Generate report frame and buttons
        reports_frame = LabelFrame(frame, text="Generate CSV Reports")
        reports_frame.grid(row=0, column=2, sticky="NESW", padx=50, pady=5)
        Button(reports_frame, text="Developers", command=lambda: Welcome.generate_report("Developer")).pack()
        Button(reports_frame, text="Customers", command=lambda: Welcome.generate_report("Customer")).pack()
        Button(reports_frame, text="Products", command=lambda: Welcome.generate_report("Product")).pack()
        Button(reports_frame, text="Purchases", command=lambda: Welcome.generate_report("Purchase")).pack()
        Button(reports_frame, text="Film Orders", command=lambda: Welcome.generate_report("FilmOrder")).pack()
        # Quit button
        Button(frame, text="Quit", command=root.quit).grid(row=1, column=0, columnspan=3)


    ##### Welcome functions for Developer
    def developer():
        clear_frame()
        Label(frame, text="Developer").pack()
        Label(frame, text="Enter your Developer ID:").pack()
        # text entry field
        e_id = Entry(frame, width=50)
        e_id.pack()
        # called when Go button is clicked. Checks if id is valid
        def on_go_button_click():
            id = e_id.get()
            if Welcome.is_valid_developer_id(id):
                Developer.menu(id)
            else:
                messagebox.showerror("Developer Login", "Could not locate Developer with ID #" + str(id) + ".")
        # Go button
        Button(frame, text="Go", command=on_go_button_click).pack()
        # Back button
        Button(frame, text="Back", command=Welcome.welcome).pack()

    def is_valid_developer_id(id):
        return query.checkValidDeveloperID(mydb, mycursor, id)


    ##### Welcome functions for Customer
    def customer():
        clear_frame()
        Label(frame, text="Customer").pack()
        Button(frame, text="Log In", command=Welcome.customer_login).pack()
        Button(frame, text="New Customer", command=Welcome.new_customer).pack()
        # Back button
        Button(frame, text="Back", command=Welcome.welcome).pack()

    def customer_login():
        clear_frame()
        Label(frame, text="Customer Login").pack()
        Label(frame, text="Enter your Customer ID:").pack()
        # text entry field
        e_id = Entry(frame, width=50)
        e_id.pack()
        # called when Go button is clicked. Checks if id is valid
        def on_go_button_click():
            id = e_id.get()
            if Welcome.is_valid_customer_id(id):
                Customer.menu(id)
            else:
                messagebox.showerror("Customer Login", "Could not locate Customer with ID #" + str(id) + ".")
        # Go button
        Button(frame, text="Go", command=on_go_button_click).pack()
        # Back button
        Button(frame, text="Back", command=Welcome.customer).pack()

    def is_valid_customer_id(id):
        return query.checkValidCustomerID(mydb, mycursor, id)
        

    def new_customer():
        clear_frame()
        Label(frame, text="Create Customer Account").pack()
        # widgets to get user info
        Label(frame, text="First and Last Name").pack()
        e_name = Entry(frame, width=50)
        e_name.pack()
        Label(frame, text="Email").pack()
        e_email = Entry(frame, width=50)
        e_email.pack()
        Label(frame, text="Address").pack()
        e_address = Entry(frame, width=50)
        e_address.pack()
        # called when Go button is clicked. Checks if id is valid
        def on_go_button_click():
            # TODO: error handling for empty/incorrect fields
            id = Welcome.create_new_customer(e_name.get(), e_email.get(), e_address.get())
            Customer.menu(id)
        # Go button
        Button(frame, text="Go", command=on_go_button_click).pack()
        # Back button
        Button(frame, text="Back", command=Welcome.customer).pack()

    def create_new_customer(name, email, address):
        # run query to create new customer in db
        return query.createNewCustomerAndGetID(mydb, mycursor, name, email, address) # returns ID of new customer

    # View Premium Customers (Premium is purchase total of > $100)
    def view_premium_customers():
        clear_frame()
        Label(frame, text="Premium Customers").pack()
        Label(frame, text="Below are customers that have spent $100 or more on Purchases.\nThese are the kinds of people you want to be friends with.").pack()

        # ------------ SET UP TREE -----------------
        # Create treeview frame
        tree_frame = Frame(frame)
        tree_frame.pack(pady=10)

        my_tree = get_initialized_tree(tree_frame)
        my_tree.pack()

        # Define our columns
        my_tree['columns'] = ("Name", "TotalSpent")

        # Format our columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Name", anchor=W, width=150)
        my_tree.column("TotalSpent", anchor=CENTER, width=80)

        # Create headings
        my_tree.heading("Name", text="Customer Name", anchor=W)
        my_tree.heading("TotalSpent", text="Total Spent", anchor=CENTER)
        # ------------------------------------------

        # query to get all premium customer tuples from db in format (name, totalSpent)
        premium_customer_data = query.getAllPremiumCustomers(mydb, mycursor)
        # Add data to tree
        i = 0
        for record in premium_customer_data:
            my_tree.insert(parent='', index='end', iid=i, values=(record[0], "$"+str(record[1])))
            i+=1

        # Back button
        Button(frame, text="Back", command=Welcome.welcome).pack()

    # Queries requested data and generates csv file, takes in table name
    def generate_report(table_name):
        # query data
        data = query.getAllDataFromTable(mydb, mycursor, table_name)
        file_name = "reports/" + table_name.lower() + "s.csv"
        # write to file
        write_csv(file_name, data)
        # display success message
        messagebox.showinfo("Generate Report", "Successfully generated report of all " + table_name + "s to '" + file_name + "'.")





##### ----------------- DEVELOPER -----------------
class Developer:
    id = -1
    name = ""
    email = ""
    address = ""
    availRolls = -1

    def menu(id):
        clear_frame()

        # query customer info from db and store info locally
        developer_info_tuple = query.getDeveloperAttributes(mydb, mycursor, id)
        (Developer.id, Developer.name, Developer.email, Developer.address, Developer.availRolls) = developer_info_tuple

        # Display info
        Label(frame, text="Developer Menu").pack()
        Label(frame, text="Welcome, "+Developer.name).pack()
        Label(frame, text="ID: "+str(Developer.id)).pack()
        Label(frame, text="Name: "+Developer.name).pack()
        Label(frame, text="Address: "+Developer.address).pack()
        Label(frame, text="Available Rolls: "+str(Developer.availRolls)).pack()

        # Update available rolls button
        Button(frame, text="Update Available Rolls", command=Developer.updateAvailRolls).pack()
        # View orders button
        Button(frame, text="View Orders", command=Developer.viewOrders).pack()

        # Back button
        Button(frame, text="Back", command=Welcome.welcome).pack()
        # Quit button
        Button(frame, text="Quit", command=root.quit).pack()

    def updateAvailRolls():
        clear_frame()

        # ------ Update Avail Rolls Helper Functions ------
        def modAvailRolls(modAmt):
            # Update local class
            if Developer.availRolls + modAmt >= 0:
                Developer.availRolls += modAmt
            else: # sets to 0 instead of negative number
                Developer.availRolls = 0

            # Update database
            query.updateDevelopersAvailableRolls(mydb, mycursor, Developer.id, Developer.availRolls)
            # Update widgit label
            currRolls.config(text="Current Available Rolls: " + str(Developer.availRolls))

        # ------ Update Avail Rolls Page ------
        Label(frame, text="Update Available Rolls").pack()
        currRolls = Label(frame, text="Current Available Rolls: " + str(Developer.availRolls))
        currRolls.pack()

        # Change available rolls slider
        modScale = Scale(frame, from_=1, to=50, orient=HORIZONTAL)
        modScale.pack()

        # Add button
        Button(frame, text="Add", command=lambda: modAvailRolls(modScale.get())).pack()

        # Subtract button
        Button(frame, text="Subtract", command=lambda: modAvailRolls(modScale.get() * -1)).pack()

        # Back button
        Button(frame, text="Back", command=lambda: Developer.menu(Developer.id)).pack()

    def viewOrders():
        clear_frame()
        # Display header
        Label(frame, text="View Orders").pack()

        # called on slider value change, refreshes tree with developers with enough available rolls
        def refresh_order_tree(choice):
            # clear all items in tree
            for item in my_tree.get_children():
                my_tree.delete(item)

            # display either all orders or current orders, depending on radio buttons
            if choice == 0:
                orderData = query.getDeveloperOrderHistory(mydb, mycursor, Developer.id)
            else:
                orderData = query.getDeveloperCurrentOrders(mydb, mycursor, Developer.id)
            # Add data to tree
            i = 0
            for record in orderData:
                my_tree.insert(parent='', index='end', iid=i, values=record)
                i+=1
        
        # Create radio buttons
        option = IntVar()
        option.set("All Orders")
        button1 = Radiobutton(frame, text="All Orders", variable=option, value=0, command=lambda: refresh_order_tree(0))
        button1.pack(anchor=CENTER)
        button1.select()
        Radiobutton(frame, text="Current Orders", variable=option, value=1, command=lambda: refresh_order_tree(1)).pack(anchor=CENTER)

        # Create treeview frame
        tree_frame = Frame(frame)
        tree_frame.pack(pady=10)
        # initialize tree
        my_tree = get_initialized_tree(tree_frame)
        my_tree.pack()
        # Define our columns
        my_tree['columns'] = ("CustomerName", "Quantity", "TotalPrice", "DatePlaced", "DateDelivered", "OrderStatus", "Link")
        # Format our columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("CustomerName", anchor=CENTER, width=150)
        my_tree.column("Quantity", anchor=CENTER, width=60)
        my_tree.column("TotalPrice", anchor=CENTER, width=70)
        my_tree.column("DatePlaced", anchor=CENTER, width=140)
        my_tree.column("DateDelivered", anchor=CENTER, width=140)
        my_tree.column("OrderStatus", anchor=CENTER, width=140)
        my_tree.column("Link", anchor=W, width=200)
        # Create headings
        my_tree.heading("CustomerName", text="Customer Name", anchor=CENTER)
        my_tree.heading("Quantity", text="Quantity", anchor=CENTER)
        my_tree.heading("TotalPrice", text="Total Price", anchor=CENTER)
        my_tree.heading("DatePlaced", text="Date Placed", anchor=CENTER)
        my_tree.heading("DateDelivered", text="Date Delivered", anchor=CENTER)
        my_tree.heading("OrderStatus", text="Status", anchor=CENTER)
        my_tree.heading("Link", text="Link", anchor=W)
        
        # initialize order data and refresh tree
        orderData = query.getDeveloperOrderHistory(mydb, mycursor, Developer.id)
        refresh_order_tree(option.get())

        # updates status of selected order with value from dropdown
        def updateStatus(selectedOrder):
            # if nothing selected
            if len(selectedOrder) == 0:
                messagebox.showerror("Change Status", "No order selected. Please select an order before attempting to edit.")
                return
            orderTuple = orderData[int(selectedOrder[0])]
            orderID = orderTuple[7]
            newStatus = clicked.get()
            query.updateOrderStatus(mydb, mycursor, orderID, newStatus)
            # refresh order tree view
            refresh_order_tree(option.get())
            messagebox.showinfo("Change Status", "Successfully updated " + orderTuple[0] + "'s order status to '" + newStatus + "'.")

        def addLink(selectedOrder):
            # if nothing selected
            if len(selectedOrder) == 0:
                messagebox.showerror("Change Status", "No order selected. Please select an order before attempting to edit.")
                return
            orderTuple = orderData[int(selectedOrder[0])]
            orderID = orderTuple[7]
            newLink = linkInput.get()
            query.updateOrderLink(mydb, mycursor, orderID, newLink)
            # refresh order tree view
            refresh_order_tree(option.get())
            messagebox.showinfo("Change Status", "Successfully updated " + orderTuple[0] + "'s link to receive their film.")

        # Create dropdown order status selection
        options = [
            "PENDING",
            "RECEIVED",
            "DEVELOPED",
            "SCANNED",
            "SENT"
        ]
        clicked = StringVar()
        drop = OptionMenu(frame, clicked, *options).pack()
        clicked.set("PENDING")

        # Update Status button
        Button(frame, text="Update Order Status", command=lambda: updateStatus(my_tree.selection())).pack()

        ttk.Separator(frame, orient=HORIZONTAL).pack(fill='x', pady=5)

        # Add Link text entry field
        Label(frame, text="Add Link to Film:").pack()
        linkInput = Entry(frame, width=30)
        linkInput.pack()

        # Add Link button
        Button(frame, text="Add Link", command=lambda: addLink(my_tree.selection())).pack()

        ttk.Separator(frame, orient=HORIZONTAL).pack(fill='x', pady=5)

        # Back button
        Button(frame, text="Back", command=lambda: Developer.menu(Developer.id)).pack()




##### ----------------- CUSTOMER -----------------
class Customer:
    id = -1
    name = ""
    email = ""
    address = ""

    def menu(id):
        clear_frame()

        # query customer info from db
        customer_info_tuple = query.getCustomerAttributes(mydb, mycursor, id)
        # store info locally
        (Customer.id, Customer.name, Customer.email, Customer.address) = customer_info_tuple

        # Display info
        Label(frame, text="Customer Menu").pack()
        Label(frame, text="Welcome, "+Customer.name).pack()
        Label(frame, text="ID: "+str(Customer.id)).pack()
        Label(frame, text="Name: "+Customer.name).pack()
        Label(frame, text="Address: "+Customer.address).pack()

        # Display options
        Label(frame, text="Options").pack()
        # View History
        Button(frame, text="View History", command=Customer.view_history).pack()
        # View Store
        Button(frame, text="View Store", command=Customer.view_store).pack()
        # Place Order
        Button(frame, text="Place Order", command=Customer.place_order).pack()
        # Update Account Info
        Button(frame, text="Update Account Info", command=Customer.update_account).pack()
        # Delete Account
        Button(frame, text="Delete Account", command=Customer.delete_account).pack()

        # Back button
        Button(frame, text="Back", command=Welcome.welcome).pack()
        # Quit button
        Button(frame, text="Quit", command=root.quit).pack()

    def view_history():
        clear_frame()
        # Display header
        Label(frame, text="View History").pack()
        # views purchase history or order history, user selects which one

        # define variable to hold selected value
        option = IntVar()
        option.set("Purchases")
        # create radiobuttons
        Radiobutton(frame, text="Purchases", variable=option, value=0).pack(anchor=CENTER)
        Radiobutton(frame, text="Orders", variable=option, value=1).pack(anchor=CENTER)

        def on_go_button_clicked():
            choice = option.get()
            if choice == 0:
                Customer.view_purchase_history(tree_frame)
            else:
                Customer.view_order_history(tree_frame)

        myButton = Button(frame, text="Go", command=on_go_button_clicked)
        myButton.pack()
        # Create treeview frame
        tree_frame = Frame(frame)
        tree_frame.pack(pady=10)
        # Back button
        Button(frame, text="Back", command=lambda: Customer.menu(Customer.id)).pack()
        # Quit button
        Button(frame, text="Quit", command=root.quit).pack()

    def view_purchase_history(tree_frame):
        # clear tree frame before adding data
        for widgets in tree_frame.winfo_children():
            widgets.destroy()

        # ------------ SET UP TREE -----------------
        my_tree = get_initialized_tree(tree_frame)
        my_tree.pack()

        # Define our columns
        my_tree['columns'] = ("Date", "Name", "Quantity", "TotalPrice")

        # Format our columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Date", anchor=W, width=140)
        my_tree.column("Name", anchor=W, width=250)
        my_tree.column("Quantity", anchor=CENTER, width=60)
        my_tree.column("TotalPrice", anchor=CENTER, width=70)

        # Create headings
        my_tree.heading("Date", text="Date Purchased", anchor=W)
        my_tree.heading("Name", text="Product Name", anchor=W)
        my_tree.heading("Quantity", text="Quantity", anchor=CENTER)
        my_tree.heading("TotalPrice", text="Total Price", anchor=CENTER)
        # ------------------------------------------

        # query to get all product tuples from db in format (date, name, quantity, price)
        purchase_data = query.getPurchaseHistory(mydb, mycursor, Customer.id)
        # Add data to tree
        i = 0
        for record in purchase_data:
            # total price = quantity * price
            total_price = record[2] * record[3]
            my_tree.insert(parent='', index='end', iid=i, values=(record[0], record[1], record[2], "$"+str(total_price)))
            i+=1
    
    def view_order_history(tree_frame):
        # clear tree frame before adding data
        for widgets in tree_frame.winfo_children():
            widgets.destroy()

        # ------------ SET UP TREE -----------------
        my_tree = get_initialized_tree(tree_frame)
        my_tree.pack()

        # Define our columns
        my_tree['columns'] = ("DevName", "Quantity", "TotalPrice", "DatePlaced", "DateDelivered", "OrderStatus", "Link")

        # Format our columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("DevName", anchor=W, width=150)
        my_tree.column("Quantity", anchor=CENTER, width=60)
        my_tree.column("TotalPrice", anchor=CENTER, width=70)
        my_tree.column("DatePlaced", anchor=W, width=140)
        my_tree.column("DateDelivered", anchor=W, width=140)
        my_tree.column("OrderStatus", anchor=W, width=140)
        my_tree.column("Link", anchor=W, width=200)

        # Create headings
        my_tree.heading("DevName", text="Developer", anchor=W)
        my_tree.heading("Quantity", text="# Rolls", anchor=CENTER)
        my_tree.heading("TotalPrice", text="Total Price", anchor=CENTER)
        my_tree.heading("DatePlaced", text="Date Placed", anchor=W)
        my_tree.heading("DateDelivered", text="Date Delivered", anchor=W)
        my_tree.heading("OrderStatus", text="Order Status", anchor=W)
        my_tree.heading("Link", text="Link to Photos", anchor=W)
        # ------------------------------------------

        # query to get all order tuples from db in format (developer name, quantity, price, date placed, date delivered, link)
        order_data = query.getCustomerOrderHistory(mydb, mycursor, Customer.id)
        # Add data to tree
        i = 0
        for record in order_data:
            my_tree.insert(parent='', index='end', iid=i, values=record)
            i+=1

    def view_store():
        clear_frame()
        # Display header
        Label(frame, text="View Store").pack()
        Label(frame, text="Select a product below and click the Purchase button to purchase.").pack()

        # ------------ SET UP TREE -----------------
        # Create treeview frame
        tree_frame = Frame(frame)
        tree_frame.pack(pady=10)

        my_tree = get_initialized_tree(tree_frame)
        my_tree.pack()

        # Define our columns
        my_tree['columns'] = ("Name", "Description", "Price")

        # Format our columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Name", anchor=W, width=250)
        my_tree.column("Description", anchor=W, width=400)
        my_tree.column("Price", anchor=CENTER, width=60)

        # Create headings
        my_tree.heading("Name", text="Product Name", anchor=W)
        my_tree.heading("Description", text="Description", anchor=W)
        my_tree.heading("Price", text="Price", anchor=CENTER)
        # ------------------------------------------

        # query to get all product tuples from db
        product_data = query.getAllProductTuples(mydb, mycursor)
        # Add data to tree
        i = 0
        for record in product_data:
            my_tree.insert(parent='', index='end', iid=i, values=(record[1], record[2], "$"+str(record[3])))
            i+=1
        # quantity slider
        quantity_slider = Scale(frame, from_=1, to=20, orient=HORIZONTAL, length=200)
        quantity_slider.pack()

        # purchase product function triggered by purchase button
        def purchase_product():
            selection = my_tree.selection()
            if len(selection) == 0:
                messagebox.showerror("Product Purchase", "No product selected. Please select a product before purchasing.")
                return
            # get product_tuple from selection
            product_tuple = product_data[int(selection[0])]
            product_id = product_tuple[0]
            quantity = quantity_slider.get()
            decision = messagebox.askyesno("Product Purchase", "Are you sure you would like to purchase " + str(quantity) + " of item \"" + product_tuple[1] + "\"?")
            if decision:
                # query to create purchase in db
                query.createPurchase(mydb, mycursor, Customer.id, product_id, get_curr_datetime(), quantity)
                messagebox.showinfo("Product Purchase", "Successfully purchased " + str(quantity) + " of item \"" + product_tuple[1] + "\".")

        # Purchase button
        Button(frame, text="Purchase Item", command=purchase_product).pack()
        # Back button
        Button(frame, text="Back", command=lambda: Customer.menu(Customer.id)).pack()
        # Quit button
        Button(frame, text="Quit", command=root.quit).pack()

    def place_order():
        clear_frame()
        # Display header
        Label(frame, text="Place Order").pack()
        Label(frame, text="Enter number of rolls you would like to have developed. Then select Find Developers.\nThen choose a developer and select Place Order.").pack()

        # called on slider value change, refreshes tree with developers with enough available rolls
        def refresh_developer_tree(num_rolls):
            # clear all items in tree
            for item in my_tree.get_children():
                my_tree.delete(item)
            # query to get all product tuples from db
            developer_data = query.getAllDeveloperTuplesWithEnoughAvailableRolls(mydb, mycursor, num_rolls)
            # Add data to tree
            i = 0
            for record in developer_data:
                my_tree.insert(parent='', index='end', iid=i, values=(record[1], record[2], record[3], str(record[4])))
                i+=1

        # quantity slider
        num_rolls_slider = Scale(frame, from_=1, to=10, orient=HORIZONTAL, command=refresh_developer_tree)
        num_rolls_slider.pack()

        # Create treeview frame
        tree_frame = Frame(frame)
        tree_frame.pack(pady=10)
        # initialize tree
        my_tree = get_initialized_tree(tree_frame)
        my_tree.pack()
        # Define our columns
        my_tree['columns'] = ("Name", "Email", "Address", "AvailRolls")
        # Format our columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Name", anchor=W, width=150)
        my_tree.column("Email", anchor=W, width=200)
        my_tree.column("Address", anchor=W, width=250)
        my_tree.column("AvailRolls", anchor=CENTER, width=80)
        # Create headings
        my_tree.heading("Name", text="Developer Name", anchor=W)
        my_tree.heading("Email", text="Developer Email", anchor=W)
        my_tree.heading("Address", text="Developer Address", anchor=W)
        my_tree.heading("AvailRolls", text="Available Rolls", anchor=CENTER)

        # initially fill developer tree with default 1 roll
        refresh_developer_tree(1)

        # places order with selected developer
        def place_order():
            quantity = num_rolls_slider.get()
            developer_data = query.getAllDeveloperTuplesWithEnoughAvailableRolls(mydb, mycursor, quantity)
            selection = my_tree.selection()
            if len(selection) == 0:
                messagebox.showerror("Place Order", "No developer selected. Please select a developer before placing order.")
                return
            # get developer_tuple from selection
            developer_tuple = developer_data[int(selection[0])]
            developer_id = developer_tuple[0]
            # cost of a roll is $10
            total_cost = quantity * 10.00
            cost_str = ("%.2f" % total_cost)
            decision = messagebox.askyesno("Product Purchase", "Are you sure you would like to have " + str(quantity) + " roll(s) developed by " + developer_tuple[1] + " for $" + cost_str + "?")
            if decision:
                # query to decrement available rolls for developer in db
                query.decrementAvailableRollsForDeveloper(mydb, mycursor, developer_id, quantity)
                # query to create order in db
                query.createOrder(mydb, mycursor, Customer.id, developer_id, get_curr_datetime(), quantity, total_cost)
                # refresh developer tree view
                refresh_developer_tree(quantity)
                messagebox.showinfo("Product Purchase", "Successfully placed order for " + str(quantity) + " roll(s) developed by " + developer_tuple[1] + " for $" + cost_str + ".")



        # Place order button
        Button(frame, text="Place Order", command=place_order).pack()
        # Back button
        Button(frame, text="Back", command=lambda: Customer.menu(Customer.id)).pack()
        # Quit button
        Button(frame, text="Quit", command=root.quit).pack()

    def update_account():
        clear_frame()
        # Display header
        Label(frame, text="Update Account Info").pack()

        # Display entry fields
        # Name
        Label(frame, text="First and Last Name").pack()
        e_name = Entry(frame, width=50)
        e_name.pack()
        e_name.insert(0, Customer.name)
        # Email
        Label(frame, text="Email").pack()
        e_email = Entry(frame, width=50)
        e_email.pack()
        e_email.insert(0, Customer.email)
        # Address
        Label(frame, text="Address").pack()
        e_address = Entry(frame, width=50)
        e_address.pack()
        e_address.insert(0, Customer.address)

        # called when Save button is clicked. Checks if id is valid
        def on_save_button_click():
            # save locally
            Customer.name = e_name.get()
            Customer.email = e_email.get()
            Customer.address = e_address.get()
            # run query to update record in db
            query.updateCustomerAttributes(mydb, mycursor, Customer.id, Customer.name, Customer.email, Customer.address)
            # display success message
            messagebox.showinfo("Update Account", "Account information successfully updated.")
            Customer.menu(Customer.id)
        # Go button
        Button(frame, text="Save", command=on_save_button_click).pack()

        # Back button
        Button(frame, text="Back", command=lambda: Customer.menu(Customer.id)).pack()
        # Quit button
        Button(frame, text="Quit", command=root.quit).pack()

    def delete_account():
        # open pop-up window
        response = messagebox.askyesno("Delete Account", "Are you sure you would like to delete this account? This action cannot be undone.")
        if response == 1:
            query.deleteCustomer(mydb, mycursor, Customer.id)
            messagebox.showinfo("Delete Account", "Account successfully deleted.")
            Welcome.welcome()






##### ----------------- MAIN PROGRAM -----------------

argv = sys.argv #store command line arguments
if len(argv) < 3:#ensure there are at least 3 command line arguments 
    print("Username and then password should be input as command line arguments for MySQL.")
    sys.exit()#quit the executable 

list = database.startDB(argv[1], argv[2])
mydb = list[0]
mycursor = list[1]

# header
Label(root, text="Z41 Database App", font="Arial 32 bold").pack()

# create frame
frame = LabelFrame(root)
frame.pack(side="top", padx=10, pady=10, fill="both")

# display welcome
Welcome.welcome()
root.mainloop()

print("Closing the database connection")
database.endDB(mydb)