from argparse import Action
import re  # importing regular expression operations
import sqlite3
from profile import userprofile # importing sqlite for database
from student import Student # importing student class
from friends import * # import all functions from the friends module
from jobs import * # import all functions from the jobs module
from settings import * # import all functions from the settings module
from messages import * # import all functions from the messages module
from inputAPIs import * # import all functions from the input API module
from outputAPIs import * # import all functions from the output API module
import datetime



# function to check if profile exists
def profileExists(studentUserName: str) -> bool:
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()
    c.execute("SELECT * FROM profile WHERE username = ?", (studentUserName, ))
    res = c.fetchall()
    c.close()
    conn.close()
    if res:
        return True
    return False


# function to check if there are pending messages
def hasPendingMessages(studentUserName: str) -> bool:
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()
    c.execute("SELECT pending FROM students WHERE username = ?", (studentUserName, ))
    pendingMessagesFrom = c.fetchone()[0]
    c.close()
    conn.close()
    if pendingMessagesFrom.strip():
        return True
    return False

# Function to check if recently applied
def recentlyApplied(studentUserName: str) -> bool:
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()
    c.execute("SELECT appliedDate FROM jobstatus WHERE username = ?", (studentUserName, ))
    dates = [d[0] for d in c.fetchall() if d]
    dates = sorted(dates, reverse=True)
    now = datetime.datetime.now()

    c.close()
    conn.close()

    for d in dates:
        try:
            appliedTime = datetime.datetime(*[int(e) for e in d.split("-")])
            timeDelta = now - appliedTime
            if timeDelta.days <= 7:
                return True
            else:
                return False
        except Exception:
            continue
    return False


# Add an entry with all students with the new student so as to notify new admission
def markNewStudentNotificationEntry(newStudent):
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()
    c.execute("SELECT username FROM students WHERE username != ?", (newStudent, ))
    allStudents = set([s[0] for s in c.fetchall() if s])
    for s in allStudents:
        c.execute("INSERT INTO new_student_notifs VALUES(?, ?)",(s, newStudent))

    conn.commit()

    c.close()
    conn.close()


# Get all new admission notifications
def checkNewAdmissions(studentUserName: str) -> list:
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    c.execute("SELECT notif_username FROM new_student_notifs WHERE username = ?", (studentUserName,))
    newAdmissions = set([s[0] for s in c.fetchall() if s])

    data = []
    for s in newAdmissions:
        c.execute("SELECT firstname, lastname FROM students WHERE username = ?", (s, ))
        record = c.fetchone()
        data.append(tuple([s] + list(record)))

    c.close()
    conn.close()
    return data

# Delete a new admission entry for the current user
def deleteNewAdmissionNotification(curUser, newusername):
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()
    c.execute("DELETE FROM new_student_notifs where username = ? and notif_username = ?",(curUser, newusername))
    conn.commit()

    c.close()
    conn.close()



# Function to show notifications
def showNotification(message: str) -> None:
    print(
        "\n!!! NOTIFICATION !!! {}".format(message)
    )




def menuOptions(tempStudent):
    while True:
        # code goes here...
        # connecting to sqlite database
        conn = sqlite3.connect('incollege.db')
        c = conn.cursor()

        c.execute("SELECT pending FROM students WHERE username = ?", (tempStudent.username, ))
        pending = c.fetchone()[0]

        if(pending != ''):
            print(
                "\n!!! NOTIFICATION !!! You have a pending friend request! Select Friends to accept/reject your request(s)."
            )



        print(
            "\nChoose an option:\n1) Job search / Internships\n2) Friends\n3) Learn a new skill\n4) View Profile\n5) InCollege Important Links\n6) Inbox\n0) LOG OUT\n"
        )  # menu list
        action = input("Type a number from 1-6, or 0 to go back: "
                       )  # collect user input/option
        if action == "0":  # option 0 : log out
            conn.close()
            main_menu()  # returns back to welcome screen
        elif action == "1":  # option 1 : Jobs and internships
            conn.close()
            jobs(tempStudent) # redirects to job page
        elif action == "2":  # option 2 : friends
            conn.close()
            friends(tempStudent)
        elif action == "3":  # option 3 : learn new skill
            conn.close()
            loadTraining()
        elif action == "4":  # option 4 : profile
            conn.close()
            userprofile(tempStudent)
        elif action == "5":  # option 5 : important links
            conn.close()
            importantLinks(tempStudent)  # redirects to important links
        elif action == "6": # option 6: inbox
            conn.close()
            inbox(tempStudent)
        else:
            print("Invalid entry!")  # otherwise invalid entry and loop back


