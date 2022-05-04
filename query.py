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
        UPDATE TABLE Customer(Name, Email, Address)
        SET Name = ''' + "'" + name + "'" + "AND Email = '" + email + "' AND Address = '" + address + "'" + '''
        WHERE CustomerID = ''' + str(id) + ";"
        mycursor.execute(query)
        mydb.commit()
    
    def updateDeveloperAttributes(mydb, mycursor, id, name, email, address):
        query = '''
        UPDATE TABLE Developer(Name, Email, Address)
        SET Name = ''' + "'" + name + "'" + "AND Email = '" + email + "' AND Address = '" + address + "'" + '''
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
