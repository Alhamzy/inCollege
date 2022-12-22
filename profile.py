import sqlite3
from outputAPIs import storeProfiles # import functions from the output API module
from sys import exc_info # importing sqlite for database

# username text 0
# title text 1
# major text 2
# university text 3
# about text 4

# job_title text 1
# job_employer text 2
# date_started text 3
# date_ended text 4
# job_location text 5
# job_description text 6

# school_name text 1
# degree text 2
# years_attended text 3

def displayProfile(user, firstname, lastname):
    # code goes here...
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    c.execute("SELECT * FROM profile WHERE username = ?", (user, ))
    userProfile = c.fetchone()

    # heading
    print("\n" + firstname.upper() + " " + lastname.upper() + "'S PROFILE")
    print("------------------------------\n")

    # Title
    if (userProfile[1] == ''):
        title = "N\A"
    else:
        title = userProfile[1]
    print("1. Title: " + title)

    # Major
    if (userProfile[2] == ''):
        major = "N\A"
    else:
        major = userProfile[2]
    print("2. Major: " + major)

    # University
    if (userProfile[3] == ''):
        uni = "N\A"
    else:
        uni = userProfile[3]
    print("3. University: " + uni)

    # About
    if (userProfile[4] == ''):
        about = "N\A"
    else:
        about = userProfile[4]
    print("4. About: " + about)

    # Experience
    c.execute("SELECT job_title FROM exp WHERE username = ?", (user, ))
    hasExperience = c.fetchall()
    if not hasExperience:
        exp = "No job experience to show"
    else:
        exp = '| '
        for experience in hasExperience:
            exp = exp + experience[0] + " | "
    print("5. Experience: " + exp)

    # Education
    c.execute("SELECT school_name FROM edu WHERE username = ?", (user, ))
    hasEducation = c.fetchall()
    if not hasEducation:
        edu = "No school education to show"
    else:
        edu = '| '
        for education in hasEducation:
            edu = edu + education[0] + " | "
    print("6. Education: " + edu)

    conn.close()


def inputCheck(query):
    while True:
        user_input = input(query)
        if user_input == "" or user_input.isspace():
            continue
        else:
            return user_input


def userprofile(tempStudent):
    # code goes here...
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    c.execute("SELECT * FROM profile WHERE username = ?", (tempStudent.username, ))
    createdProfile = c.fetchone()
    if not createdProfile:
        print("\nYOU HAVE NOT CREATED YOUR PROFILE\nTo create a new profile [Enter 1], To go back to main menu [Enter 0].")
        while True:
            action = input("Enter option: ")
            if action == '0':
                conn.close()
                break
            elif action == '1':
                conn.close()
                createProfile(tempStudent)
                break
            else:
                print("Invalid entry!\n")
                continue
    else:
        # Options
        while True:
            displayProfile(tempStudent.username, tempStudent.firstname, tempStudent.lastname)
            print("\nTo view your Experience details [Enter 1]\nTo view your Education details [Enter 2]\nTo update your profile [Enter 3]\nTo go back [Enter 0]: ")

            action = input("Enter Option: ")
            if action == "0":
                conn.close()
                break
            elif action == "1":
                c.execute("SELECT * FROM exp WHERE username = ?", (tempStudent.username, ))
                hasExperience = c.fetchall()
                if not hasExperience:
                    print("\nNothing to see here...")
                    input("\n[Press Enter to go back]")
                else:
                    print("\n Your Jobs:")
                    i = 1
                    for experience in hasExperience:
                        print(str(i) + ". " + "[Title: " + experience[1] + "]" + "\nEmployer: " + experience[2] + "\nDate Started: " + experience[3] + "\nDate Ended: " + experience[4] + "\nLocation: " + experience[5] + "\nDescription: " + experience[6] + "\n")                        
                        i+=1
                    input("[Press Enter to go back]")
                continue

            elif action == "2":
                c.execute("SELECT * FROM edu WHERE username = ?", (tempStudent.username, ))
                hasEducation = c.fetchall()
                if not hasEducation:
                    print("\nNothing to see here...")
                    input("\n[Press Enter to go back]")
                else:
                    print("\n Your Schools:")
                    i = 1
                    for education in hasEducation:
                        print(str(i) + ". " + "[School: " + education[1] + "]" + "\nDegree: " + education[2] + "\nYears: " + education[3] + " year(s)")
                        i+=1
                    input("\n[Press Enter to go back]")
                continue

            elif action == "3":
                updateProfile(tempStudent)
                break
            else:
                print("Invalid entry!")  # otherwise invalid entry and loop back
                continue


