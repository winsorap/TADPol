import csv
import os
import tkinter as tk
from itertools import zip_longest
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.scrolledtext import ScrolledText

import function


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.title("TADPol")
        self.resizable(0, 0)

        self.frames = {}

        # For loop through each of the frames and their sizes
        for F, geometry in zip((MainMenu, ViewData, AnalyseData, DeleteData),
                               ('350x450+750+350', '845x660+490+250', '1007x785+440+150', '705x325+600+350')):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = (frame, geometry)
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame('MainMenu')

    def show_frame(self, page_name):
        frame, geometry = self.frames[page_name]
        self.update_idletasks()
        self.geometry(geometry)
        frame.tkraise()


class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self,
                         bg='blue',
                         fg='yellow',
                         font='bold',
                         relief=RAISED,
                         text='Hello! What would you like to do today?')
        label.pack(side=TOP,
                   fill=BOTH,
                   pady=4)

        upload_button = tk.Button(self,
                                  text='Upload Data',
                                  height=4,
                                  width=30,
                                  command=function.upload)
        upload_button.pack(side=TOP,
                           fill=X,
                           padx=4,
                           pady=4)

        view_button = tk.Button(self,
                                text='View Data',
                                height=4,
                                width=30,
                                command=lambda: controller.show_frame('ViewData'))
        view_button.pack(side=TOP,
                         fill=X,
                         padx=4,
                         pady=4)

        analyse_button = tk.Button(self,
                                   text='Analyse Data',
                                   height=4,
                                   width=30,
                                   command=lambda: controller.show_frame('AnalyseData'))
        analyse_button.pack(side=TOP,
                            fill=X,
                            padx=4,
                            pady=4)

        delete_button = tk.Button(self,
                                  text='Delete Data',
                                  height=4,
                                  width=30,
                                  command=lambda: controller.show_frame('DeleteData'))
        delete_button.pack(side=TOP,
                           fill=X,
                           padx=4,
                           pady=4)

        quit_button = tk.Button(self,
                                text='Quit',
                                height=4,
                                width=30,
                                command=label.quit)
        quit_button.pack(side=TOP,
                         fill=X,
                         padx=4,
                         pady=4)

        # Label which describes buttons at bottom of screen via mouse over functions
        self.status = tk.Label(self,
                               text="Ready",
                               bd=1,
                               relief=SUNKEN,
                               anchor=W)
        self.status.pack(side=BOTTOM,
                         fill=X,
                         padx=4,
                         pady=2)

        # Adds mouse over event functions to buttons
        upload_button.bind("<Enter>",
                           self.upload_button_enter)
        upload_button.bind("<Leave>",
                           self.leave)
        view_button.bind("<Enter>",
                         self.view_button_enter)
        view_button.bind("<Leave>",
                         self.leave)
        analyse_button.bind("<Enter>",
                            self.analyse_button_enter)
        analyse_button.bind("<Leave>",
                            self.leave)
        delete_button.bind("<Enter>",
                           self.delete_button_enter)
        delete_button.bind("<Leave>",
                           self.leave)
        quit_button.bind("<Enter>",
                         self.quit_button_enter)
        quit_button.bind("<Leave>",
                         self.leave)

    # Mouse over status bar functions
    def upload_button_enter(self, event):
        self.status.configure(text="Upload a CSV file to the database")

    def view_button_enter(self, event):
        self.status.configure(text="View data that has already been uploaded to the database")

    def analyse_button_enter(self, event):
        self.status.configure(text="Analyse data that has already been uploaded to the database")

    def delete_button_enter(self, event):
        self.status.configure(text="Delete data that has already been uploaded to the database")

    def quit_button_enter(self, event):
        self.status.configure(text="Exit the program")

    def leave(self, event):
        self.status.configure(text="Ready")


