import sqlite3 # importing sqlite for database

from profile import displayProfile

# Friend Options
def friends(tempStudent):
    # code goes here...
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    c.execute("SELECT pending FROM students WHERE username = ?", (tempStudent.username, ))
    pending = c.fetchone()[0]

    while True:
        if(pending != ''):
            print(
                "\n!!! NOTIFICATION !!! You have a pending friend request! View your pending friend requests to accept/reject your request(s)."
            )

        print("\nChoose an option:\n1) Find friends & send requests\n2) View your pending friend requests\n3) Show my network\n0) G0 BACK\n")
        action = input("Type 1-3, or 0 to go back: ")
        if action == "0":
            conn.close()
            break
        elif action == "1":
            conn.close()
            sendRequests(tempStudent)
        elif action == "2":
            conn.close()
            pendingRequests(tempStudent)
        elif action == "3":
            conn.close()
            friendlist(tempStudent)
        else:
            print("\nInvalid entry!")

def sendRequests(tempStudent):
    # code goes here...
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    while True:

        print("\nSTUDENT SEARCH")
        query = input("Search for students in the system by last name, university, major: ")
        query = query.lower()
        c.execute("SELECT * FROM students WHERE lower(lastname) = ?", (query, ))
        lastnames_inclusive = c.fetchall()
        lastnames = []
        for students in lastnames_inclusive:
            if students[0] == tempStudent.username:
                continue
            lastnames.append(students)

        if lastnames:
            print("Here is a list of students with the last name " + query)
            queryCounter = 0
            for students in lastnames:
                queryCounter+=1
                print(str(queryCounter) + ". " + students[2] + " " + students[3])
            conn.close()
            sendTo(tempStudent, lastnames)
            break
        else:
            c.execute("SELECT * FROM profile WHERE lower(university) = ?", (query, ))
            universities_inclusive = c.fetchall()
            universities = []
            for students in universities_inclusive:
                if students[0] == tempStudent.username:
                    continue
                universities.append(students)

            if universities:
                print("Here is a list of students who go to " + query)
                queryCounter = 0
                for students in universities:
                    c.execute("SELECT * FROM students WHERE username = ?", (students[0], ))
                    student = c.fetchone()
                    queryCounter+=1
                    print(str(queryCounter) + ". " + student[2] + " " + student[3])
                conn.close()
                sendTo(tempStudent, universities)
                break
            else:
                c.execute("SELECT * FROM profile WHERE lower(major) = ?", (query, ))
                majors_inclusive = c.fetchall()
                majors = []
                for students in majors_inclusive:    
                    if students[0] == tempStudent.username:
                        continue
                    majors.append(students)

                if majors:
                    print("Here is a list of students who major in " + query)
                    queryCounter = 0
                    for students in majors:
                        c.execute("SELECT * FROM students WHERE username = ?", (students[0], ))
                        student = c.fetchone()
                        queryCounter+=1
                        print(str(queryCounter) + ". " + student[2] + " " + student[3])
                    conn.close()
                    sendTo(tempStudent, majors)
                    break
                else:
                    print("NO RESULTS")
                    input("[Press Enter to search again]")
                    continue


def sendTo(tempStudent, queryList):
    # coee goes here...
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    while True:
        action = input("\n1 to send friend request, 0 to go back: ")
        if action == "0":
            conn.close()
            break
        elif action == "1":
            while True:
                action = input("Enter the respective number from your search list to send your request (or 0 to cancel): ")
                if not action:
                    print("\nERROR: Cannot be empty")
                    continue
                elif action == "0":
                    break
                elif not action.isnumeric():
                    print("\nERROR: Must be a numeric value")
                    continue
                else:
                    actionNum = int(action)
                    if not (actionNum < 1 or actionNum > len(queryList)):
                        doublecheck = input("Are you sure you want to send a friend request to " + queryList[actionNum-1][2] + " " + queryList[actionNum-1][3] + " (y/n) ")
                        if doublecheck == "y" or doublecheck == "yes":
                            c.execute("SELECT pending FROM students WHERE username =  ?", (queryList[actionNum-1][0], ))
                            oldpending = c.fetchone()[0]
                            newpending = oldpending + tempStudent.username + ","

                            # update friend list
                            c.execute("UPDATE students SET pending = ? WHERE username =  ?", (newpending, queryList[actionNum-1][0]))
                            conn.commit()
                            print("\nFriend request sent!")
                            conn.close()
                            break
                        else:
                            print("\nCancelling operation. Returning back...")
                            conn.close()
                            break
                    else:
                        print("\nERROR: The number you selected is out of your search list range.")
                        continue
            break
        else:
            print("Invalid entry!")
            continue
        


