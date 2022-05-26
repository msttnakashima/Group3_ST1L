#reference for tkinter: https://pythonexamples.org/python-tkinter-login-form/

#import tkinter
from tkinter import *       
from functools import partial
from tkinter import font as tkfont      # formatting purposes

#reference for mysql connector: https://www.youtube.com/watch?v=oDR7k66x-AU&t=427s&ab_channel=DiscoverPython

# install mysql 
import mysql.connector as mariadb

#create mysql connection 
dbConnect = mariadb.connect(user ="test", password='cmsc127', host ='localhost', port ='3306')
dbCursor = dbConnect.cursor()

# show databases then use CMSC127Project
dbCursor.execute("SHOW DATABASES")

#CHECKING PURPOSES ONLY: prints all databases in MariaDB if it has connected successfully (delete / comment after)
for x in dbCursor:
    print(x)

# use 'cmsc127project' database
dbCursor.execute("USE cmsc127project")

# Code reference for changing between frames:
# https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
class SampleApp(Tk):
    
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family="Arial", size=18, weight="bold")   # formatting purposes (set font properties)
        self.subtitle_font = tkfont.Font(family = "Arial", size = 12, weight = "bold")

        # pages / frames are in a stack (frames that need to be visible will be raised above other frames)
        # NOTE: self parameter is always needed in the parameter of functions under SampleApp class 
            # self - refers to the current instance of the class & used to access variables that belongs to the class
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # NOTE: always add newly created pages in the parameters
        for F in (LandingPage, TasksMainPage, AboutPage, AllTasksPage, AllCategoriesPage, AddCategoryPage):
            page_name = F.__name__                              # get page name
            frame = F(parent=container, controller=self)        # frame
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LandingPage")                          # start with landing page

    # show_frame - function to show a frame for a specific page 
    def show_frame(self, page_name):
        frame = self.frames[page_name]      # frame = frame for the specific page 
        frame.tkraise()                     # raise frame above others 

    # addCategory - function to add category to the database (accessible by connector.addCategory())
    def addCategory(self, name, dbCursor): 
        # select statement to get the maximum value of categoryid + 1 (for the id of the to-be-added category)
        dbCursor.execute("SELECT MAX(categoryid)+1 FROM category;")     
        for id in dbCursor:     # loop through the result of the select statement 
            tempId = id         # store the value of MAX(categoryid) + 1 to tempId; tempId = (<int>,)

        #insert statement 
        insertCat = ("INSERT INTO category (categoryid, categoryname) VALUES (%s, %s);")
        args = tempId[0], name                  # parameters for %s (tempId[0] will only get the int)
        dbCursor.execute(insertCat, args)       # execute insert statement
        dbConnect.commit()                      # commit changes (insert statement)
        
        print("Added", name, "successfully!")

