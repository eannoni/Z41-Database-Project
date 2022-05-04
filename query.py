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
        SELECT CustomerID 
        FROM Customer
        WHERE Name = '''
        query2 += "\'" + name + "\' AND Email = \'" + email + "\' AND Address = \'" + address + "\';"
        mycursor.execute(query2)
        return mycursor.fetchone()[0]

    # TODO: take in ID and return tuple of attributes belonging to the customer
    def getCustomerAttributes(mydb, mycursor, id):
        # add query here
        return mycursor.fetchone()