import sqlite3 # importing sqlite for database
from outputAPIs import * # import functions from the output API module
import datetime


# Function to show notifications
def showNotification(message: str) -> None:
    print(
        "\n!!! NOTIFICATION !!! {}".format(message)
    )


# function to get number of applied jobs
def getAppliedJobCount(studentUserName: str) -> int:
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()
    c.execute("SELECT title FROM jobstatus WHERE username = ? and applied = ?", (studentUserName, "ON", ))
    appledJobs = c.fetchall()
    c.close()
    conn.close()
    return len(appledJobs)


# function to get the titles of new jobs. New means the job is not in the users database entries.
def getNewJobs(studentUserName: str) -> list:
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    # If the jobs posted by same user to be considered for notification, use the following line
    c.execute("SELECT title FROM jobs")

    # If the jobs posted by same user not to be considered for notification, use the following line
    # c.execute("SELECT title FROM jobs WHERE username != ?", (studentUserName, ))

    allJobs = set([j[0] for j in c.fetchall() if j])
    c.execute("SELECT title FROM jobstatus WHERE username = ?", (studentUserName, ))
    jobsInDb = set([j[0] for j in c.fetchall() if j])
    for job in jobsInDb:
        if job in allJobs:
            allJobs.remove(job)
    c.close()
    conn.close()
    return allJobs


# function to get the titles of new jobs that the user applied but deleted
def getDeletedJobs(studentUserName: str) -> list:
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    c.execute("SELECT title FROM jobs")

    deletedJobs = set()

    allJobs = set([j[0] for j in c.fetchall() if j])
    c.execute("SELECT title FROM jobstatus WHERE username = ? and applied = ?", (studentUserName, "ON"))
    appliedJobs = set([j[0] for j in c.fetchall() if j])
    for job in appliedJobs:
        if job not in allJobs:
            deletedJobs.add(job)
    c.close()
    conn.close()
    storeAppliedJobs()
    storeSavedJobs()
    return deletedJobs


def jobs(tempStudent):

    # code goes here...
    jobCount = getAppliedJobCount(tempStudent.username)
    if jobCount:
        showNotification("You have currently applied for {} jobs".format(jobCount))

    unappliedJobs = getNewJobs(tempStudent.username)
    for job in unappliedJobs:
        showNotification("A new job {} has been posted".format(job))

    deletedJobs = getDeletedJobs(tempStudent.username)
    for job in deletedJobs:
        showNotification("A job that you applied for has been deleted: {}".format(job))

    while True:
        print("\nChoose an option:\n1) Post a job\n2) View jobs\n3) View jobs posted by you\n0) G0 BACK\n")
        action = input("Type 1, or 0 to go back: ")
        if action == "0":
            break
        elif action == "1":
            postJobs(tempStudent)
        elif action == "2":
            viewJobs(tempStudent)
        elif action == "3":
            viewPostedJobs(tempStudent)
        else:
            print("Invalid entry!")

def postJobs(tempStudent):
    # code goes here...
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    c.execute("SELECT * FROM jobs")
    jobs = c.fetchall() # collects every row
    numOfJobs = len(jobs)  # gets number of jobs

    if numOfJobs >= 10:  # if there is 10 jobs then no other jobs can be created
        input(
            "All permitted jobs have been created, please come back later. Press Enter to go back.\n"
        )
    else:  # else a job can be created
        print("Fill the following fields: ")
        #a title, a description, the employer, a location, and a salary
        while True:
            title = input("Title: ")
            if not title:
                print("Cannot be empty\n")
            else:
                break
        while True:
            desc = input("Description: ")
            if not desc:
                print("Cannot be empty\n")
            else:
                break
        while True:
            employer = input("Employer: ")
            if not employer:
                print("Cannot be empty\n")
            else:
                break
        while True:
            location = input("Location: ")
            if not location:
                print("Cannot be empty\n")
            else:
                break
        while True:
            salary = input("Salary: ")
            if not salary:
                print("Cannot be empty\n")
            elif not salary.isnumeric():
                print("Must be a numeric value\n")
            else:
                break

        # insert entry into job table
        c.execute("INSERT INTO jobs VALUES(?, ?, ?, ?, ?, ?)", (tempStudent.username, title, desc, employer, location, salary))
        conn.commit() # commit to database
        conn.close()  # close database
        storeJobs()

        print("\nThank you " + tempStudent.firstname +" for creating a new job. ")
        input("[Press Enter to return]")  # print confirmation message