# LandingPage - landing page for the application (first window)
class LandingPage(Frame): 

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # label for the page 
        label = Label(self, text="Task Management App", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        # button to go to 'view all tasks' page (includes viewing, searching, creating, editing, deleting, and marking tasks as done)
        button1 = Button(self, text="Tasks and Categories",
            command=lambda: controller.show_frame("TasksMainPage"))      

        # button to go to 'about the creators' page (includes members and desc of app) 
        button2 = Button(self, text="About",
            command=lambda: controller.show_frame("AboutPage"))    

        # button to exit the program 
        button3 = Button(self, text="Exit",
            command=lambda: controller.destroy())                   

        # formatting purposes (position, width, padding)
        button1.pack(side = "top", fill = "x", pady = 20)
        button2.pack(side = "top", fill = "x", pady = 20)
        button3.pack(side = "top", fill = "x", pady = 20)

# TasksMainPage - 'tasks' page
class TasksMainPage(Frame): 

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        frame = Frame(self, parent)

        # button to view all tasks
        allTasksBtn = Button(self, text="View all tasks", width=48, command=lambda: controller.show_frame("AllTasksPage"))
        allTasksBtn.pack(side = 'top', fill = 'x', pady = 60)  

        # button to view all categories
        allCategoriesBtn = Button(self, text="View all categories", width=48, command=lambda: controller.show_frame("AllCategoriesPage"))
        allCategoriesBtn.pack(side = 'top', fill = 'x', pady = 60)  

        # button to go back to the main page 
        menubutton = Button(self, text = "Go back to the main page", command=lambda: controller.show_frame("LandingPage"))
        menubutton.pack(side = 'top', fill = 'x', pady = 60)

        frame.pack()

#AllTasks - view all tasks page
class AllTasksPage(Frame): 
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        frame = Frame(self, parent)

        # box to list all tasks
        self.listbox_tasks = Listbox(frame, height=15, width=70)
        self.listbox_tasks.pack(side=LEFT)

        # scrollbar for tasks list 
        scrollbar_tasks = Scrollbar(frame)
        scrollbar_tasks.pack(side=RIGHT, fill=Y)

        # vertical scrollbar properties
        self.listbox_tasks.config(yscrollcommand=scrollbar_tasks.set)
        scrollbar_tasks.config(command=self.listbox_tasks.yview)

        # button to customize view of tasks by day
        viewTasksByBtn = Button(self, text="Sort by day", width=48)
        viewTasksByBtn.pack(side = 'bottom', fill = 'x')

        # button to customize view of tasks by month
        viewTasksByBtn = Button(self, text="Sort by month", width=48)
        viewTasksByBtn.pack(side = 'bottom', fill = 'x')

        #button to add a task to a category
        addTaskCategoryBtn = Button(self, text = "Add a task to a category", width=48, )
        addTaskCategoryBtn.pack(side = 'bottom', fill = 'x')

        #button to search for a task
        searchTaskBtn = Button(self, text = "Search for a task", width=48)
        searchTaskBtn.pack(side = 'bottom', fill = 'x')

        #button to mark a task as done 
        markDoneBtn = Button(self, text = "Mark as done", width=48)
        markDoneBtn.pack(side = 'bottom', fill = 'x')

        # button to edit a task 
        editTaskBtn = Button(self, text = "Edit a task", width=48)
        editTaskBtn.pack(side = 'bottom', fill = 'x')

        # button to delete a task 
        deleteTaskBtn = Button(self, text="Delete task", width=48)
        deleteTaskBtn.pack(side = 'bottom', fill = 'x')

        # button to add a task
        addTaskBtn = Button(self, text="Add task", width=48)
        addTaskBtn.pack(side = 'bottom', fill = 'x') 

        menubutton = Button(self, text = "Go back to the previous page", command=lambda: controller.show_frame("TasksMainPage"))
        menubutton.pack(anchor = NE)

        frame.pack()

        self.after(1000, self.taskUpdate)   # for every 1000 milliseconds, update the page

    # update page (update list of tasks)
    def taskUpdate(self):
        # select all tasks
        dbCursor.execute("SELECT CONCAT(DATE_FORMAT(duedate, '%M-%d-%Y'), ': ', tasktitle, ' - ', description, ' | Status: ', status) FROM task;")
        self.listbox_tasks.delete(0, END)                   # remove data in the listbox display               
        for task in dbCursor:                               # iterate over the results of the select statement
            for j in range(len(task)):                      
                self.listbox_tasks.insert(END, task[j])     # insert categories in the listbox display
        self.after(1000, self.taskUpdate)                   # for every 1000 milliseconds, update the page

#AllCategoriesPage - view all categories page
class AllCategoriesPage(Frame): 
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        frame = Frame(self, parent)

        # box to list all categories
        self.listbox_category = Listbox(frame, height=15, width=70)
        self.listbox_category.pack(side=LEFT)

        # scrollbar for categories list 
        scrollbar_category = Scrollbar(frame)
        scrollbar_category.pack(side=RIGHT, fill=Y)

        # vertical scrollbar properties
        self.listbox_category.config(yscrollcommand=scrollbar_category.set)
        scrollbar_category.config(command=self.listbox_category.yview)

        #button to search for a category
        searchCategoryBtn = Button(self, text = "Search for a category", width=48)
        searchCategoryBtn.pack(side = 'bottom', fill = 'x')

        # button to delete a category 
        deleteCategoryBtn = Button(self, text="Delete category", width=48)
        deleteCategoryBtn.pack(side = 'bottom', fill = 'x')

        # button to edit a category
        editCategoryBtn = Button(self, text = "Edit a category", width=48)
        editCategoryBtn.pack(side = 'bottom', fill = 'x')

        # button to add a category
        addCategoryBtn = Button(self, text="Add a category", width=48, command=lambda: controller.show_frame("AddCategoryPage"))
        addCategoryBtn.pack(side = 'bottom', fill = 'x' ) 

        # button to customize view of tasks by category
        viewTasksByBtn = Button(self, text="View tasks by category", width=48)
        viewTasksByBtn.pack(side = 'bottom', fill = 'x')    

        # button to go to the prev page
        menubutton = Button(self, text = "Go back to the previous page", command=lambda: controller.show_frame("TasksMainPage"))
        menubutton.pack(anchor = NE)

        frame.pack()

        self.after(1000, self.categoryUpdate)   # for every 1000 milliseconds, update the page

    # update page (update list of categories)
    def categoryUpdate(self):
        dbCursor.execute("SELECT categoryname FROM category;")      # select all categories
        self.listbox_category.delete(0, END)                        # remove data in the listbox display
        for category in dbCursor:                                   # iterate over the results of the select statement 
            for j in range(len(category)):
                self.listbox_category.insert(END, category[j])      # insert categories in the listbox display
        self.after(1000, self.categoryUpdate)                               # for every 1000 milliseconds, update the page

#AddCategoryPage - page to add a category 
class AddCategoryPage(Frame): 
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # button to go to the prev page
        menubutton = Button(self, text = "Go back to the previous page", command=lambda: controller.show_frame("AllCategoriesPage"))
        menubutton.pack(anchor = NE)

        label = Label(self, text="Add a category", font=controller.title_font)
        label.pack(side="top", pady=10)

        label1 = Label(self, text="Category name")
        label1.pack()
        catName = Entry(self)
        catName.pack()

        buttonAddCat = Button(self, text="Add category", command=lambda: controller.addCategory(catName.get(), dbCursor))
        buttonAddCat.pack()

# AboutPage - about page 
class AboutPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text = 'CMSC 127 project\n\nJamie Mari O. Ciron\nRalph Jason D. Corrales\nAriel Raphael F. Magno\nMarie Sophia Therese T. Nakashima')

        # button to go to the main page
        label.pack(side = "top", fill = "x", pady = 10)
        button = Button(self, text = "Go to the main page",
        command=lambda: controller.show_frame("LandingPage"))
        button.pack()

# mainProgram - starts the application
def mainProgram(): 
    if __name__ == "__main__":
        root = SampleApp()
        root.title("127 Task management app")
        root.mainloop()

mainProgram()
