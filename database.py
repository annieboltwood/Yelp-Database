#Annie Boltwood

#Imports
import pyodbc
import uuid 
import datetime
import secrets

#Connecting to Database
connection = pyodbc.connect('DRIVER={SQL Server};Server=cypress.csil.sfu.ca;database=aeb17354;pwd=jQ4LhA2LJRFmj367')
cursor = connection.cursor()


# example user ID for testing: __hr-GtD9qh8_sYSGTRqXw and _08KWbJrc27Qdt6_OWU9yQ
# example of business ID for testing: g2leve1c8LW9ZTlEygMK8Q

#Initialize User
current_user = None

#Accesses Database to Validate ID
#Used for user ID and Business ID
def valid_ID(id, typeID, database):
    #Retrieving user IDs from database and storing in array 
    SQLCommand = ("SELECT "+ str(typeID) +" FROM "+ str(database)) 
    cursor.execute(SQLCommand)
    queryList = cursor.fetchall()

    #Returns true if ID matches any of the results
    return any(attribute[0] == id for attribute in queryList)

#Perform Login Function
def perform_login():
    global current_user
    #Login Screen
    print("[LOGIN]")
    print("Please input your user credentials to access the system.")
    id = input("User ID: ")

    #Loops Error until ID is valid
    while not valid_ID(id,"user_id","user_yelp"):
        print("ERROR Invalid user ID. Please try again.")
        id = input("User ID: ")

    #Sets global var current_user to the valid ID
    current_user = id

    #Interface Messages
    print("Login successful")
    print("Welcome user " + current_user + "!")
    print()

#Helper function for menu function to take valid integer input in a range
def takeIntInput(strInput, min, max):
    num = None

    while (num is None) or (num < min or num > max):
        error = False
        try:
            #Cast int, if Error, then retry
            num = input("Please enter " + strInput + ": ")
            if (len(num) == 0):
                return None
            num = int(num)
        except ValueError:
                print("ERROR invalid integer")
                num = None
                error = True

        if(error!= True):
           
            if (num < min or num > max):
                print("ERROR Integer not within " + str(min) + "-" + str(max) + " range")
    return num

#Helper function for menu function to take valid integer input given a minimum
def takeIntInputMin(strInput, min):
    num = None

    while (num is None) or (num < min):
        error = False
        try:
            #Cast int, if Error, then retry
            num = input("Please enter " + strInput + ": ")
            if (len(num) == 0):
                return None
            num = int(num)
        except ValueError:
                print("ERROR invalid integer")
                num = None
                error = True

        if(error!= True):
           
            if (num < min):
                print("ERROR Integer not less than " + str(min))
    return num

#Menu Selection Function
def menu():

    #Main Menu Interface
    print("[MENU]")
    print("----------------")
    print("[1] Search Business")
    print("[2] Search Users")
    print("[3] Make Friend")
    print("[4] Review Business")
    print("[5] Exit")
    print()

    #call input helper function
    num = takeIntInput("your menu selection", 1, 5)
    print()

    while(num == None):
        print("Selection cannot be blank! Try again")
        num = takeIntInput("your menu selection", 1, 5)
        print()

    #Input Options
    if (num == 1):
        searchBusiness()
    if (num == 2):
        searchUsers()
    if (num == 3):
        makeFriend()
    if (num == 4):
        reviewBusiness()
    #If num if 5, then the loop finishes and program closes

#Function to take order input
def orderInputBusiness():
    order = None

    #Interface
    print("How would you like to order the results?")
    print("Type [n] to order by name")
    print("Type [c] to order by city")
    print("Type [s] to order by stars")
    print("Press [ENTER] for default sort by name")

    #Checks if input meets the conditions
    while order is None or (order not in ["n","c","s"] and order != ""):
        if(order is not None):
            print("ERROR please try again")

        order = input("Please enter the order: ").lower()
    
    print()
    return order


#Search Business Function
def searchBusiness():

    #Interface
    print("[SEARCH BUSINESS]")
    print("----------------")
    print("Instructions: You will be prompted to input filters for the search")
    print("Press [ENTER] to skip a filter")

    #Collecting Information
    #Star input requires separate function 
    minStar = takeIntInput("the minimim number of stars", 1,5)
    city = input("City: ")
    name = input("Business Name: ")
    print()
    
    #Apply Filters to Query
    q = ("SELECT * FROM business b WHERE 0=0")
    if (minStar != None):
        q += " AND b.stars >= " + str(minStar)
    if (city != ""):
        q += " AND b.city LIKE '%" + city + "%'"
    if (name != ""):
        q += " AND b.name LIKE '%" + name + "%'"

    #Function to input the order of the results
    order = orderInputBusiness()
    
    #Order by Specified input
    if(order == "n" or order == ""):
        q += " ORDER BY b.name"
    if(order == "c"):
        q += " ORDER BY b.city"
    if(order == "s"):
        q += " ORDER BY b.stars"
    
    #Getting results
    cursor.execute(q)
    queryList = cursor.fetchall()
    count = 0
    for attribute in queryList:
        count += 1
        print("[BUSINESS "+ str(count) + "]")
        print("ID: ", attribute[0])
        print("Name: ", attribute[1])
        print("Address: ", attribute[2])
        print("City: ", attribute[3])
        print("Stars: ", attribute[5])
        print("")

    #Printing Number of Results found 
    print()
    if (not queryList):
        print("[NO RESULTS MATCH THE CRITERIA]")
        print()
    else:
        print("[TOTAL: " + str(count) + " RESULTS FOUND]")
        print()

    #Return to menu
    menu()

