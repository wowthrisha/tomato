import csv
from datetime import date
from datetime import datetime

#Modules Used:
#CSV - To read a CSV file consisting of serial numbers and dates
#datetime - To use methods pertaining to dates for calculation and formatting


#The Repository class gives the function to read data from the CSV file.
class Repository:
    #
    #_init_:
    #
    #Parameters: None
    #Function: Declares the file name of the CSV file for later use.
    #Return: None
    #
    
    def _init_(self):
        self.fileName = "Record.csv"
        
    #
    #getComputedDates:
    #
    #Parameters: None
    #Function: (1)
    #          (2)
    #          (3)
    #Return: The dictionary containing the serial numbers and corresponding dates.
    #
    def getComputedDates(self):
        #(1) Opens the file, nagivates to where the data starts, declares an empty dictionary.
        self.fileName = "Record.csv"
        self.file = open(self.fileName, "r")
        self.reader = csv.reader(self.file)
        next(self.reader)
        self.storageDurationDictionary = {}

        #(2) Iterates over the list of rows, and assigns key value pairs to the dictionary.
        for dataRow in self.reader:
            self.storageDurationDictionary[dataRow[0]] = dataRow[1][1:]
            
        #(3) File is closed and finished dictionary is returned.
        self.file.close()
        return self.storageDurationDictionary


#The Transport class is the heart of the program.
class Transport:
    #
    #requiredList:
    #
    #Parameters: A nested list
    #Function: Seperates the location from the a tuple object.
    #Return: Final list
    #
    def requiredList(nestedList):
        requiredList=[]
        for place, distance in nestedList:
            requiredList.append(place)

        return requiredList

    #
    #sortedDict:
    #
    #Parameters: A dictionary
    #Function: (1) 
    #          (2)
    #return: None
    #
    def sortedDict(self, dictionary):
        #(1): Uses dictionary comprehension to convert it back into a dictionary.
        sortedDict={place:distance for place,distance in sorted(dictionary.items())}

        #(2): Forms three lists for factories, markets, and cold storages each with the set of locations based on the travel duration
        #     Uses the requiredList() function to seperate locations. Sort is based on the key which requires a lambda function.
        #     These lists are now usable attributes.
        Transport.market = Transport.requiredList(sorted(sortedDict["3market"].items(),key=lambda x:x[1]))
        Transport.factory = Transport.requiredList(sorted(sortedDict["2factory"].items(),key=lambda x:x[1]))
        Transport.coldStorage = Transport.requiredList(sorted(sortedDict["1cold_storage"].items(),key=lambda x:x[1]))
        
    #
    #assignPlaces:
    #
    #Parameters: A dictionary with serial numbers and dates
    #Function:(1)
    #         (2)
    #         (3)
    #         (4)
    #Return: A sorted result dictionary.
    #
    def assignPlaces(self, computedDates):
        Transport.dictFactory = {}
        Transport.dictMarket = {}
        Transport.dictColdStorage = {}

        for key, value in computedDates.items():

            #(1)
            if int(value[-2:]) <= 10:
                date = int(value[-2:])
                length = len(Transport.factory)
                interval = 10/length #Dividing 10 days equally for each location
                for j in range(length):
                    while interval*(j) < date <= interval*(j+1) :
                        Transport.dictFactory.update({(key,value):Transport.factory[j]})
                        break
            #(2)
            elif 10 < int(value[-2:]) <= 20 and len(Transport.market) <= 5:
                date = int(value[-2:])
                length = len(Transport.coldStorage)
                interval = 10 / length
                for j in range(length):
                    while 10 + interval *j < date <= 10 + interval * (j + 1):
                        Transport.dictColdStorage.update({(key,value):Transport.coldStorage[j]})
                        break

            #(3)   
            else:
                date = float(value[-2:])
                length = len(Transport.market)
 
                #the last slot of days can be 8 or 9 or 10 or 11 
                #here since we have 5 locations it's better to assume 10 
                #else crates would have to be distributed unequally based on a priority
                #it can be included in future developments
                #d=(date.today().day-20)/c this would give higher priority to last few days of tomatoes
                #i.e.if 29 days , 9/5 , first day of tomatoes would be separated(less fresh)(less priority)

                interval = 10/length
                for j in range(length):
                    while 20 + interval * j < date <= 20 + interval *(j + 1):
                        Transport.dictMarket.update({(key,value):Transport.market[j]})
                        break
        
        #(4) The final dictionary is set up, as a nested dictionary, and it is returned.
        finalDict={
            "factory":Transport.dictFactory,
            "cold_storage":Transport.dictColdStorage,
            "market":Transport.dictMarket}
        
        return finalDict

#This class's purpose is to run the program.
class Main:
    #
    #_init_:
    #
    #Parameters: None
    #Function: Sets up instances of the Repository and Transportation classes. Also goes on
    #          to delcare a dictionary of places and distances. Then sorts this dictionary
    #          with the sortedDict() method of the Transport class.
    #Return: None
    #
    def _init_(self):
        self.repository = Repository()
        self.transport = Transport()
        self.placesDict = {
            "3market":{"Chennai":1,"Lucknow":4,"Delhi":5,"Ahmedabad":3.5,"Hyderabad":1.5},
            "2factory":{"Chennai":1,"Madurai":0.5},
            "1cold_storage":{"Bhopal":2,"Hyderabad":1.5}}
        self.transport.sortedDict(self.placesDict)
        
    #
    #generateResult:
    #
    #Parameters: None
    #Function: Uses the getComputedDates method from the Repository class, to pass as a
    #          parameter for the assignPlaces method of the Transport class to get the resultant
    #          dictionary. Then format the dictionary for proper viewing.
    #Return: None
    #
    def generateResult(self):
        self.repository = Repository()
        self.transport = Transport()
        self.placesDict = {
            "3market":{"Chennai":1,"Lucknow":4,"Delhi":5,"Ahmedabad":3.5,"Hyderabad":1.5},
            "2factory":{"Chennai":1,"Madurai":0.5},
            "1cold_storage":{"Bhopal":2,"Hyderabad":1.5}}
        self.transport.sortedDict(self.placesDict)
        self.result = self.transport.assignPlaces(self.repository.getComputedDates())

        for key, value in self.result.items():
#            print(value.items())
            if key == "factory":
                print("\nFactory\n")
                for nkey,nvalue in value.items():
                    print("Crateid ", nkey, " to ", nvalue)

            elif key == "cold_storage":
                print("\nCold storage\n")
                for nkey,nvalue in value.items():
                    print("Crateid ", nkey, " to ", nvalue)

            else:
                print("\nMarket\n")
                for nkey, nvalue in value.items():
                    print("Crateid ", nkey, " to ", nvalue)

run = Main()
run.generateResult()
