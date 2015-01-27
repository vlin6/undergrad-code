# Victor Lin, A2, vlin6@gatech.edu, 903004194
#"I worked on the homework assignment alone, using only this semester's course materials."

from tkinter import *
import csv 

##Outline of Objectives
##function: packs rectangular objects into a 2D space, like packing boxes into a flat truck
##given: 1) dimensions of space you are packing objects into, 2) list of boxes
##write two algorithms: 1) packs largest boxes first 2) packs smallest first
##report: 1) how many boxes packed, 2) which boxes packed, 3) which aren't packed, 4) how much space unfilled
##CSV format: BOX ID, length (number of rows), width (number of columns)
class box_packer():

    def __init__(self, aWin):
        # self.a will represent percent of boxes packed, or packed boxes / total boxes
        self.a = 0
        # self.b will represent percent of truck filled, or filled locations / total locations
        self.b = 0
        self.truck = []
        self.fileName = "..."
        self.boxes = []
        self.processedBoxes = []
        self.unpackedBoxes = []
        self.packedBoxes = []
        self.myWin = aWin

        #Row 0: Label, entry, button
        label1 = Label(aWin, text = "Boxes File:").grid(row = 0, column = 0, sticky = E)
        v = StringVar(); v.set("...")
        self.e = Entry(aWin, width = 75, state = "readonly", textvariable = v)
        self.e.grid (row = 0, column = 1, columnspan = 2, sticky = W + E)
        button1 = Button(aWin, text = "Select File", command = self.openFileClicked).grid(row = 0, column = 3, sticky = E)

        #Row 1: label, label
        label2 = Label (aWin, text = "Truck Dimensions")
        label3 = Label (aWin, text = "Packing Algorithm")
        label2.grid(row = 1, column = 1, sticky = W)
        label3.grid(row = 1, column = 2, sticky = W)

        #Radiobutton value set-up
        self.v1 = StringVar()
        self.v1.set("none")

         #Row 2: Width entry, largest box rb1
        label4 = Label(aWin, text = "Width:"); label4.grid(row = 2, column = 0, sticky = E)
        self.eWidth = Entry (aWin, state = NORMAL); self.eWidth.grid(row = 2, column = 1, sticky = W)
        self.rb1 = Radiobutton (aWin, text = "Largest Box First", variable = self.v1, value = "largest")
        self.rb1.grid(row = 2, column = 2, sticky = W)


        #Row 3: Length entry, smallest box rb2
        label5 = Label(aWin, text = "Length:"); label5.grid(row = 3, column = 0, sticky = E)
        self.eLength = Entry (aWin, state = NORMAL); self.eLength.grid(row = 3, column = 1, sticky = W)
        self.rb2 = Radiobutton (aWin, text = "Smallest Box First", variable = self.v1, value = "smallest")
        self.rb2.grid(row = 3, column = 2, sticky = W)

        #Row 4: button
        self.button2 = Button (aWin, text = "Pack Boxes & Save Results", command = self.packNSaveClicked)
        self.button2.grid(row = 4, columnspan = 4, sticky = W + E)

    #stores file name in self.fileName and returns it
    def openFileClicked(self):

        self.fileName = filedialog.askopenfilename()
        self.e.config(state = NORMAL)
        self.e.delete(0,END)
        self.e.insert(0,self.fileName)
        if len(self.e.get()) == 0:
            self.e.insert(0,"...")
        self.e.config(state = "readonly")
        return self.fileName

    #opens the file, reads it, and stores data as object variable which points it to a list of lists 
    def readBoxesFile(self):
        f = open (self.fileName, "r")
        self.boxes = f.readlines()
        ending = len(self.boxes)

        #Split the string into three parts
        for i in range (ending):
            self.boxes[i] = self.boxes[i].replace(" ", "")
            self.boxes[i] = self.boxes[i].strip()
            self.boxes[i] = self.boxes[i].split(",")
            #Convert the second and third part of the string into integers if possible. 
            try:
                self.boxes[i][1] = int(self.boxes[i][1])
            except:
                raise ValueError
            try:
                self.boxes[i][2] = int(self.boxes[i][2])
            except:
                raise ValueError 
        f.close()
        
    #CSV format: BOX ID, length (number of rows = y), width (number of columns = x)
    #return True if the box can be packed into the truck starting at location (row, col)
    #return False if it cannot be packed starting at that location
        
    def isValidlocation (self, row, column, length, width):
        #Iterate through each row to the length of box
        for y in range(length):
            #Iterate through each element of row up to width of box
            for x in range(width):
                try:
                #y = starting row, x = starting column
                    if self.truck[y+row][x+column] != "":
                        return False
                except IndexError:
                #Or, if the truck isn't big enough...
                    return False
                except:
                    print ("Except in method isValidlocation")
                    return False
        return True


    #Accepts a row and a column, then fills the truck with BOX ID of the box in the form of list aBox.
    #aList contains: BOX ID, length (number of rows = y), width (number of columns = x)
    def fillTruckLocation(self, row, column, aBox):

        boxLength = aBox[1]
        boxWidth = aBox[2]        
        for y in range (boxLength):
            for x in range (boxWidth):
                self.truck[row+y][column+x] = aBox[0]

        #Because when we passed in row = 1, column = 1, we have to convert it into index form, which is (0, 0).

        
    #Look through the truck, find the first empty cell (traverse each row from left to right).
    #Try to pack the box (using self.fillTruckLocation) into this empty cell; if it fits, return true.
    #If it doesn't fit, try to find another empty cell; if there are none, return false.

    def packBox(self, aBox):
        truckLength = len(self.truck); truckWidth = len(self.truck[0])
        boxLength = aBox[1]; boxWidth = aBox[2]

        #Go through each row
        for y in range (truckLength):
            #Go through each column
            for x in range (truckWidth):
                if self.isValidlocation(y, x, boxLength, boxWidth):
                    self.fillTruckLocation (y, x, aBox)
                    self.packedBoxes.append(aBox[0])
                    return True
                
        self.unpackedBoxes.append(aBox[0])
                    
        return False

    
    #Pack all boxes into the truck. 
    def packTruck(self):
    #When two boxes have same area, take the box that is closer to the input file.

        totalBox = len(self.boxes)
        self.processedBoxes = []
        area = 0
        
        for i in range (totalBox):
            area = self.boxes[i][1] * self.boxes[i][2]
            self.processedBoxes.append([int(area), self.boxes[i][0], self.boxes[i][1], self.boxes[i][2]])
    
        #If self.v1.get() = "largest", pack boxes with the largest area.
        #The strVar() itself is not the string. You need to get the string from the strVar().
    
        if self.v1.get() == "largest":
            self.processedBoxes.sort()
            self.processedBoxes.reverse()
            
        #If self.v1.get() = "smallest", pack boxes with the smallest area.
        elif self.v1.get() == "smallest":
            self.processedBoxes.sort()
        
        for i in range (totalBox):
            del self.processedBoxes[i][0]

        for i in range (totalBox):
            self.packBox(self.processedBoxes[i])

    def writeTruckToCSV(self):
        with open('truckview.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(self.truck)
                    
    def packNSaveClicked(self):
    #1) Set up truck object variable with appropriate number of empty spaces.
        try:
            truckWidth = int(self.eWidth.get())
        except:
            messagebox.showerror ("Error", "Type in an appropriate width.")
        try:
            truckLength = int(self.eLength.get())
        except:
            messagebox.showerror ("Error", "Type in an appropriate length.")

        #Create a truck of truckLength and truckWidth, with each row being a list and the each column being the index.
        self.truck = []

        try:
            for y in range(truckLength):
            # y will represent each row, so create a row as a list.
                self.truck.append([])
                for x in range(truckWidth):
                # x will represent each column, so append an index with "".
                    self.truck[y].append("")
        except:
            pass
            
        #2) read in file with information about boxes
                
        try:
            self.readBoxesFile()
        except:
            messagebox.showerror ("Error", "You gave a malformed CSV file.")
                 
        #3) pack the boxes

        self.packTruck()
            
        #4) write contents of the truck out to "truckview.csv"

        self.writeTruckToCSV()
            
        #5) add some widgets to the GUI (dynamically changing the GUI)

        #Attaining values for self.a and self.b
        
                    
        boxesPacked = len(self.packedBoxes)
        totalBoxes = len(self.boxes)

        self.a = boxesPacked / totalBoxes

        truckFilled = 0
        truckArea = (truckLength*truckWidth)
        for y in range (len(self.truck)):
            for x in range (len(self.truck[y])):
                if self.truck[y][x] != "":
                    truckFilled += 1
        self.b = truckFilled / truckArea

        #Row 5: Packing Statistics
        
        self.aLabel = Label (aWin, text = "Packing Statistics")
        self.aLabel.grid (row = 5, columnspan = 4, sticky = W + E)

        #Row 6: 2 Frames

        #Frame 1: Percent of Boxes Packed, Percent of Truck Filled

        self.f1 = Frame (aWin)
        self.f1.grid(row = 6, column = 0)
        self.aLabel1 = Label (self.f1, text = "Percent of Boxes Packed: {:.2%} ".format(self.a))
        self.aLabel2 = Label (self.f1, text = "Percent of Truck Filled: {:.2%} ".format(self.b))
        self.aLabel1.pack(); self.aLabel2.pack()
        self.packedBoxes = []

        #Frame 2: Boxes not packed

        self.f2 = Frame (aWin)
        self.f2.grid(row = 6, column = 2)
        self.aLabel3 = Label (self.f2, text = "Boxes not packed:")
        self.aLabel3.pack(side = TOP)

        for item in self.unpackedBoxes:
            bLabel = Label(self.f2, text = item)
            bLabel.pack(side = TOP)


            
        
    
aWin = Tk()
o = box_packer(aWin)
aWin.mainloop()
