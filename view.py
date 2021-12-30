import csv
import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText


# Standalone .py file to test functionality of the View Data frame

class ViewData(tk.Tk):

    def __init__(self):
        super().__init__()

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
                                       command=self.quit)
# command=lambda: [self.controller.show_frame('MainMenu'),
#                  self.main_menu_return(event=None)])
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

    # Refreshes data - Only called if delete function is used
    def refresh_data(self):
        self.data_textbox.delete(1.0, END)
        self.get_data()

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


# Driver code
if __name__ == '__main__':
    view = ViewData()
    view.title("TADPol")
    view.geometry('845x660+490+250')
    view.resizable(0, 0)
    view.mainloop()