def viewJobs(tempStudent):
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    while True:

        #look up user jobs (student created)
        c.execute("SELECT * FROM jobs WHERE username = ?",(tempStudent.username,))
        userJobs = c.fetchall()
        #look up all jobs in db
        c.execute("SELECT * FROM jobs")
        allJobs = c.fetchall()

        if allJobs:
            jobList = []
            #List all jobs
            print("\nListing all jobs:")
            i=0
            for job in allJobs:
                # save all jobs in a separate list
                jobList.append(job)
                i += 1
                print(i,") ", job[1])


            filterMenu = i + 1

            #user inputs choice from all jobs

            choice = int(input("\nEnter corresponding number of job to view it: (To filter list enter {0} or 0 to go back)\n".format(filterMenu))) # if n jobs are listed, then entering "n + 1" takes you to the filter menu
            if choice == filterMenu: # filter jobs

                while True:
                    print( "\nEnter one of the choices below: (or 0 to go back)", # show filter options
                            "\n1) Show only jobs you applied to",
                            "\n2) Show only jobs you did not apply to",
                            "\n3) Show only saved jobs")
                    filterOp = input("\n")
                    if filterOp == "1": # list all jobs in db where that user applied to, if any
                        while True:
                            c.execute("SELECT * FROM jobstatus WHERE username = ? and applied = ?",(tempStudent.username,'ON'))
                            appliedJobs = c.fetchall()

                            if appliedJobs:
                                i=1
                                for job in appliedJobs: # print all job titles
                                    print(i, ") ", job[1])

                                # give student to apply to the job they choose
                                choice = int(input("\nEnter a corresponding number of job to view its details: (or 0 to go back)\n"))
                                if choice >= 1 and choice >=i: #view job and give permission to save
                                    choiceJob = appliedJobs[choice-1]

                                     # print job details job
                                    print("\nJob details\n"
                                          "\nTitle:", choiceJob[1],
                                          "\nDescription: ",choiceJob[2],
                                          "\nEmployer: ",choiceJob[3],
                                          "\nLocation: ",choiceJob[4],
                                          "\nSalary:",choiceJob[5])

                                    # show save status
                                    c.execute("SELECT * FROM jobstatus WHERE username = ? and title = ? and saved = ?",(tempStudent.username,choiceJob[1],'ON'))
                                    currentJobIsSaved = c.fetchall()
                                    if currentJobIsSaved:
                                        saved = 'ON'
                                        print("Saved: Yes")
                                    else:
                                        saved = 'OFF'
                                        print("Saved: No")

                                    # show application status
                                    c.execute("SELECT * FROM jobstatus WHERE username = ? and title = ? and applied = ?",(tempStudent.username,choiceJob[1],'ON'))
                                    appliedToJob = c.fetchall()
                                    if appliedToJob:
                                        alreadyApplied = 'ON'
                                        print("Applied: Yes")

                                    else:
                                        alreadyApplied = 'OFF'
                                        print("Applied: No")

                                    jobOps = input("\nEnter 1 to save/unsave job or 2 to apply for this job (or 0 to go back)\n")
                                    if jobOps == "1": # save toggle
                                         if saved == 'ON': # if the job is saved already unsave
                                             if jobInDB == 'ON':# if in db just update record
                                                 c.execute("UPDATE jobstatus SET saved = ? WHERE username = ? and title = ?",('OFF',tempStudent.username,choiceJob[1],))
                                                 conn.commit()
                                             else: # insert as new job modification in jobstatus table
                                                 c.execute("INSERT INTO jobstatus VALUES(?,?,?,?,?,?,?,?)",(tempStudent.username,choiceJob[1],'OFF','ON','','','','',))
                                                 conn.commit()

                                             if jobInDB == 'OFF':
                                                 c.execute("UPDATE jobstatus SET saved = ? WHERE username = ? and title = ?",('OFF',tempStudent.username,choiceJob[1],))
                                                 conn.commit()
                                             else:
                                                 c.execute("INSERT INTO jobstatus VALUES(?,?,?,?,?,?,?,?)",(tempStudent.username,choiceJob[1],'OFF','OFF','','','','',))
                                                 conn.commit()

                                         elif saved == 'OFF': # if not saved change to saved
                                             if jobInDB == 'ON':# if in db just update record
                                                 c.execute("UPDATE jobstatus SET saved = ? WHERE username = ? and title = ?",('ON',tempStudent.username,choiceJob[1],))
                                                 conn.commit()
                                             else: # insert as new job modification in jobstatus table
                                                 c.execute("INSERT INTO jobstatus VALUES(?,?,?,?,?,?,?,?)",(tempStudent.username,choiceJob[1],'OFF','ON','','','','',))
                                                 conn.commit()

                                             if jobInDB == 'OFF':
                                                 c.execute("UPDATE jobstatus SET saved = ? WHERE username = ? and title = ?",('ON',tempStudent.username,choiceJob[1],))
                                                 conn.commit()
                                             else:
                                                 c.execute("INSERT INTO jobstatus VALUES(?,?,?,?,?,?,?,?)",(tempStudent.username,choiceJob[1],'OFF','ON','','','','',))
                                                 conn.commit()

                                    elif jobOps =="0":
                                        break

                                    else:
                                        print("Invalid input..")
                                        break
                                else:
                                    print("Invalid input..")
                                    break

                            else:
                                print("No jobs have been applied to..")
                                continue


                    elif filterOp == "2": # list all jobs in db where that user did not apply to, if any
                        while True:
                            unAppliedJobs = []
                            for jobs in allJobs: # search all jobs and append unapplied jobs to list
                                c.execute("SELECT * FROM jobstatus WHERE username = ? and title = ? and applied = ?",(tempStudent.username,jobs[1],'ON',)) # filter by checking if each job is saved in jobstatus
                                appliedJobTitle = c.fetchone()
                                if appliedJobTitle:
                                    if job[1] == appliedJobTitle[1]: # if title in job db matches jobstatus
                                        continue
                                    else:
                                        unAppliedJobs.append(job) # if job is has not been applied to save in separate list


                            # print unappliedjobs
                            print("Listing jobs that have not been applied to:\n")
                            i=0
                            for job in unAppliedJobs:
                                i += 1
                                print(i,") ",job[1]) # print each title


                            # give student to apply to the job they choose
                            choice = int(input("\nEnter corresponding number of job to view its details: (or 0 to go back)\n"))
                            if choice >= 1 and choice <=i: #view job and give permission to save
                                 # print job details
                                choiceJob = unAppliedJobs[choice-1]
                                print(choiceJob[1])
                                print("Job details"
                                        "Title:", choiceJob[1],
                                        "Description: ",choiceJob[2],
                                        "Employer: ",choiceJob[3],
                                        "Location: ",choiceJob[4],
                                        "Salary:",choiceJob[5])
                                # show save status
                                c.execute("SELECT * FROM jobstatus WHERE username = ? and title = ? and saved = ?",(tempStudent.username,choiceJob[1],'ON',))
                                currentJobIsSaved = c.fetchall()
                                if currentJobIsSaved:
                                    saved = 'ON'
                                    print("Saved: Yes")
                                else:
                                    saved = 'OFF'
                                    print("Saved: No")

                                # show application status
                                c.execute("SELECT * FROM jobstatus WHERE username = ? and title = ? and applied = ?",(tempStudent.username,choiceJob[1],'ON',))
                                appliedToJob = c.fetchall()
                                if appliedToJob:
                                    alreadyApplied = 'ON'
                                    print("Applied: Yes")
                                else:
                                    alreadyApplied = 'OFF'
                                    print("Applied: No")

                                # give ability to save or apply
                                jobOps = input("\nEnter 1 to save/unsave job or 2 to apply for this job (or 0 to go back)\n")
                                if jobOps == "1": # save toggle
                                    if saved == 'ON': # if the job is saved already unsave
                                        if jobInDB == 'ON':# if in db just update record
                                            c.execute("UPDATE jobstatus SET saved = ? WHERE username = ? and title = ?",('OFF',tempStudent.username,choiceJob[1],))
                                            conn.commit()
                                        else: # insert as new job modification in jobstatus table
                                            c.execute("INSERT INTO jobstatus VALUES(?,?,?,?,?,?,?,?)",(tempStudent.username,choiceJob[1],'OFF','ON','','','','',))
                                            conn.commit()

                                        if jobInDB == 'OFF':
                                            c.execute("UPDATE jobstatus SET saved = ? WHERE username = ? and title = ?",('OFF',tempStudent.username,choiceJob[1],))
                                            conn.commit()
                                        else:
                                            c.execute("INSERT INTO jobstatus VALUES(?,?,?,?,?,?,?,?)",(tempStudent.username,choiceJob[1],'OFF','OFF','','','','',))
                                            conn.commit()

                                    elif saved == 'OFF': # if not saved change to saved
                                        if jobInDB == 'ON':# if in db just update record
                                            c.execute("UPDATE jobstatus SET saved = ? WHERE username = ? and title = ?",('ON',tempStudent.username,choiceJob[1],))
                                            conn.commit()
                                        else: # insert as new job modification in jobstatus table
                                            c.execute("INSERT INTO jobstatus VALUES(?,?,?,?,?,?,?,?)",(tempStudent.username,choiceJob[1],'OFF','ON','','','','',))
                                            conn.commit()

                                        if jobInDB == 'OFF':
                                            c.execute("UPDATE jobstatus SET saved = ? WHERE username = ? and title = ?",('ON',tempStudent.username,choiceJob[1],))
                                            conn.commit()
                                        else:
                                            c.execute("INSERT INTO jobstatus VALUES(?,?,?,?,?,?,?,?)",(tempStudent.username,choiceJob[1],'OFF','ON','','','','',))
                                            conn.commit()

                                elif jobOps =="2": # give permission to apply
                                    curDate = datetime.datetime.now()
                                    dateStr = "{}-{}-{}".format(curDate.year, "%02d" % curDate.month, "%02d" % curDate.day)
                                    if alreadyApplied == 'OFF':
                                        gradDate = ''
                                        while not gradDate:
                                            gradDate = input("\nEnter graduation date: ")
                                        prefStartDate = ''
                                        while not gradDate:
                                            prefStartDate = input("\nEnter preferred start date: ")
                                        appDescription = ''
                                        while not appDescription:
                                            appDescription = input("Explain why you think you are a good fit for this role: ")
                                        # insert into jobstatus db
                                        #check if job has been pushed to jobstatus table before, if so then update

                                        curDate = datetime.datetime.now()
                                        dateStr = "{}-{}-{}".format(curDate.year, "%02d" % curDate.month, "%02d" % curDate.day)

                                        if jobInDB == 'ON':
                                            c.execute("UPDATE jobstatus SET applied = ? and appliedDate = ? WHERE username = ? and title = ?",('ON', dateStr, tempStudent.username,choiceJob[1],))
                                            conn.commit
                                        else:
                                            c.execute("INSERT INTO jobstatus VALUES(?,?,?,?,?,?,?,?)",(tempStudent.username,choiceJob[1],'ON','OFF',gradDate,prefStartDate,appDescription, dateStr,)) # insert application details as a new record
                                            conn.commit()
                                            alreadyApplied = 'ON'
                                            break
                                    else: # already applied to job
                                        print("You already applied to this job..")
                                        break


                                elif jobOps =="0":
                                    break
                                else:
                                    print("Invalid input..")
                                    break

                            elif choice == "0":
                                print("Invalid input..")
                                break
                            else:
                                print("Invalid input..")
                                break


                    elif filterOp == "3": # filter for all saved jobs
                        while True:
                            c.execute("SELECT * FROM jobstatus WHERE username = ? and saved = ?",(tempStudent.username,'ON'))
                            savedJobs = c.fetchall() # fetch all the jobs saved by user

                            # print jobs
                            print("\nListing all saved jobs:")
                            if savedJobs: #if any saved jobs exists
                                i=1
                                for job in savedJobs:
                                    print(i,") ",job[1])
                                    i += 1

                                choice = int(input("\nEnter the corresponding number of the job to view its details: (or 0 to go back)\n"))
                                if choice >= 1 and choice <= i:

                                    # print job details
                                    choiceJob = savedJobs[choice - 1]
                                    print("\nJob details\n"
                                          "\nTitle:", choiceJob[1],
                                          "\nDescription: ",choiceJob[2],
                                          "\nEmployer: ",choiceJob[3],
                                          "\nLocation: ",choiceJob[4],
                                          "\nSalary:",choiceJob[5])

                                    # show save status
                                    c.execute("SELECT * FROM jobstatus WHERE username = ? and title = ? and saved = ?",(tempStudent.username,choiceJob[1],'ON',))
                                    currentJobIsSaved = c.fetchall()
                                    if currentJobIsSaved:
                                        saved = 'ON'
                                        print("Saved: Yes")
                                    else:
                                        saved = 'OFF'
                                        print("Saved: No")

                                     # show application status
                                    c.execute("SELECT * FROM jobstatus WHERE username = ? and title = ? and applied = ?",(tempStudent.username,choiceJob[1],'ON',))
                                    appliedToJob = c.fetchall()
                                    if appliedToJob:
                                        alreadyApplied = 'ON'
                                        print("Applied: Yes")

                                    else:
                                        alreadyApplied = 'OFF'
                                        print("Applied: No")

                                    # give ability to save or apply
                                    jobOps = input("\nEnter 1 to save/unsave job or 2 to apply for this job (or 0 to go back)\n")
                                    if jobOps == "1": # save toggle
                                         if saved == 'ON': # if the job is saved already unsave
                                             if jobInDB == 'ON':# if in db just update record
                                                 c.execute("UPDATE jobstatus SET saved = ? WHERE username = ? and title = ?",('OFF',tempStudent.username,choiceJob[1],))
                                                 conn.commit()
                                             else: # insert as new job modification in jobstatus table
                                                 c.execute("INSERT INTO jobstatus VALUES(?,?,?,?,?,?,?,?)",(tempStudent.username,choiceJob[1],'OFF','ON','','','','',))
                                                 conn.commit()

                                             if jobInDB == 'OFF':
                                                 c.execute("UPDATE jobstatus SET saved = ? WHERE username = ? and title = ?",('OFF',tempStudent.username,choiceJob[1],))
                                                 conn.commit()
                                             else:
                                                 c.execute("INSERT INTO jobstatus VALUES(?,?,?,?,?,?,?,?)",(tempStudent.username,choiceJob[1],'OFF','OFF','','','','',))
                                                 conn.commit()

                                         elif saved == 'OFF': # if not saved change to saved
                                             if jobInDB == 'ON':# if in db just update record
                                                 c.execute("UPDATE jobstatus SET saved = ? WHERE username = ? and title = ?",('ON',tempStudent.username,choiceJob[1],))
                                                 conn.commit()
                                             else: # insert as new job modification in jobstatus table
                                                 c.execute("INSERT INTO jobstatus VALUES(?,?,?,?,?,?,?,?)",(tempStudent.username,choiceJob[1],'OFF','ON','','','','',))
                                                 conn.commit()

                                             if jobInDB == 'OFF':
                                                 c.execute("UPDATE jobstatus SET saved = ? WHERE username = ? and title = ?",('ON',tempStudent.username,choiceJob[1],))
                                                 conn.commit()
                                             else:
                                                 c.execute("INSERT INTO jobstatus VALUES(?,?,?,?,?,?,?,?)",(tempStudent.username,choiceJob[1],'OFF','ON','','','','',))
                                                 conn.commit()


                                    elif jobOps =="2": # give permission to apply
                                        curDate = datetime.datetime.now()
                                        dateStr = "{}-{}-{}".format(curDate.year, "%02d" % curDate.month, "%02d" % curDate.day)

                                        if alreadyApplied == 'OFF':
                                            gradDate = ''
                                            while not gradDate:
                                                gradDate = input("\nEnter graduation date: ")
                                            prefStartDate = ''
                                            while not gradDate:
                                                prefStartDate = input("\nEnter preferred start date: ")
                                            appDescription = ''
                                            while not appDescription:
                                                appDescription = input("Explain why you think you are a good fit for this role: ")
                                            # insert into jobstatus db
                                            #check if job has been pushed to jobstatus table before, if so then update
                                            if jobInDB == 'ON':
                                                c.execute("UPDATE jobstatus SET applied = ? WHERE username = ? and title = ?",('ON',tempStudent.username,choiceJob[1],))
                                                conn.commit
                                            else:
                                                c.execute("INSERT INTO jobstatus VALUES(?,?,?,?,?,?,?,?)",(tempStudent.username,choiceJob[1],'ON','OFF',gradDate,prefStartDate,appDescription,dateStr,)) # insert application details as a new record
                                                conn.commit()
                                                alreadyApplied = 'ON'
                                                break
                                        else: # already applied to job
                                            print("You already applied to this job..")
                                            break

                                    elif jobOps == "0":
                                        break

                                elif choice == "0":
                                    break
                                else:
                                    print("Invalid input..\n")
                                    break
                            else:
                                print("\nNo saved jobs..")
                                break

                    elif filterOp == "0":
                        break


            elif choice >= 1 and choice <= i: # view job details
                while True:
                    choiceJob = allJobs[choice-1]
                    # print job details job
                    print(  "\nJob details"
                            "\nTitle:", choiceJob[1],
                            "\nDescription: ",choiceJob[2],
                            "\nEmployer: ",choiceJob[3],
                            "\nLocation: ",choiceJob[4],
                            "\nSalary:",choiceJob[5])

                    # show save status
                    c.execute("SELECT * FROM jobstatus WHERE username = ? and title = ? and saved = ?",(tempStudent.username,choiceJob[1],'ON',))
                    currentJobIsSaved = c.fetchall()
                    if currentJobIsSaved:
                        saved = 'ON'
                        print("Saved: Yes")
                    else:
                        saved = 'OFF'
                        print("Saved: No")

                     # show application status
                    c.execute("SELECT * FROM jobstatus WHERE username = ? and title = ? and applied = ?",(tempStudent.username,choiceJob[1],'ON',))
                    appliedToJob = c.fetchall()
                    if appliedToJob:
                        alreadyApplied = 'ON'
                        print("Applied: Yes")
                    else:
                        alreadyApplied = 'OFF'
                        print("Applied: No")

                    if checkJobStatus(tempStudent) == 'ON':
                        jobInDB = 'ON'
                    else:
                        jobInDB = 'OFF'



                    # give ability to save or apply
                    jobOps = input("\nEnter 1 to save/unsave job or 2 to apply for this job (or 0 to go back)\n")
                    if jobOps == "1": # save toggle
                        if saved == 'ON': # if the job is saved already unsave
                            if jobInDB == 'ON':# if in db just update record
                                c.execute("UPDATE jobstatus SET saved = ? WHERE username = ? and title = ?",('OFF',tempStudent.username,choiceJob[1],))
                                conn.commit()
                            else: # insert as new job modification in jobstatus table
                                c.execute("INSERT INTO jobstatus VALUES(?,?,?,?,?,?,?,?)",(tempStudent.username,choiceJob[1],'OFF','ON','','','','',))
                                conn.commit()

                            if jobInDB == 'OFF':
                                c.execute("UPDATE jobstatus SET saved = ? WHERE username = ? and title = ?",('OFF',tempStudent.username,choiceJob[1],))
                                conn.commit()
                            else:
                                c.execute("INSERT INTO jobstatus VALUES(?,?,?,?,?,?,?,?)",(tempStudent.username,choiceJob[1],'OFF','OFF','','','','',))
                                conn.commit()

                        elif saved == 'OFF': # if not saved change to saved
                            if jobInDB == 'ON':# if in db just update record
                                c.execute("UPDATE jobstatus SET saved = ? WHERE username = ? and title = ?",('ON',tempStudent.username,choiceJob[1],))
                                conn.commit()
                            else: # insert as new job modification in jobstatus table
                                c.execute("INSERT INTO jobstatus VALUES(?,?,?,?,?,?,?,?)",(tempStudent.username,choiceJob[1],'OFF','ON','','','','',))
                                conn.commit()

                            if jobInDB == 'OFF':
                                c.execute("UPDATE jobstatus SET saved = ? WHERE username = ? and title = ?",('ON',tempStudent.username,choiceJob[1],))
                                conn.commit()
                            else:
                                c.execute("INSERT INTO jobstatus VALUES(?,?,?,?,?,?,?,?)",(tempStudent.username,choiceJob[1],'OFF','ON','','','','',))
                                conn.commit()

                    elif jobOps =="2": # give permission to apply
                            curDate = datetime.datetime.now()
                            dateStr = "{}-{}-{}".format(curDate.year, "%02d" % curDate.month, "%02d" % curDate.day)
                            if alreadyApplied == 'OFF':
                                gradDate = ''
                                while not gradDate:
                                    gradDate = input("\nEnter graduation date: ")
                                prefStartDate = ''
                                while not gradDate:
                                    prefStartDate = input("\nEnter preferred start date: ")
                                appDescription = ''
                                while not appDescription:
                                    appDescription = input("Explain why you think you are a good fit for this role: ")
                                # insert into jobstatus db
                                c.execute("INSERT INTO jobstatus VALUES(?,?,?,?,?,?,?,?)",(tempStudent.username,choiceJob[1],'ON','OFF',gradDate,prefStartDate,appDescription,dateStr)) # insert application details
                                conn.commit()
                                alreadyApplied = 'ON'
                                break
                            else: # already applied to job
                                print("You already applied to this job..")
                                break
                    else: # already applied to job
                        print("You already applied to this job..")
                        break

            elif choice == "0":
                break
            else:
                print("\nInvalid input..")
                break

        else:
            print("No jobs have been listed, going back..")
            storeAppliedJobs()
            storeSavedJobs()
            return
    
    storeAppliedJobs()
    storeSavedJobs()

