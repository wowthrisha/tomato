import csv
from datetime import date
from datetime import datetime
import os
import math

class Repository:
    def __init__(self):
        self.fileName = "Record.csv"

    def createFile(self):
        self.file = open(self.fileName, "w", newline = "")
        self.writer = csv.writer(self.file)
        self.writer.writerow(["Serial Number", "Harvest Date"])
        self.file.close()
        print("File created.")

    def removeFile(self):
        if os.path.exists(self.fileName):
            os.remove(self.fileName)
            print("File removed.")

    def enterTomatoData(self):
        self.file = open(self.fileName, "a+", newline = "")
        self.writer = csv.writer(self.file)
        
        while True:
            self.writer.writerow([
                input("Enter the serial number of the crate: "),
                date.today()])
            
            choice = int(input("Enter 1 to continue and 0 to abort: "))

            if choice != 1:
                break

        self.file.close()
        print("Data entered.")

    def computeDates(self):
        self.file = open(self.fileName, "r")
        self.reader = csv.reader(self.file)
        next(self.reader)
        self.storageDurationDictionary = {}

        for dataRow in self.reader:
            self.timeDelta = date.today() - datetime.strptime(dataRow[1],'%Y-%m-%d').date()
            self.storageDurationDictionary[dataRow[0]] = int(math.fabs(self.timeDelta.days))

        self.file.close()
        print(self.storageDurationDictionary)

