# -*- coding: utf-8 -*-

# Business Manager Legacy Version 1.43.1

'''
Changelog:
- Legacy Version in case something breaks.

'''

import os
import time
from appJar import gui
loginChecker = False

global reglist
reglist = []
global DB_NAME
DB_NAME = "contacts.db"
global DB2_NAME
DB2_NAME = "registry.db"

error = ''
accumulator = 0
mem = 0
op = ''

global row
row = []
global column
column = []
global priceC
priceC = []
# Remove this later:


def bypass(btn):
    if btn == "Bypass":
        app.infoBox("Success", "Access Granted")
        app.setTabbedFrameDisableAllTabs("Tabs", False)
        app.setToolbarEnabled()
        app.setToolbarPinned()
        app.setToolbarButtonDisabled("LOGOUT", False)
        app.enableMenubar()


def press(btn):
    if btn == 'Refresh Contacts':
        app.refreshDbTable('table')
    elif btn == 'Refresh Registry':
        global row
        row = []
        global column
        column = []
        app.refreshDbTable('table2')
        global x
        x = 0
        x = app.getTableRowCount("table2")
        print(x)
        for i in range(x):
            row = app.getTableRow("table2", i)
            column.append(row[1])

    elif btn == 'Refresh Checkout':
        app.refreshListBox("List1")
        i = 0
        for i in range(x):
            app.addListItem("List1", column[i])


def checkout(btn):
    if btn == "CHECKOUT":
        global row2
        row2 = []
        global column2
        column2 = []
        global x2
        x2 = 0
        x2 = app.getTableRowCount("table2")
        print(x2)
        for i2 in range(x2):
            row = app.getTableRow("table2", i2)
            column.append(row[3])
        i2 = 0
        for i2 in range(x2):
            global priceList
            priceList = []
            priceList.append(column[i2])
            pl = priceList
            app.infoBox("Checkout", pl)


'''
    elif btn == "print":
        reg = app.getTableRow("table2", 1)
        reglist.append(reg)
        print(reglist)
'''


def changeLabel():
    app.setLabel("bar", error + str(accumulator))


def doTheMath(a, b, o):
    if o == "add":
        return a + b
    if o == "sub":
        return b - a
    if o == "mul":
        return a * b
    if o == "div":
        return b/a


'''
def press(button):
    global accumulator
    global mem
    global op

    print("A button was pressed: " + button)
    changeLabel()
    if button == "C":
        accumulator = 0
        op = ""
        mem = 0
    elif button == "=":
        accumulator = doTheMath(accumulator, mem, str(op))
        mem = 0
        op = ""
    elif button == "+":
        op = "add"
        mem = accumulator
        accumulator = 0
    elif button == "-":
        op = "sub"
        mem = accumulator
        accumulator = 0
    elif button == "x":
        op = "mul"
        mem = accumulator
        accumulator = 0
    elif button == "÷":
        op = "div"
        mem = accumulator
        accumulator = 0
    else:
        accumulator = accumulator * 10 + int(button)
        print("Acc: " + str(accumulator) + ", op: " + op + ", mem: " + str(mem))
        changeLabel()
'''


def runSql(sql):
    print(sql)
    data = []
    import sqlite3
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute(sql)
        for r in c:
            data.append(r)
    return data


def setup():
    ''' creates a new database if needed '''
    import sqlite3
    from sqlite3 import Error

    proj = ''' INSERT INTO projects(Item Name, Description, Price, Stock) VALUES(?,?,?,?) '''
    task = ''' INSERT INTO tasks(Name, Address, Mobile) VALUES(?,?,?) '''

    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute(""" CREATE TABLE IF NOT EXISTS projects (
                        id integer PRIMARY KEY,
                        Item Name text NOT NULL,
                        Description text,
                        Price integer,
                        Stock integer
                    ); """)

        c.execute("""CREATE TABLE IF NOT EXISTS tasks (
                        id integer PRIMARY KEY,
                        Name text NOT NULL,
                        Address text,
                        Mobile integer
                    );""")

        global projects
        global tasks

#        project_id = c.lastrowid
#        for i in range(1):
        #            c.execute(task, ('test', 'test2app', 1234))


def changeDb():
    table = app.optionBox("table")
    app.replaceDbTable("table", DB_NAME, table)
#    app.label("title", "Database: " + table)


def changeDb2():
    table = app.optionBox("table2")
    app.replaceDbTable("table2", DB_NAME, table)