def general():
    # code goes here...
    while True:
        # GENERAL
        print(
            "\nSelect any of the following links:\n1) Sign Up\n2) Help Center\n3) About\n4) Press\n5) Blog\n6) Careers\n7) Developers\n0) GO BACK\n"
        )
        action = input("Type a number from 1-7 , or 0 to go back: "
                       )  # collect user input/option
        if action == "1":  # option 1
            new_account()
        elif action == "2":  # option 2
            print("We're here to help")
            input("[Press Enter to go back]")
        elif action == "3":  # option 3
            print(
                "In College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide"
            )
            input("[Press Enter to go back]")
        elif action == "4":  # option 4
            print(
                "In College Pressroom: Stay on top of the latest news, updates, and reports"
            )
            input("[Press Enter to go back]")
        elif action == "5":  # option 5
            print("Under construction...")
            input("[Press Enter to go back]")
        elif action == "6":  # option 6
            print("Under construction...")
            input("[Press Enter to go back]")
        elif action == "7":  # option 7
            print("Under construction...")
            input("[Press Enter to go back]")
        elif action == "0":  # option 0 : go back
            usefulLinks()
        else:
            print("Invalid entry!")  # otherwise invalid entry and loop back


def usefulLinks():
    # code goes here...
    while True:
        # link list
        print(
            "\nSelect any of the following links:\n1) General\n2) Browse InCollege\n3) Business Solutions\n4) Directories\n0) GO BACK\n"
        )
        action = input("Type a number from 1-4 , or 0 to go back: "
                       )  # collect user input/option
        if action == "1":  # option 1
            general()
        if action == "2":  # option 2
            print("Under construction...")
            input("[Press Enter to go back]")
        if action == "3":  # option 3
            print("Under construction...")
            input("[Press Enter to go back]")
        if action == "4":  # option 4
            print("Under construction...")
            input("[Press Enter to go back]")
        elif action == "0":  # option 0 : go back
            main_menu()
        else:
            print("Invalid entry!")  # otherwise invalid entry and loop back


