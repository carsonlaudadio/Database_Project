from turtle import window_width
from django.db import connection
from matplotlib.pyplot import text
import mysql.connector
from mysql.connector import errorcode
from tkinter import *
from tkinter import ttk
import tkinter as tk
import re
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timezone
import certifi
from numpy import empty
import pymongo
from usersList_fetch import fetchFirstNames

m_rPlantName = []
m_rTemperature = []
m_rUsersName = []
m_aRegisteredPlants = []
m_rRegistered_plants = []
m_sPlantDesignationID = []
m_sPlantName = []
m_aUserID = []
count = 1


uri = "mongodb+srv://carsonlaudadio:Portas123!@cluster0.5lze99u.mongodb.net/?retryWrites=true&w=majority"
        
def delete():
   listbox.delete(0,END)
   #Label(top, text="Nothing Found Here!", font=('TkheadingFont, 20')).pack()

def printInput():
        inp = inputtxt.get(1.0, "end-1c")
        print(inp)
        return inp

def get_plant() :
    for i in listbox.curselection() :
        print("right here")
        print(listbox.get(i))
    return listbox.get(i)

def get_user() :
    for i in listbox_users.curselection() :
        print(listbox_users.get(i))
    return listbox_users.get(i)

def insert_user_with_Mongo():
    try:
            # Preparing SQL query to INSERT a record into the database
        UserID = inputtxt.get(1.0, "end-1c")
        first_name = inputtxt_first_name.get(1.0, "end-1c")
        last_name = inputtxt_last_name.get(1.0, "end-1c")
        sensor_ID = inputtxt_sensor_ID.get(1.0, "end-1c")
        client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
        database = client['plantlyDB']
        userInputs = {"time":datetime.now(),"user_id":UserID,"first_name":first_name,"last_name":last_name,"sensor_ID":sensor_ID}
        database["users"].insert_one(userInputs)
        Label(top, text="Input Accepted!", font=('TkheadingFont, 16')).pack()
    except:
        # Rolling back in case of error
        Label(top, text="Failed to add user. Try different inputs", textvariable=UserID, font=('TkheadingFont, 16')).pack()
        print("\nunsuccessful. failed to add user \n{}, {}, {}\n".format(UserID,first_name,last_name))
        cnx.rollback()

def insert_user() :
    # Preparing SQL query to INSERT a record into the database
    UserID = inputtxt.get(1.0, "end-1c")
    first_name = inputtxt_first_name.get(1.0, "end-1c")
    last_name = inputtxt_last_name.get(1.0, "end-1c")
    print("\n\n{}, {}".format(first_name, last_name))
    sql = """INSERT INTO users VALUES ((%s), (%s), (%s), 'AL','coolio','notapassword');"""
    try:
    # Executing the SQL command
        cursor.execute(sql, (UserID, first_name, last_name,))
    # Commit your changes in the database
        cnx.commit()
        #updating listbox_users
        users_name_query = ("SELECT first_name, last_name  FROM users")
        cursor.execute(users_name_query)
        for(UsersName) in cursor:
            print("{}".format(UsersName))
        m_rUsersName.append(UsersName)
        print("\nName of Users:\n")
        n = len(m_rUsersName)
        listbox_users.delete(0, END)
        for i in range(n):
            listbox_users.insert(END, m_rUsersName[i])
        Label(top, text="Input Accepted!", font=('TkheadingFont, 16')).pack()
    
    except:
    # Rolling back in case of error
        Label(top, text="Failed to add user. Try different inputs", textvariable=UserID, font=('TkheadingFont, 16')).pack()
        print("\nunsuccessful. failed to add user {}, {}, {}\n".format(UserID,first_name,last_name))
        cnx.rollback()

def get_plant_details() : 
    if m_sPlantDesignationID is not 0 :
        del m_sPlantDesignationID[:] 
    plant_selection = get_plant()
    m_sPlantSelection =str(''.join(plant_selection))
    queriedForPlantID = ("SELECT PlantDesignationID FROM plantcatalog WHERE PlantName = (%s)")
    cursor.execute(queriedForPlantID, (m_sPlantSelection,))
    for(PlantDesignationID) in cursor:
        m_sPlantDesignationID.append(PlantDesignationID)
    bar = str(m_sPlantDesignationID[0])
    foo = removeSymbols(bar)
    m_iFoo = int(foo)
    return m_iFoo
