# Victor Lin, A2, vlin6@gatech.edu, 903004194
#"I worked on the homework assignment alone, using only this semester's course materials."
#"I used Dr. Summet's DMSI course notes for downloading images and for SQLs."
#"http://www.summet.com/dmsi/html/guiProgramming.html#adding-images-to-your-gui, http://www.summet.com/dmsi/html/pymysql.html#sql-fundamentals"

from tkinter import *
import urllib.request
import pymysql

class LoginPage:

    def __init__(self, rootWin):
        self.mainWin = rootWin
        self.LoginPage()
        self.register()
        self.loginUp()
        
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
    #To prepare for the next homework, make sure you store firstname to self.firstname.
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
            self.mainWin.destroy()
            tup = cursor.fetchone()
            self.firstname = tup[1]

        cursor.close()
        db.commit()

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
            

rootWin = Tk()
o = LoginPage (rootWin)
rootWin.mainloop()
        
