#imports
import pandas as pd #I learnt how to use CSV files on pandas: https://www.youtube.com/watch?v=ClNP-lTzKgI
from datetime import * #learned how to import time: https://docs.python.org/3/library/datetime.html#examples-of-usage-date

##############
#ticket class#
##############

#class for the desired bus ticket
class busTicket():
    
    #initilisation
    def __init__(self, title, ExistingTicket, purchaseDate, purchaseTime):
        
        #the entire ticket
        ticketData = pd.read_csv("bus_ticket_data.csv")
        self.__ticket = ticketData[(ticketData["topup_title"] == title)]

        #catagory
        findCatagory = self.__ticket.loc[self.__ticket["topup_title"] == title, "category_title"]
        self.__catagory = str(findCatagory.iloc[0])
        
        #catagory description
        findCatagoryDesc = self.__ticket.loc[self.__ticket["topup_title"] == title, "category_description"]
        self.__catagoryDesc = str(findCatagoryDesc.iloc[0])

        #topup
        findTopup = self.__ticket.loc[self.__ticket["topup_title"] == title, "topup_title"]
        self.__topup = str(findTopup.iloc[0])

        #topup description
        findTopupDesc = self.__ticket.loc[self.__ticket["topup_title"] == title, "topup_description"]
        self.__topupDesc = str(findTopupDesc.iloc[0])

        #topup price
        findPrice = self.__ticket.loc[self.__ticket["topup_title"] == title, "topup_price_in_pence"]
        self.__price = (int(findPrice.iloc[0]))/100

        #entitlement type
        findEntitlementType = self.__ticket.loc[self.__ticket["topup_title"] == title, "topup_entitlement_type"]
        self.__entitlementType = str(findEntitlementType.iloc[0])

        #entitlement unit
        findEntitlementUnit = self.__ticket.loc[self.__ticket["topup_title"] == title, "topup_entitlement_unit"]
        self.__entitlementUnit = str(findEntitlementUnit.iloc[0])

        #entitlement value
        findEntitlementValue = self.__ticket.loc[self.__ticket["topup_title"] == title, "topup_entitlement_value"]
        self.__entitlementValue = float(findEntitlementValue.iloc[0])

        #entitlement quantity
        findEntitlementQuantity = self.__ticket.loc[self.__ticket["topup_title"] == title, "topup_entitlement_quantity"]
        self.__entitlementQuantity = float(findEntitlementQuantity.iloc[0])

        #entitlement start
        findEntitlementStart = self.__ticket.loc[self.__ticket["topup_title"] == title, "topup_entitlement_start_date"]
        self.__entitlementStart = str(findEntitlementStart.iloc[0])

        #entitlement end
        findEntitlementEnd = self.__ticket.loc[self.__ticket["topup_title"] == title, "topup_entitlement_end_date"]
        self.__entitlementEnd = str(findEntitlementEnd.iloc[0])

        #class name
        findClassName = self.__ticket.loc[self.__ticket["topup_title"] == title, "topup_passenger_class_name"]
        self.__className = str(findClassName.iloc[0])

        #quantity
        findQuantity = self.__ticket.loc[self.__ticket["topup_title"] == title, "topup_passenger_class_quantity"]
        self.__quantity = str(findQuantity.iloc[0])

        from datetime import date

        #date and time of purchase
        if ExistingTicket == False:
            self.__purchaseDate = str(date.today())
            self.__purchaseTime = str(datetime.now().time())
        else:
            self.__purchaseDate = purchaseDate
            self.__purchaseTime = purchaseTime

    #stores the ticket purchased
    def storeTicket(self, username):
        
        purchasedTickets = pd.read_csv("purchased_tickets.csv")
        purchasedTickets.loc[len(purchasedTickets)] = [username, self.__topup, self.__entitlementStart, self.__entitlementEnd, self.__purchaseTime, self.__purchaseDate]
        purchasedTickets.to_csv("purchased_tickets.csv", index=False) #stores the purchased ticket

    #gets the price of the ticket
    def getPrice(self):
        return self.__price
    
    #prints all the statistics of a ticket
    def showStatistics(self):
        print(f"{self.__topup} statistics: \n")

        print(f"catagory: {self.__catagory}")
        print(f"catagory description: {self.__catagoryDesc}")
        print(f"topup name: {self.__topup}")
        print(f"topup description: {self.__topupDesc}")
        print(f"price: {self.__price}")
        print(f"entitlement type: {self.__entitlementType}")

        #the if statements remove the values if they are blank in the csv table
        if self.__entitlementUnit != "nan":
            print(f"entitlement unit: {self.__entitlementUnit}")
        if not pd.isna(self.__entitlementValue):
            print(f"entitlement value: {self.__entitlementValue}")
        if not pd.isna(self.__entitlementQuantity):
            print(f"fentitlement quantity: {self.__entitlementQuantity}")
        if self.__entitlementStart != "nan":
            print(f"entitlement start date: {self.__entitlementStart}")
        if self.__entitlementEnd != "nan":
            print(f"entitlement end date: {self.__entitlementEnd}")

        print(f"class: {self.__className}")
        print(f"quantity: {self.__quantity}")
        print(f"date of purchase: {self.__purchaseDate}")
        print(f"time of purchase: {self.__purchaseTime}")
        print("----------------------------")

    #changes the price of the the ticket
    def changePrice(self, newPrice):
        ticketData = pd.read_csv("bus_ticket_data.csv")
        newPricePence = newPrice*100
        ticketData.loc[ticketData["topup_title"] == self.__topup, "topup_price_in_pence"] = int(newPricePence)
        ticketData.to_csv("bus_ticket_data.csv", index=False)

