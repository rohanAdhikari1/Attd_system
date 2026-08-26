import os
import cv2
import numpy as np
from tkinter import *
from PIL import ImageTk, Image
from pyzbar.pyzbar import decode
from datetime import datetime
import Crypto
import DBhelper as db

# EncodeGenerator.folderinitialize()
studentInfo = 0

imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))


# print(len(imgModeList))

def attdqr(win):
    global imgBackground, imgModeList, counter, modeType, id, imgStudent, cam
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)
    cam.set(cv2.CAP_PROP_FRAME_COUNT, 60)
    cam.set(cv2.CAP_PROP_FPS, 60)
    cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

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

    modeType = 0
    counter = 0
    id = -1
    imgStudent = []

    def on_closing():
        global cam
        cam.release()
        cv2.destroyAllWindows()
        root.destroy()

    def camrunner():
        global imgBackground, imgModeList, counter, modeType, id, imgStudent
        mydata = None
        studentInfo = []
        helper = db.DBhelper()
        if cam is not None:
            success, img = cam.read()
            if success:
                imgBackground[162:162 + 480, 55:55 + 640] = img
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                dtm = decode(img)
                if dtm:
                    for barcode in dtm:
                        mydata = None
                        mydata = barcode.data.decode("utf-8")
                        pts = np.array([barcode.polygon], np.int32)
                        pts.reshape((-1, 1, 2))
                        cv2.polylines(img, [pts], True, (255, 0, 255), 5)
                        id = Crypto.decrypt_id(mydata)
                        if counter == 0:
                            counter = 1
                            modeType = 1
                    if counter != 0:
                        if counter == 1:
                            # Get the Data
                            id = 123456
                            studentInfo = helper.fetch_by_id(id)
                            if studentInfo == 0 or studentInfo == 1 or studentInfo is None or studentInfo[0] is None:
                                modeType = 4
                                counter = 0
                                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                            else:
                                imgspath = "Images/{}.png".format(id)
                                imgStudent = cv2.resize(cv2.imread(imgspath), (216, 216))
                                # Update data of attendance
                                datetimeObject = datetime.strptime(studentInfo[2], "%Y-%m-%d %I:%M:%S %p")
                                secondsElapsed = (datetime.now() - datetimeObject).days
                                if secondsElapsed >= 1:
                                    date = datetime.now().strftime("%Y-%m-%d")
                                    time = datetime.now().strftime("%I:%M:%S %p")
                                    fire = helper.insert_data(
                                        "insert into reports (uid,date,time) values({},'{}','{}')".format(id, date,
                                                                                                          time))
                                    if fire:
                                        helper.update_user(id, date + " " + time)
                                        modeType = 2
                                        counter = 0
                                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                                        counter = 2
                                else:
                                    modeType = 3
                                    counter = 2
                                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                        if modeType != 4:

                            if 20 <= counter:
                                modeType = 1

                            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                            if counter >= 20:
                                # cv2.putText(imgBackground, str(studentInfo[3]), (861, 125),
                                #             cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                                # cv2.putText(imgBackground, str(studentInfo[2]), (1006, 550),#major
                                #             cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                                cv2.putText(imgBackground, str(id), (1006, 493),  # id
                                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                                # cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                                #             cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                                # cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                #             cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                                # cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                #             cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                                # (w, h), _ = cv2.getTextSize(studentInfo[1], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                                # offset = (414 - w) // 2
                                # cv2.putText(imgBackground, str(studentInfo[1]), (808 + offset, 445),
                                #             cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                                imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                            counter += 1
                else:
                    modeType = 0
                    counter = 0
                imgBackground[162:162 + 480, 55:55 + 640] = img
                framergba = cv2.cvtColor(imgBackground, cv2.COLOR_BGR2RGB)
                imgbs = Image.fromarray(framergba)
                imgBg = ImageTk.PhotoImage(imgbs)
                takeattn_img.config(image=imgBg)
                takeattn_img.image = imgBg
                takeattn_img.after(1, camrunner)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    camrunner()
    root.mainloop()
