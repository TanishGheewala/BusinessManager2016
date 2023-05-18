# -*- coding: utf-8 -*-

# Tanish Gheewala IB Computer Science IA
# Business Manager

# Importing required libraries and defining global variables
import os
import time
import tkinter

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
global row2
row2 = []
global column
column = []
global priceC
priceC = []

# sqlite3 connection code
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

# main button functions
def press(btn):
    if btn == 'Refresh Contacts':
        app.refreshDbTable('table')
    elif btn == 'Refresh Registry':
        global row
        row = []
        global row2
        row2 = []
        global column
        column = []
        global column2
        column2 = []
        app.refreshDbTable('table2')
        global x
        x = 0
        global x2
        x2 = 0
        x = app.getTableRowCount("table2")
        print(x)
        for i in range(x):
            row = app.getTableRow("table2", i)
            column.append(row[1])
            row2 = app.getTableRow("table2", i)
            column2.append(row[3])

    elif btn == 'Refresh Checkout':
        app.refreshListBox("List1")
        i = 0
        for i in range(x):
            app.addListItem("List1", column[i])


# checkout function
def checkout(btn):
    if btn == "CHECKOUT":
        global pricelist
        pricelist = []
        pricelist = [int(u) for u in column2]
        print(pricelist)
        pricelistfinal = 0
        pricelistfinal = sum(pricelist)
        print(pricelistfinal)
        app.infoBox("Final Price", pricelistfinal)


def changeLabel():
    app.setLabel("bar", error + str(accumulator))


# main database code
def setup():
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


def changeDb():
    table = app.optionBox("table")
    app.replaceDbTable("table", DB_NAME, table)

def changeDb2():
    table = app.optionBox("table2")
    app.replaceDbTable("table2", DB_NAME, table)


# for configuring grids with appJar
'''
def setNavPositionTop(self, top=True):
    oldNavPos = self.navPos
    pady = (0, 5)
    if top:
        self.navPos = 0
    else:
        self.navPos = 1
    if oldNavPos != self.navPos:
        if self.navPos == 0:
            self.grid_rowconfigure(1, weight=0)
            self.grid_rowconfigure(2, weight=1)
            pady = (5, 0)
        else:
            self.grid_rowconfigure(1, weight=1)
            self.grid_rowconfigure(2, weight=0)
        self.frameStack.grid_remove()
        self.prevButton.grid_remove()
        self.posLabel.grid_remove()
        self.nextButton.grid_remove()

        self.frameStack.grid(row=int(not self.navPos) + 1, column=0,
                             columnspan=3, sticky=N + S + E + W, padx=5, pady=5)
        self.prevButton.grid(row=self.navPos + 1, column=0, sticky=S + W, padx=5, pady=pady)
        self.posLabel.grid(row=self.navPos + 1, column=1, sticky=S + E + W, padx=5, pady=pady)
        self.nextButton.grid(row=self.navPos + 1, column=2, sticky=S + E, padx=5, pady=pady)
'''

# function to add a row

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

# function to delete a row
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

# function to delete a row
def deleteRow(btn, row=None):
    print(btn, row)
    if row is None:
        btn, row = "Delete", btn
    if btn == "Delete":
        rowData = app.getTableRow('table', row)
        app.selectTableRow("table", row, highlight=True)
        if app.okBox("Delete Row " + str(row+1), "Are you sure you want to delete row " + str(row+1) + "?"):
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
        if app.okBox("Delete Row    " + str(row+1), "Are you sure you want to delete row " + str(row+1) + "?"):
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


# oop classes to manage tabs via appJar
'''
def _tabbedFrameMaker(self, master, useTtk=False, **kwargs):
  global OrderedDict
   # if OrderedDict is None:
#        from collections import OrderedDict

    class TabBorder(Frame, object):
        def __init__(self, master, **kwargs):
            super(TabBorder, self).__init__(master, **kwargs)
            self.config(borderwidth=0, highlightthickness=0, bg='darkGray')

    class TabContainer(frameBase, object):
        def __init__(self, master, **kwargs):
            super(TabContainer, self).__init__(master, **kwargs)
            TabBorder(self, height=2).pack(side=TOP, expand=True, fill=X)
            TabBorder(self, width=2).pack(side=LEFT, fill=Y, expand=0)

    class TabText(labelBase, object):
        def __init__(self, master, func, text, **kwargs):
            super(TabText, self).__init__(master, text=text, **kwargs)
            self.disabled = False
            self.DEFAULT_TEXT = text
            self.hidden = False
            self.bind("<Button-1>", lambda *args: func(text))
            self.border = TabBorder(master, width=2)
'''

# calculator function
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
        if tempVal == 0:
            app.infoBox("Calculator", '0')
        else:
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


# main login checker, to check if username/password is entered or not, and if it is accurate
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

# main register code to register a new Account
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


# main login button to login to an existing account
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

# logout function

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

    notesapp2 = app.getTextArea("Notes2")
    with open('notes2.txt', 'w') as f:
        for line in notesapp2:
            f.write(line)

    app.entry("username", "")
    app.setEntryFocus("username")
    app.entry("password", "")


#    open('login.txt', 'w').close()


# some of this code messes up the program when i tested it on macOS, so i have disabled it for now