#########
#sign up#
#########

#used to create an account
def signUp():
    print("now entering sign up:")

    #asks to submite a username and password
    username = input("enter a username: ")
    password = input("enter a password: ")
    confirmPassword = input("confirm password: ")

    customerData = pd.read_csv("customer_data.csv")
    doesUsernameExist = customerData[(customerData["customer"] == username)] #checks if the username exists

    if password != confirmPassword: #checks if password and confirm password matches
        print("password and confirm password does not match")
        print("----------------------------")
        signUp()
    elif not doesUsernameExist.empty: #presence check
        print("username is already taken")
        print("----------------------------")
        signUp()
    else:
        addCustomer(username, password)
        print("----------------------------")
        menu(username)

#adds a new customer to the "customer_data.csv" file after sign up
def addCustomer(username, password):
    customerData = pd.read_csv("customer_data.csv") 

    #saves the data
    #how to write in a csv panda in https://stackabuse.com/reading-and-writing-csv-files-in-python-with-pandas/
    customerData.loc[len(customerData)] = [username, password, False, 0.0]
    customerData.to_csv("customer_data.csv", index=False)

#######
#login#
#######

#used to enter already existing account
def login():
    print("now entering login:")
    username = input("enter a username: ")
    password = input("enter a password: ")
    findAccount(username, password)

#finds if the account is valid
def findAccount(username, password):

    try:
        #extracts the correct username and password if possible
        customerData = pd.read_csv("customer_data.csv")
        passwordTracker = customerData.loc[(customerData["customer"] == username, "password")]
        passwordCheck = str(passwordTracker.iloc[0])
    except IndexError: #presence check
        incorrectData()

    try:
        if password != passwordCheck: #checks if the correct password was inputted
            incorrectData()
        else: #if both username and password is valid
            print("logging in")
            print("----------------------------")
    except UnboundLocalError:
        return
    menu(username)

#subroutine incase there is wrong credentials durings login
def incorrectData():
    print("username or password does not match")
    print("----------------------------")
    login()

######
#menu#
######

#system for menu navigation
def menu(username):

    #selects an option
    try:
        print("you are now in the menu:")
        action = int(input("""select an action to do:
    1 - select ticket to purchase
    2 - check and add to balance
    3 - view purchased tickets
    4 - gain admin permission
    5 - change ticket price (admin only)
    6 - logout
    7 - close program
    option: """))
    except ValueError:
        invalidError()
        menu(username)
        return

    #selects an option to preform based on the action input
    print("----------------------------")
    if action == 1: #select ticket to purchase
        print("select and purchase a ticket was selected")
        selectTicket(username, True)
    elif action == 2: #check and add to balance
        checkBalance(username)
    elif action == 3: #view purchased ticket
        viewTickets(username)
    elif action == 4: #gain admin permision
        gainAdmin(username)
    elif action == 5: #change price
        confirmAdmin(username)
    elif action == 6: #logout
        startUp()
    elif action == 7: #close program
        return()
    else:
        print("not within range")
        menu(username)

#prints out an error if a user does not input a number
def invalidError():
    print("please output a number")
    print("----------------------------")

###################
#admin permissions#
###################

