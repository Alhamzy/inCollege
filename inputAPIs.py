import sqlite3 # importing sqlite for database
import itertools

def loadUsers():
    # code goes here...
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    with open('./input_apis/studentAccounts.txt') as f:
        for line1,line2,line3 in itertools.zip_longest(*[f]*3):

            c.execute("SELECT * FROM students")
            accounts = c.fetchall() # collects every row
            numOfAccounts = len(accounts)  # gets number of accounts

            if numOfAccounts == 10:  # if there is 10 accounts then no other accounts can be created
                break

            info = line1.split(",")
            password = line2.strip()

            alreadyExists = False
            for account in accounts:  # checks every account in the database
                if account[0] == info[0]:  # check for exsiting user
                    alreadyExists = True

            if alreadyExists == True:  # if username alredy exists, loop back
                continue

            c.execute("INSERT INTO students VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (info[0], password, info[1], info[2], 'eng', 'ON', 'ON', 'ON', '', '', '', 's'))

            conn.commit() # commit to database
            
    conn.close()  # close database
    f.close() # close file

def loadJobs():
    # code goes here...
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    with open('./input_apis/newJobs.txt') as f:
        for line1,line2,line3,line4,line5,line6,line7 in itertools.zip_longest(*[f]*7):

            c.execute("SELECT * FROM jobs")
            jobs = c.fetchall() # collects every row
            numOfJobs = len(jobs)  # gets number of jobs

            if numOfJobs == 10:  # if there is 10 jobs then no other jobs can be created
                break
            
            username = line1.rstrip()
            title = line2.rstrip()
            description = line3.rstrip()
            employer = line4.rstrip()
            location = line5.rstrip()
            salary = line6.rstrip()

            alreadyExists = False
            for job in jobs:  # checks every account in the database
                if job[0] == username and job[1] == title:  # check for exsiting jobs
                    alreadyExists = True

            if alreadyExists == True:  # if job alredy exists, loop back
                continue

            c.execute("INSERT INTO jobs VALUES(?, ?, ?, ?, ?, ?)", (username, title, description, employer, location, salary))

            conn.commit() # commit to database
            
    conn.close()  # close database
    f.close() # close file

def loadTraining():
    # code goes here...
    while True:
        # skill list
        print("\nSelect any skills you want to learn:")
        print("1) Agile Course")
        print("2) Learn to Code Securely")
        count = 2
        for line in open("./input_apis/newTraining.txt", 'r').readlines():
            count += 1
            print("{}) {}".format(count, line.strip()))
        print("0) GO BACK")

        addSkill = input("Type a number from 1-{} , or 0 to go back: ".format(count))  # collect user input/option

        if addSkill >= "1" and addSkill <= "{}".format(count):  # option 1 - ? are under construction
            print("Under construction...")
            input("[Press Enter to go back]")
        elif addSkill == "0":  # option 0 : go back
            break  # returns back to menu options
        else:
            print("Invalid entry!")  # otherwise invalid entry and loop back