#    app.label("title", "Database: " + table)


def addRow(a):
    table = app.optionBox("table")
    values = app.table("table")
    sql = "INSERT INTO " + table + " VALUES ("
    for v in values:
        sql += "'" + v + "', "

    sql = sql[:-2] + ")"
    try:
        runSql(sql)
        app.refreshDbTable("table")
    except:
        app.errorBox("SQL Error", "Unable to add row, check id is unique and numeric")


def addRow2(a):
    table = app.optionBox("table2")
    values = app.table("table2")
    sql = "INSERT INTO " + table + " VALUES ("
    for v in values:
        sql += "'" + v + "', "

    sql = sql[:-2] + ")"
    try:
        runSql(sql)
        app.refreshDbTable("table2")
    except:
        app.errorBox("SQL Error", "Unable to add row, check id is unique and numeric")


def deleteRow(btn, row=None):
    print(btn, row)
    if row is None:
        btn, row = "Delete", btn
    if btn == "Delete":
        rowData = app.getTableRow('table', row)
        app.selectTableRow("table", row, highlight=True)
        if app.okBox("Delete Row " + str(row), "Are you sure you want to delete row " + str(row) + "?"):
            table = app.optionBox("table")
            sql = "DELETE FROM " + table + " WHERE id='" + str(rowData[0]) + "'"
            runSql(sql)
            app.refreshDbTable("table")
        try:
            app.selectTableRow("table", row, highlight=False)
        except:
            pass


def deleteRow2(btn, row=None):
    print(btn, row)
    if row is None:
        btn, row = "Delete", btn
    if btn == "Delete":
        rowData = app.getTableRow('table2', row)
        app.selectTableRow("table", row, highlight=True)
        if app.okBox("Delete Row    " + str(row), "Are you sure you want to delete row " + str(row) + "?"):
            table = app.optionBox("table2")
            sql = "DELETE FROM " + table + " WHERE id='" + str(rowData[0]) + "'"
            runSql(sql)
            app.refreshDbTable("table2")
        try:
            app.selectTableRow("table2", row, highlight=False)
        except:
            pass


# check the database exists, make if not
try:
    con = sqlite3.connect('file:'+DB_NAME+'?mode=rw', uri=True)
except:
    setup()


'''
def edit(btn):
    if btn == "EN":
        app.editMenu = True
    else:
        app.editMenu = False
'''


def calculator(btn):
    if btn == "  +  ":
        v1 = int(app.getEntry("value1"))
        v2 = int(app.getEntry("value2"))
        tempVal = (v1 + v2)
        app.infoBox("Calculator", tempVal)
    if btn == "  -  ":
        v1 = int(app.getEntry("value1"))
        v2 = int(app.getEntry("value2"))
        tempVal = (v1 - v2)
        app.infoBox("Calculator", tempVal)
    if btn == "  *  ":
        v1 = int(app.getEntry("value1"))
        v2 = int(app.getEntry("value2"))
        tempVal = (v1 * v2)
        app.infoBox("Calculator", tempVal)
    if btn == "  /  ":
        v1 = int(app.getEntry("value1"))
        v2 = int(app.getEntry("value2"))
        tempVal = (v1 / v2)
        app.infoBox("Calculator", tempVal)
    if btn == "  C  ":
        app.entry("value1", "")
        app.setEntryFocus("value1")
        app.entry("value2", "")
        tempVal = 0


def loginCheck(u, p):
    loginChecker = False

    if u != "" and p != "":
        userfile = open('login.txt', 'r')
        userfileread = userfile.read()
        if u in userfileread:
            passfile = open('login.txt', 'r')
            passfileread = passfile.read()
            if p in passfileread:
                loginChecker = True
            else:
                loginChecker = False
                app.infoBox("ERROR", "Incorrect Password")
    else:
        app.infoBox("ERROR", "No Username/Password Entered")
    return loginChecker


def register(btn):
    if btn == "Clear Registration Data":
        app.entry("newusername", "")
        app.setEntryFocus("newusername")
        app.entry("newpassword", "")

    elif btn == "Register":
        newusername = app.getEntry("newusername")
        newpassword = app.getEntry("newpassword")
        global register
        register = []
        if newusername == "" or newpassword == "":
            app.infoBox("ERROR", "No Username/Password Entered")
        else:
            register.append(newusername + '\n' + newpassword)
            with open('login.txt', 'w') as f:
                for line in register:
                    f.write(line)
                    f.write('\n')
            app.infoBox("Success", "Successfully Registered")


