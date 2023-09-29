from datetime import datetime,date
#import time 

#Below is the data of locations that we assume to already have from the transporters
#the number specifies the travel duration in days

places_dict={"3market":{"Chennai":1,"Lucknow":4,"Delhi":5,"Ahmedabad":3.5,"Hyderabad":1.5},"2factory":{"Chennai":1,"Madurai":0.5},"1cold_storage":{"Bhopal":2,"Hyderabad":1.5}}

class Interface:
    crateid=[]
    def inp(self):
        """inp = input("Was there an harvest today? Yes/No ")
        if inp.lower() == "yes":
            n=int(input("Enter number of crates harvested today "))
            datetoday = date.today().strftime("%d-%m-%y")
            for i in range(1,n+1):
                Interface.crateid.append([i,datetoday])"""

        #creating user input assuming 1 crate is harvested on each day
        #crateid format[(crate_no,"dd-mm-yyyy"),(....)]

        for i in range(1,10):
            Interface.crateid.append([1,"0"+str(i)+"-09-2023"])
        for i in range(10,31):
            Interface.crateid.append([1,str(i)+"-09-2023"])
    
class Transport(Interface):

    #function to separate locations and distances as they are embodied as one data

    def required_list(nested_list):
        c=[]
        for a,b in nested_list:
            c.append(a)
        return c
    
    #each list below will contain the respective set of loactions

    factory=[]
    market=[]
    cold_storage=[]
    
    #function to sort the nested dictionary containing (type of destination) and (loaction with travel duration)
    """sorting is done based on the assumption that 
        tomatoes ripe over a span of 30 days consisting of 3 stages 
        0 to 10 days , 11 to 20 days, 21 to month end
        every tomato from start of the month is stored in the same location and transported on the month's last day       
        0 to 10 (most ripened)goes to factory
        since factories grind the tomatoes for pickle or sauce 
        11 to 20 go for cold storage 
        since most ripened tomatoes are unsuitable for storage, fairly ripened tomatoes serve the purpose better
        21 to end day go to the market
        since they are the most fresh lot , they can have a relatively larger shelf life

        within each of the 3 categories they are futher classified based on the travel duration
        within each 10 day span it is sorted such that 
        tomatoes of 1st few days go to a location with the smallest travel duration
        and last few days have the largest travel duration
        this method of efficient transportation keeps the tomatoes comparatively fresher"""

    def sorted_dict(self,d):

        #sorted(dict) fn gives an object like[(key,value),(key,value),...], sorted based on the dict key

        sorted_dict={i:j for i,j in sorted(d.items())}

        #we have used dict comprehension to convert it back into a dict

        #we are forming 3 lists for factory , market and cold_storage each with the set of loactions sorted based on the travel duration
        #to separate location from the tuple object returned by sorted function we create function required_list
        #since we sort based on value(duration) we use the parameter ,key, in sorted 
        #and enter the required sorting criterion using lambda function

        Transport.market=Transport.required_list(sorted(sorted_dict["3market"].items(),key=lambda x:x[1],reverse=True))
        Transport.factory=Transport.required_list(sorted(sorted_dict["2factory"].items(),key=lambda x:x[1],reverse=True))
        Transport.cold_storage=Transport.required_list(sorted(sorted_dict["1cold_storage"].items(),key=lambda x:x[1],reverse=True))

    """def leap(year):
        if year%100==0:
            if year%400==0:
                return True
            else:
                return False
        else:
            if year%4==0:
                return True
            else:
                return False"""

    #displaying output as the nested dictionary of {types of destination : {crateid:location}}

    def output():
        final_dict={"factory":Transport.dictf,"cold_storage":Transport.dictc,"market":Transport.dictm}
        print(final_dict)
    
    #creating a dict for each of the 3 destinations to store crateid with location

    dictf={}
    dictm={}
    dictc={}

    def assign_places(self):
        for a,b in Interface.crateid:
            if int(b[0:2])<=10:
                e=int(b[0:2])
                c=len(Transport.factory)
                d=10/c #dividing 10 days equally for each location
                for j in range(c):
                    while d*(j)<e<=d*(j+1) :
                        Transport.dictf.update({(a,b):Transport.factory[j]})
                        break
            elif 10<int(b[0:2])<=20 and len(Transport.market)<=5:
                e=int(b[0:2])
                c=len(Transport.cold_storage)
                d=10/c
                for j in range(c):
                    while 10+d*j<e<=10+d*(j+1):
                        Transport.dictc.update({(a,b):Transport.cold_storage[j]})
                        break
            else:
                e=float(b[0:2])
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
                        Transport.dictm.update({(a,b):Transport.market[j]})
                        break
        Transport.output()

    """def check_day(self):            
        today=30
        month=date.today().month
        year=date.today().year
        if today >=27 :
            if month == (1 or 3 or 5 or 7 or 8 or 10 or 12):
                if today == 31:
                    Transport.assign_places()
            elif month == (4 or 6 or 9 or 11):
                if today == 30:
                    Transport.assign_places()
            else:
                if Transport.leap(year):
                    if today == 29:
                        Transport.assign_places()
                else:
                    if today == 28:
                        Transport.assign_places()"""
        
"""while True:
    data=Interface()
    data.input()
    process=Transport()
    process.sorted_dict(places_dict)
    process.check_day()
    time.sleep(86400)"""

data=Interface()
data.inp()
process=Transport()
process.sorted_dict(places_dict)
process.assign_places()