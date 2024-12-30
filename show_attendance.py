import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *
import tkinter.font as font

# Setting up the file paths properly
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Get the directory of the current file

attendance_path = os.path.join(BASE_DIR, "Attendance")


def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject == "":
            t = "Please enter the subject name."
            text_to_speech(t)
        else:
            try:
                 path = os.path.join(attendance_path, Subject) # Getting the correct path
                 filenames = glob(
                os.path.join(path,f"{Subject}*.csv")
                 ) # fixed local path issues
                 if not filenames: #check if filenames contains anything, otherwise raise filenotfound
                     raise FileNotFoundError("No CSV files found for this Subject")
                 df = [pd.read_csv(f) for f in filenames]
                 newdf = df[0]
                 for i in range(1, len(df)):
                   newdf = newdf.merge(df[i], how="outer")
                 newdf.fillna(0, inplace=True)
                 newdf["Attendance"] = 0
                 for i in range(len(newdf)):
                    # Corrected to calculate the mean of presence correctly (numeric columns only)
                    numeric_columns = newdf.columns[2:-1] # selecting columns containing dates only
                    newdf["Attendance"].iloc[i] = str(int(round(newdf.loc[i,numeric_columns].mean() * 100))) + '%'
                    #newdf.sort_values(by=['Enrollment'],inplace=True)
                 newdf.to_csv(os.path.join(path,"attendance.csv"), index=False)


                 root = tkinter.Tk()
                 root.title("Attendance of "+Subject)
                 root.configure(background="black")
                 cs = os.path.join(path,"attendance.csv")
                 with open(cs, newline="") as file:
                   reader = csv.reader(file)
                   r = 0

                   for col in reader:
                     c = 0
                     for row in col:
                        label = tkinter.Label(
                            root,
                            width=10,
                            height=1,
                            fg="yellow",
                            font=("times", 15, " bold "),
                            bg="black",
                            text=row,
                            relief=tkinter.RIDGE,
                        )
                        label.grid(row=r, column=c)
                        c += 1
                     r += 1
                 root.mainloop()
                 print(newdf)


            except FileNotFoundError as e:
                 f = f"Error:  {e}"
                 text_to_speech(f)
                 print("FileNotFoundError",e)
            except Exception as e: # catching any other errors that are not file not found
                f = f"Error: {e}"
                text_to_speech(f)
                print("Unexpected Error",e)


    subject = Tk()
    subject.iconbitmap(os.path.join(BASE_DIR, "AMS.ico"))
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")
    # subject_logo = Image.open("UI_Image/0004.png")
    # subject_logo = subject_logo.resize((50, 47), Image.ANTIALIAS)
    # subject_logo1 = ImageTk.PhotoImage(subject_logo)
    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)
    # l1 = tk.Label(subject, image=subject_logo1, bg="black",)
    # l1.place(x=100, y=10)
    titl = tk.Label(
        subject,
        text="Which Subject of Attendance?",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=100, y=12)

    def Attf():
        sub = tx.get()
        if sub == "":
            t="Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(
            os.path.join(BASE_DIR,"Attendance", sub)
            )


    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=10,
        relief=RIDGE,
    )
    attf.place(x=360, y=170)

    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="yellow",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="View Attendance",
        command=calculate_attendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=195, y=170)
    subject.mainloop()