# appJar's widget, toolbar, and main window containers
'''
class Toolbar(frameBase, object):
    def __init__(self, master, **kwargs):
        super(Toolbar, self).__init__(master, **kwargs)
        self.BG_COLOR = None
        self.pinned = True
        self.pinBut = None
        self.inUse = False
        self.toolbarMin = None
        self.location = None


class LabelBox(ParentBox):
    def setup(self):
        self.theLabel = None
        self.theWidget = None
        return LabelBox


class ButtonBox(ParentBox):
    def setup(self):
        self.theWidget = None
        self.theButton = None
        return ButtonBox


class WidgetBox(ParentBox):
    def setup(self):
        self.theWidgets = []
        return WidgetBox


class ListBoxContainer(Frame, object):
    def __init__(self, parent, **opts):
        super(ListBoxContainer, self).__init__(parent)


class PagedWindow(Frame, object):
    def __init__(self, parent, title=None, **opts):
        buttonFont = opts.pop('buttonFont', None)
        titleFont = opts.pop('titleFont', None)
        super(PagedWindow, self).__init__(parent, **opts)
        self.config(width=300, height=400)
        self.frameStack = FrameStack(self)
        self.shouldShowPageNumber = True
        self.shouldShowTitle = True
        self.title = title
        self.navPos = 1
        self.titleLabel = Label(self, font=titleFont)
        self.prevButton = Button(self, text="PREVIOUS", command=self.showPrev,
                                 state="disabled", width=10, font=buttonFont)
        self.nextButton = Button(self, text="NEXT", command=self.showNext,
                                 state="disabled", width=10, font=buttonFont)
        self.prevButton.bind("<Control-Button-1>", self.showFirst)
        self.nextButton.bind("<Control-Button-1>", self.showLast)
        self.posLabel = Label(self, width=8, font=titleFont)



def setPrevButton(self, title):
    self.prevButton.config(text=title)


def setNextButton(self, title):
    self.nextButton.config(text=title)


if not isinstance(names[0], list):
    names = [names]
    if funcs is not None:
        funcs = [funcs]


def addButtons(self, names, funcs, row=None, column=0, colspan=0, rowspan=0, fill=False):
    if not isinstance(names, list):
        raise Exception(
            "Invalid button: " +
            names +
            ". It must be a list of buttons.")

    singleFunc = self._checkFunc(names, funcs)

    frame = self._makeWidgetBox()(self.getContainer())
    if not self.ttk:
        frame.config(background=self._getContainerBg())

    if not isinstance(names[0], list):
        names = [names]
        if funcs is not None:
            funcs = [funcs]
'''

# main toolbar function

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

# calendar, to calculate difference between two dates
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

# file search app
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


# all help functions


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

# timer
def timer():
    app.setStatusbar(time.strftime("%X"))


def showDate(btn):
    print(app.getDatePicker("dp"))
    print("The date:")




# checkout menu list manager

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

# notes app pages 1 and 2
def stack(btn):
    if btn == "NEXT":
        notesapp = app.getTextArea("Notes")
        with open('notes.txt', 'w') as f:
            for line in notesapp:
                f.write(line)
        app.nextFrame("Pages")

    elif btn == "PREV":
        notesapp2 = app.getTextArea("Notes2")
        with open('notes2.txt', 'w') as f:
            for line in notesapp2:
                f.write(line)
        app.prevFrame("Pages")


# GUI STARTS HERE


with gui("Business Manager", "640x480", log="trace") as app:
    app.setLogLevel("ERROR")
    app.showSplash("Welcome to the Business Manager")
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
        #login tab
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
        #notes tab
        with app.tab("Notes", bg="slategrey"):
            with app.frameStack("Pages", start=0):
                with app.frame():
                    notesread = open('notes.txt', 'r')
                    notesappread = notesread.read()
                    app.addTextArea("Notes", text=notesappread)
                with app.frame():
                    notesread2 = open('notes2.txt', 'r')
                    notesappread2 = notesread2.read()
                    app.addTextArea("Notes2", text=notesappread2)
            app.buttons(["PREV", "NEXT"], stack)
        #contacts tab
        with app.tab("Contacts", bg="slategrey", sticky="new"):
            with app.labelFrame("Contacts List:"):

                app.editMenu = True
                app.addDbOptionBox("table", DB_NAME, change=changeDb, right="demo")
                app.config(sticky="NEWS", stretch="both")
                app.table("table", DB_NAME, "tasks", kind='database', action=deleteRow, addRow=addRow, actionButton=[
                          "Delete"], showMenu=True, disabledEntries=[0], actionHeading='Delete?', sticky='ew')
                app.setOptionBox("table", "tasks", callFunction=False)
                app.refreshDbTable('table')
                app.button("Refresh Contacts", press, sticky="e")
        #calculator tab
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
        #registry tab
        with app.tab("Records", bg="slategrey", sticky="new"):
            with app.labelFrame("Records List:"):
                app.editMenu = True
                app.addDbOptionBox("table2", DB2_NAME, change=changeDb2, right="demo")
                app.config(sticky="NEWS", stretch="both")
                app.table("table2", DB2_NAME, "projects", kind='database', action=deleteRow2, addRow=addRow2, actionButton=[
                    "Delete2"], showMenu=True, disabledEntries=[0], actionHeading='Delete2?', sticky='ew')
                app.setOptionBox("table2", "tasks", callFunction=False)
                app.refreshDbTable("table2")

                app.button("Refresh Registry", press, sticky="e")
        #checkout tab
        with app.tab("Checkout", bg="slategrey", sticky="new"):
            app.listbox("List1", [], pos=(0, 0, 1, 4), bg="light grey")
            app.listbox("List2", [], pos=(0, 2, 1, 4), bg="light grey")
            app.button("<", move, pos=(0, 1))
            app.button("<<", move, pos=(3, 1))
            app.button(">>", move, pos=(2, 1))
            app.button(">", move, pos=(1, 1))
            app.button("Refresh Checkout", press, pos=(4, 0))
            app.button("CHECKOUT", checkout, pos=(4, 2))

    logout()