# lists all jobs posted by user, ability to show details and delete individually
def viewPostedJobs(tempStudent):
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    while True:
    # fetch all jobs posted by user
        c.execute("SELECT * FROM jobs WHERE username = ?",(tempStudent.username,))
        postedJobs = c.fetchall() # list of all jobs

        #if any exist print them all
        if postedJobs:
            print("\nListing jobs posted by you:")
            i=0
            for job in postedJobs:
                i += 1
                print(i,") ", job[1])

            deleteChoice = int(input("\nEnter corresponding number of job to delete: (or 0 to go back)\n")) # give choice to delete

            if deleteChoice >=1 and deleteChoice <= i:
                while True:
                    confirm = input("\nAre you sure you want to delete this posted job? (Enter y/n)\n")
                    if confirm == "y":
                        jobChoice = postedJobs[deleteChoice-1]
                        c.execute("DELETE FROM jobs WHERE username = ? and title = ?",(tempStudent.username,jobChoice[1],))
                        conn.commit()
                        # store in api
                        storeJobs()
                        print("\nJob post has been deleted..\n")
                        break
                    elif confirm == "n":
                        break
                    else:
                        print("\nInvalid input..")
                        continue
            elif deleteChoice == "0":
                break
            break
        else:
            print("\nNo jobs currently posted..")
            return



#function that checks if a job has been pushed to the jobstatus table before or not
def checkJobStatus(tempStudent):
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    c.execute("SELECT * FROM jobstatus WHERE username = ?",(tempStudent.username,)) #check db to see if any jobs were modified by user
    exists = c.fetchall()
    if exists:
        return 'ON'
    else:
        return 'OFF'
