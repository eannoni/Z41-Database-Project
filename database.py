import sys
import mysql.connector

class database:

    def connectToMySQL(username, pw):#return the database object connecting to the correct schema
        return mysql.connector.connect(host = "localhost", user = username, password = pw, auth_plugin = 'mysql_native_password', database = "Z41")

    def ensureTablesExist(mydb, mycursor): 
        #store the queries to create the tables
        tableCreationQueries = [
            '''
            CREATE TABLE IF NOT EXISTS Customer(
                CustomerID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(50) NOT NULL,
                Email VARCHAR(62) NOT NULL,
                Address VARCHAR(95) NOT NULL,
                isDeleted BLOB DEFAULT (0)
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS Product(
                ProductID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(50) NOT NULL,
                Description VARCHAR(280),
                Price DECIMAL(8,2) NOT NULL
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS Purchase(
            PurchaseID INT AUTO_INCREMENT PRIMARY KEY,
            CustomerID INT,
            ProductID INT,
            Date DATETIME NOT NULL,
            Quantity INT NOT NULL,
            FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
            FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS Developer(
                DeveloperID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(50) NOT NULL ,
                Email VARCHAR(62) NOT NULL ,
                Address VARCHAR(95) NOT NULL ,
                AvailableRolls INT NOT NULL
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS FilmOrder(
                OrderID INT AUTO_INCREMENT PRIMARY KEY,
                CustomerID INT,
                DeveloperID INT,
                Status VARCHAR(20) NOT NULL ,
                DatePlaced DATETIME NOT NULL ,
                DateDelivered DATETIME,
                Link VARCHAR(40),
                Quantity INT NOT NULL ,
                Price DECIMAL(8,2) ,
                FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
                FOREIGN KEY (DeveloperID) REFERENCES Developer(DeveloperID)
            );
            '''
        ]
        #execute the queries
        for query in tableCreationQueries:
            mycursor.execute(query)
            mydb.commit()

    def insertDataIfEmptyTables(mydb, mycursor):
        #set the tables, and the values to insert into them into a dictionary
        tables = {
            "Customer": '''
                        INSERT INTO Customer(Name, Email, Address) VALUES("Eli Annoni", "annoni@chapman.edu", "1 University Drive Orange, CA 92866"),
                                                                        ("Ian Hakeman", "hakeman@chapman.edu", "1 University Drive Orange, CA 92866"),
                                                                        ("Sierra Clibourne", "clibourne@chapman.edu", "420 Cool Person Drive Orange, CA 92866"),
                                                                        ("Jerry Seinfeld", "seinfeld@gmail.com", "323 South Street Malibu, CA 93714"),
                                                                        ("Rick Astely", "rick@yahoo.com", "7234 N Morgan Street New York, NY 12354"),
                                                                        ("Erik Linstead", "linstead@chapman.edu", "206 Grand Ave Orange, CA 92868"),
                                                                        ("Elizabeth Stevens", "stevens@chapman.edu", "314 Center Street Orange, CA 92868"),
                                                                        ("Chris Rock", "chrisrock@rock.com", "132 East Ketchup Street Los Angeles, CA 93104"),
                                                                        ("Will Smith", "smith@aol.com", "2054 Moon avenue Fresno, CA 93124"),
                                                                        ("Evan Weissbart", "weissbart@chapman.edu", "1120 East Palmyra Ave Orange, CA 92866"),
                                                                        ("Chelsea Parlett", "cparlett@chapman.edu", "1503 Glassell St Orange, CA 92866"),
                                                                        ("Gabriel Garcia", "gabrielgarcia@chapman.edu", "1042 Grand Ave Orange, CA 92866");
                        ''',
            "Developer": '''
                        INSERT INTO Developer(Name, Email, Address, AvailableRolls) VALUES("Curren Taber", "ctaber@chapman.edu", "1 University Drive Orange, CA 92866", 5),
                                                                                        ("Scott Fitzpatrick", "sfitzpatrick@chapman.edu", "915 E Katella Ave Anaheim, CA 92805", 28),
                                                                                        ("Rene German", "german@chapman.edu", "Steak and Lobster Lane Orange, CA 92805", 12),
                                                                                        ("Anthony Foley", "afoley@chapman.edu", "431 Shaffer Ave Orange, CA 92866", 14),
                                                                                        ("Trent Johnson", "tj@glue.com", "412 E Katella Ave Anaheim, CA 92806", 21),
                                                                                        ("Lucy Shupe", "shupe@lmu.edu", "324 Sepulveda Blvd Venice, CA 91165", 11),
                                                                                        ("Sally Sue", "sue@hotmail.edu", "5 West Star Street City Of Industry, CA 91148", 16),
                                                                                        ("Kelly Kapoor", "kapoor@dundermifflin.com", "3 Paper Street Scranton, PA 23415", 13),
                                                                                        ("Kevin Malone", "ashtonkutcher@dundermifflin.com", "3 Paper Street Scranton, PA 23415", 17),
                                                                                        ("Connor Martindale", "martindale@chapman.edu", "123 Disneyland Road Anaheim, CA 92802", 19),
                                                                                        ("Derek Prate", "prate@chapman.edu", "18342 Prate Ave Yorba Linda, CA 92879", 24),
                                                                                        ("Lucas Torti", "torti@chapman.edu", "20 Gehrig Ave Fullerton, CA 92864", 61);
                        ''', 
            "Product": '''
                        INSERT INTO Product(Name, Description, Price) VALUES("Zine41: Winter - Limited Print", NULL, 20.00),
                                                                            ("Liford HP65 35mm 36 Exposure Roll", "35mm film", 7.00),
                                                                            ("Harman EZ35 Reusable Film Camera", "Reusable, motorized camera", 55.00),
                                                                            ("Zine41: Summmer - Limited Print", NULL, 22.00),
                                                                            ("Zine41: Autumn - Limited Print", NULL, 21.00),
                                                                            ("Zine41: Spring - Limited Print", NULL, 20.00),
                                                                            ("Canon 35mm Film", "35mm film", 8.00),
                                                                            ("Nikon 40mm Film", "40mm premium film", 10.00);
            ''',
            "Purchase": '''
                        INSERT INTO Purchase(CustomerID, ProductID, Date, Quantity) VALUES(1, 2, "2022-03-12 08:40:20", 6),
                                                                                        (2, 1, "2022-04-29 14:05:07", 3),
                                                                                        (2, 3, "2022-02-06 12:23:16", 1),
                                                                                        (7, 4, "2022-04-03 09:16:57", 6),
                                                                                        (5, 3, "2022-05-03 22:06:53", 4),
                                                                                        (8, 7, "2022-02-17 20:02:45", 7),
                                                                                        (11, 2, "2022-03-23 17:04:23", 5),
                                                                                        (5, 6, "2022-05-02 14:53:24", 2),
                                                                                        (4, 8, "2022-04-30 15:35:43", 4),
                                                                                        (9, 3, "2022-01-04 03:23:52", 2);
            ''', 
            "FilmOrder": '''
                        INSERT INTO FilmOrder(CustomerID, DeveloperID, Status, DatePlaced, DateDelivered, Link, Quantity, Price) VALUES(1, 2, "SENT", "2022-02-19 08:32:01", "2022-03-01 18:43:23", "https://we.tl/t-PqU2FqsXzF", 8, 80.00),
                                                                                                                                        (2, 1, "RECEIVED", "2022-02-03 07:14:19", NULL, NULL, 5, 50.00),
                                                                                                                                        (2, 3, "DEVELOPED", "2022-04-27 03:52:52", NULL, NULL, 2, 20.00),
                                                                                                                                        (8, 10, "RECEIVED", "2022-05-02 04:56:42", NULL, NULL, 4, 40.00),
                                                                                                                                        (5, 4, "DEVELOPED", "2022-04-14 15:12:04", NULL, NULL, 6, 60.00),
                                                                                                                                        (11, 8, "SENT", "2022-03-04 09:35:25", "2022-04-06 14:26:43", "www.brain.gov", 8, 80.00),
                                                                                                                                        (9, 2, "SENT", "2022-04-02 18:04:26", "2022-04-24 19:34:56", "www.google.com", 9, 90.00),
                                                                                                                                        (6, 7, "DEVELOPED", "2022-05-01 04:30:42", NULL, NULL, 5, 50.00),
                                                                                                                                        (4, 7, "RECEIVED", "2022-05-02 09:20:21", NULL, NULL, 2, 20.00),
                                                                                                                                        (10, 5, "DEVELOPED", "2022-04-30 13:50:39", NULL, NULL, 13, 130.00);
            '''
        } 
        #loop through the dictionary and see if tables are empty, if so, run the insert queries
        for table, query in tables.items():
            mycursor.execute("SELECT COUNT(*) FROM " + table + ";")
            count = mycursor.fetchone()[0]
            if count < 1:#if empty
                mycursor.execute(query)
                mydb.commit()

    def endDB(mydb):
        mydb.commit()
        mydb.close()

    def startDB(username, pw):
        try:#connect to the correct database given username and password
            mydb = database.connectToMySQL(username, pw)
        except:
            try:#if that failed, try to connect and make the schema
                mydb = mysql.connector.connect(host = "localhost", user = username, password = pw, auth_plugin = 'mysql_native_password')
                mycursor = mydb.cursor()
                #create the DB
                mycursor.execute("CREATE SCHEMA Z41;")
                #then try connecting again to the schema we just made
                mydb = database.connectToMySQL(username, pw)
            except:#if that also failed, username and password is wrong
                print("Incorrect password for username", username)
                sys.exit()#quit since we couldn't connect

        #print the connection
        print(mydb)

        #create cursor object to interact with mySQL
        mycursor = mydb.cursor()

        #make the tables if they don't exist
        database.ensureTablesExist(mydb, mycursor)
        print("Tables exist")

        database.insertDataIfEmptyTables(mydb, mycursor)
        print("Tables have starting data in them")

        return [mydb, mycursor]