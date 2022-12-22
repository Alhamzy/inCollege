import sqlite3 # importing sqlite for database
from argparse import Action

# Testing the messages module

tempStudent = 'jdog'
def test_student_accounts_api_1() -> None:
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    c.execute("SELECT * from students WHERE username = ?", (tempStudent, ))
    inDatabase = c.fetchone()
    if inDatabase:
        assert True
    else:
        assert False
    c.close()

tempStudent = 'rae'
def test_student_accounts_api_2() -> None:
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    c.execute("SELECT * from students WHERE username = ?", (tempStudent, ))
    inDatabase = c.fetchone()
    if inDatabase:
        assert True
    else:
        assert False
    c.close()

tempStudent = 'tom'
def test_student_accounts_api_3() -> None:
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    c.execute("SELECT * from students WHERE username = ?", (tempStudent, ))
    inDatabase = c.fetchone()
    if inDatabase:
        assert True
    else:
        assert False
    c.close()

tempStudent = 'tom'
def test_new_jobs_api_2() -> None:
    # connecting to sqlite database
    conn = sqlite3.connect('incollege.db')
    c = conn.cursor()

    c.execute("SELECT * from jobs WHERE username = ? and title = ?", (tempStudent, "Graphic Designer"))
    inDatabase = c.fetchall()
    if inDatabase:
        assert True
    else:
        assert False
    c.close()