#admin permissions
#password is 12345 (amazing I know)
def gainAdmin(username):
    customerData = pd.read_csv("customer_data.csv")
    findAdmin = customerData.loc[customerData["customer"] == username, "admin"]
    admin = bool(findAdmin.iloc[0])
    if admin == True:
        print("you are alreadt admin")
    else:

        #system to make a user admin
        password = input("please enter password to become admin: ") #password is 12345
        if password == "12345":
            print("password correct!")
            print("you are now admin")
            customerData.loc[customerData["customer"] == username, "admin"] = True
            customerData.to_csv("customer_data.csv", index=False)
        else:
            print("incorrect")
    print("----------------------------")
    menu(username)

#confirms if the user is an admin
def confirmAdmin(username):
    
    customerData = pd.read_csv("customer_data.csv")
    findAdmin = customerData.loc[customerData["customer"] == username, "admin"]
    admin = bool(findAdmin.iloc[0])

    #checks if the user has admin priverliges
    if admin == False:
        print("access denied: you are not an admin")
        print("----------------------------")
        menu(username)
    else:
        print("change price was selected")
        selectTicket(username, False)

#############
#view ticket#
#############

#view previously purchased tickets
def viewTickets(username):
    print("view purchased tickets was selected:")

    purchasedTicketData = pd.read_csv("purchased_tickets.csv")
    purchasedTickets = purchasedTicketData.loc[purchasedTicketData["ticket_holder"] == username, "topup_title"].reset_index(drop = True)
    purchaseDate = purchasedTicketData.loc[purchasedTicketData["ticket_holder"] == username, "date_of_purchase"].reset_index(drop = True)
    purchaseTime = purchasedTicketData.loc[purchasedTicketData["ticket_holder"] == username, "time_of_purchase"].reset_index(drop = True)
    if purchasedTickets.empty:
        print("you have no tickets to view")
        print("----------------------------")
        menu(username)
        return
    print("your owned tickets:")
    print(purchasedTickets)

    #gets a ticket to view
    while True:
        try:
            ticketOption = int(input("please select the ticket title number: "))
            selectedTicket = purchasedTickets.iloc[ticketOption] #the option the user selected
            break
        except ValueError:
            print("please submit a number")
            print("----------------------------")
        except IndexError: #range check
            print("not within range")
            print("----------------------------")
    ticketDate = str(purchaseDate.iloc[ticketOption])
    ticketTime = str(purchaseTime.iloc[ticketOption])
    print(ticketDate)

    #shows the statstics of the selected ticket
    ticket = busTicket(selectedTicket, True, ticketDate, ticketTime)
    print("----------------------------")
    ticket.showStatistics()

    menu(username)

#################
#purchase ticket#
#################

#first set of filter to select the tickets, asking for the catagory type
def selectTicket(username, buyTicket):

    while True:
        try:
            #asks for the catagory of the ticket to filter the search
            catagoryType = int(input("""select a ticket catagory:
                1 - Achademic Year tickets
                2 - single Tickets - City Zone
                3 - 24 hour Tickets - City zone
                4 - Group Tickets
                5 - Season Tickets - city Zone
                6 - Network Tickets
                7 - NCT partners
                option: """))
            break

        except ValueError:
            print("please input a number")
            print("----------------------------")
    
    print("----------------------------")
    #moves to topup based on input of tiket type
    if catagoryType == 1: #Academic Year Tickets
        selectTopup(username, "Academic Year Tickets", buyTicket)
    elif catagoryType == 2: #Single Tickets - City Zone
        selectTopup(username, "Single Tickets - City Zone", buyTicket)
    elif catagoryType == 3: #24 Hour Tickets - City Zone
        selectTopup(username, "24 Hour Tickets - City Zone", buyTicket)
    elif catagoryType == 4: #Group Tickets
        selectTopup(username, "Group Tickets", buyTicket)
    elif catagoryType == 5: #Season Tickets - City Zone
        selectTopup(username, "Season Tickets - City Zone", buyTicket)
    elif catagoryType == 6: #Network Tickets
        selectTopup(username, "Network Tickets", buyTicket)
    elif catagoryType == 7: #NCT Partners
        selectTopup(username, "NCT Partners", buyTicket)
    else:
        print("not within range")
        selectTicket(username, buyTicket)

        

