from turtle import window_width
from django.db import connection
from matplotlib.pyplot import text
import mysql.connector
from mysql.connector import errorcode
from tkinter import *
from tkinter import ttk
import tkinter as tk
import re

from numpy import empty


m_rPlantName = []
m_rTemperature = []
m_rUsersName = []
m_aRegisteredPlants = []
m_rRegistered_plants = []
m_sPlantDesignationID = []
m_sPlantName = []
m_aUserID = []
count = 1

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
    print("\n\ncleaned selection:\n")
    print(cleaned_selection)
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
    if m_aRegisteredPlants is not 0 :
        del m_aRegisteredPlants[:]
    UserID_selection = get_user_details()
    print(UserID_selection)
    print("\n\n\nRegistered Plants:\n")
    registered_plants_query = ("SELECT PlantName FROM registered_plants INNER JOIN users ON users.UserID = registered_plants.UserID WHERE users.UserID = (%s);")
    cursor.execute(registered_plants_query, (UserID_selection,))
    for(PlantName) in cursor:
        m_aRegisteredPlants.append(PlantName)
        print(m_aRegisteredPlants)
    n = len(m_aRegisteredPlants)
    element = ''
    for i in range(n):
        listbox.insert(1, m_aRegisteredPlants[i])
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

  users_name_query = ("SELECT first_name, last_name  FROM users")
  cursor.execute(users_name_query)
  for(UsersName) in cursor:
        print("{}".format(UsersName))
        m_rUsersName.append(UsersName)
  print("\nName of Users:\n")
  print(m_rUsersName)

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

###############################################
#Fill the user text box with the list of users in the database
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
ttk.Button(top, text="Insert User", command=insert_user).pack()
quit_button.pack()
frm = ttk.Frame(root, padding=20)
frm.grid()
top.mainloop()
cursor.close()
cnx.close()