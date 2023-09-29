import csv
from datetime import date
from datetime import datetime
import math

class Repository:
    def __init__(self):
        self.fileName = "Record.csv"

    def getComputedDates(self):
        self.file = open(self.fileName, "r")
        self.reader = csv.reader(self.file)
        next(self.reader)
        self.storageDurationDictionary = {}

        for dataRow in self.reader:
            self.timeDelta = date.today() - datetime.strptime(dataRow[1][1:],'%Y-%m-%d').date()
            self.storageDurationDictionary[dataRow[0]] = dataRow[1][1:]

        self.file.close()

        return self.storageDurationDictionary

class Transport:
    def __init__(self):
        pass
    
    def required_list(nested_list):
        c=[]
        for a,b in nested_list:
            c.append(a)
        return c

    def sorted_dict(self,d):
        sorted_dict={i:j for i,j in sorted(d.items())}

        #we have used dict comprehension to convert it back into a dict

        #we are forming 3 lists for factory , market and cold_storage each with the set of loactions sorted based on the travel duration
        #to separate location from the tuple object returned by sorted function we create function required_list
        #since we sort based on value(duration) we use the parameter ,key, in sorted 
        #and enter the required sorting criterion using lambda function

        Transport.market = Transport.required_list(sorted(sorted_dict["3market"].items(),key=lambda x:x[1],reverse = True))
        Transport.factory = Transport.required_list(sorted(sorted_dict["2factory"].items(),key=lambda x:x[1],reverse = True))
        Transport.cold_storage = Transport.required_list(sorted(sorted_dict["1cold_storage"].items(),key=lambda x:x[1],reverse = True))

    def assign_places(self, computedDates):
        Transport.dictf = {}
        Transport.dictm = {}
        Transport.dictc = {}
        
        for key, value in computedDates.items():
            print(value[-2:])
            
            if int(value[-2:]) <= 10:
                e=int(value[-2:])
                c=len(Transport.factory)
                d=10/c #dividing 10 days equally for each location
                for j in range(c):
                    while d*(j)<e<=d*(j+1) :
                        Transport.dictf.update({(key,value):Transport.factory[j]})
                        break

            elif 10<int(value[-2:])<=20 and len(Transport.market)<=5:
                e=int(value[-2:])
                c=len(Transport.cold_storage)
                d=10/c
                for j in range(c):
                    while 10+d*j<e<=10+d*(j+1):
                        Transport.dictc.update({(key,value):Transport.cold_storage[j]})
                        break
            else:
                e=float(value[-2:])
                c=len(Transport.market)
 
                #the last slot of days can be 8 or 9 or 10 or 11 
                #here since we have 5 locations it's better to assume 10 
                #else crates would have to be distributed unequally based on a priority
                #it can be included in future developments
                #d=(date.today().day-20)/c this would give higher priority to last few days of tomatoes
                #i.e.if 29 days , 9/5 , first day of tomatoes would be separated(less fresh)(less priority)

                d=10/c
                for j in range(c):
                    while 20+d*j<e<=20+d*(j+1):
                        Transport.dictm.update({(key,value):Transport.market[j]})
                        break
        
    
        final_dict={"factory":Transport.dictf,"cold_storage":Transport.dictc,"market":Transport.dictm}
        return final_dict

class Main:
    def __init__(self):
        self.repository = Repository()
        self.transport = Transport()
        self.placesDict = {"3market":{"Chennai":1,"Lucknow":4,"Delhi":5,"Ahmedabad":3.5,"Hyderabad":1.5},"2factory":{"Chennai":1,"Madurai":0.5},"1cold_storage":{"Bhopal":2,"Hyderabad":1.5}}
        self.transport.sorted_dict(self.placesDict)
    
    def generateResult(self):
        return self.transport.assign_places(self.repository.getComputedDates())

run = Main()
print(run.generateResult())
        