#unfortunately the query relies on the last name to match
#if two users were to have the same last name issues may arise
#this is a bug fix that will need to be completed
def theLastWord(my_str) :
    word_list = my_str.split()  # list of words
    #returns the last word in a string that contains first and last name
    return word_list[-1]

def get_user_details() :  
    selection = get_user()
    #the information comes in as tuples e.g., (4, )
    #this section removes and converts to a string for the query
    m_sSelection =str(selection)
    stripped_selection = removeSymbols(m_sSelection)
    cleaned_selection = theLastWord(stripped_selection)
    #print("\n\ncleaned selection:\n")
    #print(cleaned_selection)
    
    #Querying using MongoDB
    client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
    database = client['plantlyDB']
    mycol = database["users"]
    myquery = {"first_name": selection }
    output = mycol.find(myquery)
    
    try:
            client.admin.command('ping')
            print("\n\nYou successfully connected to users in get_user_details()!")
    except Exception as e:
            print('\n')
            print(e)
            print('\nping failed')
    try:
        print("output is: {}".format(output))
        userIDQuery = {"user_id": {}}
        m_iFoo = mycol.find_one(userIDQuery)
        print(m_iFoo)
        # iterate pymongo documents with a for loop
        #for doc in output:
        #append each document's ID to the list
            #m_aUserID += [doc["first_name"]]
            #print(doc)
        # print out the IDs
        #print ("\n\ntotal # of names:", len(m_aUserID))
        #print(m_aUserID)
  
        #print ("\n\ntotal # of queried names:", len(m_aUserID))
        
    except:
        print("You did not sucessfully find the UserID. Check get_user_details.")
    #this section is about taking the query and cleaning the output
        user_query = ("SELECT UserID FROM users WHERE last_name = (%s)")
        cursor.execute(user_query, (cleaned_selection,))
        for(UserID) in cursor:
            m_aUserID.append(UserID)
            print(m_aUserID)
        foo = m_aUserID[-1]
        bar = str(foo)
        cleaned_selection = removeSymbols(bar)
        m_iFoo = int(cleaned_selection)
        print(m_iFoo)
    

    
    return m_iFoo

def addNewPlantToUser() :
    top = Toplevel()
    top.geometry("200x200") 
    top.title("About this Plant...")

def plant_catalog_selection() :
    m_sPlantDesignationID = get_plant_details()
    if m_sPlantName is not 0 :
        del m_sPlantName[:]
    query_aPlantCatalog= ("SELECT PlantName, IdealSoil_pH, IdealSunlight, IdealTemperature, Environment FROM plantcatalog WHERE PlantDesignationID = %s")
    cursor.execute(query_aPlantCatalog, (m_sPlantDesignationID,))
    print("\n\n")
    for(PlantName) in cursor:
        m_sPlantName.append(PlantName)
    bar = str(m_sPlantName[0])
    foo = removeSymbols(bar)
    print(foo)
    top = Toplevel()
    top.geometry("200x200") 
    top.title("About this Plant...")
    msg = Message(top, text=foo)
    msg.pack()
    button = Button(top, text="Dismiss", command=top.destroy)
    button.pack()
    return foo

def users_registered_plants() :
    try:
        print("\n\nI'M HERE\n\n")
        UserID_selection = get_user_details()
        print("The User ID selected is: {}\n".format(UserID_selection))
        if m_aRegisteredPlants is not empty :
            del m_aRegisteredPlants[:]
        else:
            addNewPlantToUser()
            print("\n\nWait...I'm here\n")
        print("\n\n\nRegistered Plants:\n")
        
        database = client['plantlyDB']
        mycol = database["sensorData"]
        myquery = {"humidity": 1014 }
        output = mycol.find(myquery)
        firstNames = []
        try:
                client.admin.command('ping')
                print("\n\nPinged your deployment. You successfully connected to your sensor data!")
        except Exception as e:
                print('\nping failed\n\n{}\n'.format(e))
        try:
            # iterate pymongo documents with a for loop
            for doc in output:
            # append each document's ID to the list
                m_rRegistered_plants += [doc["temperature"]]
            # print out the IDs
            print(m_rRegistered_plants)
            print ("\n\ntotal # of queried plants:", len(m_rRegistered_plants))
           
        except:
            registered_plants_query = ("SELECT PlantName FROM registered_plants INNER JOIN users ON users.UserID = registered_plants.UserID WHERE users.UserID = (%s);")
            print(m_aRegisteredPlants)
            cursor.execute(registered_plants_query, (UserID_selection,))
        for(PlantName) in cursor:
            m_aRegisteredPlants.append(PlantName)
            print(m_aRegisteredPlants)
        n = len(m_aRegisteredPlants)
        element = ''
        for i in range(n):
            listbox.insert(1, m_aRegisteredPlants[i])
    except:
        m_aRegisteredPlants = 0
    return m_aRegisteredPlants
