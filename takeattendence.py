import os
import pickle
import cv2
import cvzone
import numpy as np
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from datetime import datetime
from DBhelper import DBhelper
import sound


def takeattn(win):
    root = Toplevel(win)
    width = 1300
    height = 650
    screen_width = root.winfo_screenwidth()  # Width of the screen
    screen_height = root.winfo_screenheight()  # Height of the screen

    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2) - 20

    root.geometry('%dx%d+%d+%d' % (width, height, x, y))
    root.title("Attendence System")
    root.configure(bg="#fff")
    root.resizable(False, False)
    img = PhotoImage(file='Resources/login.png')
    root.iconphoto(False, img)
    takeattn_img = Label(root, bg='white')
    takeattn_img.pack()
    helper = DBhelper()
    global cap, modeType, imgBackground, counter,Id,studentInfo,count
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 640)
    cap.set(4, 480)
    cap.set(cv2.CAP_PROP_FRAME_COUNT, 60)
    cap.set(cv2.CAP_PROP_FPS, 60)
    cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
    OPENCV_VIDEOIO_PRIORITY_MSMF = 0

    modeType = 0
    counter = 0
    count = 0
    Id = -1
    studentInfo = []
    imgStudent = []

    def on_closing():
        global cap
        cv2.destroyAllWindows()
        cap = None
        root.destroy()

    imgBackground = cv2.imread('Resources/background.png')

    # Importing the mode images into a list
    folderModePath = 'Resources/Modes'
    modePathList = os.listdir(folderModePath)
    imgModeList = []
    for path in modePathList:
        imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
    # print(len(imgModeList))

    # Load the encoding file
    print("Loading Encode File ...")
    facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    try:
        recognizer.read('data/trainer.yml')
    except:
        messagebox.showerror("Model not found,please train model")
        on_closing()
    print("Encode File Loaded")

    def show_image(imgBackground):
        framergba = cv2.cvtColor(imgBackground, cv2.COLOR_BGR2RGB)
        imgBg = ImageTk.PhotoImage(Image.fromarray(framergba))
        takeattn_img.config(image=imgBg)
        takeattn_img.update()
        takeattn_img.after(1,camrunner)

    def camrunner():
        global modeType,imgBackground,counter,Id,studentInfo,count,cap
        if cap is not None:
            success, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = facedetect.detectMultiScale(gray, 1.2, 5)

            imgBackground[162:162 + 480, 55:55 + 640] = img
            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            for (x, y, w, h) in faces:
                crop_img = gray[y:y + h, x:x + w]
                Id, conf = recognizer.predict(crop_img)
                print(conf)
                if conf < 65:
                    bbox = 55 + x, 162 + y, w, h
                    imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                    if counter == 0:
                        counter = 1
                        modeType = 5
                    elif counter < 2:
                        counter += 1
                else:
                    # if count > 3:
                    #     modeType = 4
                    counter = 0
                    #     count = 0
                    # else:
                    #     count += 1

                if counter >= 2:
                    if counter == 3:
                        # Get the Data
                        studentInfo = helper.fetch_by_id(Id)
                        if studentInfo == 0 or studentInfo == 1 or studentInfo is None or studentInfo[0] is None:
                            modeType = 4
                            counter = 0
                        else:
                            imgspath = "Images/{}.png".format(id)
                            # imgStudent = cv2.resize(cv2.imread(imgspath), (216, 216))
                            date = datetime.now().strftime("%Y-%m-%d")
                            time = datetime.now().strftime("%I:%M:%S %p")
                            # Update data of attendance
                            datetimeObject = datetime.strptime(studentInfo[2],
                                                               "%Y-%m-%d %I:%M:%S %p")
                            secondsElapsed = (datetime.now() - datetimeObject).days
                            if secondsElapsed >= 1:
                                date = datetime.now().strftime("%Y-%m-%d")
                                time = datetime.now().strftime("%I:%M:%S %p")
                                fire = helper.insert_data(
                                    "insert into reports (uid,date,time) values({},'{}','{}')".format(Id, date, time))
                                if fire:
                                    helper.update_user(Id, date + " " + time)
                                    sound.playsound("welcome")
                                    modeType = 2
                                    counter = 7
                            else:
                                modeType = 3
                                counter = 7
                    if modeType != 4:
                        if 15 <= counter:
                            modeType = 1

                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                        if counter >= 15:
                            cv2.putText(imgBackground, str(studentInfo[3]), (633, 125),
                                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                            # cv2.putText(imgBackground, str(studentInfo[3]), (861, 125),
                            #             cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                            # cv2.putText(imgBackground, str(studentInfo[2]), (1006, 550),#major
                            #             cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                            cv2.putText(imgBackground, str(Id), (1006, 493),  # id
                                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                            # cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                            #             cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                            # cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                            #             cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                            # cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                            #             cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                            (w, h), _ = cv2.getTextSize(studentInfo[1], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                            offset = (414 - w) // 2
                            cv2.putText(imgBackground, str(studentInfo[1]), (808 + offset, 445),
                                        cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                            # imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                        counter += 1
                    else:
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                        # if counter >= 30:
                        #     counter = 0
                        #     modeType = 0
                        #     studentInfo = []
                        #     imgStudent = []
            if counter == 0:
                modeType = 0
                counter = 0
                studentInfo = []
                imgStudent = []
            show_image(imgBackground)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    camrunner()
    root.mainloop()