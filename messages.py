import sqlite3 # importing sqlite for database

def inbox(tempStudent):

    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    while True:
        c.execute("SELECT pendingMsgs FROM students WHERE username = ?", (tempStudent.username, ))
        pending = c.fetchone()[0]
        if(pending != ''):
            print("\n!!! NOTIFICATION !!! You have a new message in your inbox!")
        action = input("\nChoose an option:\n1) View all messages\n2) View new messages\n3) Send a message\n0) G0 BACK\n")
        if action == "0":
            break
        elif action == "1":
            viewMessages(tempStudent)
        elif action == "2":
            newMessages(tempStudent)
        elif action == "3":
            sendMessage(tempStudent)
        else:
            print("Invalid entry!")


def viewMessages(tempStudent):
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()
    # look up messages
    c.execute("SELECT * FROM messages WHERE recepient = ?",(tempStudent.username,))
    messages = c.fetchall()
    if len(messages) == 0:
        input("\nThere are no messages to display. Press any key to go back: ")
        conn.close()
        return
    msgCounter = 0
    newMessages = []
    for message in messages:
        msgCounter += 1
        newMessages.append([message[0], message[2]])
        print("\n" + str(msgCounter) + ") From:", message[0], "\nMessage:", message[2])
    conn.close()
    messageAction(tempStudent, newMessages, msgCounter)

def newMessages(tempStudent):
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()
    # look up messages
    c.execute("SELECT pendingMsgs FROM students WHERE username =  ?", (tempStudent.username, ))
    pendingMsgs = c.fetchone()[0]

    if pendingMsgs == '':
        print("\nYOU HAVE NO NEW MESSAGES IN YOUR INBOX")
        input("\n[Press Enter to go back]")
        conn.close()

    else:
        c.execute("UPDATE students SET pendingMsgs = ? WHERE username =  ?", ('', tempStudent.username))
        conn.commit()
        pendingMsgs = pendingMsgs.split(",")
        pendingMsgs.pop()
        newMessages = []
        for msg in pendingMsgs:
            newMessages.append(msg.split(":"))

        print("\nYOU HAVE THESE NEW MESSAGES IN YOUR INBOX: ")
        msgCounter = 0
        for msg in newMessages:
            msgCounter += 1
            print("\n" + str(msgCounter) + ") From:", msg[0], "\nMessage:", msg[1])
        
        conn.close()
        messageAction(tempStudent, newMessages, msgCounter)
        

def messageAction(tempStudent, newMessages, msgCounter):
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()
    while True:
        action = input("\nChoose an option:\n1) Reply to a message\n2) Delete a message\n0) GO BACK\n")
        if action == "0":
            conn.close()
            break
        elif action == "1" or action == "2":
            while True:
                choice = input("\nEnter the respective number from the list of messages (or 0 to cancel): ")
                if not choice:
                    print("\nERROR: Cannot be empty")
                    continue
                elif choice == "0":
                    break
                elif not choice.isnumeric():
                    print("\nERROR: Must be a numeric value")
                    continue
                else:
                    actionNum = int(choice)
                    if not (actionNum < 1 and actionNum > msgCounter):
                        if action == "1":
                            recepient = newMessages[actionNum-1][0];
                            conn.close()
                            send(tempStudent, recepient)
                            break
                        else:
                            c.execute("DELETE FROM messages WHERE recepient = ? AND message = ?", (tempStudent.username, newMessages[actionNum-1][1]))
                            conn.commit()
                            print("\nMessage deleted successfully.")
                            input("Press any key to go back: ")
                            conn.close()  # close database
                            break
                    else:
                        print("\nERROR: The number you selected is out of your list range.")
                        continue
                    break
        else:
            print("\nInvalid entry")
            continue

def sendMessage(tempStudent):
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    if tempStudent.membership == 'p':
        # display all users
        c.execute("SELECT * FROM students ORDER BY username");
        students = c.fetchall();
        print("\nHere is a list of all students in the system by username:")
        for s in students:
            print(s[0])

    if tempStudent.membership == 's':
        # check if user is friends with recepient
        c.execute("SELECT friends FROM students WHERE username = ?", (tempStudent.username, ))
        friendUsernames = c.fetchone()[0]
        if friendUsernames == '':
            print("\nYou need a PLUS membership to send messages to people not in your friends list. You currently have no friends")
            input("\nPress any key to go back:")
            conn.close()
            return
        else:
            friendUsernames = friendUsernames.split(",")
            friendUsernames.pop()
            print("\nHere is a list of all students in your friends list:")
            for s in friendUsernames:
                print(s)

    while True:
        recepient = input("\nEnter the username of the person you wish to send a message to (or 0 to go back): ")
        # check if user exists
        if recepient == "0":
            return
        c.execute("SELECT * FROM students WHERE username = ?", (recepient, ))
        student = c.fetchone()
        if not student:
            print("\nThe username you entered does not exist.")
        elif recepient == tempStudent.username:
            print("\nYou cannot send a message to yourself!")
        else:
            break

    if tempStudent.membership == 's' and recepient not in friendUsernames:
        print("\nYou need a PLUS membership to send messages to people not in your friends list.")
        input("\nPress any key to go back: ")
        conn.close()
        return

    # all validations check, send message
    conn.close()
    send(tempStudent, recepient)
    

def send(tempStudent, recepient):
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()
    message = input("\nEnter the message you wish to send: ")
    c.execute("INSERT INTO messages VALUES(?, ?, ?)", (tempStudent.username, recepient, message))
    c.execute("SELECT pendingMsgs FROM students WHERE username =  ?", (recepient, ))
    oldpending = c.fetchone()[0]
    newpending = oldpending + tempStudent.username + ":" + message + ","
    c.execute("UPDATE students SET pendingMsgs = ? WHERE username =  ?", (newpending, recepient))
    conn.commit() # commit to database
    print("\nMessage sent successfully! They will be notified upon logging in.")
    input("Press any key to go back: ")
    conn.close()  # close database



    

            
    