def createProfile(tempStudent):
    # code goes here...
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    c.execute("INSERT INTO profile VALUES(?, ?, ?, ?, ?)", (tempStudent.username, '', '', '', ''))
    conn.commit()
    conn.close()

    # output api
    storeProfiles()
    print("Profile created!")
    


def updateProfile(tempStudent):
    while True:
        # code goes here...
        # connecting to sqlite database
        conn = sqlite3.connect('incollege.db')
        c = conn.cursor()

        print("\nSelect which information you would like to change by entering the respective number or enter 0 to go back.")
        c.execute("SELECT * FROM profile WHERE username = ?", (tempStudent.username, ))
        userProfile = c.fetchone()

        action = input("Enter option: ")
        if action == '1': ## UPDATES TITLE

            if (userProfile[1] == ''):
                title = "N\A"
            else:
                title = userProfile[1]

            print("\nCurrent Title: " + title)
            change = input("Would you like to change it? (y/n) ")
            
            if change == 'y':
                new_title = input("New Title: ")
                c.execute("UPDATE profile SET title = ? WHERE username = ?", (new_title, tempStudent.username))
                conn.commit()
                storeProfiles()
                displayProfile(tempStudent.username, tempStudent.firstname, tempStudent.lastname)
                continue
            else:
                print("Cancelling...")
                break

        elif action == '2': ## UPDATE MAJOR

            if (userProfile[2] == ''):
                major = "N\A"
            else:
                major = userProfile[2]

            print("\nCurren Major: " + major)
            change = input("Would you like to change it? (y/n) ")
            
            if change == 'y':
                new_major = input("New Major: ")
                new_major = new_major.title()
                c.execute("UPDATE profile SET major = ? WHERE username = ?", (new_major, tempStudent.username))
                conn.commit()
                storeProfiles()
                displayProfile(tempStudent.username, tempStudent.firstname, tempStudent.lastname)
                continue
            else:
                print("Cancelling...")
                break
            
        elif action == '3': # UPDATE UNIVERSITY
            
            if (userProfile[3] == ''):
                uni = "N\A"
            else:
                uni = userProfile[3]

            print("\nCurrent University: " + uni)
            change = input("Would you like to chnage it? (y/n) ")

            if change == 'y':
                new_uni = input("New University: ")
                new_uni = new_uni.title()
                c.execute("UPDATE profile SET university = ? WHERE username = ?", (new_uni, tempStudent.username))
                conn.commit()
                storeProfiles()
                displayProfile(tempStudent.username, tempStudent.firstname, tempStudent.lastname)
                continue
            else:
                print("Cancelling...")
                break

        elif action == '4': # UPDATE ABOUT

            if (userProfile[4] == ''):
                about = "N\A"
            else:
                about = userProfile[4]

            print("\nCurrent About: " + about)
            change = input("Would you like to chnage it? (y/n) : ")

            if change == 'y':
                new_about = input("New About: ")
                c.execute("UPDATE profile SET about = ? WHERE username = ?", (new_about, tempStudent.username))
                conn.commit()
                storeProfiles()
                displayProfile(tempStudent.username, tempStudent.firstname, tempStudent.lastname)
                continue
            else:
                print("Cancelling...")
                break

        elif action == '5':
            while True:
                c.execute("SELECT job_title FROM exp WHERE username = ?", (tempStudent.username, ))
                hasExperience = c.fetchall()
                if not hasExperience:
                    exp = "No job experience to show"
                else:
                    exp = '| '
                    for experience in hasExperience:
                        exp = exp + experience[0] + " | "
                print("\nCurrent Experience: " + exp)

                change = input("Would you like to add or remove a job?\nTo add [Enter a], To remove [Enter r], To go back [Enter 0] :  ")
                if change == 'a':
                    
                    if len(hasExperience) == 3:
                        print("\nYOU CAN ONLY HAVE A MAXIMUM OF 3 JOB EXPERIENCES!")
                        input("[Press Enter to go back]")
                    else:
                        print("\nADD A JOB\n")
                        addTitle = inputCheck("Enter title: ")
                        addTitle = addTitle.title()
                        addEmployer = inputCheck("Enter employer: ")
                        addDateStarted = inputCheck("Enter date started: ")
                        addDateEnded = inputCheck("Enter data ended: ")
                        addLocation = inputCheck("Enter job location: ")
                        addDescription = inputCheck("Enter description: ")

                        c.execute("INSERT INTO exp VALUES(?, ?, ?, ?, ?, ?, ?)", (tempStudent.username, addTitle, addEmployer, addDateStarted, addDateEnded, addLocation, addDescription))
                        conn.commit()
                        storeProfiles()
                    continue

                elif change == 'r':

                    if not hasExperience:
                        print("\nYOU HAVE NO JOBS TO REMOVE!")
                        input("[Press Enter to go back]")
                    else:
                        deleteJob(tempStudent.username)
                    continue

                elif change == '0':

                    conn.close()
                    break

                else:
                    
                    print("\nInvalid Entry!\n")
                    continue
            displayProfile(tempStudent.username, tempStudent.firstname, tempStudent.lastname)
            continue
            
        elif action == '6':
            while True:
                c.execute("SELECT school_name FROM edu WHERE username = ?", (tempStudent.username, ))
                hasEducation = c.fetchall()
                if not hasEducation:
                    edu = "No school education to show"
                else:
                    edu = '| '
                    for education in hasEducation:
                        edu = edu + education[0] + " | "
                print("\nCurrent Education: " + edu)

                change = input("Would you like to add or remove a school?\nTo add [Enter a], To remove [Enter r], To go back [Enter 0] :  ")
                if change == 'a':
                    
                    print("\nADD EDUCATION\n")
                    addSchoolName = inputCheck("Enter school name: ")
                    addSchoolName = addSchoolName.title()
                    addDegree = inputCheck("Enter degree: ")
                    addYearsAttended = inputCheck("Enter years attended: ")

                    c.execute("INSERT INTO edu VALUES(?, ?, ?, ?)", (tempStudent.username, addSchoolName, addDegree, addYearsAttended))
                    conn.commit()
                    storeProfiles()

                    continue

                elif change == 'r':

                    if not hasEducation:
                        print("\nYOU HAVE NO EDUCATION TO REMOVE!")
                        input("[Press Enter to go back]")
                    else:
                        deleteEducation(tempStudent.username)
                    continue

                elif change == '0':

                    conn.close()
                    break

                else:                    
                    print("\nInvalid Entry!\n")
                    continue

            displayProfile(tempStudent.username, tempStudent.firstname, tempStudent.lastname)
            continue


        elif action == '0':
            break
        else:
            print("Invalid entry!\n")
            continue


