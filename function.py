import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# Static function to upload CSV files to database


def upload():
    selected_file = filedialog.askopenfilename(title="Select a CSV file",
                                               filetypes=[("CSV file", "*.csv*")])
    if not selected_file:
        print('User cancelled file upload.')
        return

    # Returns file name as a string from user selected file path
    file_name = os.path.basename(selected_file)

    # Destination of selected file
    dst = r'Database'
    database = os.listdir(dst)

    try:
        # For loop to check if selected file name already exists in the database folder
        # Prevents accidental overwriting of files
        for item in database:
            if item == file_name:
                tk.messagebox.showerror('TADPol', 'Error - This file name already exists on the database!\n'
                                                  'Please rename the file and try again.')
                return

        # Copies selected file to database
        # Executes only if selected file name is not already in the database folder
        shutil.copy(selected_file, dst)
        print(selected_file + " has been uploaded!")
        tk.messagebox.showinfo('TADPol', 'File uploaded successfully!')
    except shutil.SameFileError as e:
        print(e)
        tk.messagebox.showerror('TADPol', 'Error - You cannot select a file from the database folder!')
    except IOError as e:
        print(e)
        tk.messagebox.showerror('TADPol', 'Error - Unable to copy file to the database folder destination!')
