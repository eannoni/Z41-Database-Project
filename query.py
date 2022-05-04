class query:
    def checkValidDeveloperID(mydb, mycursor, ID):
        query = '''
        SELECT COUNT(*)
        FROM Developer
        WHERE DeveloperID = '''
        query += ID + ";"
        mycursor.execute(query)
        count = mycursor.fetchone()[0]
        if count > 0:
            return True
        else:
            return False

    def checkValidCustomerID(mydb, mycursor, ID):
        query = '''
        SELECT COUNT(*)
        FROM Customer
        WHERE CustomerID = '''
        query += ID + ";"
        mycursor.execute(query)
        count = mycursor.fetchone()[0]
        if count > 0:
            return True
        else:
            return False
    
    def createNewCustomerAndGetID(mydb, mycursor, name, email, address):
        query = '''
        INSERT INTO Customer(Name, Email, Address) 
        VALUES ('''
        query += "\'" + name + "\', \'" + email + "\', \'" + address + "\');"
        mycursor.execute(query)
        mydb.commit()
        query2 = '''
        SELECT LAST_INSERT_ID() 
        FROM Customer;'''
        mycursor.execute(query2)
        return mycursor.fetchall()[0][0]

    def getCustomerAttributes(mydb, mycursor, id):
        # add query here
        query = '''
        SELECT CustomerID, Name, Email, Address
        FROM Customer
        WHERE CustomerID = '''
        query += str(id) + ";"
        mycursor.execute(query)
        return mycursor.fetchone()
        

    def updateCustomerAttributes(mydb, mycursor, id, name, email, address):
        query = '''
        UPDATE Customer
        SET Name = ''' + "'" + name + "'" + ", Email = '" + email + "', Address = '" + address + "'" + '''
        WHERE CustomerID = ''' + str(id) + ";"
        mycursor.execute(query)
        mydb.commit()
    
    def updateDeveloperAttributes(mydb, mycursor, id, name, email, address):
        query = '''
        UPDATE Developer
        SET Name = ''' + "'" + name + "'" + ", Email = '" + email + "', Address = '" + address + "'" + '''
        WHERE DeveloperID = ''' + str(id) + ";"
        mycursor.execute(query)
        mydb.commit()

    def deleteCustomer(mydb, mycursor, id):
        query = '''
        DELETE FROM Customer
        WHERE CustomerID = ''' + str(id) + ";"
        mycursor.execute(query)
        mydb.commit()

    def getDeveloperAttributes(mydb, mycursor, id):
        query = '''
        SELECT DeveloperID, Name, Email, Address, AvailableRolls
        FROM Developer
        WHERE DeveloperID = ''' + str(id) + ";"
        mycursor.execute(query)
        return mycursor.fetchone()

    # UNTESTED
    def updateDevelopersAvailableRolls(mydb, mycursor, id, value):
        query = '''
        UPDATE Developer 
        SET AvailableRolls = ''' + str(value) + '''
        WHERE DeveloperID = ''' + str(id) + ";"
        mycursor.execute(query)
        mydb.commit()

    # UNTESTED
    def updateOrderStatus(mydb, mycursor, id, status):
        query = '''
        UPDATE FilmOrder
        SET Status = ''' + str(status) + '''
        WHERE OrderID = ''' + str(id) + ";"
        mycursor.execute(query)
        mydb.commit()

    # UNTESTED
    def updateOrderLink(mydb, mycursor, id, link):
        query = '''
        UPDATE FilmOrder
        SET Link = ''' + str(link) + '''
        WHERE OrderID = ''' + str(id) + ";"
        mycursor.execute(query)
        mydb.commit()

    # UNTESTED
    def getAllDeveloperTuples(mydb, mycursor):
        query = '''SELECT * FROM Developer;'''
        mycursor.execute(query)
        return mycursor.fetchall()

    def getAllProductTuples(mydb, mycursor):
        query = '''SELECT * FROM Product;'''
        mycursor.execute(query)
        return mycursor.fetchall()

    # UNTESTED
    def decrementAvailableRollsForDeveloper(mydb, mycursor, id, rollsToRemove):
        mycursor.execute("SELECT AvailableRolls FROM Developer WHERE DeveloperID = " + str(id) + ";")
        count = mycursor.fetchone()[0]
        result = count - rollsToRemove
        query = '''UPDATE Developer
        SET AvailableRolls = ''' + str(result) + '''
        WHERE DeveloperID = ''' + str(id) + ";"
        mycursor.execute(query)
        mydb.commit()

    # UNTESTED
    def createOrder(mydb, mycursor, custID, devID, status, datePlaced, Quantity, Price):
        query = '''
        INSERT INTO FilmOrder(CustomerID, DeveloperID, Status, DatePlaced, Quantity, Price)
        VALUES(''' + str(custID) + ", " + str(devID) + ", '" + str(status) + "', '" + str(datePlaced) + "', " + str(Quantity) + ", " + str(Price) + ");"
        mycursor.execute(query)
        mydb.commit()

    def createPurchase(mydb, mycursor, custID, prodID, date, quantity):
        query = '''
        INSERT INTO Purchase(CustomerID, ProductID, Date, Quantity)
        VALUES(''' + str(custID) + ", " + str(prodID) + ", '" + date + "', " + str(quantity) + ");"
        mycursor.execute(query)
        mydb.commit()