def login(btn):

    if btn == "Clear Login Data":
        app.entry("username", "")
        app.setEntryFocus("username")
        app.entry("password", "")

    elif btn == "Submit":
        username = app.getEntry("username")
        password = app.getEntry("password")
        loginChecker = False
        loginChecker = loginCheck(username, password)

        if loginChecker is True:
            app.infoBox("Success", "Access Granted")
            app.setTabbedFrameDisableAllTabs("Tabs", False)
            app.setToolbarEnabled()
            app.setToolbarPinned()
            app.setToolbarButtonDisabled("LOGOUT", False)
            app.enableMenubar()
        elif loginChecker is False:
            logout()

    elif username == "":
        app.infoBox("ERROR", "No Username Entered")
    else:
        app.infoBox("ERROR", "Incorrect Username")
        logout()


def logoutFunction():
    return app.yesNoBox("Confirm Exit", "Are you sure you want to exit?")


def logout(btn=None):
    app.setTabbedFrameDisableAllTabs("Tabs")
    app.setTabbedFrameDisabledTab("Tabs", "Login", False)
    app.setTabbedFrameSelectedTab("Tabs", "Login")
    app.setToolbarDisabled()
    app.setToolbarButtonEnabled("EXIT")
    app.disableMenubar()
    notesapp = app.getTextArea("Notes")
    with open('notes.txt', 'w') as f:
        for line in notesapp:
            f.write(line)

#    open('login.txt', 'w').close()


def toolbar(btn):
    if btn == "EXIT":
        app.stop()
    elif btn == "LOGOUT":
        logout()
    elif btn == "FULL-SCREEN":
        if app.exitFullscreen():
            app.setToolbarIcon("FULL-SCREEN", "FULL-SCREEN")
        else:
            app.setSize("fullscreen")
            app.setToolbarIcon("FULL-SCREEN", "FULL-SCREEN-EXIT")
    elif btn == "ACCESS":
        app.showAccess()
    elif btn == "FILE":
        app.startSubWindow("File Search", modal=True)
        app.gui("Set Size()")
        app.showAllSubWindows()
        app.setSize(400, 400)
        app.addLabelEntry("Start Path")
        app.setEntry("Start Path", "/Users/phantomtnt/Desktop")
        app.addLabelEntry("File Ending")
        app.setEntry("File Ending", ".db")
        app.addListBox("files", [])
        app.setListBoxRows("files", 15)
        app.addButton("Search", search)
        app.link("File Search Help", fileSearchHelp, sticky="e")
        app.stopSubWindow()


def calendar(btn):
    global store1
    global store2
    global finalval

    if btn == "Store1":
        store1 = app.getDatePicker("dp")
    if btn == "Store2":
        store2 = app.getDatePicker("dp")
    if btn == "Calculate":
        finalval = (store2 - store1)
        app.infoBox("The difference is:", finalval)


def search(button):
    startDir = app.getEntry("Start Path")
    fileEnding = app.getEntry("File Ending")
    app.clearListBox("files")
    for path, dirs, files, in os.walk(startDir):
        for fileName in files:
            if (fileName.endswith(fileEnding)):
                app.addListItem("files", path + "/" + fileName)


def changeTab(tabName):
    print("Changing to: ", tabName)
    app.setTabbedFrameSelectedTab("Tabs", tabName)
    print("done")


def loginHelp(nbtn):
    app.infoBox("Login Help", "You may need to register first.")


def registerHelp(nbtn):
    app.infoBox("Register Help", "Just input a new username and password.")


def calcHelp(nbtn):
    app.infoBox("Calculator Help", "Enter Value 1 and 2, then use the operator buttons.")


def calHelp(nbtn):
    app.infoBox("Calendar Help", "Store 2 dates, and calculate the days between them.")


def toolbarHelp(nbtn):
    app.infoBox("Toolbar Help", "The EXIT Button quits the application. The LOGOUT Button saves all data and logs out the user. The ACCESS Button opens up the Accessibility options menu which contains various features to tweak with to adjust your experience. The FULL-Screen Button puts the app in Full-Screen mode.")


def fileSearchHelp(nbtn):
    app.infoBox("File Search Help", "Input values and let the file search app find them for you")

# CONTINUE WORK HERE

# CONTINUE WORK ON TOOLBAR HELP MENU

