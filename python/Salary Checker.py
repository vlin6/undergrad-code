# Victor Lin, A2, vlin6@gatech.edu, 903004194
#"I worked on the homework assignment alone, using only this semester's course materials."

import urllib.request
from tkinter import *
from re import findall
import csv

#==========================================================================#
#Downloads salary data from the internet and compares it to a CSV file.    #
#                                                                          #
#CSV File: Last Name, First Name, Salary 2000, Salary for 2012             #
#HTML Full Name, Salary 2000, Salary 2012                                  #
#Might be missing salary data for 2000 or 2012. Indicated by " - "         #
#People that appear in the CSV file might not appear in the HTML data.     #
#                                                                          #
#Return a CSV File:                                                        #
# Name        | 2000        | 2012                                         #
# Last, First | Salary 2000 | Salary 2012...                               #
#                                                                          #
#Order                                                                     #
#                                                                          #
#Salary data for both years, alphabetical order;                           #
#alphabetize by last name, unless same last name, then sort by first name. #
#Salary data for 2000.                                                     #
#Salary data for 2012.                                                     #
#Denote lack of data with " - ".                                           #
#==========================================================================#

class infoGUI:

    def __init__(self, win):
        Button (win, text = "Load Input CSV File", command = self.loadCSVclicked).grid(sticky = EW, columnspan = 2)
        Label (win, text = "File Path").grid(row = 1, sticky = EW, columnspan = 2)
        Label (win, text = "Input CSV File").grid(row = 2, column = 0)
        Label (win, text = "Website URL").grid(row = 3, column = 0)
        Label (win, text = "Output CSV File").grid(row = 4, column = 0)
        self.v1 = StringVar(); self.v2 = StringVar(); self.v3 = StringVar()
        Entry (win, width = 60, textvariable = self.v1, state = 'readonly').grid(row = 2, column = 1)
        Entry (win, width = 60, textvariable = self.v2).grid(row = 3, column = 1)
        Entry (win, width = 60, textvariable = self.v3, state = 'readonly').grid(row = 4, column = 1)
        self.b1 = Button (win, text = "Process Data", state = DISABLED, command = self.PDclicked)
        self.b1.grid(row = 5, sticky = EW, columnspan = 2)


    #Prompts user to select a file, then passes the name of the CSVFile into "loadCSVFile".
    #If loadCSVFile method returns a ist of data, store it, place name of loaded CSVfile in entry, activate "Process Data".
    #If loadCSVFile returns a None, pop up an error dialog. 
    def loadCSVclicked(self):
        self.text = filedialog.askopenfilename()
        var = self.loadCSVfile(self.text)
        if var == None:
            messagebox.showerror ("Error", "Invalid Input CSV File.")
        else:
            self.listCSV = var
            self.b1.config (state = NORMAL)
            self.v1.set(self.text)
        
    #Takes a string representing a file name, returns a CSV Data as a list of lists or None.         
    def loadCSVfile(self, fileName):
        try:
            with open (fileName, 'r') as csvfile:
                txtreader = csv.reader(csvfile)
                self.listCSV = list(txtreader)
            return self.listCSV
        except:
            return None

    #Check the URL and pass it as an argument to the downloadSalaryData function.
    #If the download fails, show a warning message, and return None.
    #If the download was successful, call convertHTMLtoCSVFormat, pass it to mergeData, and call saveSalaryData.
    #Return None.
    def PDclicked(self):
        if self.downloadSalaryData(self.v2.get()) == None:
            messagebox.showwarning("Warning", "Incorrect URL")
        else:
            self.htmlData = self.downloadSalaryData(self.v2.get())
            self.listHTML = self.convertHTMLtoCSVFormat(self.htmlData)
            self.mergeData(self.listHTML, self.listCSV)
            self.saveSalaryData(self.aDict)
            
    #Takes in a url, and return the data or None.
    def downloadSalaryData(self, urlName):
        try: 
            response = urllib.request.urlopen(urlName)
            html = response.read()
            htmlStr = str(html)
            #Name, number/-, number/-
            regex = "<tr><td>([^<]*)</td><td>([^<]*)</td><td>([^<]*)</td>"
            htmlData = findall (regex, htmlStr)
            for i in range(len(htmlData)):
                htmlData[i] = list(htmlData[i])
            return htmlData
        except:
            return None

    #Takes in htmlData and return in the proper CSVFile format.
    def convertHTMLtoCSVFormat(self, htmlData):
        listHTML = []
        for row in htmlData:
            firstName = ""
            lastName = ""
            name = row[0]
            space = name.find(" ")
            if space == -1:
                listHTML.append(["Last Name", "First Name", "2000", "2012"])
            else:
                firstName = name[:space]
                lastName = name[space+1:]
                listHTML.append ([lastName, firstName, row[1], row[2]])
        return listHTML

            
    #Takes in a HTMLData list and a CSVFile list, return a dictionary of merged data.
    def mergeData(self, listHTML, listCSV):
        self.aDict = {}
        for person in listHTML:
            self.aDict[(person[0],person[1])] = (person[2],person[3])
        for person in listCSV:
            key = (person[0],person[1])
            if not key in self.aDict:
               if person [0] == 'Name':
                    pass
               else: 
                    self.aDict[key] = (person[2],person[3])
            else:
               if person[2] != "-" and person[3] == "-":
                    self.aDict[key] = (person[2], self.aDict[key][1])
               elif person[2] == "-" and person[2] != "-":
                    self.aDict[key] = (self.aDict[key][0], person[3])
        
        return self.aDict

    #Use an asksaveasfilename file dialog to ask the user for a filename to save the data to.
    #Write data to that file.
    #Update the GUI by adding the file name to the correct entry.
    def saveSalaryData(self, aDict):
       name = filedialog.asksaveasfilename()
       self.v3.set(name)
       listBoth = []
       list2000 = [] # lacks data for 2012
       list2012 = []
        
       for key in self.aDict:
            if key == ('Last Name', 'First Name'):
                pass
            elif self.aDict[key][0] != "-" and self.aDict[key][1] != "-":
                listBoth.append(key)
            elif self.aDict[key][0] != "-" and self.aDict[key][1] == "-":
                list2000.append(key)
            elif self.aDict[key][1] != "-" and self.aDict[key][0] == "-":
                list2012.append(key)


       listBoth.sort()
       list2000.sort()
       list2012.sort()
       try:    
           with open (name, 'w') as csvfile:
                txtwriter = csv.writer(csvfile)
                txtwriter.writerow(['Name'] + ['2000'] + ['2012'])
                for key in listBoth:
                    txtwriter.writerow( [str(key[0]) + ", " + str(key[1])] + [self.aDict[key][0]] + [self.aDict[key][1]])
                for key in list2000:
                    txtwriter.writerow([str(key[0]) + ", " + str(key[1])] + [self.aDict[key][0]] + ['-'])
                for key in list2012:
                    txtwriter.writerow([str(key[0]) + ", " + str(key[1])] + ['-'] + [self.aDict[key][1]])
       except:
           messagebox.showerror("Error", "Save a file first!")
win = Tk()
win.title ("City of Shamalamadingdong - Data Merger")
o = infoGUI(win)
win.mainloop()
