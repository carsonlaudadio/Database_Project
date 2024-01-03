
Name. 
carsonlaudadio_source_code.py

Description. 
launches an application that allows the user to manage a user DATABASE
for a plant app called platnly. The database manager (this code) allows
the user to select an existing list of users and view which plants are 
registered to them.
They can then view the details of on each plant that the user owns.
Towards the bottom the user has the ability to add users to the database.


Visuals.
Buttons to execut each section are located right below list boxes. For 
inserting a user there are three open text fields. 

Installation.
1) The user needs to save 'carsonlaudadio_source_code.py' to their directory.

2) Before running, the user needs to add their mySQL information on line 159.

3) The user will need to run a server with the sql code 
   'carsonlaudadio_Generate.sql'

4) Execute the code in the command line of a terminal by typing:
   python carsonlaudadio_source_code.py

Usage.
1) Select a user from the list of red names

2) Click 'Select User' button

3) Select a plant from the list of yellow names
    - NOTE: some users do not have any regisered plants. Recommend selecting
            'carlton ladidio' for the best selection
    - NOTE: descriptors to those plant details have not been added. user is looking
            at plant ideal temperature, sun, soil pH and environment

4) Optional- if the user wishes to clear the list of plants click 'Clear Selection'

5) Inserting a user
    a. input a number greater than 15 for the user's ID. If a users alredy exists 
       the program wil not allow the user to input a new user. Try choosing another
       user ID.
    b. insert a single first name
    c. insert the last name in the last fields
    d. click 'Insert User'
        -NOTE: if the user attempts to insert an additional name during a session the
               previously entered name will appear. This is a bug. The name was correctly
               stored. 

6) Click the 'Quit' button to exit the application
    -NOTE: doesn't stop the script. To end the code click ctrl+c and then click the python
           rocket icon. 

Support.
contact carson laudadio ASAP if you are grading!
cjl0031@uah.edu
(970) 210-2664


Roadmap.
1) Fix the following bugs: 
    a. user list duplication after insert more than one user
    b. fix format of plant details
    c. fix quit button

2)  add descriptions to plant 'ideal attributes'

3)  add 'remove user' button to remove users

4)  add more fields to add more user attributes

5)  add method to add/remove registered plants to users
