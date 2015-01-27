# Victor Lin, A2, vlin6@gatech.edu, 903004194
#"I worked on the homework assignment alone, using only this semester's course materials."
#"I used Dr. Summet's DMSI course notes for downloading images and for SQLs."
#"http://www.summet.com/dmsi/html/guiProgramming.html#adding-images-to-your-gui, http://www.summet.com/dmsi/html/pymysql.html#sql-fundamentals"

from tkinter import *
import urllib.request
import pymysql


# HW 9a ========================================================================================================================================

class LoginPage:

    def __init__(self, rootWin):
        self.mainWin = rootWin
        self.LoginPage()
        self.register()
        self.loginUp()
        
        #Remove this test run later:
 #       self.v1a.set("gburdell3")
 #       self.v1b.set("Password123")
        
    def LoginPage(self):
        
        #Get an image from the website below and uses it as the logo.
        url = "http://content.sportslogos.net/logos/31/690/thumbs/2492.gif"
        response = urllib.request.urlopen(url)
        myPicture = response.read()
        import base64
        b64_data = base64.encodebytes(myPicture)

        self.photo1 = PhotoImage(data=b64_data)

        Label(self.mainWin, image=self.photo1).grid(column = 1)
        
        self.mainWin.title("Login")

        #Sets up the rest of the GUI.
        Label (self.mainWin, text = "Username").grid(row = 1, sticky = E)
        self.v1a = StringVar()
        Entry (self.mainWin, width = 30, textvariable = self.v1a).grid(row = 1, column = 1)

        Label (self.mainWin, text = "Password").grid(row = 2, sticky = E)
        self.v1b = StringVar()
        Entry (self.mainWin, width = 30, textvariable = self.v1b).grid(row = 2, column = 1)

        
        Button (self.mainWin, text = "Register", command = self.regisUp).grid(row = 3, column = 1, sticky = E)
        Button (self.mainWin, text = "Login", command = self.LoginCheck).grid(row = 3, column = 2)

    def register(self):
        #Creates a second window.
        self.secondWin = Toplevel()
        self.secondWin.title ("GtPizza New User Registration")

        #Get an image from the website below and uses it as the logo.
        url = "http://content.sportslogos.net/logos/31/690/thumbs/2492.gif"
        response = urllib.request.urlopen(url)
        myPicture = response.read()
        import base64
        b64_data = base64.encodebytes(myPicture)

        self.photo2 = PhotoImage(data=b64_data)

        Label(self.secondWin, image=self.photo2).grid(column = 1)

        
        Label (self.secondWin, text = "First Name").grid(row = 1, sticky = W)
        self.v2a = StringVar()
        Entry (self.secondWin, width = 30, textvariable = self.v2a).grid(row = 1, column = 1)

        Label (self.secondWin, text = "Username").grid(row = 2, sticky = W)
        self.v2b = StringVar()
        Entry (self.secondWin, width = 30, textvariable = self.v2b).grid(row = 2, column = 1)
        
        Label (self.secondWin, text = "Password").grid(row = 3, sticky = W)
        self.v2c = StringVar()
        Entry (self.secondWin, width = 30, textvariable = self.v2c).grid(row = 3, column = 1)

        Label (self.secondWin, text = "Confirm Password").grid(row = 4, sticky = W)
        self.v2d = StringVar()
        Entry (self.secondWin, width = 30, textvariable = self.v2d).grid(row = 4, column = 1)

        Button (self.secondWin, text = "Cancel", command = self.loginUp).grid(row = 5, column = 1, sticky = E)
        Button (self.secondWin, text = "Register", command = self.RegisterNew).grid(row = 5, column = 2)

    def loginUp(self):
        self.secondWin.withdraw()
        self.mainWin.deiconify()

    def regisUp(self):
        self.mainWin.withdraw()
        self.secondWin.deiconify()

    #Checks if what is typed into the page matches any users currently in the database.
    #Call connect method, create a cursor from the database connection that is returned.
    #Check what was passed to see if any matches are returned. Pop a messagebox for a match, pop one if it doesn't.
    #Test run: gburdell3, Password123.
    def LoginCheck(self):
        db = self.connect()
        cursor = db.cursor()
        sql = "SELECT * FROM PizzaUsers WHERE USERNAME =%s AND Password =%s"
        num = cursor.execute(sql, (self.v1a.get(), self.v1b.get()))
        if num == 0:
            messagebox.showwarning("Failure", "Username and password pair does not exist!")
        else:
            messagebox.showinfo("Success", "Login successful!")