class ViewData(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Directory name of CSV files
        self.dir_name = r'Database'

        # Returns list of file names within Database folder
        self.file_list = os.listdir(self.dir_name)

        # Label which confirms the View Data menu
        self.label = Label(self,
                           width=75,
                           bg='blue',
                           fg='yellow',
                           font='bold',
                           relief=RAISED,
                           text='View Data')
        self.label.grid(row=0,
                        columnspan=6,
                        padx=10,
                        pady=5,
                        sticky=N)

        # Label which confirms the file name currently open
        self.data_label = tk.Label(self,
                                   width=50,
                                   bg='green',
                                   fg='black',
                                   font='bold',
                                   relief=RAISED,
                                   text='Select A File to Open:')
        self.data_label.grid(row=1,
                             columnspan=6,
                             pady=5)

        # Listbox widget of files in Database folder
        self.data_listbox = Listbox(self,
                                    height=7,
                                    width=65)

        # Scrollbar widget for data listbox
        self.scrollbar_lb = Scrollbar(self,
                                      orient=VERTICAL)

        self.data_listbox.config(yscrollcommand=self.scrollbar_lb.set)
        self.scrollbar_lb.config(command=self.data_listbox.yview)

        self.data_listbox.grid(row=2,
                               columnspan=6,
                               pady=5)

        self.scrollbar_lb.grid(row=2,
                               column=4,
                               sticky=N + S)

        # For loop to add file names to data listbox widget within above Directory
        # Sorted alphabetically
        for item in sorted(self.file_list, key=str.lower):
            if not item.endswith('.csv'):
                continue
            else:
                self.data_listbox.insert(END, item)

        self.open_file_button = Button(self,
                                       text='Open File',
                                       height=2,
                                       width=15,
                                       command=self.get_data)
        self.open_file_button.grid(row=3,
                                   columnspan=6,
                                   pady=5)

        # Read only textbox of data extracted from CSV file
        self.data_textbox = ScrolledText(self,
                                         height=20,
                                         width=100,
                                         wrap=WORD)

        self.data_textbox.grid(row=4,
                               columnspan=6,
                               sticky=NSEW,
                               padx=10,
                               pady=5)

        self.main_menu_button = Button(self,
                                       height=2,
                                       width=20,
                                       text='Back to Main Menu',
                                       command=lambda: [self.controller.show_frame('MainMenu'),
                                                        self.main_menu_return(event=None)])
        self.main_menu_button.grid(row=6,
                                   columnspan=6,
                                   pady=5)

        # Label which describes buttons at bottom of screen via mouse over functions
        self.status = tk.Label(self,
                               text='Ready',
                               bd=1,
                               relief=SUNKEN,
                               anchor=W)
        self.status.grid(row=7,
                         columnspan=6,
                         sticky=NSEW,
                         padx=4,
                         pady=2)

        # Adds mouse over event functions to buttons
        self.data_listbox.bind("<Enter>",
                               self.data_listbox_enter)
        self.data_listbox.bind("<Leave>",
                               self.leave)
        self.data_textbox.bind("<Enter>",
                               self.data_textbox_enter)
        self.data_textbox.bind("<Leave>",
                               self.leave)
        self.open_file_button.bind("<Enter>",
                                   self.open_file_enter)
        self.open_file_button.bind("<Leave>",
                                   self.leave)
        self.main_menu_button.bind("<Enter>",
                                   self.main_menu_button_enter)
        self.main_menu_button.bind("<Leave>",
                                   self.leave)

        # Allows for user selection via double click, as well as open file button
        self.data_listbox.bind('<Double-Button-1>', self.double_click)

    # Function to insert CSV data into data textbox widget
    def get_data(self):
        # Prevents exception if user does not select anything
        self.data = self.data_listbox.curselection()
        if self.data == ():
            print('No file has been selected!')
            messagebox.showinfo('TADPol', 'No file has been selected!')
            return

        # User selected file from listbox
        self.selected_file = self.data_listbox.get(self.data_listbox.curselection())

        # Loop through Database folder files
        for item in self.file_list:

            if item == self.selected_file:
                try:
                    # Checks if Database folder exists, and then changes CWD
                    if os.path.exists(self.dir_name):
                        os.chdir(self.dir_name)
                        print('Current working directory changed to: ' + self.dir_name)

                        # Empties textbox
                        self.data_textbox.config(state=NORMAL)
                        self.data_textbox.delete(1.0, END)

                        # Updates label confirming file currently open
                        self.data_label.config(text='File Currently Open: ' + self.selected_file)

                        # Opens file, loops through rows and adds data from row 'Text' to Data textbox
                        with open(self.selected_file, 'r', newline='') as file:
                            reader = csv.DictReader(file)
                            for row in reader:
                                text = row['Text']
                                print('Data displayed is:\n' + text)
                                self.data_textbox.insert(END, text + '\n' + '\n')

                        # Makes data textbox read only outside of loop
                        self.data_textbox.config(state=DISABLED)

                        # Changes CWD back to original
                        os.chdir(os.path.dirname(__file__))
                        print('Current working directory changed to: ' + __file__)

                        # Tells the user if the selected file has no data
                        if len(self.data_textbox.get(1.0, END)) <= 1:
                            print('No data exists in the selected file!')
                            messagebox.showinfo('TADPol', 'No data exists in the selected file!')
                except FileNotFoundError as e:
                    print(e)
                    messagebox.showerror('TADPol', 'Unable to find the selected file!')
                    os.chdir(os.path.dirname(__file__))
                    print('Current working directory changed to: ' + __file__)
                    self.data_label.config(text='Select A File to Open:')
                except KeyError as e:
                    print(e)
                    print('Unable to open - The CSV file has been saved in the wrong format!')
                    messagebox.showerror('TADPol', 'Unable to open - The CSV file has been saved in the wrong format!')
                    os.chdir(os.path.dirname(__file__))
                    print('Current working directory changed to: ' + __file__)

    # Allows for double click function to get data
    def double_click(self, event):
        self.get_data()

    # Clears existing data textbox upon returning to main menu
    def main_menu_return(self, event):
        self.data_textbox.config(state=NORMAL)
        self.data_textbox.delete(1.0, END)
        self.data_textbox.config(state=DISABLED)
        self.data_label.config(text='Select A File to Open:')

    # Mouse over functions
    def data_listbox_enter(self, event):
        self.status.configure(text="Select a CSV file to open")

    def data_textbox_enter(self, event):
        self.status.configure(text="Displays text of the selected CSV file")

    def open_file_enter(self, event):
        self.status.configure(text="Opens the selected CSV file")

    def main_menu_button_enter(self, event):
        self.status.configure(text="Return to the main menu")

    def clear_button_enter(self, event):
        self.status.configure(text="Clears selected data")

    def leave(self, event):
        self.status.configure(text="Ready")


class AnalyseData(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Directory name of CSV files
        self.dir_name = r'Database'

        # Returns list of file names within Database folder
        self.file_list = os.listdir(self.dir_name)

        # Lists to be populated by data selected by user
        self.list1 = []  # Red
        self.list2 = []  # Yellow
        self.list3 = []  # Green
        self.list4 = []  # Cyan
        self.list5 = []  # Orange

        # Frame title
        self.main_label = tk.Label(self,
                                   width=75,
                                   bg='blue',
                                   fg='yellow',
                                   font='bold',
                                   relief=RAISED,
                                   text='Analyse Data')
        self.main_label.grid(row=0,
                             columnspan=6,
                             padx=10,
                             pady=5,
                             sticky=N)

        # Asks user to open file, and updates with name of CSV file chosen
        self.data_label = tk.Label(self,
                                   width=50,
                                   bg='green',
                                   fg='black',
                                   font='bold',
                                   relief=RAISED,
                                   text='Select A File to Open:')
        self.data_label.grid(row=1,
                             columnspan=6,
                             pady=5)

        # Listbox widget of files in Database folder
        self.data_listbox = Listbox(self,
                                    height=7,
                                    width=46)

        # Scrollbar widget for data listbox
        self.scrollbar_lb = Scrollbar(self,
                                      orient=VERTICAL)

        self.data_listbox.config(yscrollcommand=self.scrollbar_lb.set)
        self.scrollbar_lb.config(command=self.data_listbox.yview)

        self.data_listbox.grid(row=2,
                               columnspan=6,
                               pady=5)

        self.scrollbar_lb.grid(row=2,
                               column=2,
                               sticky=N + S)

        # For loop to add CSV file names to data listbox widget within above Directory
        # Sorted alphabetically
        for item in sorted(self.file_list, key=str.lower):
            if not item.endswith('.csv'):
                continue
            else:
                self.data_listbox.insert(END, item)

        self.open_file_button = Button(self,
                                       text='Open File',
                                       height=2,
                                       width=15,
                                       command=self.get_data)
        self.open_file_button.grid(row=3,
                                   columnspan=6,
                                   pady=5)

        # Textbox of data extracted from CSV file
        self.data_textbox = ScrolledText(self,
                                         height=13,
                                         width=120,
                                         wrap=WORD)
        self.data_textbox.grid(row=4,
                               columnspan=6,
                               sticky=NSEW,
                               padx=10,
                               pady=5)

        # Buttons to code data highlighted by user
        self.code_button1 = tk.Button(self,
                                      width=12,
                                      height=1,
                                      text='Code in Box 1',
                                      command=self.code_data1)
        self.code_button1.grid(row=5,
                               column=0,
                               padx=10)

        self.code_button2 = tk.Button(self,
                                      width=12,
                                      height=1,
                                      text='Code in Box 2',
                                      command=self.code_data2)
        self.code_button2.grid(row=6,
                               column=0,
                               padx=10)

        self.code_button3 = tk.Button(self,
                                      width=12,
                                      height=1,
                                      text='Code in Box 3',
                                      command=self.code_data3)
        self.code_button3.grid(row=7,
                               column=0,
                               padx=10)

        self.code_button4 = tk.Button(self,
                                      width=12,
                                      height=1,
                                      text='Code in Box 4',
                                      command=self.code_data4)
        self.code_button4.grid(row=8,
                               column=0,
                               padx=10)

        self.code_button5 = tk.Button(self,
                                      width=12,
                                      height=1,
                                      text='Code in Box 5',
                                      command=self.code_data5)
        self.code_button5.grid(row=9,
                               column=0,
                               padx=10)

        # Data textbox widgets which consist of data highlighted by user
        self.data_tb1 = Text(self,
                             height=1,
                             width=65,
                             bg='red',
                             cursor='arrow',
                             state=DISABLED)
        self.data_tb1.grid(row=5,
                           column=1)

        self.data_tb2 = Text(self,
                             height=1,
                             width=65,
                             bg='yellow',
                             cursor='arrow',
                             state=DISABLED)
        self.data_tb2.grid(row=6,
                           column=1)

        self.data_tb3 = Text(self,
                             height=1,
                             width=65,
                             bg='green',
                             cursor='arrow',
                             state=DISABLED)
        self.data_tb3.grid(row=7,
                           column=1)

        self.data_tb4 = Text(self,
                             height=1,
                             width=65,
                             bg='cyan',
                             cursor='arrow',
                             state=DISABLED)
        self.data_tb4.grid(row=8,
                           column=1)

        self.data_tb5 = Text(self,
                             height=1,
                             width=65,
                             bg='orange',
                             cursor='arrow',
                             state=DISABLED)
        self.data_tb5.grid(row=9,
                           column=1)

        # Code textbox widgets to allow users to input code for TA
        self.code_tb1 = Text(self,
                             height=1,
                             width=15)
        self.code_tb1.grid(row=5,
                           column=3)

        self.code_tb2 = Text(self,
                             height=1,
                             width=15)
        self.code_tb2.grid(row=6,
                           column=3)

        self.code_tb3 = Text(self,
                             height=1,
                             width=15)
        self.code_tb3.grid(row=7,
                           column=3)

        self.code_tb4 = Text(self,
                             height=1,
                             width=15)
        self.code_tb4.grid(row=8,
                           column=3)

        self.code_tb5 = Text(self,
                             height=1,
                             width=15)
        self.code_tb5.grid(row=9,
                           column=3)

        # Clear buttons to clear data and code textbox widgets
        self.clear_button1 = tk.Button(self,
                                       height=1,
                                       width=5,
                                       text='Clear',
                                       command=self.clear_tb1)
        self.clear_button1.grid(row=5,
                                column=4,
                                padx=10,
                                pady=5)

        self.clear_button2 = tk.Button(self,
                                       height=1,
                                       width=5,
                                       text='Clear',
                                       command=self.clear_tb2)
        self.clear_button2.grid(row=6,
                                column=4,
                                pady=5)

        self.clear_button3 = tk.Button(self,
                                       height=1,
                                       width=5,
                                       text='Clear',
                                       command=self.clear_tb3)
        self.clear_button3.grid(row=7,
                                column=4,
                                pady=5)

        self.clear_button4 = tk.Button(self,
                                       height=1,
                                       width=5,
                                       text='Clear',
                                       command=self.clear_tb4)
        self.clear_button4.grid(row=8,
                                column=4,
                                pady=5)

        self.clear_button5 = tk.Button(self,
                                       height=1,
                                       width=5,
                                       text='Clear',
                                       command=self.clear_tb5)
        self.clear_button5.grid(row=9,
                                column=4,
                                pady=5)

        # Save button to save coded data to a CSV file
        self.save_button = tk.Button(self,
                                     width=30,
                                     text='Save All Data',
                                     height=2,
                                     command=self.save_data)
        self.save_button.grid(row=11,
                              columnspan=6,
                              padx=5,
                              pady=5)

        # Clears all coded data
        self.clear_all_button = tk.Button(self,
                                          width=20,
                                          text='Clear All Codes',
                                          height=2,
                                          command=self.clear_all)
        self.clear_all_button.grid(row=7,
                                   column=5)

        # Back button to return to main menu
        self.main_menu_button = Button(self,
                                       width=30,
                                       text='Back to Main Menu',
                                       height=2,
                                       command=self.main_menu_prompt)
        # lambda: controller.show_frame('MainMenu'))
        self.main_menu_button.grid(row=12,
                                   columnspan=6,
                                   pady=5)

        # Label which describes buttons at bottom of screen via mouse over functions
        self.status = tk.Label(self,
                               text='Ready',
                               bd=1,
                               relief=SUNKEN,
                               anchor=W)
        self.status.grid(row=13,
                         columnspan=6,
                         sticky=NSEW,
                         padx=4,
                         pady=5)

        # Adds mouse over event functions to buttons
        self.data_listbox.bind("<Enter>",
                               self.data_listbox_enter)
        self.data_listbox.bind("<Leave>",
                               self.leave)
        self.data_textbox.bind("<Enter>",
                               self.data_textbox_enter)
        self.data_textbox.bind("<Leave>",
                               self.leave)
        self.open_file_button.bind("<Enter>",
                                   self.open_file_enter)
        self.open_file_button.bind("<Leave>",
                                   self.leave)
        self.main_menu_button.bind("<Enter>",
                                   self.main_menu_button_enter)
        self.main_menu_button.bind("<Leave>",
                                   self.leave)
        self.save_button.bind("<Enter>",
                              self.save_data_enter)
        self.save_button.bind("<Leave>",
                              self.leave)
        self.code_button1.bind("<Enter>",
                               self.code_button_enter)
        self.code_button1.bind("<Leave>",
                               self.leave)
        self.code_button2.bind("<Enter>",
                               self.code_button_enter)
        self.code_button2.bind("<Leave>",
                               self.leave)
        self.code_button3.bind("<Enter>",
                               self.code_button_enter)
        self.code_button3.bind("<Leave>",
                               self.leave)
        self.code_button4.bind("<Enter>",
                               self.code_button_enter)
        self.code_button4.bind("<Leave>",
                               self.leave)
        self.code_button5.bind("<Enter>",
                               self.code_button_enter)
        self.code_button5.bind("<Leave>",
                               self.leave)
        self.data_tb1.bind("<Enter>",
                           self.data_tb_enter)
        self.data_tb1.bind("<Leave>",
                           self.leave)
        self.data_tb2.bind("<Enter>",
                           self.data_tb_enter)
        self.data_tb2.bind("<Leave>",
                           self.leave)
        self.data_tb3.bind("<Enter>",
                           self.data_tb_enter)
        self.data_tb3.bind("<Leave>",
                           self.leave)
        self.data_tb4.bind("<Enter>",
                           self.data_tb_enter)
        self.data_tb4.bind("<Leave>",
                           self.leave)
        self.data_tb5.bind("<Enter>",
                           self.data_tb_enter)
        self.data_tb5.bind("<Leave>",
                           self.leave)
        self.code_tb1.bind("<Enter>",
                           self.code_tb_enter)
        self.code_tb1.bind("<Leave>",
                           self.leave)
        self.code_tb2.bind("<Enter>",
                           self.code_tb_enter)
        self.code_tb2.bind("<Leave>",
                           self.leave)
        self.code_tb3.bind("<Enter>",
                           self.code_tb_enter)
        self.code_tb3.bind("<Leave>",
                           self.leave)
        self.code_tb4.bind("<Enter>",
                           self.code_tb_enter)
        self.code_tb4.bind("<Leave>",
                           self.leave)
        self.code_tb5.bind("<Enter>",
                           self.code_tb_enter)
        self.code_tb5.bind("<Leave>",
                           self.leave)
        self.clear_all_button.bind("<Enter>",
                                   self.clear_all_button_enter)
        self.clear_all_button.bind("<Leave>",
                                   self.leave)
        self.clear_button1.bind("<Enter>",
                                self.clear_button_enter)
        self.clear_button1.bind("<Leave>",
                                self.leave)
        self.clear_button2.bind("<Enter>",
                                self.clear_button_enter)
        self.clear_button2.bind("<Leave>",
                                self.leave)
        self.clear_button3.bind("<Enter>",
                                self.clear_button_enter)
        self.clear_button3.bind("<Leave>",
                                self.leave)
        self.clear_button4.bind("<Enter>",
                                self.clear_button_enter)
        self.clear_button4.bind("<Leave>",
                                self.leave)
        self.clear_button5.bind("<Enter>",
                                self.clear_button_enter)
        self.clear_button5.bind("<Leave>",
                                self.leave)

        # Allows for file selection via user double click
        self.data_listbox.bind('<Double-Button-1>', self.double_click)

    # Function to insert CSV data into data textbox widget
    def get_data(self):
        # Prevents exception if user does not select anything
        self.data = self.data_listbox.curselection()
        if self.data == ():
            print('No file has been selected!')
            messagebox.showinfo('TADPol', 'No file has been selected!')
            return

        # User selected file from listbox
        self.selected_file = self.data_listbox.get(self.data_listbox.curselection())

        # Loop through Database folder files
        for item in self.file_list:
            if item == self.selected_file:
                try:
                    # Checks if Database folder exists, and then changes CWD
                    if os.path.exists(self.dir_name):
                        os.chdir(self.dir_name)
                        print('Current working directory changed to: ' + self.dir_name)

                        # Empties textbox
                        self.data_textbox.config(state=NORMAL)
                        self.data_textbox.delete(1.0, END)

                        # Updates label confirming file currently open
                        self.data_label.config(text='File Currently Open: ' + self.selected_file)

                        # Opens file, loops through rows and adds data from row 'Text' to Data textbox
                        with open(item, 'r', newline='') as file:
                            reader = csv.DictReader(file)
                            for row in reader:
                                text = row['Text']
                                self.data_textbox.insert(END, text + '\n' + '\n')
                                print('Data displayed is:\n' + text)

                            # Makes data textbox read only outside of loop
                            self.data_textbox.config(state=DISABLED)

                            # Adds prompt to back button, to avoid loss of work
                            self.main_menu_button.config(command=self.main_menu_prompt)

                            # Changes CWD back to original
                            os.chdir(os.path.dirname(__file__))
                            print('Current working directory changed to: ' + __file__)

                            # Tells the user if the selected file has no data
                            if len(self.data_textbox.get(1.0, END)) <= 1:
                                print('No data exists in the selected file!')
                                messagebox.showinfo('TADPol', 'No data exists in the selected file!')
                                return
                except FileNotFoundError as e:
                    print(e)
                    messagebox.showerror('TADPol', 'No data was found in the selected file!')
                    os.chdir(os.path.dirname(__file__))
                    print('Current working directory changed to: ' + __file__)
                    self.data_label.config(text='Select A File to Open:')
                except KeyError as e:
                    print(e)
                    print('Unable to open - The CSV file has been saved in the wrong format!')
                    messagebox.showerror('TADPol', 'No data exists in the selected file!')
                    os.chdir(os.path.dirname(__file__))
                    print('Current working directory changed to: ' + __file__)

    # Allows for double click function to get data
    def double_click(self, event):
        self.get_data()

    # Functions to input selected text into empty data textbox widgets and lists
    def code_data1(self):
        self.data_tb1.config(state=NORMAL)
        ranges = self.data_textbox.tag_ranges(tk.SEL)
        if ranges:
            print('Selected Text is %r' % self.data_textbox.get(*ranges))
            self.data_tb1.insert(END,
                                 self.data_textbox.get(*ranges) + ', ')
            self.list1.append(self.data_textbox.get(*ranges))
        else:
            messagebox.showinfo('TADPol',
                                'No text has been selected!')
            print('No text has been selected!')
        self.data_tb1.config(state=DISABLED)

    def code_data2(self):
        self.data_tb2.config(state=NORMAL)
        ranges = self.data_textbox.tag_ranges(tk.SEL)
        if ranges:
            print('Selected Text is %r' % self.data_textbox.get(*ranges))
            self.data_tb2.insert(END,
                                 self.data_textbox.get(*ranges) + ', ')
            self.list2.append(self.data_textbox.get(*ranges))
        else:
            messagebox.showinfo('TADPol',
                                'No text has been selected!')
            print('No text has been selected!')
        self.data_tb2.config(state=DISABLED)

    def code_data3(self):
        self.data_tb3.config(state=NORMAL)
        ranges = self.data_textbox.tag_ranges(tk.SEL)
        if ranges:
            print('Selected Text is %r' % self.data_textbox.get(*ranges))
            self.data_tb3.insert(END,
                                 self.data_textbox.get(*ranges) + ', ')
            self.list3.append(self.data_textbox.get(*ranges))
        else:
            messagebox.showinfo('TADPol',
                                'No text has been selected!')
            print('No text has been selected!')
        self.data_tb3.config(state=DISABLED)

    def code_data4(self):
        self.data_tb4.config(state=NORMAL)
        ranges = self.data_textbox.tag_ranges(tk.SEL)
        if ranges:
            print('Selected Text is %r' % self.data_textbox.get(*ranges))
            self.data_tb4.insert(END,
                                 self.data_textbox.get(*ranges) + ', ')
            self.list4.append(self.data_textbox.get(*ranges))
        else:
            messagebox.showinfo('TADPol',
                                'No text has been selected!')
            print('No text has been selected!')
        self.data_tb4.config(state=DISABLED)

    def code_data5(self):
        self.data_tb5.config(state=NORMAL)
        ranges = self.data_textbox.tag_ranges(tk.SEL)
        if ranges:
            print('Selected Text is %r' % self.data_textbox.get(*ranges))
            self.data_tb5.insert(END,
                                 self.data_textbox.get(*ranges) + ', ')
            self.list5.append(self.data_textbox.get(*ranges))
        else:
            messagebox.showinfo('TADPol',
                                'No text has been selected!')
            print('No text has been selected!')

    # Clears selected data and code textbox, as well as list
    def clear_tb1(self):
        self.data_tb1.config(state=NORMAL)
        self.data_tb1.delete('1.0', END)
        self.data_tb1.config(state=DISABLED)
        self.code_tb1.delete('1.0', END)
        self.list1.clear()

    def clear_tb2(self):
        self.data_tb2.config(state=NORMAL)
        self.data_tb2.delete('1.0', END)
        self.data_tb2.config(state=DISABLED)
        self.code_tb2.delete('1.0', END)
        self.list2.clear()

    def clear_tb3(self):
        self.data_tb3.config(state=NORMAL)
        self.data_tb3.delete('1.0', END)
        self.data_tb3.config(state=DISABLED)
        self.code_tb3.delete('1.0', END)
        self.list3.clear()

    def clear_tb4(self):
        self.data_tb4.config(state=NORMAL)
        self.data_tb4.delete('1.0', END)
        self.data_tb4.config(state=DISABLED)
        self.code_tb4.delete('1.0', END)
        self.list4.clear()

    def clear_tb5(self):
        self.data_tb5.config(state=NORMAL)
        self.data_tb5.delete('1.0', END)
        self.data_tb5.config(state=DISABLED)
        self.code_tb5.delete('1.0', END)
        self.list5.clear()

    def clear_all(self):
        self.question = messagebox.askyesno('TADPol',
                                            'Are you sure that you want to clear all boxes without saving first?')
        if self.question is True:
            self.clear_tb1()
            self.clear_tb2()
            self.clear_tb3()
            self.clear_tb4()
            self.clear_tb5()
        else:
            return

    # Saves coded data as a CSV file in a location selected by the user
    def save_data(self):
        self.save_file = filedialog.asksaveasfilename(title='Save a CSV file',
                                                      defaultextension='.csv',
                                                      filetypes=[('CSV file', '.csv')])
        if not self.save_file:
            return
        try:
            with open(self.save_file, 'w', newline='') as csv_file:
                # Obtains strings from code textbox widgets
                # end-1c removes the auto new line at the end of the strings
                column1 = str(self.code_tb1.get('1.0', 'end-1c'))
                column2 = str(self.code_tb2.get('1.0', 'end-1c'))
                column3 = str(self.code_tb3.get('1.0', 'end-1c'))
                column4 = str(self.code_tb4.get('1.0', 'end-1c'))
                column5 = str(self.code_tb5.get('1.0', 'end-1c'))

                data_lists = [self.list1,
                              self.list2,
                              self.list3,
                              self.list4,
                              self.list5]
                export_data = zip_longest(*data_lists)

                writer = csv.writer(csv_file)
                writer.writerow((column1,
                                 column2,
                                 column3,
                                 column4,
                                 column5))
                writer.writerows(export_data)

                messagebox.showinfo('TADPol', 'File saved successfully!')
        except PermissionError as e:
            print(e)
            messagebox.showerror('TADPol', 'Error: File name is already open! Please choose a different '
                                           'location or file name.')

    def main_menu_prompt(self):
        self.question = messagebox.askyesno('TADPol',
                                            'Are you sure that you wish to return to the main menu '
                                            + ' without saving first?')
        if self.question is True:
            self.data_textbox.config(state=NORMAL)
            self.data_textbox.delete(1.0, END)
            self.data_textbox.config(state=DISABLED)
            self.clear_tb1()
            self.clear_tb2()
            self.clear_tb3()
            self.clear_tb4()
            self.clear_tb5()
            self.data_label.config(text='Select A File to Open:')
            self.controller.show_frame('MainMenu')
        else:
            return

    # Mouse over functions for status bar
    def data_listbox_enter(self, event):
        self.status.configure(text="Select a CSV file to open")

    def data_textbox_enter(self, event):
        self.status.configure(text="Displays the text of the selected CSV file")

    def open_file_enter(self, event):
        self.status.configure(text="Opens the selected CSV file")

    def save_data_enter(self, event):
        self.status.configure(text="Saves coded data into a new CSV file")

    def main_menu_button_enter(self, event):
        self.status.configure(text="Return to the main menu")

    def clear_button_enter(self, event):
        self.status.configure(text="Clears this row of coded data")

    def code_button_enter(self, event):
        self.status.configure(text="Adds highlighted text into this coloured box")

    def data_tb_enter(self, event):
        self.status.configure(text="Previously coded data is contained in this textbox")

    def code_tb_enter(self, event):
        self.status.configure(text="Enter your chosen code in this textbox for the highlighted data")

    def clear_all_button_enter(self, event):
        self.status.configure(text="Clears all rows of selected coded data")

    def leave(self, event):
        self.status.configure(text="Ready")


class DeleteData(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Directory name of CSV files
        self.dir_name = r'Database'

        # Returns list of file names within Database folder
        self.file_list = os.listdir(self.dir_name)

        # Label which confirms the View Data menu
        self.label = Label(self,
                           width=75,
                           bg='blue',
                           fg='yellow',
                           font='bold',
                           relief=RAISED,
                           text='Delete Data')
        self.label.grid(row=0,
                        columnspan=6,
                        padx=10,
                        pady=5,
                        sticky=N)

        # Label which confirms the file name currently open
        self.data_label = tk.Label(self,
                                   width=50,
                                   bg='green',
                                   fg='black',
                                   font='bold',
                                   relief=RAISED,
                                   text='Select A File to Delete:')
        self.data_label.grid(row=1,
                             columnspan=6,
                             pady=5)

        # Listbox widget of files in Database folder
        self.data_listbox = Listbox(self,
                                    height=7,
                                    width=54)

        # Scrollbar widget for data listbox
        self.scrollbar_lb = Scrollbar(self,
                                      orient=VERTICAL)

        self.data_listbox.config(yscrollcommand=self.scrollbar_lb.set)
        self.scrollbar_lb.config(command=self.data_listbox.yview)

        self.data_listbox.grid(row=2,
                               columnspan=6,
                               pady=5)

        self.scrollbar_lb.grid(row=2,
                               column=4,
                               sticky=N + S)

        # For loop to add file names to data listbox widget within above Directory
        # Sorted alphabetically
        for item in sorted(self.file_list, key=str.lower):
            if not item.endswith('.csv'):
                continue
            else:
                self.data_listbox.insert(END, item)

        self.delete_file_button = Button(self,
                                         text='Delete File',
                                         height=2,
                                         width=15,
                                         command=self.delete_data)
        self.delete_file_button.grid(row=3,
                                     columnspan=6,
                                     pady=5)

        self.main_menu_button = Button(self,
                                       height=2,
                                       width=20,
                                       text='Back to Main Menu',
                                       command=lambda: controller.show_frame('MainMenu'))

        self.main_menu_button.grid(row=6,
                                   columnspan=6,
                                   pady=5)

        # Label which describes buttons at bottom of screen via mouse over functions
        self.status = tk.Label(self,
                               text='Ready',
                               bd=1,
                               relief=SUNKEN,
                               anchor=W)
        self.status.grid(row=7,
                         columnspan=6,
                         sticky=NSEW,
                         padx=4,
                         pady=2)

        # Adds mouse over event functions to buttons
        self.data_listbox.bind("<Enter>",
                               self.data_listbox_enter)
        self.data_listbox.bind("<Leave>",
                               self.leave)
        self.delete_file_button.bind("<Enter>",
                                     self.delete_file_enter)
        self.delete_file_button.bind("<Leave>",
                                     self.leave)
        self.main_menu_button.bind("<Enter>",
                                   self.main_menu_button_enter)
        self.main_menu_button.bind("<Leave>",
                                   self.leave)

        # Allows for user selection via double click, as well as open file button
        self.data_listbox.bind('<Double-Button-1>', self.double_click)

    # Function to insert CSV data into data textbox widget
    def delete_data(self):
        # Prevents exception if user does not select anything
        data = self.data_listbox.curselection()
        if data == ():
            print('No file has been selected!')
            messagebox.showinfo('TADPol', 'No file has been selected!')
            return

        # User selected file from listbox
        selected_file = self.data_listbox.get(self.data_listbox.curselection())

        # Loop through Database folder files
        for item in self.file_list:
            if item == selected_file:
                try:
                    # Checks if Database folder exists, and then changes CWD
                    if os.path.exists(self.dir_name):
                        os.chdir(self.dir_name)
                        print('Current working directory changed to: ' + self.dir_name)
                        question = messagebox.askyesno('TADPol',
                                                       'Are you sure that you wish to permanently delete ' +
                                                       selected_file + '? This action cannot be undone.')
                        if question is True:
                            os.remove(selected_file)
                            self.data_listbox.delete(tk.ANCHOR)
                            os.chdir(os.path.dirname(__file__))
                            print('Current working directory changed to: ' + __file__)
                        else:
                            # Changes CWD back to original
                            os.chdir(os.path.dirname(__file__))
                            print('Current working directory changed to: ' + __file__)
                            return
                except FileNotFoundError as e:
                    print(e)
                    messagebox.showerror('TADPol', 'Unable to find the selected file!')
                    os.chdir(os.path.dirname(__file__))
                    print('Current working directory changed to: ' + __file__)
                except PermissionError as e:
                    print(e)
                    messagebox.showerror('TADPol', 'Unable to delete - Please close the selected file first!')
                    os.chdir(os.path.dirname(__file__))
                    print('Current working directory changed to: ' + __file__)
                else:
                    print(selected_file + " has been removed!")
                    messagebox.showinfo('TADPol', selected_file + ' was deleted successfully!')

    # Allows for double click function to delete data
    def double_click(self, event):
        self.delete_data()

    # Mouse over functions
    def data_listbox_enter(self, event):
        self.status.configure(text="Select a CSV file to delete")

    def delete_file_enter(self, event):
        self.status.configure(text="Deletes the selected CSV file")

    def main_menu_button_enter(self, event):
        self.status.configure(text="Return to the main menu")

    def leave(self, event):
        self.status.configure(text="Ready")


# Driver code
if __name__ == '__main__':
    app = App()
    app.mainloop()