#Search User Function
def searchUsers():
    #Interface
    print("[SEARCH USER]")
    print("----------------")
    print("Instructions: You will be prompted to input filters for the search")
    print("Press [ENTER] to skip a filter")

    #Collecting Information
    minReviewCount = takeIntInputMin("The minimum review count",1)
    minAvgStars = takeIntInput("The minimum average stars",1,5)
    name = input("User's Name:")
    print()

    #Apply Filters to Query
    q = "SELECT * FROM user_yelp y WHERE 0=0"
    if (minReviewCount != None):
        q += " AND y.review_count >= " + str(minReviewCount)
    if (minAvgStars != None):
        q += " AND y.average_stars >=" + str(minAvgStars)
    if (name != ""):
        q += " AND y.name LIKE '%" + name + "%'"
    
    #Order by Name
    q += " ORDER BY y.name"

    #Getting Results
    cursor.execute(q)
    queryList = cursor.fetchall()
    count = 0
    for attribute in queryList:
        count += 1
        print("[BUSINESS "+ str(count) + "]")
        print("ID: ", attribute[0])
        print("Name: ", attribute[1])
        print("Review Count: ", attribute[2])
        if(attribute[4] == 0):
            print("Useful: NO")
        if(attribute[4] > 0):
            print("Useful: YES")
        if(attribute[5] == 0):
            print("Funny: NO")
        if(attribute[5] > 0):
            print("Funny: YES")
        if(attribute[6] == 0):
            print("Cool: NO")
        if(attribute[6] > 0):
            print("Cool: YES")
        print("Average Stars: ", attribute[8])
        print("Register Date: ", attribute[3])
        print("")

    #Printing Number of Results found 
    print()
    if (not queryList):
        print("[NO RESULTS MATCH THE CRITERIA]")
        print()
    else:
        print("[TOTAL: " + str(count) + " RESULTS FOUND]")
        print()

    #Return to Menu
    menu()

def makeFriend():
   
    #Interface
    print("[MAKE FRIEND]")
    print("----------------")
    print("Instructions: You will be prompted to input the user ID of the person you want to become friends with")
    print("Press [ENTER] to cancel friend selection")
    friend = input("Enter friends's User ID: ")
    print()

    #Check that the friend ID is valid
    while((not valid_ID(friend, "user_id", "user_yelp") or (friend is current_user))and friend != ""):
        print("ERROR Input Invalid")
        friend = input("Try again. Enter friends's User ID: ")
        print()
    
    #Insert friendship if the action was not skipped
    if(friend != "" and friend != current_user):
        q = f"INSERT INTO friendship (user_id, friend) VALUES ('{current_user}','{friend}')"
        try:
            cursor.execute(q)
            connection.commit()
            print("Friendship with user: " + friend + " SUCCESSFUL!")
            print()
        except:
            print("ERROR You are already friends with user " + friend)
            print()
    elif(friend == current_user):
        print("ERROR you cannot be friends with yourself")
    else:
        print("Friend Selection Cancelled")
        print()
    
    print()
    #Return to main menu
    menu()


def reviewBusiness():
    #Interface
    print("[WRITE A REVIEW]")
    print("----------------")
    print("Instructions: You will be prompted to input the business ID of the business you want to review")
    print("Press [ENTER] to cancel review insertion")
    id = input("Enter Business ID: ")

    #Call the valid_ID function with arguments that check for valid business
    while((valid_ID(id,"business_id","business") is False) and (id != "")):
        print("ERROR Input Invalid")
        id = input("Try again. Enter Business ID: ")
        print()

    #If actions are not cancelled, then insert review
    if(id != ""):
        starNum = takeIntInput("the number of stars you would like to give this business", 1, 5)
        rID = secrets.token_hex(11)
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        q = f"INSERT INTO review  (review_id, user_id, business_id, stars, useful, funny, cool, date) VALUES ('{rID}','{current_user}','{id}',{starNum}, 0, 0, 0, '{time}')"

        try:
            cursor.execute(q)
            connection.commit()
            print("Add Review to business " + id + " SUCCESSFUL!")
            print()
        except:
            print("ERROR review was not able to be inserted")
            print()
    else:
        print("Review Business Cancelled!")
        print()

    menu()


#Main function
def main():

    #Welcome Interface
    print("[YELP DATABASE]")
    print("----------------")
    print("Welcome to Yelp Data Edmonton!")
    print("Please log in with a valid yelp user ID and follow the prompted instructions to retrieve yelp data")
    print()

    #Login function is called
    perform_login()

    #Menu Function Called
    menu()
    connection.close()
    
    print()
    print("[PROGRAM END]")

#Run the program
main()


#End of Program
