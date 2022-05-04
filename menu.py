# tkinter imports
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from query import query
from database import database

import sys
import time

root = Tk()
root.title("Z41 Demo")
root.geometry("800x500")

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



##### ----------------- WELCOME -----------------
class Welcome:
    # clears frame and populates
    def welcome():
        clear_frame()
        Label(frame, text="Are you a Developer or a Customer?").pack()
        Button(frame, text="Developer", command=Welcome.developer).pack()
        Button(frame, text="Customer", command=Welcome.customer).pack()
        # View Premium Customers (Premium is purchase total of > $100)
        Button(frame, text="View Premium Customers", command=Welcome.view_premium_customers).pack()
        # Quit button
        Button(frame, text="Quit", command=root.quit).pack()


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
            my_tree.insert(parent='', index='end', iid=i, values=(premium_customer_data[i][0], "$"+str(premium_customer_data[i][1])))
            i+=1

        # Back button
        Button(frame, text="Back", command=Welcome.welcome).pack()



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
            Developer.availRolls += modAmt
            if Developer.availRolls < 0: #prevents negative val and instead sets to 0
                Developer.availRolls = 0

            # Update DB
            query.updateDeveloperAttributes(mydb, mycursor, Developer.id, Developer.name, Developer.email, Developer.address, Developer.availRolls)

        # ------ Update Avail Rolls Page ------
        Label(frame, text="Update Available Rolls").pack()
        Label(frame, text="Current Available Rolls: " + str(Developer.availRolls)).pack()

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

        # ------ View Order Helper Functions ------
        def showOrders():
            if dropSelection.get() == "All Orders":
                print("showing all orders")
                # TODO: show all dev's order with given tuple
            else: #current orders
                print("showing current orders")
                # TODO: show current dev's order with given tuple

        # ------ View Order Page ------
        Label(frame, text="View Orders").pack()

        # View Option Drop Down
        dropSelection = StringVar()
        dropSelection.set("All Orders") #set default dropdown selection
        drop = OptionMenu(frame, dropSelection, "All Orders", "Current Orders").pack()

        # View button (for the selected view type)
        Button(frame, text="View", command=showOrders).pack()

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
        Radiobutton(frame, text="Purchases", variable=option, value=0).pack(anchor=W)
        Radiobutton(frame, text="Orders", variable=option, value=1).pack(anchor=W)

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
            my_tree.insert(parent='', index='end', iid=i, values=(purchase_data[i][0], purchase_data[i][1], purchase_data[i][2], "$"+str(total_price)))
            i+=1
    
    def view_order_history(tree_frame):
        # clear tree frame before adding data
        for widgets in tree_frame.winfo_children():
            widgets.destroy()

        # ------------ SET UP TREE -----------------
        my_tree = get_initialized_tree(tree_frame)
        my_tree.pack()

        # Define our columns
        my_tree['columns'] = ("DevName", "Quantity", "TotalPrice", "DatePlaced", "DateDelivered", "Link")

        # Format our columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("DevName", anchor=W, width=150)
        my_tree.column("Quantity", anchor=CENTER, width=60)
        my_tree.column("TotalPrice", anchor=CENTER, width=70)
        my_tree.column("DatePlaced", anchor=W, width=140)
        my_tree.column("DateDelivered", anchor=W, width=140)
        my_tree.column("Link", anchor=W, width=200)

        # Create headings
        my_tree.heading("DevName", text="Developer", anchor=W)
        my_tree.heading("Quantity", text="# Rolls", anchor=CENTER)
        my_tree.heading("TotalPrice", text="Total Price", anchor=CENTER)
        my_tree.heading("DatePlaced", text="Date Placed", anchor=W)
        my_tree.heading("DateDelivered", text="Date Delivered", anchor=W)
        my_tree.heading("Link", text="Link to Photos", anchor=W)
        # ------------------------------------------

        # query to get all order tuples from db in format (developer name, quantity, price, date placed, date delivered, link)
        order_data = query.getOrderHistory(mydb, mycursor, Customer.id)
        # Add data to tree
        i = 0
        for record in order_data:
            my_tree.insert(parent='', index='end', iid=i, values=order_data[i])
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
            my_tree.insert(parent='', index='end', iid=i, values=(product_data[i][1], product_data[i][2], "$"+str(product_data[i][3])))
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