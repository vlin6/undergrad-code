# Victor Lin, A2, vlin6@gatech.edu, 903004194
#"I worked on the homework assignment alone, using only this semester's course materials."

#Currently, the date is set to Nov 11.

from tkinter import *
import urllib.request
import xml.etree.ElementTree as etree
import datetime
#http://docs.python.org/2/library/datetime.html

    #.find() looks for ONE INSTANCE of tags in the next layer.
    #.findall() ALL INSTANCES
    #.findall(.\\) looks for tags in all layers.

#GUI:
class GUI:

    def __init__(self, win):

        
        Label (win, text = "Parse IBM for EOS dates within 365 days", bg = "red").pack()
        Button (win, text = "Download File", command = self.clicked).pack(fill = X)

    def clicked (self):

        self.download()
        self.filter(self.dataList)
        self.writeXML(self.filterList)

    #Stores software data in a list and passes it to the filter function
    def download (self):
        try: 
            self.dataList = []
            #Download XML from given url.
            url = "http://www.ibm.com/software/support/lifecycle/rss/PLCWeeklyXMLDownload.xml"
            response = urllib.request.urlopen(url)
            #for testing: response = "PLCWeeklyXMLDownload.xml"

        
            
            xml = etree.parse(response)
            #Software Title, Version Number, Release Number, modLevelNumber and End of Service date
            root = xml.getroot()

            #Goes through each SWTitleRecord.
            for SWTitleRecord in root:

                    for child in SWTitleRecord:

                        #Software title
                        if child.tag == "SWTitle":
                            SWTitle = child.text
                            #print(SoftwareTitle)

                    Versions = SWTitleRecord.findall(".//Version")
                    for version in Versions:
                        for item in version:
                            if item.tag == "versionNumber":
                                vNum = item.text
                            elif item.tag == "Release_Mods":
                                Release_Mods = item
                                for mod in Release_Mods:
                                
                                    for info in mod:
                                        #Release Number
                                        if info.tag == "releaseNumber":
                                                releaseNum = info.text

                                        #modLevelNumber
                                        elif info.tag == "modLevelNumber":
                                                modNum = info.text

                                        #End of Service date
                                        elif info.tag == "PLCInfo":

                                                eos = info.attrib["eosDate"]
                                                if eos == "":
                                                    break
                                                else:
                                                    eosParsed = self.parseIBMDate(eos)
                                                    self.dataList.append((SWTitle, vNum, releaseNum, modNum, eosParsed))


            messagebox.showinfo("Download succeeded!", "Download successful! Press 'OK' to save your file.")

        except:
            messagebox.showerror("Error", "Unable to download file, check your internet connection!")


    def parseIBMDate (self, eosString):

        self.monthDict = {"Jan" : 1, "Feb" : 2, "Mar" : 3, "Apr" : 4, "May" : 5, "Jun" : 6, "Jul" : 7, "Aug" : 8, "Sep" : 9, "Oct" : 10, "Nov" : 11, "Dec" : 12, "N/A" : "N/A"}

        if eosString != "":
            eosList = eosString.split(" ")
            day = int(eosList[0])
            month = int(self.monthDict[eosList[1]])
            year = int(eosList[2])
            eosDate = datetime.date(year, month, day)
            return eosDate

        return eosString

    def filter (self, aList):

        self.filterList = []
        today = datetime.date.today()
        #for testing: today = datetime.date(2013, 11, 11)
        
        for software in aList:
            eosDate = software[4]
            difference = eosDate - today
            diff0 = datetime.timedelta(days = 0)
            diff365 = datetime.timedelta(days = 365)
            
            if difference > diff0 and difference < diff365:
                self.filterList.append(software)

    def writeXML (self, filterList):

        self.monthDictRestore = { 1 : "Jan", 2 : "Feb", 3 : "Mar", 4 : "Apr", 5 : "May", 6 : "Jun", 7 : "Jul", 8 : "Aug", 9 : "Sep", 10 : "Oct", 11 : "Nov", 12 : "Dec" }

        #Software Title, Version Number, Release Number, modLevelNumber and End of Service date
        if messagebox.askyesno("Save file", "Do you want to save your file as XML?"):
                filename = filedialog.asksaveasfilename()
                if ".xml" not in filename:
                    filename += ".xml"
                rootVar = etree.Element("Packages")
                for software in filterList:
                    date = software[4]
                    year = date.year; month = date.month; day = date.day
                    month = self.monthDictRestore[month]

                    eosDate = str(day) + " " + str(month) + " " + str(year)
                    modLevelNum = software[3]
                    releaseNum = software[2]
                    versionNum = software[1]
                    packageNode = etree.SubElement(rootVar, "Package", eosDate = eosDate,
                                                   modLevelNum = modLevelNum, releaseNum = releaseNum,
                                                   versionNum = versionNum)
                    packageNode.text = software[0]
                messagebox.showinfo("Success!", "File successfully saved!")

                packageTree = etree.ElementTree(rootVar)
                packageTree.write(filename, "UTF-8")
        
win = Tk()
o = GUI(win)
win.mainloop()