##            tup = cursor.fetchone()
##            self.firstname = tup[1]
            self.HomePage()
            self.mainWin.withdraw()

        cursor.close()
        db.commit()
        db.close()

    def connect(self):
       try:
            db = pymysql.connect( host = "academic-mysql.cc.gatech.edu", user = "vlin6",
                          passwd = "dwcPTX9A", db = "cs2316db")
            return db
       except:
            messagebox.showerror("Error", "Check your internet connection!")

    #Check: 1) username (under 20 char) and password filled (first name entry can be left blank)
    #       2) password contains at least one number and one uppercase letter
    #       3) passwords match
    #       4) username already exists, 
    #Insert into data. Pop a message box if registration is successful, hide registration window, display login window.
    #.commit()!
    def RegisterNew(self):
        #self.v2a is first name, self.v2b is username, self.v2c is password, self.v2d is password check. 

        firstname = self.v2a.get()

        username = self.v2b.get()
        usernameOK = False
        #Username check (under 20 char).
        if len(self.v2b.get()) < 20 and len(self.v2b.get()) > 0:

            #Check if username is already in data base.
            db = self.connect()
            cursor = db.cursor()
            sql = "SELECT * FROM PizzaUsers WHERE USERNAME =%s"
            num = cursor.execute(sql, (username))
            cursor.close()
            db.commit()
            if num != 0:
                messagebox.showerror("Error", "Username already in database!")
            else:
                usernameOK = True
                
            
        else:
            messagebox.showerror("Error", "Make sure you type in a user name under 20 characters.")

        #Password check.
        password = self.v2c.get()
        password2 = self.v2d.get()
        passwordOK = False
        if len(password) > 0 and len(password) < 20:
           
            #Checks if passwords match.
            if password == password2:
                
                #Checks if password contains at least one number and one uppercase letter
                oneNum = False; oneUp = False
                numStr = "1234567890"; capStr = "QWERTYUIOPASDFGHJKLZXCVBNM"

                for char in password:
                    if char in numStr:
                        oneNum = True
                    if char in capStr:
                        oneUp = True

                if oneNum == True and oneUp == True:
                    passwordOK = True

                else:
                    messagebox.showerror("Error", "Your password must contain at least one uppercase letter and one number.")
                                   
            else:
                messagebox.showerror("Error", "Your passwords do not match.")
                
        else:
            messagebox.showerror("Error", "Make sure you type in a password.")

        #Insert into data.
        if usernameOK == True and passwordOK == True:
            db = self.connect()
            cursor = db.cursor()
            sql = "INSERT INTO PizzaUsers (USERNAME, FirstName, Password) VALUES (%s, %s, %s)"
            if firstname == "":
                firstname = None
            cursor.execute(sql,(username, firstname, password))
            cursor.close()
            db.commit()
            messagebox.showinfo("Success!", "Registration successful!")
            self.loginUp()
            
# HW 9b ===================================================================================================================================