def importantLinks(tempStudent):
    #code goes here...
    while True:
        print(
            "\nSelect any of the following links:\n1) Copyright Notice\n2) About\n3) Accessibility\n4) User Agreement\n5) Privacy Policy\n6) Cookie Policy\n7) Copyright Policy\n8) Brand Policy\n9) Languages\n0) GO BACK\n"
        )
        action = input("Type a number from 1-9 , or 0 to go back: "
                       )  # collect user input/option
        if action == "1":
            print(
                "COPYRIGHT NOTICE\n-----------------------------\nInCollege respects the rights of copyright holders.\nNo image or information display on this site may be reproduced, transmitted or copied (other than for the purposes of fair dealing, as defined in the Copyright Act 1968) without the express written permission of InCollege. Contravention is an infringement of the Copyright Act and its amendments and may be subject to legal action."
            )
            input("\n[Press Enter to go back]")
        if action == "2":
            print(
                "ABOUT\n-----------------------------\nWelcome to InCollege, the #1 tool for connecting with students and industry professionals. The program was created by a group of students at the University of South Florida with hopes to connect students to one another and provide a platform for employers to reach out."
            )
            input("\n[Press Enter to go back]")
        if action == "3":
            print(
                "ACCESSIBILITY\n-----------------------------\nThe current iteration of this program is only accessible to consumers in the NA and EU regions"
            )
            input("\n[Press Enter to go back]")
        if action == "4":
            print(
                "USER AGREEMENT\n-----------------------------\nWelcome, and thanks for using InCollege. When you use our product and services, you're agreeing to our terms of services."
            )
            input("\n[Press Enter to go back]")
        if action == "5":
            print(
                "PRIVACY POLICY\n-----------------------------\nInCollege doesn't make money from ads. So we don't collect data in order to advertise to you. the tracking we do at Medium is to make our product work as well as possible. In order to give you the best possible experience, we collect information from your interactions with our network.\n"
            )
            if tempStudent.username == '':
                print("You must Login to access Guest Controls")
                input("[Press Enter to go back]")
            else:
                guestControls(tempStudent)
        if action == "6":
            print(
                "COOKIE POLICY\n-----------------------------\nAt InCollege, we believe in being clear and open about how we use your information. In the spirit of tranparency, this policy provides detailed information about how and when we use cookies"
            )
            input("\n[Press Enter to go back]")
        if action == "7":
            print(
                "COPYRIGHT POLICY\n-----------------------------\nTo obtain permission to reproduce copyrighted works outside of InCollege and/or to use such works in ways that are not covered by our license or other prior agreements, employees should request permissions online at www.copyright.com or contact the Rights and Licensing Department of the copyright holder. Questions on specific procedures should be directed to the our legal team, who serves as our copyright officer."
            )
            input("\n[Press Enter to go back]")
        if action == "8":
            print(
                "BRAND POLICY\n-----------------------------\nThe InCollege brand should not be represented in a way that in not in line with the standards that demonstrate what the company is, what it does, and what it stands for."
            )
            input("\n[Press Enter to go back]")
        if action == "9":
            print("LANGUAGES\n-----------------------------\n")
            if tempStudent.username == '':
                print("Language: ENGLISH\nYou must Login to change Language")
                input("[Press Enter to go back]")
            else:
                languages(tempStudent)
        elif action == "0":  # option 0 : go back
            if tempStudent.username == '':
                main_menu()
            else:
                menuOptions(tempStudent)
        else:
            print("Invalid entry!")  # otherwise invalid entry and loop back


def login():
    # code goes here...
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    print("LOG IN\n---------------")
    while True:
        # user login input
        curUser = input("\nEnter user name: ")
        curPass = input("Enter password: ")

        c.execute("SELECT * from students WHERE username = ? AND password = ?", (curUser, curPass))
        inDatabase = c.fetchone()
        if not inDatabase:
            print("\nIncorrect username/password, please try again")  # if no matches found in the entire file print error
        else:
            print("\nYou have successfully logged in!")
            # creates a temporary student object that the program uses to display information
            tempStudent = Student(inDatabase[0], inDatabase[1], inDatabase[2], inDatabase[3], inDatabase[4], inDatabase[5], inDatabase[6], inDatabase[7], inDatabase[8], inDatabase[9], inDatabase[10], inDatabase[11])
            conn.close() # close connection


            if not profileExists(curUser):
                showNotification("Don't forget to create a profile")

            if not recentlyApplied(curUser):
                showNotification("Remember - you are going to want to have a job when you graduate. Make sure that you start to apply for jobs today!")

            if hasPendingMessages(curUser):
                showNotification("You have messages waiting for you")

            newAdmissions = checkNewAdmissions(curUser)
            for newusername, firstname, lastname in newAdmissions:
                showNotification("{} {} has joined InCollege".format(firstname, lastname))
                deleteNewAdmissionNotification(curUser, newusername)


            menuOptions(tempStudent)  # after successful login redirect to the menu options


