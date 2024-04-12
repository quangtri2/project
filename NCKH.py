import cv2
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
from tkinter import messagebox, filedialog
import numpy as np
from pyzbar.pyzbar import decode
import serial
import pandas as pd
import pypyodbc as odbc
import sys
Arduino_Serial = serial.Serial("COM3",9600)
s = Arduino_Serial.readline()

# Defining CreateWidgets() function to create necessary tkinter widgets
def createwidgets():
    root.feedlabel = Label(root, bg="steelblue", fg="white", text="HỆ THỐNG PHÂN LOẠI HÀNG ỨNG DỤNG MÃ QRcode", font=('Comic Sans MS', 20))
    root.feedlabel.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

    root.cameraLabel = Label(root, bg="steelblue", borderwidth=3, relief="groove")
    root.cameraLabel.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

    root.textLable = Label(root, text='LOẠI HÀNG HÓA', bg="sky blue", fg="white", font=('Comic Sans MS', 20))
    root.textLable.grid(row=3, column=1, padx=20, pady=30)

    root.textLable = Label(root, text='', bg="white", fg="black", font=('Comic Sans MS', 20))
    root.textLable.grid(row=4, column=1, padx=0, pady=10)

    #root.captureBTN = Button(root, text="CAPTURE", command=Capture, bg="LIGHTBLUE", font=('Comic Sans MS', 15),
                              #width=20)
    #root.captureBTN.grid(row=5, column=2, padx=10, pady=10)
    #Calling ShowFeed() function

    ShowFeed()


# Defining ShowFeed() function to display webcam feed in the cameraLabel;
def ShowFeed():
    # Capturing frame by frame
    ret, frame = root.cap.read()

    if ret:
        # Flipping the frame vertically
        frame = cv2.flip(frame, 1)
        for barcode in decode(frame):
            # print(barcode.data)
            mydata = barcode.data.decode('utf-8')
            print(mydata)

            destPath.set(mydata)
            root.textLable.configure(text=destPath.get())

            if mydata == 'VACCINE ASTRAZENECA':
                myOutput = 'Trong Kho'
                myColor = (0, 255, 0)
                Arduino_Serial.write('1'.encode())
                checkPath.set(TRUE)

            elif mydata == 'Hoang Xuan Tai':
                myOutput = 'Trong Kho'
                myColor = (0, 255, 0)
                Arduino_Serial.write('2'.encode())
                checkPath.set(TRUE)

            elif mydata == 'VACCINE VEROCELL':
                myOutput = 'Trong Kho'
                myColor = (0, 255, 0)
                Arduino_Serial.write('3'.encode())
                checkPath.set(TRUE)

            elif mydata == 'VACCINE NANOCOVAX':
                myOutput = 'Trong Kho'
                myColor = (0, 255, 0)
                Arduino_Serial.write('4'.encode())
                checkPath.set(TRUE)

            elif mydata == 'DRINKS':
                myOutput = 'Trong Kho'
                myColor = (0, 255, 0)
                Arduino_Serial.write('5'.encode())
                checkPath.set(TRUE)

            elif mydata == 'FRUITS':
                myOutput = 'Trong Kho'
                myColor = (0, 255, 0)
                Arduino_Serial.write('6'.encode())
                checkPath.set(TRUE)

            elif mydata == 'VEGETABLE':
                myOutput = 'Trong Kho'
                myColor = (0, 255, 0)
                Arduino_Serial.write('7'. encode())
                checkPath.set(TRUE)

            elif mydata == 'FOOD':
                myOutput = 'Trong Kho'
                myColor = (0, 255, 0)
                Arduino_Serial.write('8'.encode())
                checkPath.set(TRUE)

            else:
                myOutput = 'Khong trong kho'
                myColor = (0, 0, 255)
                checkPath.set(FALSE)

            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, myColor, 5)
            pts2 = barcode.rect
            cv2.putText(frame, myOutput, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_TRIPLEX, 0.9, myColor, 2)
            print(checkPath.get())
        # Displaying date and time on the feed
        cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (20, 30), cv2.FONT_HERSHEY_DUPLEX, 0.5,
                    (0, 255, 255))

        # Changing the frame color from BGR to RGB
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        # Creating an image memory from the above frame exporting array interface
        videoImg = Image.fromarray(cv2image)

        # Creating object of PhotoImage() class to display the frame
        imgtk = ImageTk.PhotoImage(image=videoImg)

        # Configuring the label to display the frame
        root.cameraLabel.configure(image=imgtk)

        # Keeping a reference
        root.cameraLabel.imgtk = imgtk

        # Calling the function after 10 milliseconds
        root.cameraLabel.after(10, ShowFeed)
    else:
        # Configuring the label to display the frame
        root.cameraLabel.configure(image='')


# Defining Capture() to capture and save the image and display the image in the imageLabel
# def Capture():
#     # Storing the date in the mentioned format in the image_name variable
#     image_name = datetime.now().strftime('%d-%m-%Y %H-%M-%S')
#     root.textLable.configure(text=destPath.get())
#     #
#     # # Capturing the frame
#     # ret, frame = root.cap.read()

 #    open file
    # with open('D:\OneDrive\Desktop\mydata.txt') as f:
    # myDataList = f.read().splitlines()
    # print(myDataList)

# Creating object of tk class
root = tk.Tk()

# Creating object of class VideoCapture with webcam index
root.cap = cv2.VideoCapture(0)

# Setting width and height
width, height = 600, 400
root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Setting the title, window size, background color and disabling the resizing property
root.title("Hoang Xuan Tai")
root.geometry("700x800")
root.resizable(True, True)
#root.configure(background="yellow")

# Creating tkinter variables
destPath = StringVar()
checkPath = BooleanVar()
createwidgets()
root.mainloop()
cv2.destroyAllWindows()