# BASICALLY HAVE MULTIPLE INFOBOXES WITH EACH BUTTON's FUNCTION ON EACH INFOBOX

#  !!!!!!!!!!!!!!!!!!!!!!!!


def timer():
    app.setStatusbar(time.strftime("%X"))


def showDate(btn):
    print(app.getDatePicker("dp"))
    print("The date:")


'''
def registryDeleteRow(dRow):
    app.deleteTableRow("Registry", dRow)


def registryAddRow():
    app.addTableRow("Registry", app.getTableEntries('Registry'))
'''


def move(direction):
    if direction == ">":
        for item in app.getListBox("List1"):
            app.addListItem("List2", item)
            app.removeListItem("List1", item)
    elif direction == "<":
        for item in app.getListBox("List2"):
            app.addListItem("List1", item)
            app.removeListItem("List2", item)
    elif direction == "<<":
        app.addListItems("List1", app.getAllListItems("List2"))
        app.clearListBox("List2")
    elif direction == ">>":
        app.addListItems("List2", app.getAllListItems("List1"))
        app.clearListBox("List1")
    if direction == "Delete":
        for item in app.getListBox("List1"):
            app.removeListItem("List1", item)
        for item in app.getListBox("List2"):
            app.removeListItem("List2", item)


def add(entry):
    if entry == "List1Entry":
        app.addListItem("List1", app.getEntry("List1Entry"))
        app.clearEntry("List1Entry")


# GUI STARTS HERE


with gui("Business Manager", "640x480", log="trace") as app:
    app.setLogLevel("ERROR")
