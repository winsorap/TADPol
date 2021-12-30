import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox


# Standalone .py file to test functionality of the Delete Data frame

class DeleteData(tk.Tk):

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
                                       command=self.quit)
# command=lambda: controller.show_frame('MainMenu'))
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
                            print(selected_file + " has been removed!")
                            tk.messagebox.showinfo('TADPol', selected_file + ' was deleted successfully!')
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
    delete = DeleteData()
    delete.title("TADPol")
    delete.geometry('705x325+600+350')
    delete.resizable(0, 0)
    delete.mainloop()