def pendingRequests(tempStudent):
    # code goes here...
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    c.execute("SELECT pending FROM students WHERE username = ?", (tempStudent.username, ))
    pendingUsernames = c.fetchone()[0]

    if pendingUsernames == '':
        print("\nYOU HAVE NO PENDING FRIEND REQUESTS")
        input("\n[Press Enter to go back]")
        conn.close()
    else:

        pendingUsernames = pendingUsernames.split(",")
        pendingUsernames.pop()
        friendList = []

        for pendingUsername in pendingUsernames:
            c.execute("SELECT * FROM students WHERE username = ?", (pendingUsername, ))
            fname = c.fetchone()[2]
            c.execute("SELECT * FROM students WHERE username = ?", (pendingUsername, ))
            lname = c.fetchone()[3]
            fullname = fname  + " " + lname
            friendList.append(fullname)
        
        print("\nYOU HAVE FRIEND REQUESTS FROM THE FOLLOWING PEOPLE: ")
        friendCounter = 0
        for friend in friendList:
            friendCounter+=1
            print(friendCounter, ". " + friend)
        while True:
            action = input("Type 1 to select friend request to accept/reject, or 0 to go back: ")
            if action == "0":
                conn.close()
                break
            elif action == "1":
                while True:
                    action = input("\nEnter the respective number from your pending request list (or 0 to cancel): ")
                    if not action:
                        print("\nERROR: Cannot be empty")
                        continue
                    elif action == "0":
                        break
                    elif not action.isnumeric():
                        print("\nERROR: Must be a numeric value")
                        continue
                    else:
                        actionNum = int(action)
                        if not (actionNum < 1 or actionNum > friendCounter):

                            while True:
                                print("\nDo you want to accept or reject this friend request from " + friendList[actionNum-1] + "?")
                                decision = input("Type 1 to accept, 2 to reject, or 0 to cancel and go back: ")
                                if decision == "1":

                                    index = 1
                                    newPendingList = ''

                                    for pendingUsername in pendingUsernames:
                                        if index == actionNum:
                                            continue
                                        newPendingList = newPendingList + pendingUsername + ","
                                        index+=1

                                    # update pending list
                                    c.execute("UPDATE students SET pending = ? WHERE username =  ?", (newPendingList, tempStudent.username))
                                    conn.commit()
                                    
                                    # update your friend's list
                                    c.execute("SELECT friends FROM students WHERE username = ?", (tempStudent.username, ))
                                    friendUsernames = c.fetchone()[0]
                                    friendUsernames = friendUsernames + pendingUsernames[actionNum-1] + ","
                                    c.execute("UPDATE students SET friends = ? WHERE username =  ?", (friendUsernames, tempStudent.username))
                                    conn.commit()

                                    # update second-party friend's list
                                    c.execute("SELECT friends FROM students WHERE username = ?", (pendingUsernames[actionNum-1], ))
                                    friendUsernames = c.fetchone()[0]
                                    friendUsernames = friendUsernames + tempStudent.username + ","
                                    c.execute("UPDATE students SET friends = ? WHERE username =  ?", (friendUsernames, pendingUsernames[actionNum-1]))
                                    conn.commit()

                                    print("\nYou and " + friendList[actionNum-1] + " are now friends!")
                                    conn.close()
                                    break
                                    
                                elif decision == "2":
                                    index = 1
                                    newPendingList = ''

                                    for pendingUsername in pendingUsernames:
                                        if index == actionNum:
                                            continue
                                        newPendingList = newPendingList + pendingUsername + ","
                                        index+=1

                                    # update pending list
                                    c.execute("UPDATE students SET pending = ? WHERE username =  ?", (newPendingList, tempStudent.username))
                                    conn.commit()
                                    print("\nFriend request rejected")
                                    conn.close()
                                    break

                                elif decision == "0":
                                    print("\nCancelling operation. Returning back...")
                                    conn.close()
                                    break
                                else:
                                    print("\nInvalid Entry")
                                    continue
                        
                        else:
                            print("\nERROR: The number you selected is out of your list range.")
                            continue
                        break
                break
            else:
                print("\nInvalid entry")
                continue