##########################################################

def removeSymbols(stringWithPuncuation) :
    m_sStringStripped = re.sub(r'[^\w]', ' ', stringWithPuncuation)
    return m_sStringStripped

try:
  cnx = mysql.connector.connect(user='root', password='fulminata',
                                database='Plantly')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:

#retrieving static data from database
  cursor = cnx.cursor()
  PlantName_query = ("SELECT PlantName FROM plantcatalog")
  cursor.execute(PlantName_query)
  for(PlantName) in cursor:
        print("{}".format(PlantName))
        m_rPlantName.append(PlantName)
  print(m_rPlantName)

  Temperature_query = ("SELECT IdealTemperature FROM plantcatalog")
  cursor.execute(Temperature_query)
  for(PlantName) in cursor:
        m_rTemperature.append(PlantName)
  print(m_rTemperature)

 



##################################################
root = Tk()
top = Tk()
top.background=("green")
top.geometry("400x875")  
# create listbox object
label_registeredPlantBox = Label(top, text = "\nSelect palnt to see details")
listbox = Listbox(top, height = 10, 
                  width = 15, 
                  bg = "grey",
                  activestyle = 'dotbox', 
                  font = "Helvetica",
                  fg = "yellow")
# create listbox object
label_userBox = Label(top, text = "\nSelect user to see list of registered plants")
listbox_users = Listbox(top, height = 14, 
                  width = 15, 
                  bg = "grey",
                  activestyle = 'dotbox', 
                  font = "Helvetica",
                  fg = "red")
# Define the size of the window.

# TextBox Creation UserID input
label_userID = Label(top, text = "\nInupt numerical ID of new User (input>15)")
inputtxt = tk.Text(top, bg="light gray",
                   height = 1,
                   width = 15)

# TextBox Creation first_name input
label_first_name = Label(top, text = "\nInupt first name of new User")
inputtxt_first_name = tk.Text(top, bg="light gray",
                   height = 1,
                   width = 15)

# TextBox Creation last_name input
label_last_name = Label(top, text = "\nInupt last name of new User")
inputtxt_last_name = tk.Text(top, bg="light gray",
                   height = 1,
                   width = 15)

# TextBox Creation last_name input
label_plant_sensor_ID = Label(top, text = "\nInupt Plant Sensor ID")
inputtxt_sensor_ID = tk.Text(top, bg="light gray",
                   height = 1,
                   width = 15)

###############################################


######################################get_users###################
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
database = client['plantlyDB']
mycol = database["users"]
myquery = {}
output = mycol.find(myquery)
firstNames = []

try:
        client.admin.command('ping')
        print("\n\nPinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
        print('\n')
        print(e)
        print('\nping failed')
         

      
  # iterate pymongo documents with a for loop
for doc in output:
  # append each document's ID to the list
    m_rUsersName += [doc["first_name"]]
   

# print out the IDs

print ("\n\ntotal # of names:", len(m_rUsersName))
n = len(m_rUsersName)

element = ''
for i in range(n):
    listbox_users.insert(1, m_rUsersName[i])
label_title = Label(top, text="Plantly Database Manager!", font=('TkheadingFont, 20'))
#insert list of plants
m_rRegistered_plants = users_registered_plants
listbox.insert(1, '')
################################################

select_user_button = Button(top, text="Select User", command=users_registered_plants)
submit_button = Button(top, text="Get Details", command=plant_catalog_selection)
quit_button = Button(top, text="Quit", command=top.destroy)
label_title.pack()
label_userBox.pack()
listbox_users.pack()
select_user_button.pack()
label_registeredPlantBox.pack()
listbox.pack()
submit_button.pack()
ttk.Button(top, text="Clear Selection", command=delete).pack()
label_userID.pack()
inputtxt.pack()
label_first_name.pack()
inputtxt_first_name.pack()
label_last_name.pack()
inputtxt_last_name.pack()
label_plant_sensor_ID.pack()
inputtxt_sensor_ID.pack()
ttk.Button(top, text="Insert User", command=insert_user_with_Mongo).pack()
quit_button.pack()
frm = ttk.Frame(root, padding=20)
frm.grid()
top.mainloop()
cursor.close()
cnx.close()