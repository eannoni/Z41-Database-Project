# tkinter imports
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from query import query
from database import database
import sys

root = Tk()
root.title("Z41 Demo")
root.geometry("800x500")

# clear frame
def clear_frame():
   for widgets in frame.winfo_children():
      widgets.destroy()



##### ----------------- WELCOME -----------------
class Welcome:
    # clears frame and populates
    def welcome():
        clear_frame()
        Label(frame, text="Are you a Developer or a Customer?").pack()
        Button(frame, text="Developer", command=Welcome.developer).pack()
        Button(frame, text="Customer", command=Welcome.customer).pack()
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
                Label(frame, text="Could not locate Developer ID", fg="red").pack()
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
                Label(frame, text="Could not locate Customer ID", fg="red").pack()
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

    # TODO: move to query file
    def create_new_customer(name, email, address):
        # TODO: RUN QUERY TO CREATE RECORD
        # TODO: RUN QUERY TO GET ID OF NEW RECORD
        #return 1001 # TODO: RETURN ACTUAL ID
        return query.createNewCustomerAndGetID(mydb, mycursor, name, email, address) # returns ID of new customer




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
        developer_info_tuple = query.getDeveloperAttributes(mydb, mycursor, str(id))
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
        print("Customer ID: ", Customer.id)
        # Back button
        Button(frame, text="Back", command=lambda: Customer.menu(Customer.id)).pack()
        # Quit button
        Button(frame, text="Quit", command=root.quit).pack()

    def view_store():
        clear_frame()
        # Display header
        Label(frame, text="View Store").pack()

        # ------------ SET UP TREE -----------------
        # # Create treeview frame
        # tree_frame = Frame(root)
        # tree_frame.pack(pady=10)

        # # Create treeview scrollbar
        # tree_scroll = Scrollbar(tree_frame)
        # tree_scroll.pack(side=RIGHT, fill=Y)

        # # Create treeview
        # my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        # my_tree.pack()

        # # Configure Scrollbar
        # tree_scroll.config(command=my_tree.yview)

        # # Define our columns
        # my_tree['columns'] = ("Name", "ID", "Favorite Pizza")

        # # Format our columns
        # my_tree.column("#0", width=0, stretch=NO)
        # my_tree.column("Name", anchor=W, width=120)
        # my_tree.column("ID", anchor=CENTER, width=80)
        # my_tree.column("Favorite Pizza", anchor=W, width=120)

        # # Create headings
        # # my_tree.heading("#0", text="")
        # my_tree.heading("Name", text="Name", anchor=W)
        # my_tree.heading("ID", text="ID", anchor=CENTER)
        # my_tree.heading("Favorite Pizza", text="Favorite Pizza", anchor=W)
        # ------------------------------------------

        #TODO: QUERY TO GET ALL PRODUCTS
        products = [
            [1001, "z41 Zine", "Magazine thingy", 20.00],
            [1002, "16mm Roll", "New film roll", 15.00],
            [1002, "8mm Roll", "A different film roll", 12.00]
        ]
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