def friendlist(tempStudent):
    # coee goes here...
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    c.execute("SELECT friends FROM students WHERE username = ?", (tempStudent.username, ))
    friendUsernames = c.fetchone()[0]

    if friendUsernames == '':
        print("\nTHERE ARE NO FRIENDS IN YOUR FIRENDLIST!")
        input("\n[Press Enter to go back]")
        conn.close()
    else:

        friendUsernames = friendUsernames.split(",")
        friendUsernames.pop()
        friendList = []
        for friendUsername in friendUsernames:
            c.execute("SELECT * FROM students WHERE username = ?", (friendUsername, ))
            fname = c.fetchone()[2]
            c.execute("SELECT * FROM students WHERE username = ?", (friendUsername, ))
            lname = c.fetchone()[3]
            fullname = fname  + " " + lname
            friendList.append(fullname)
        
        print("\nFRIEND LIST: ")
        friendCounter = 0
        for friend in friendList:
            friendCounter+=1
            print(friendCounter, ". " + friend)
        while True:
            action = input("Type 1 to view profile, 2 to remove friend, or 0 to go back: ")
            if action == "0":
                conn.close()
                break
            elif action == '1':
                while True:
                    action = input("\nEnter the respective number from your friend list to view their profile (or 0 to cancel): ")
                    if not action:
                        print("\nERROR: Cannot be empty")
                        continue
                    elif action == "0":
                        conn.close()
                        friendlist(tempStudent)
                    elif not action.isnumeric():
                        print("\nERROR: Must be a numeric value")
                        continue
                    else:
                        actionNum = int(action)
                        if not (actionNum < 1 or actionNum > friendCounter):

                            c.execute("SELECT * FROM students WHERE username = ?", (friendUsernames[actionNum-1], ))
                            selected_friend = c.fetchone()
                            break
                        else:
                            print("\nERROR: The number you selected is out of your list range.")

                c.execute("SELECT * FROM profile WHERE username = ?", (friendUsernames[actionNum-1], ))
                createdProfile = c.fetchone()
                if not createdProfile:
                    print("\nYOUR FRIEND HAS NOT CREATED A PROFILE")
                    input("[Press Enter to go back]")
                else:
                    displayProfile(selected_friend[0], selected_friend[2], selected_friend[3])
                    input("[Press Enter to go back]")
                break

            elif action == "2":
                while True:
                    action = input("\nEnter the respective number from your friend list to remove (or 0 to cancel): ")
                    if not action:
                        print("\nERROR: Cannot be empty")
                        continue
                    elif action == "0":
                        conn.close()
                        break
                    elif not action.isnumeric():
                        print("\nERROR: Must be a numeric value")
                        continue
                    else:
                        actionNum = int(action)
                        if not (actionNum < 1 or actionNum > friendCounter):
                            doublecheck = input("Are you sure you want to remove " + friendList[actionNum-1] + " from your friend list? (y/n) ")
                            if doublecheck == "y" or doublecheck == "yes":
                                
                                # update friend list
                                index = 1
                                newFriendList = ''
                                for friendUsername in friendUsernames:
                                    if index == actionNum:
                                        continue
                                    newFriendList = newFriendList + friendUsername + ","
                                    index+=1
                                c.execute("UPDATE students SET friends = ? WHERE username =  ?", (newFriendList, tempStudent.username))
                                conn.commit()

                                # update second party's friend list
                                c.execute("SELECT friends FROM students WHERE username = ?", (friendUsernames[actionNum-1], ))
                                otherFriendUsernames = c.fetchone()[0]
                                otherFriendUsernames = otherFriendUsernames.split(",")
                                otherFriendUsernames.pop()

                                newFriendList = ''
                                for otherFriendUsername in otherFriendUsernames:
                                    if otherFriendUsername == tempStudent.username:
                                        continue
                                    newFriendList = newFriendList + otherFriendUsername + ","

                                c.execute("UPDATE students SET friends = ? WHERE username =  ?", (newFriendList, friendUsernames[actionNum-1]))
                                conn.commit()

                                print("\n" + friendList[actionNum-1] + " has been removed from your friend's list.")
                                conn.close()
                            else:
                                print("\nCancelling operation. Returning back...")
                                conn.close()
                        else:
                            print("\nERROR: The number you selected is out of your list range.")
                            continue
                        break
                break
            else:
                print("\nInvalid entry")
                continue