def new_account():
    # code goes here...
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    c.execute("SELECT * FROM students")
    accounts = c.fetchall() # collects every row
    numOfAccounts = len(accounts)  # gets number of accounts

    if numOfAccounts == 10:  # if there is 10 accounts then no other accounts can be created
        input(
            "All permitted accounts have been created, please come back later. Press Enter to return to Main menu. \n"
        )
        main_menu()
    else:  # else an account can be created
        print("SIGN UP\n---------------")

        while True: # validating membership
            membership = input("\nThere are two tiers available: STANDARD and PLUS. PLUS members pay $10/mo but have access to additional features and benefits within the program. Would you like to sign up to be a STANDARD member or a PLUS member? (s/p): ")
            if membership != "s" and membership != "p":
                print("\nInvalid input. Please enter 's' for a STANDARD membership or 'p' for a PLUS membership")
            else:
                break

        while True:  # validating username
            user = input("\nEnter username: ")  # gets username input
            alreadyExists = False
            for account in accounts:  # checks every account in the database
                if account[0] == user:  # check for exsiting user
                    alreadyExists = True

            if alreadyExists == True:  # if username alredy exists print error message so loop back
                print("\nUsername is already taken")
            else:  # else the user name is valid so break
                break

        while True:  # validating password
            password = input("Enter password: ")  # gets password input
            if len(password) < 8 or len(
                    password
            ) > 12:  # if password length is invalid, print error message, and loop back
                print("Password must be 8 to 12 characters long")
            elif re.search(
                    r'[!@#$%^&*]', password
            ) is None:  # if no special character exists, print error message, and loop back
                print("Passowrd must contain at least one special character")
            elif re.search(
                    r'\d', password
            ) is None:  # if no digit exists, print error message, and loop back
                print("Password must contain at least one digit")
            elif re.search(
                    '[A-Z]', password
            ) is None:  # if no capital letter exists, print error message, and loop back
                print("Password must contain at least one capital letter")
            elif bool(
                    re.search(r'\s', password)
            ):  # if there is a space character, print error message, and loop back
                print("Password cannot contain spaces")
            else:  # else password is valid so break
                break

        while True:  # validating first name
            fname = input("Enter first name: ")  # get first name input
            if not fname.isalpha():  # if first name doesn't contain valid characters, print error message, and loop back
                print("First name must contain valid alphabetic characters only")
            elif fname == '':
                print("First name cannot be empty")
            else:  # first name is valid so break
                break

        while True:  # validating last name
            lname = input("Enter last name: ")  # get last name input
            if not lname.isalpha():  # if last name doesn't contain valid characters, print error message, and loop back
                print("Last name must contain valid alphabetic characters only")
            elif lname == '':
                print("Last name cannot be empty")
            else:  # last name is valid so break
                break

        c.execute("INSERT INTO students VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user, password, fname, lname, 'eng', 'ON', 'ON', 'ON', '', '', '', membership))

        conn.commit() # commit to database
        conn.close()  # close database
        markNewStudentNotificationEntry(user)
        storeUsers()

        print("\nThank you for creating a new account. ")# print confirmation message
        input("[Press Enter to go back]")
        main_menu()  # return back to welcome screen


def find_friends():
    # code goes here...
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    while True:
        nameQuery = input("\nEnter friend's full name (Or type 0 to go back): ")
        if (nameQuery == "0"):
            main_menu()

        fullName = nameQuery.split(" ")
        containsSpaces = bool(re.search(r"\s", nameQuery))
        if not containsSpaces:
            print("Invalid full name. There must be at least one space")
            continue
        firstName = fullName[0]
        lastName = fullName[1]
        break;


    c.execute("SELECT * from students WHERE firstname = ? AND lastname = ?", (firstName, lastName))
    inDatabase = c.fetchone()
    if not inDatabase:
        print("\nThey are not yet a part of the InCollege system yet")
        input("\n[Press Enter to go back]")
        conn.close() # close connection
        main_menu()  # after successful login redirect to the main menu
    else:
        print("\nThey are a part of the InCollege system")
        input("\n[Press Enter to go back]")
        conn.close() # close connection
        alt_main()  # after successful login redirect to the main menu


def alt_main():
    print(
        "\nHey! It looks like one of your friends is already in our system. InCollege is the #1 tool for connecting with students and industry professionals."
    )  # alternate message
    while True:
        val = input(
            "Please pick an option from the following menu (1-3):\n\n" +
            "1) Login\n2) Create a new account\n3) Exit the program\n")
        if val == '1':
            login()  # calls the login function
        elif val == '2':
            new_account()  # calls the new account function
        elif val == '3':
            exit()
        else:
            print("\nInvalid input.")


def main_menu():
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    res = c.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='{}';""".format('students')).fetchall()
    if res == []:
        c.execute("""CREATE TABLE students (
                     username text,
                     password text,
                     firstname text,
                     lastname text,
                     language text,
                     email text,
                     sms text,
                     ads text,
                     friends text,
                     pending text,
                     pendingMsgs text,
                     membership text
             )""")

    res = c.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='{}';""".format('jobs')).fetchall()
    if res == []:
        c.execute("""CREATE TABLE jobs (
                     username text,
                     title text,
                     description text,
                     employer text,
                     location text,
                     salary text
             )""")

    res = c.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='{}';""".format('profile')).fetchall()
    if res == []:
        c.execute("""CREATE TABLE profile (
                     username text,
                     title text,
                     major text,
                     university text,
                     about text
             )""")

    res = c.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='{}';""".format('exp')).fetchall()
    if res == []:
        c.execute("""CREATE TABLE exp (
                     username text,
                     job_title text,
                     job_employer text,
                     date_started text,
                     date_ended text,
                     job_location text,
                     job_desc text
             )""")

    res = c.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='{}';""".format('edu')).fetchall()
    if res == []:
        c.execute("""CREATE TABLE edu (
                     username text,
                     school_name text,
                     degree text,
                     years_attended text
             )""")

    res = c.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='{}';""".format('jobstatus')).fetchall()
    if res == []:
        c.execute("""CREATE TABLE jobstatus (
                 username text,
                 title text,
                 applied text,
                 saved text,
                 graduationDate,
                 prefStartDate,
                 appDescription,
                 appliedDate text
          )""")
    else:
        checkCursor = conn.execute('select * from jobstatus')
        names = list(map(lambda x: x[0], checkCursor.description))
        if "appliedDate" not in names:
            checkCursor.execute('ALTER TABLE jobstatus ADD COLUMN "appliedDate" text')
        checkCursor.close()

    res = c.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='{}';""".format('messages')).fetchall()
    if res == []:
        c.execute("""CREATE TABLE messages (
                 username text,
                 recepient text,
                 message text
          )""")

    res = c.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='{}';""".format('new_student_notifs')).fetchall()
    if res == []:
        c.execute("""CREATE TABLE new_student_notifs (
                      username text,
                      notif_username text
               )""")

    conn.commit()
    conn.close()

    # loads users from the API
    loadUsers()
    # loads jobs from the API
    loadJobs()

    # store jobs into the API
    storeJobs()
    # store users into the API
    storeUsers()
    # store profiles into the API
    storeProfiles()
    # store applied jobs into the API
    storeAppliedJobs()
    # store saved jobs into the API
    storeSavedJobs()

    print(
        "\nWelcome to InCollege, the #1 tool for connecting with students and industry professionals. Our latest success story is about a young man named Robert, who had been struggling to find a job after graduating. He came accross the InCollege tool, and was able to find a job within a couple days. He was able to connect with other students in his profession as well as professionals. More information about Robert is available by watching the video in the menu.\n"
    )  # welcome message / home
    while True:
        val = input(
            "Please pick an option from the following menu (1-7):\n\n" +
            "1) Login\n2) Create a new account\n3) Watch the most recent success story\n4) Find friends\n5) Useful Links\n6) InCollege Important Links\n7) Exit the program\n"
        )
        if val == '1':
            login()  # calls the login function
        elif val == '2':
            new_account()  # calls the new account function
        elif val == '3':
            print("\nVideo is now playing.")  # simulates playing video
            input("Press Enter to go back.\n")
        elif val == '4':
            find_friends()  # calls the find friend function
        elif val == '5':
            usefulLinks()  # calls the useful links function
        elif val == '6':
            tempStudent = Student('', '', '', '', '', '', '', '', '', '', '', '')
            importantLinks(tempStudent)  # calls the important links function
        elif val == '7':
            exit()
        else:
            print("\nInvalid input.")


main_menu()  # Start of the program