#    app.showSplash("Welcome back!")
    app.addToolbar(["EXIT", "LOGOUT", "ACCESS", "FULL-SCREEN", "FILE"], toolbar, findIcon=True)
    app.addMenuItem("Exit", "EXIT")
    app.addMenuHelp(toolbar)
    try:
        app.setMenuIcon("Test", "LOGOUT", "LOGOUT", "right", "FOLDER")
    except:
        pass
    app.disableMenubar()
    app.addStatusbar(side="RIGHT")
    app.registerEvent(timer)
    app.stopFunction = logoutFunction

    with app.tabbedFrame("Tabs"):
        with app.tab("Login", bg="slategrey", sticky="new"):
            with app.labelFrame("Login Form"):
                app.label("username", "Username", sticky="ew")
                app.entry("username", pos=('p', 1), focus=True)
                app.label("password", "Password")
                app.entry("password", pos=('p', 1), secret=True)
                app.buttons(["Submit", "Clear Login Data"], login, colspan=2)
                app.link("Login Help", loginHelp, column=1, sticky="e")

            with app.labelFrame("Register Form"):
                app.label("New Account: ", "Username ", sticky="ew")
                app.entry("newusername", pos=('p', 1), focus=True)
                app.label("Password: ", "Password")
                app.entry("newpassword", pos=('p', 1), secret=True)
                app.buttons(["Register", "Clear Registration Data"], register, colspan=2)
                app.link("Registration Help", registerHelp, column=1, sticky="e")

            with app.labelFrame("Bypass Menu"):
                app.buttons(["Bypass"], bypass)

        with app.tab("Notes", bg="slategrey"):
            notesread = open('notes.txt', 'r')
            notesappread = notesread.read()
            app.addTextArea("Notes", text=notesappread)

        with app.tab("Contacts", bg="slategrey", sticky="new"):
            with app.labelFrame("Contacts List:"):

                app.editMenu = True
    #            app.createRightClickMenu("demo")
    #            app.addMenuItem("demo", "STOP", app.stop)
                app.addDbOptionBox("table", DB_NAME, change=changeDb, right="demo")
    #            app.label("title", "DB tester:", font=60, bg="orange", sticky="EW")
    #            app.setLabelRightClick("title", "demo")
                app.config(sticky="NEWS", stretch="both")
                app.table("table", DB_NAME, "tasks", kind='database', action=deleteRow, addRow=addRow, actionButton=[
                          "Delete"], showMenu=True, disabledEntries=[0], actionHeading='Delete?', sticky='ew')
                app.setOptionBox("table", "tasks", callFunction=False)
    #            app.button("NEW TABLE", showMakeTable, sticky="", stretch="column")
    #            app.label("PRESS ME", font={"size": 40, "underline": True}, right="demo")
    #            app.addButtons(["EN", "DI"], edit)
    #            app.button("COUNT", press)
                app.refreshDbTable('table')
                app.button("Refresh Contacts", press, sticky="e")

                # add help

        with app.tab("Calculator", bg="slategrey", sticky="nw"):
            with app.labelFrame("Calculator"):
                app.label("value1", "value1", sticky="ew")
                app.entry("value1", pos=('p', 1))
                app.label("value2", "value2")
                app.entry("value2", pos=('p', 1))
                app.buttons(["  +  ", "  -  ", "  *  ", "  /  ", "  C  "], calculator, colspan=2)
                app.link("Calculator Help", calcHelp, column=1, sticky="e")

            with app.labelFrame("Calendar"):
                app.label(" ")
                app.addDatePicker("dp")
                app.buttons(["Store1", "Store2", "Calculate"], calendar, colspan=2)
                app.setDatePickerRange("dp", 1900, 2050)
                app.setDatePicker("dp")
                app.link("Calendar Help", calHelp, column=1, sticky="e")

        with app.tab("Records", bg="slategrey", sticky="new"):
            with app.labelFrame("Records List:"):
                app.editMenu = True
    #            app.createRightClickMenu("demo")
    #            app.addMenuItem("demo", "STOP", app.stop)
                app.addDbOptionBox("table2", DB2_NAME, change=changeDb2, right="demo")
    #            app.label("title", "DB tester:", font=60, bg="orange", sticky="EW")
    #            app.setLabelRightClick("title", "demo")
                app.config(sticky="NEWS", stretch="both")
                app.table("table2", DB2_NAME, "projects", kind='database', action=deleteRow2, addRow=addRow2, actionButton=[
                    "Delete2"], showMenu=True, disabledEntries=[0], actionHeading='Delete2?', sticky='ew')
                app.setOptionBox("table2", "tasks", callFunction=False)
    #            app.button("NEW TABLE", showMakeTable, sticky="e", stretch="column")
    #            app.label("PRESS ME", font={"size": 40, "underline": True}, right="demo")
    #            app.addButtons(["EN", "DI"], edit)
    #            app.button("COUNT", press)
                app.refreshDbTable("table2")

                app.button("Refresh Registry", press, sticky="e")
    #            app.button("print", press)
    # add help

        with app.tab("Checkout", bg="slategrey", sticky="new"):
            app.listbox("List1", [], pos=(0, 0, 1, 4), bg="light grey")
            app.listbox("List2", [], pos=(0, 2, 1, 4), bg="light grey")
            app.button("<", move, pos=(0, 1))
            app.button("<<", move, pos=(3, 1))
            app.button(">>", move, pos=(2, 1))
            app.button(">", move, pos=(1, 1))
            app.button("Delete", move, pos=(4, 1))
            # app.entry("List1Entry", pos=(4, 0), bg="white",
            #          submit=add, default="Add New Item")
            app.button("Refresh Checkout", press)
            app.button("CHECKOUT", checkout)
            # add help

        with app.tab("HELP", bg="slategrey", sticky="new"):
            app.label("Welcome to the Help Menu for Business Manager 1.4")
            app.label("The application is divided into a Toolbar and the tabbed menu bar.")
            app.label("The Toolbar consists of the EXIT, LOGOUT, ACCESS, and FULLSCREEN buttons.")
            app.link("Toolbar Help", toolbarHelp)
            app.label("35j4u3gh345ygh3")

    logout()


# UNUSED


'''
        with app.tab("Better Calculator", bg="slategrey", sticky="new"):
            with app.labelFrame("Calculator 2"):
                app.addLabel("bar", error + str(accumulator), 0, 0, 3)
                app.addButtons(["1"], press, 3, 0)
                app.addButtons(["2"], press, 3, 1)
                app.addButtons(["3"], press, 3, 2)
                app.addButtons(["4"], press, 2, 0)
                app.addButtons(["5"], press, 2, 1)
                app.addButtons(["6"], press, 2, 2)
                app.addButtons(["7"], press, 1, 0)
                app.addButtons(["8"], press, 1, 1)
                app.addButtons(["9"], press, 1, 2)
                app.addButtons(["0"], press, 4, 1)
                app.addButtons(["+"], press, 3, 3)
                app.addButtons(["-"], press, 4, 3)
                app.addButtons(["x"], press, 2, 3)
                app.addButtons(["÷"], press, 1, 3)
                app.addButtons(["="], press, 4, 2)
                app.addButtons(["C"], press, 4, 0)

                # add help
'''


