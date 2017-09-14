from urllib.request import Request,urlopen
from bs4 import BeautifulSoup
import json
import sys
import sqlite3
import datetime
import os.path

#################################################
######## Variable Definitions ###################
#################################################
#Jake Key
#API_KEY = "&key=AIzaSyCByJyaQYmYnTMrZ5Pa6E3oq9yXaJrEapI"
#Sean Key
API_KEY = "&key=AIzaSyAwYtk1q7XpC5WfVzVJjNNtL3RYgjG9uIA"
TSEARCH_BASE_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="
PLACES_DETAIL_URL = "https://maps.googleapis.com/maps/api/place/details/json?placeid="
BUSINESSES = []
db_path = "saved_searches.db"
db_connected = False
#################################################
######### Function definitions ##################
#################################################
def get_listings(url_to_open):
    global BUSINESSES
    BUSINESS_DETAILS = {}

    try:
        response = urlopen(url_to_open).read().decode('utf-8')
    
    except Exception as e:
        print(e)

    responseJson = json.loads(response)
    results = responseJson['results']
    
    
    print("\n\n------------------------Results------------------------\n")
    for result in results:
        #get place_id
        place_id = result['place_id']
        print('\n')
        print(result['name'])
        BUSINESS_DETAILS['name'] = result.get('name', 'Name not found')
        
        #new Query to get individual place details
        place_info = get_placedetails(place_id)
        
        
        #List Place Details
        phone = place_info.get('formatted_phone_number',"No Phone Found")
        BUSINESS_DETAILS['phone_number'] = place_info.get('international_phone_number','No Phone Number')
        
        address = place_info.get('formatted_address',"No Address Found")
        BUSINESS_DETAILS['formatted_address'] = place_info.get('formatted_address','No Address Found')
                         
        website = place_info.get('website',"No Website Found")
        BUSINESS_DETAILS['website'] = place_info.get('website', 'No Website')
        
        if result['name'] not in BUSINESSES:
            BUSINESSES.append(BUSINESS_DETAILS)
            BUSINESS_DETAILS = {}
                         
        print (phone)
        print (address)
        print (website)
        
    print("\n")
 
#

## Note to Jake> Code refactor: Need to format to be same as listings, add second param to pass
## This allows call from handler while passing variables
def get_placedetails(place_id):
    #query place details
    response = urlopen(PLACES_DETAIL_URL + place_id + API_KEY).read().decode('utf-8')
    responseJson = json.loads(response)
    results = responseJson['result']
    return results


# Print Menu
def menu():
    print("* " * 10)
    print("Jake and Seans Python Script")
    print("* " * 10)
    print("Current Date/Time is: ",datetime.datetime.now())
    print("\n")
    print("1. Search for place")
    print("2. Search for saved businesses")
    print("3. Exit")
    selection = input("> ")
    return selection

# Handle menu selection
def handler(selection):
    if selection == "1":
        search = input("Enter search term\n> ")
        search_term = search.replace(" ", "+")
        get_url = TSEARCH_BASE_URL + search_term + API_KEY
        get_listings(get_url)
    elif selection == "2":
        selection = input("Please enter name to search for\n> ")
        search_lists(selection)
    elif selection == "3":
        sys.exit(0)
        
# Create local db to store our data
def connect_db(db_path):
        global db_connected
        if db_connected == False:
            conn = sqlite3.connect(db_path)
            print("Database Connected...")
            c = conn.cursor()
            db_connected = True
        else:
            pass
        return c, conn

# Make changes to database, pass c cursor to call
def write_to_db(c, data_to_write):
    pass

# Read data from db
def query_db(c):
    print("Querying DATABASE")
    sql = "SELECT * FROM searches"
    for row in c.execute(sql):
        print(row)
    
    

def create_new_db(db_path):
    if not os.path.isfile(db_path):
        c, conn = connect_db(db_path)
        sql = "CREATE TABLE searches(name text, phone_number text, address text, website text)"
        c.execute(sql)
        sql = "INSERT INTO searches VALUES('test','test1','test2','test3')"
        c.execute(sql)
        conn.commit()
    else:
        c, conn = connect_db(db_path)
        print(type(c))
        #c.execute("INSERT INTO searches VALUES('blah', 'blah2', 'blah3', 'blah4')")
        conn.commit()
        query_db(c)

# Function to check lists
def search_lists(selection):
    global BUSINESSES
  
    try:
        create_new_db(db_path)
    except Exception as e:
        print(e)

    for BUSINESS in BUSINESSES:
        if selection in BUSINESS['name']:
            print("\nName: ", BUSINESS['name'])
            print("Address: ", BUSINESS['formatted_address'])
            print('Phone Number: ', BUSINESS['phone_number'])
            print('Website: ', BUSINESS['website'])
            print('\n')
            


#################################################
######### Main Code #############################
#################################################

while True:
    selection = menu()
    handler(selection)
