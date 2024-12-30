import csv
import os
import cv2
import numpy as np
import pandas as pd
import datetime
import time
import tkinter as tk

# Setting up the file paths properly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
haarcasecade_path = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
trainimage_path = os.path.join(BASE_DIR, "TrainingImage")
studentdetail_path = os.path.join(BASE_DIR, "StudentDetails", "studentdetails.csv")


# take Image of user
def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen,text_to_speech):
    if (l1 == "") and (l2 == ""):
        t = "Please Enter the your Enrollment Number and Name."
        text_to_speech(t)
    elif l1 == "":
        t = "Please Enter the your Enrollment Number."
        text_to_speech(t)
    elif l2 == "":
        t = "Please Enter the your Name."
        text_to_speech(t)
    else:
        try:
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier(haarcasecade_path)
            Enrollment = l1
            Name = l2
            sampleNum = 0
            directory = Enrollment + "_" + Name
            path = os.path.join(trainimage_path, directory)
            if not os.path.exists(path):
                 os.makedirs(path)
            else: # handle existing folder
                 message.configure(text="Student data already exists!", fg="red")
                 text_to_speech("Student data already exists!")
                 return # stops executing if data exists
            while True:
                ret, img = cam.read()
                if not ret:
                    break
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sampleNum = sampleNum + 1
                    cv2.imwrite(
                        os.path.join(path,f"{Name}_{Enrollment}_{sampleNum}.jpg"),
                        gray[y: y + h, x: x + w],
                    )
                    cv2.imshow("Frame", img)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                elif sampleNum > 50:
                    break
            cam.release()
            cv2.destroyAllWindows()
            row = [Enrollment, Name]
            with open(
                studentdetail_path,
                "a+",
            ) as csvFile:
                writer = csv.writer(csvFile, delimiter=",")
                writer.writerow(row)
                csvFile.close()
            res = "Images Saved for ER No:" + Enrollment + " Name:" + Name
            message.configure(text=res, fg="green")
            text_to_speech(res)
        except FileExistsError as F:
             message.configure(text="Student Data already exists", fg = "red")
             text_to_speech("Student Data already exists")
             print(F)
        except Exception as e:
            message.configure(text=f"Error capturing image: {e}", fg="red")
            text_to_speech("Error capturing image")
            print(e)