def deleteJob(user):
    # code goes here...
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    c.execute("SELECT * FROM exp WHERE username = ?", (user, ))
    hasExperience = c.fetchall()
    i = 0
    for experience in hasExperience:
        i+=1
        print(str(i) + ". " + experience[1])

    while True:
        action = input("Which job would you like to remove? [Select number from above] : ")
        index = int(action)
        if index >= 1 or index <= i:
            selected_title = hasExperience[index-1][1]
            selected_employer = hasExperience[index-1][2]
            c.execute("DELETE from exp WHERE username = ? AND job_title = ? AND job_employer = ?", (user, selected_title, selected_employer))
            conn.commit()
            conn.close()

            print("\n" + selected_title + " was deleted from your experience list")
            break
        else:
            print("\nInvalid entry!\n")
            continue

    

def deleteEducation(user):
    # code goes here...
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    c.execute("SELECT * FROM edu WHERE username = ?", (user, ))
    hasEducation = c.fetchall()
    i = 0
    for education in hasEducation:
        i+=1
        print(str(i) + ". " + education[1])

    while True:
        action = input("Which school would you like to remove? [Select number from above] : ")
        index = int(action)
        if index >= 1 or index <= i:
            selected_school_name = hasEducation[index-1][1]
            c.execute("DELETE from edu WHERE username = ? AND school_name = ?", (user, selected_school_name))
            conn.commit()
            conn.close()

            print("\n" + selected_school_name + " was deleted from your education list")
            break
        else:
            print("\nInvalid entry!\n")
            continue
