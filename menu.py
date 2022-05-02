from tkinter import *

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
        # TODO: RUN QUERY
        return True


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
        # TODO: RUN QUERY
        return True

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
        return 1001 # TODO: RETURN ACTUAL ID



##### ----------------- DEVELOPER -----------------
class Developer:
    def menu(id):
        clear_frame()
        Label(frame, text="Developer Menu").pack()
        Label(frame, text="Welcome, Developer " + id).pack()
        # Back button
        Button(frame, text="Back", command=Welcome.welcome).pack()
        # Quit button
        Button(frame, text="Quit", command=root.quit).pack()



##### ----------------- CUSTOMER -----------------
class Customer:
    def menu(id):
        clear_frame()
        Label(frame, text="Customer Menu").pack()
        Label(frame, text="Welcome, Customer " + str(id)).pack()
        # Back button
        Button(frame, text="Back", command=Welcome.welcome).pack()
        # Quit button
        Button(frame, text="Quit", command=root.quit).pack()



##### ----------------- MAIN PROGRAM -----------------

# header
Label(root, text="Z41 Database App", font="Arial 32 bold").pack()

# create frame
frame = LabelFrame(root)
frame.pack(side="top", padx=10, pady=10, fill="both")

# display welcome
Welcome.welcome()
root.mainloop()