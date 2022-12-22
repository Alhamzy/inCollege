import sqlite3 # importing sqlite for database

def storeJobs():
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    #look up all jobs in db
    c.execute("SELECT * FROM jobs")
    allJobs = c.fetchall()

    try:
        with open('output_apis/MyCollege_jobs.txt', 'w') as f:
            for job in allJobs:
                f.write("{}\n".format(job[0]))
                f.write("{}\n".format(job[1]))
                f.write("{}\n".format(job[2]))
                f.write("{}\n".format(job[3]))
                f.write("{}\n".format(job[4]))
                f.write("{}\n".format(job[5]))
                f.write("=====\n")
    except FileNotFoundError:
        print("The 'output_apis' directory does not exist")


def storeUsers():
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    #look up all jobs in db
    c.execute("SELECT * FROM students")
    allUsers = c.fetchall()

    try:
        with open('output_apis/MyCollege_users.txt', 'w') as f:
            for user in allUsers:
                f.write("{}, {}\n".format(user[0], user[11]))
    except FileNotFoundError:
        print("The 'output_apis' directory does not exist")


def storeProfiles():
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    #look up all profiles in db
    c.execute("SELECT * FROM profile")
    allProfiles = c.fetchall()

    try:
        with open('output_apis/MyCollege_profiles.txt', 'w') as f:
            for profile in allProfiles:
                f.write("{}\n".format(profile[0]))
                f.write("{}\n".format(profile[1]))
                f.write("{}\n".format(profile[2]))
                f.write("{}\n".format(profile[3]))
                f.write("{}\n".format(profile[4]))
                f.write("=====\n")
    except FileNotFoundError:
        print("The 'output_apis' directory does not exist")


def storeAppliedJobs():
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    #look up all profiles in db
    c.execute("SELECT * FROM jobstatus WHERE applied = ?", ('ON', ))
    allAppliedJobs = c.fetchall()

    try:
        with open('output_apis/MyCollege_appliedJobs.txt', 'w') as f:
            for job in allAppliedJobs:
                f.write("{}, {}\n".format(job[1], job[0]))
                f.write("{}\n".format(job[6]))
                f.write("=====\n")
    except FileNotFoundError:
        print("The 'output_apis' directory does not exist")


def storeSavedJobs():
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    #look up all profiles in db
    c.execute("SELECT * FROM jobstatus WHERE saved = ?", ('ON', ))
    allSavedJobs = c.fetchall()

    try:
        with open('output_apis/MyCollege_savedjobs.txt', 'w') as f:
            for job in allSavedJobs:
                f.write("{}, {}\n".format(job[0], job[1]))
                f.write("=====\n")
    except FileNotFoundError:
        print("The 'output_apis' directory does not exist")