#selects the topup of the ticket
def selectTopup(username, catagory, buyTicket):
    print(f"{catagory} was selected: ")
    #gets the specific catagory of tikets
    #got how to filter in pandas in https://www.youtube.com/watch?v=kB7FV-ijdqE
    ticketData = pd.read_csv("bus_ticket_data.csv")
    ticketDataCatagory = (ticketData[(ticketData["category_title"] == catagory)]["topup_title"]).reset_index(drop = True)
    #reset an index from https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.reset_index.html
    print(ticketDataCatagory)

    try:
        ticketOption = int(input("please select the ticket title number: "))
        selectedTicket = ticketDataCatagory.iloc[ticketOption] #the option the user selected
    except ValueError:
        print("please submit a number")
        print("----------------------------")
        selectTopup(username, catagory, buyTicket)
        return
    except IndexError: #range check
        print("not within range")
        print("----------------------------")
        selectTopup(username, catagory, buyTicket)
        return
    
    #stores the ticket
    ticket = busTicket(selectedTicket, False, "", "") #makes the bus ticket based on the catagory
    print(f"the price of {selectedTicket} is £{ticket.getPrice()}")

    if buyTicket == True: #if the user is here to buy a ticket
        #proceeding with ticket purchase
        customerData = pd.read_csv("customer_data.csv")
        findBalance = customerData.loc[customerData["customer"] == username, "balance"]
        balance = float(findBalance.iloc[0])

        #purchase of the ticket
        print(f"your current balance: £{balance}")
        while True:
            choice = input("proceed with purchase? (or type 'v' to vire the ticket data) [Y/N/V]: ")
            if choice == "Y" or choice == "y":
                if attemptCharge(username, ticket) == False:
                    print("insufficent funds!")
                else:
                    ticket.storeTicket(username)
                    print("purchase successful")
                break
            elif choice == "V" or choice == "v":
                print("----------------------------")
                ticket.showStatistics()
            elif choice == "N" or choice == "n":
                break
            else:
                print("not a valid choice")
                print("----------------------------")

    else: #if the user is here to change the ticket price
        #changes the price of the ticket
        print(f"the current price is {ticket.getPrice()}")
        while True:
            try:
                newPrice = float(input("what new price would you like the ticket? £"))
                break
            except ValueError:
                print("not a number")
        ticket.changePrice(newPrice)

    print("going back to menu")
    print("----------------------------")
    menu(username)


#compares user balance to ticket price
def attemptCharge(username, ticket):
    #fetches user balance
    customerData = pd.read_csv("customer_data.csv")
    findBalance = customerData.loc[customerData["customer"] == username, "balance"]
    balance = float(findBalance.iloc[0])
    price = ticket.getPrice()

    if (balance - price) < 0: #evaluates the price
        return False
    else:
        newBalance = balance - price
        customerData.loc[customerData["customer"] == username, "balance"] = float(newBalance)
        customerData.to_csv("customer_data.csv", index=False)
        return True

#########################
#view and change balance#
#########################
    
#allows the user to add to balance
def checkBalance(username):

    print("check balance was selected:")
    customerData = pd.read_csv("customer_data.csv")
    findBalance = customerData.loc[customerData["customer"] == username, "balance"]
    balance = float(findBalance.iloc[0])
    print(f"your current balance is: £{balance}")

    #asks to add money or not
    while True:
        addFunds = input("would you like to add funds into your account? [Y/N] ")
        if addFunds == "y" or addFunds == "Y":
            #adds funds and puts it into the csv file
            fundsAdd = float(input("enter how much funds you would like to submit: ")) #funds to be added to balance
            fundsAdd = round(fundsAdd, 2)#in the senario that the user provides a number with 3 or more digets after the decimal point (eg: 9.999)
            #how to round a float: https://www.datacamp.com/tutorial/python-round-to-two-decimal-places
            newBalance = balance + fundsAdd
            customerData.loc[customerData["customer"] == username, "balance"] = float(newBalance)
            customerData.to_csv("customer_data.csv", index=False)
            print(f"your balance is now £{newBalance}")
            break
        elif addFunds == "N" or addFunds == "n":
            break
        else:
            print("not a vlid option")
            print("----------------------------")
    
    #brings user back to menu
    print("going back to menu")
    print("----------------------------")
    menu(username)

##########
#start up#
##########

#first part of the menu
def startUp():
    #asks for input
    try:
        action = int(input("""select an action to do:
        1 - login
        2 - sign up
        3 - exit program
        option: """))
    except ValueError:
        invalidError()
        startUp()
        return
 
    #selects an option to preform based on the action input
    print("----------------------------")
    if action == 1: #login
        login()
    elif action == 2: #signup
        signUp()
    elif action == 3: #exit program
        return
    else:
        print("not within range")
        startUp()

#main
if __name__ == "__main__":
    print("----------------------------")
    startUp()
