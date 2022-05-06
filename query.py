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

    def getAllDeveloperTuplesWithEnoughAvailableRolls(mydb, mycursor, numRolls):
        query = '''
        SELECT *
        FROM Developer
        WHERE AvailableRolls >= ''' + str(numRolls) + ";"
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
    def createOrder(mydb, mycursor, custID, devID, datePlaced, Quantity, Price):
        query = '''
        INSERT INTO FilmOrder(CustomerID, DeveloperID, Status, DatePlaced, Quantity, Price)
        VALUES(''' + str(custID) + ", " + str(devID) + ", 'PENDING', '" + str(datePlaced) + "', " + str(Quantity) + ", " + str(Price) + ");"
        mycursor.execute(query)
        mydb.commit()

    def createPurchase(mydb, mycursor, custID, prodID, date, quantity):
        query = '''
        INSERT INTO Purchase(CustomerID, ProductID, Date, Quantity)
        VALUES(''' + str(custID) + ", " + str(prodID) + ", '" + date + "', " + str(quantity) + ");"
        mycursor.execute(query)
        mydb.commit()

    def getPurchaseHistory(mydb, mycursor, custID):
        query = '''
        SELECT Date, Name, Quantity, Price
        FROM Purchase
        INNER JOIN Product
        ON Purchase.ProductID = Product.ProductID
        WHERE CustomerID = ''' + str(custID) + " ORDER BY Purchase.Date DESC;"
        mycursor.execute(query)
        return mycursor.fetchall()

    def getOrderHistory(mydb, mycursor, custID):
        query = '''
        SELECT Developer.Name, Quantity, Price, DatePlaced, DateDelivered, Link
        FROM FilmOrder
        INNER JOIN Developer
        ON FilmOrder.DeveloperID = Developer.DeveloperID
        WHERE CustomerID = ''' + str(custID) + " ORDER BY FilmOrder.DatePlaced DESC;"
        mycursor.execute(query)
        return mycursor.fetchall()
    
    def getCurrentOrders(mydb, mycursor, custID):
        query = '''
        SELECT Developer.Name, Quantity, Price, DatePlaced, DateDelivered, Link
        FROM FilmOrder
        INNER JOIN Developer
        ON FilmOrder.DeveloperID = Developer.DeveloperID
        WHERE CustomerID = ''' + str(custID) + " AND FilmOrder.Status != 'SENT' ORDER BY FilmOrder.DatePlaced DESC;"
        mycursor.execute(query)
        return mycursor.fetchall()

    def getAllPremiumCustomers(mydb, mycursor):
        query = '''
        SELECT Name, TotalSpent
        FROM (
            SELECT Customer.CustomerID, Customer.Name, SUM(Product.Price * Purchase.Quantity) AS TotalSpent
            FROM Customer
            INNER JOIN Purchase
            ON Customer.CustomerID = Purchase.CustomerID
            INNER JOIN Product
            ON Purchase.ProductID = Product.ProductID
            GROUP BY CustomerID
            HAVING SUM(Product.Price * Purchase.Quantity) >= 100
        ) AS PremiumCustomers;'''
        mycursor.execute(query)
        return mycursor.fetchall()