#aim: 1) GUI 1 is a 'GtPizza Homepage' ordering page, on which users place an order.
#2) GUI 2 is a 'Statistics Page'
#databased used: PizzaOrders, OrderID, User, Cheese, Pepperoni, Veggie

    def LoggedIn (self):
        self.thirdWin.deiconify()

    def HomePage (self):
        self.thirdWin = Toplevel()
        self.thirdWin.title("GtPizza Homepage")
        #Row 0
        Label(self.thirdWin, text = "Welcome to GtPizza!", relief = SUNKEN).grid(column = 1, columnspan = 2, sticky = N)
        #Row 1
        Label(self.thirdWin).grid(row = 1)
        #Row 2
        Label(self.thirdWin, text = "Cheese:").grid(row = 2, column = 1, padx = 30)
        Label(self.thirdWin, text = "Pepperoni").grid(row = 2, column = 2, padx = 30)
        Label(self.thirdWin, text = "Veggie:").grid(row = 2, column = 3, padx = 30)
        #Row 3
        Label(self.thirdWin, text = "New Order:").grid(row = 4, sticky = E)
        self.r1 = IntVar(); self.r2 = IntVar(); self.r3 = IntVar()
        Label(self.thirdWin, textvariable = self.r1).grid(row = 3, column = 1)
        Label(self.thirdWin, textvariable = self.r2).grid(row = 3, column = 2)
        Label(self.thirdWin, textvariable = self.r3).grid(row = 3, column = 3)
        #Row 4
        Label (self.thirdWin, text = "Most Recent Order:").grid(row = 3, sticky = E)
        self.n1 = IntVar(); self.n2 = IntVar(); self.n3 = IntVar()
        Entry (self.thirdWin, textvariable = self.n1, width = 5).grid(row = 4, column = 1)
        Entry (self.thirdWin, textvariable = self.n2, width = 5).grid(row = 4, column = 2)
        Entry (self.thirdWin, textvariable = self.n3, width = 5).grid(row = 4, column = 3)
        #Row 5
        Label(self.thirdWin).grid(row = 5)
        #Row 6
        Button(self.thirdWin, text = "Statistics", command = self.StatPage).grid(row = 6, columnspan = 2, sticky = EW)
        Button(self.thirdWin, text = "Place My Order", command = self.PlaceOrder).grid(row = 6, column = 2, columnspan = 2, sticky = EW)
        #Row 7
        Button(self.thirdWin, text = "Logout", command = self.Logout).grid(row = 7, columnspan = 4, sticky = EW)

        #Query the database for the most recent item.
        username = self.v1a.get()
        db = self.connect()
        cursor = db.cursor()
        sql = "SELECT Cheese, Pepperoni, Veggie FROM PizzaOrders WHERE User =%s ORDER BY OrderID DESC LIMIT 1"
        cursor.execute(sql, (username))
        tup = cursor.fetchone()
        recCheese = tup[0]; recPep = tup[1]; recVeg = tup[2]
        self.r1.set(recCheese); self.r2.set(recPep); self.r3.set(recVeg)
        cursor.close()
        db.commit()

    #Opens a statistics page.
    def StatPage (self):
        self.fourthWin = Toplevel()
        self.fourthWin.title("Statistics Page")
        #Row 0
        Label (self.fourthWin, text = "Name:").grid(column = 1)
        Label (self.fourthWin, text = "Orders Placed:").grid(row = 0, column = 2)
        #Row 1
        self.name1 = StringVar(); self.order1 = IntVar()
        Entry (self.fourthWin, textvariable = self.name1, width = 20).grid(row = 1, column = 1)
        Entry (self.fourthWin, textvariable = self.order1, width = 20).grid(row = 1, column = 2)
        #Row 2
        self.name2 = StringVar(); self.order2 = IntVar()
        Entry (self.fourthWin, textvariable = self.name2, width = 20).grid(row = 2, column = 1)
        Entry (self.fourthWin, textvariable = self.order2, width = 20).grid(row = 2, column = 2)       
        #Row 3
        self.name3 = StringVar(); self.order3 = IntVar()
        Entry (self.fourthWin, textvariable = self.name3, width = 20).grid(row = 3, column = 1)
        Entry (self.fourthWin, textvariable = self.order3, width = 20).grid(row = 3, column = 2)
        #Row 4
        Label (self.fourthWin).grid(row = 4)
        #Row 5
        f1 = Frame (self.fourthWin)
        f1.grid(row = 5, columnspan = 4, sticky = EW)
        Label (f1, text = "Total Cheese").grid(row = 0, padx = 30)
        Label (f1, text = "Total Pepperoni").grid(row = 0, column = 1, padx = 25)
        Label (f1, text = "Total Veggie").grid(row = 0, column = 2, padx = 25)

        self.sum1 = IntVar(); self.sum2 = IntVar(); self.sum3 = IntVar()
        Label (f1, textvariable = self.sum1).grid(row = 1)
        Label (f1, textvariable = self.sum2).grid(row = 1, column = 1)
        Label (f1, textvariable = self.sum3).grid(row = 1, column = 2)

        Label (f1).grid(row = 2)
        
        f1.grid(row = 5, columnspan = 4, sticky = EW)
        Label (f1, text = "Most Cheese").grid(row = 3, padx = 25)
        Label (f1, text = "Average Cheese / Order").grid(row = 3, column = 2, padx = 25)

        self.max = IntVar(); self.avg = IntVar()
        Label (f1, textvariable = self.max).grid(row = 4)
        Label (f1, textvariable = self.avg).grid(row = 4, column = 2)
        
        #Row 6
        Button (self.fourthWin, text = "Close", command = self.fourthWin.withdraw).grid(row = 6, columnspan = 4, sticky = EW)

    #Three entry boxes will display the three users with the most total orders in the database.
    #Name: first name, or N/A if null, Orders Placed: shows number of orders placed.
    #If there is a tie, order alphabetically by username. 

        #Calculations.
        db = self.connect()
        cursor = db.cursor()
        sql = "SELECT User, COUNT(*) FROM PizzaOrders GROUP BY User ORDER BY COUNT(*) DESC, User ASC LIMIT 3"
        cursor.execute (sql)
        tup = cursor.fetchall()
        print (tup)
        cursor.close()
        db.commit()
        db.close()
        
        aList = [[self.name1, self.order1], [self.name2, self.order2], [self.name3, self.order3]]
        #Remember, if you're trying to iterate through two sequences linearly, use range.
        #Use nested items only if you want staggered sequence iterations. 
        for i in range(3):
            db = self.connect()
            cursor = db.cursor()
            username = tup[i][0]
            order = tup[i][1]
            sql = "Select FirstName FROM PizzaUsers WHERE USERNAME = %s"
            cursor.execute (sql, (username))
            nameTup = cursor.fetchone()

            try:
                name = nameTup[0]
            except:
                name = None
            if name == None or name == "":
                name = "N/A"
            cursor.close()
            db.commit()
            db.close()

            aList[i][0].set(name)
            aList[i][1].set(order)

    #Total cheese, pepperoni, veggie, show total number of pizzas of each type of orders by ALL customers.
        db = self.connect()
        cursor = db.cursor()
        sql = "SELECT SUM(Cheese),SUM(Pepperoni),SUM(Veggie) FROM PizzaOrders"
        cursor.execute(sql)
        tup = cursor.fetchone()
        cursor.close()
        db.commit()
        db.close()
        self.sum1.set(tup[0]); self.sum2.set(tup[1]); self.sum3.set(tup[2])

    #Most cheese: maximum number of cheese pizzas of the user CURRENTLY LOGGED in, can be a number or None.
        username = self.v1a.get()
        db = self.connect()
        cursor = db.cursor()
        sql = "SELECT MAX(Cheese) FROM PizzaOrders WHERE User = %s"
        cursor.execute(sql, (username))
        maxCheese = cursor.fetchone()
        mostCheese = maxCheese[0]
        if mostCheese == 0:
            mostCheese = "None"
        self.max.set(mostCheese)
        cursor.close()
        db.commit()
        db.close()
        
    #Average Cheese/Order: average number of Cheese pizzas per order for all users.
        db = self.connect()
        cursor = db.cursor()
        sql = "SELECT AVG (Cheese) FROM PizzaOrders"
        cursor.execute(sql)
        tupCheese = cursor.fetchone()
        avgCheese = tupCheese[0]
        self.avg.set(avgCheese)
        cursor.close()
        db.commit()
        db.close()
        

    #Takes number of pizzas of each type (Cheese self.n1, Pepperoni self.n2, Veggie self.n3 ) and enters the order into the database.
    #If the order is not placed, either because 1) you can't connect to the database, or 2) because some of the entries are 0, display an error messagebox.
    #If successfully, placed, reset entry box values to 0 and update order labels.
    def PlaceOrder(self):
        pizzaOK = False
        username = self.v1a.get()

        try: 
            numCheese = self.n1.get(); numPep = self.n2.get(); numVeg = self.n3.get()
            if numCheese == 0 and numPep == 0 and numVeg == 0 or type(numCheese) != int or type(numPep) != int or type(numVeg) != int:
                messagebox.showerror("Error", "Enter an order for at least one pizza!")
            else:
                pizzaOK = True
        except:
            messagebox.showerror("Error", "Enter your number in digits, not in words!")

        try:
            if pizzaOK == True:
                db = self.connect()
                cursor = db.cursor()
                sql = "INSERT INTO PizzaOrders (User, Cheese, Pepperoni, Veggie) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (username, numCheese, numPep, numVeg))
                cursor.close()
                db.commit()
                db.close()
                messagebox.showinfo("Success!", "Order successfully placed!")
                self.n1.set(0); self.n2.set(0); self.n3.set(0)
        except:
            messagebox.showerror("Error", "Check your internet connection!")

        #Query the database to find the most recent order.
        db = self.connect()
        cursor = db.cursor()
        sql = "SELECT Cheese, Pepperoni, Veggie FROM PizzaOrders WHERE User =%s ORDER BY OrderID DESC LIMIT 1"
        cursor.execute(sql, (username))
        tup = cursor.fetchone()
        recCheese = tup[0]; recPep = tup[1]; recVeg = tup[2]
        self.r1.set(recCheese); self.r2.set(recPep); self.r3.set(recVeg)
        cursor.close()
        db.commit()
        
    def Logout(self):
        self.thirdWin.destroy()
        self.mainWin.deiconify()
    

rootWin = Tk()
o = LoginPage (rootWin)
rootWin.mainloop()

