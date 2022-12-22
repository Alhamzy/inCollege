import sqlite3 # importing sqlite for database

def guestControls(tempStudent):
    # code goes here...
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    while True:
        c.execute("SELECT email FROM students WHERE username = ?", (tempStudent.username, ))
        email = c.fetchone()[0]
        c.execute("SELECT sms FROM students WHERE username = ?", (tempStudent.username, ))
        sms = c.fetchone()[0]
        c.execute("SELECT ads FROM students WHERE username = ?", (tempStudent.username, ))
        ads = c.fetchone()[0]

        # guest controls
        print("Guest control settings:\n1) InCollege Email: ", email,
              "\n2) SMS: ", sms, "\n3) Targeted Advertising: ", ads,
              "\n0) GO BACK\n")
        action = input(
            "Enter 1-3 to toggle respective settings, or 0 to go back: "
        )  # collect user input/option
        if action == "1":  # option 1
            if email == "ON":
                email = "OFF"
            else:
                email = "ON"

            c.execute("UPDATE students SET email = ? WHERE username =  ?", (email, tempStudent.username))
            conn.commit()

        elif action == "2":  # option 2
            if sms == "ON":
                sms = "OFF"
            else:
                sms = "ON"

            c.execute("UPDATE students SET sms = ? WHERE username =  ?", (sms, tempStudent.username))
            conn.commit()

        elif action == "3":  # option 3
            if ads == "ON":
                ads = "OFF"
            else:
                ads = "ON"

            c.execute("UPDATE students SET ads = ? WHERE username =  ?", (ads, tempStudent.username))
            conn.commit()

        elif action == "0":  # option 0 : go back
            conn.close()
            break  # returns back to important links
        else:
            print("\nInvalid entry!\n")  # otherwise invalid entry and loop back


def languages(tempStudent):
    # code goes here...
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    c.execute("SELECT language FROM students WHERE username = ?", (tempStudent.username, ))
    lang = c.fetchone()[0]
    
    if lang == "eng":
        currentLanguage = "ENGLISH"
    elif lang == "spa":
        currentLanguage = "SPANISH"
    print("Language: ", currentLanguage, "\n")
    while True:
        action = input("Enter 1 to change language, or 0 to go back: ")
        if action == "0":
            conn.close()
            break
        elif action == "1":
            while True:
                new_lang = input("Language Options:\n1) English\n2) Spanish\n")
                if new_lang == "1":
                    lang = "eng"
                    break;
                elif new_lang == "2":
                    lang = "spa"
                    break;
                else:
                    print("Invalid selection")
                    continue

            c.execute("UPDATE students SET language = ? WHERE username =  ?", (lang, tempStudent.username))
            conn.commit()
            conn.close()

            print("\nLanguage settings have been updated!")
            input("\n[Press Enter to go back]")
            break

        else:
            print("Invalid selection")