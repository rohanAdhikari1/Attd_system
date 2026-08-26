from tkinter import *
from tkinter import ttk
import dialog
from PIL import Image, ImageTk
import cv2
import cvzone
from tkinter import messagebox
from pathlib import Path


def facecamgen(win):
    root = Toplevel(win)
    width = 880
    height = 450
    screen_width = root.winfo_screenwidth()  # Width of the screen
    screen_height = root.winfo_screenheight()  # Height of the screen
    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2) - 20

    root.geometry('%dx%d+%d+%d' % (width, height, x, y))
    root.title("Face Trainer")
    root.configure(bg="#C0C4C3")
    root.resizable(False, False)
    img = PhotoImage(file='Resources/tf.png')
    root.iconphoto(False, img)

    # varaibles
    opts = StringVar(value='Select Student name')
    global cam, std_id
    stdid = StringVar()
    facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
    cam = None

    ##########functionss
    def face_cam():
        global imgBackground, imgModeList, counter, modeType, id, imgStudent, cam
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cam.set(3, 640)
        cam.set(4, 480)
        cam.set(cv2.CAP_PROP_FRAME_COUNT, 60)
        cam.set(cv2.CAP_PROP_FPS, 60)
        cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

        def facecamrunner():
            global cam, faces, timg
            if cam is not None:
                success, img = cam.read()
                src, timg = cam.read()
                if success:
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = facedetect.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in faces:
                        bbox = x, y, w, h
                        img = cvzone.cornerRect(img, bbox, rt=0)
                    imgD = cv2.resize(img, (216, 216), None, 0.25, 0.25)
                    imgC = cv2.cvtColor(imgD, cv2.COLOR_BGR2RGB)
                    imgbs = Image.fromarray(imgC)
                    imgBg = ImageTk.PhotoImage(imgbs)
                    lb_qr.config(image=imgBg)
                    lb_qr.image = imgBg
                    lb_qr.after(1, facecamrunner)

        facecamrunner()
        show_result.place_forget()
        capture_btn.config(text="Capture")
        capture_btn.place(x=620, y=320, width=120, height=35)
        show_result.place(x=120, y=355, height=35)
        show_result.config(text="QR Code Succesfully Generated!!!")
        show_result.config(fg="green")

    def make_clear():
        global cam
        if cam is not None:
            cam.release()
            cam = None
        show_result.place_forget()
        capture_btn.place_forget()
        upload_btn.place_forget()
        lb_qr.config(image='')

    def on_closing():
        global cam
        if cam is not None:
            cam.release()
        cv2.destroyAllWindows()
        root.destroy()

    def upload_img():
        def save(timg):
            if cv2.imwrite(imagelocation, timg):
                dialog.success_dlg(root, "Image Saved", "Image is Successfully Uploaded!!!!")
        global timg
        timg = cv2.resize(timg, (216, 216), None, 0.25, 0.25)
        imagelocation = "Images/234561.png"
        if Path(imagelocation).is_file():
            check = messagebox.askyesno("Already Found",
                                        "Image Data of same user already found. Do you want to replace?", parent=root)
            if check:
                save(timg)
        else:
            save(timg)

    def capture_img():
        global faces, timg, cam, std_id
        faces_data = 0
        i = 0
        if cam is not None:
            if len(faces) > 0:
                while faces_data<=5:
                    gray = cv2.cvtColor(timg, cv2.COLOR_BGR2GRAY)
                    for (x, y, w, h) in faces:
                        crop_img = gray[y: y + h, x: x + w]
                        if faces_data<=5 and i % 1000 == 0:
                            cv2.imwrite(f"trainedimages\ "
                                        + std_id.get()
                                        + "_"
                                        + str(faces_data)
                                        + ".jpg", crop_img)
                            faces_data= faces_data+1
                        i = i + 1
                cam.release()
                cam = None
                show_result.place_forget()
                timg = cv2.resize(timg, (216, 216), None, 0.25, 0.25)
                blue, green, red = cv2.split(timg)
                img = cv2.merge((red, green, blue))
                im = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=im)
                lb_qr.config(image=imgtk)
                lb_qr.image = imgtk
                upload_btn.place(x=620, y=370, width=120, height=35)
                capture_btn.config(text="Re Capture")
            else:
                show_result.place(x=120, y=355, height=35)
                show_result.config(text="Please! Place your face inside Frame.")
                show_result.config(fg="red")
        else:
            face_cam()

    #####top label 1
    title_lb1 = Label(root, text="Student Deatils", font=("verdana", 12, "bold"),
                      fg="#F7F3F3", bg="#615F7A")
    title_lb1.place(x=15, y=10, width=470, height=45)

    #####label bg of detail
    lb_bg1 = Frame(root, bg="#E8E8E8")
    lb_bg1.place(x=15, y=55, width=470, height=375)

    wrapper = LabelFrame(lb_bg1, text="Student Lookup")
    wrapper.pack(padx=10, pady=10, fill="both", expand=False)

    ###label for select
    Label(wrapper, text="Select Student", font=("verdana", 8)).grid(row=0, column=0, pady=10, padx=10)

    ###select student
    std_name = ttk.Combobox(wrapper, textvariable=opts, width=30)
    std_name.grid(row=0, column=1, pady=10, padx=10)

    ###student data
    wrapper2 = LabelFrame(lb_bg1, text="Student Data")
    wrapper2.pack(padx=10, pady=10, fill="both", expand=False)

    # student id label
    Label(wrapper2, text="Student Name", font=("verdana", 8)).grid(row=0, column=0, pady=10, padx=10)

    ######student id entry
    std_id = Entry(wrapper2, textvariable=stdid, width=30, state="readonly")
    std_id.grid(row=0, column=1, pady=10, padx=10)

    # student name label
    Label(wrapper2, text="Student Email", font=("verdana", 8)).grid(row=0, column=0, pady=10, padx=10)

    ######student name entry
    std_id = Entry(wrapper2, textvariable=stdid, width=30, state="readonly")
    std_id.grid(row=0, column=1, pady=10, padx=10)

    # student name label
    Label(wrapper2, text="Student Phone", font=("verdana", 8)).grid(row=1, column=0, pady=10, padx=10)

    ######student name entry
    std_id = Entry(wrapper2, textvariable=stdid, width=30, state="readonly")
    std_id.grid(row=1, column=1, pady=10, padx=10)

    # student name label
    Label(wrapper2, text="Student id", font=("verdana", 8)).grid(row=2, column=0, pady=10, padx=10)

    ######student name entry
    std_id = Entry(wrapper2, textvariable=stdid, width=30, state="readonly")
    std_id.grid(row=2, column=1, pady=10, padx=10)

    # student name label
    Label(wrapper2, text="Student id", font=("verdana", 8)).grid(row=2, column=0, pady=10, padx=10)

    ######student name entry
    std_id = Entry(wrapper2, textvariable=stdid, width=30, state="readonly")
    std_id.grid(row=2, column=1, pady=10, padx=10)

    ###generate button
    capturenow_btn = Button(lb_bg1, text="Capture Face", cursor="hand2", font=("tahoma", 10, "bold"), bg="#2196F3",
                            fg="white", border=1, command=face_cam)
    capturenow_btn.place(x=40, y=250, width=120, height=35)

    ###clear button
    clear_btn = Button(lb_bg1, text="Clear", cursor="hand2", font=("tahoma", 10, "bold"), bg="#607D8B",
                       fg="white", border=1, command=make_clear)
    clear_btn.place(x=250, y=250, width=120, height=35)

    ########show result label
    show_result = Label(root, font=("verdana", 11), fg="green", bg="#E8E8E8")

    ##################################################

    #####top label 2
    title_lb2 = Label(root, text="Student Face Capture", font=("verdana", 12, "bold"),
                      fg="#F7F3F3", bg="#615F7A")
    title_lb2.place(x=505, y=10, width=355, height=45)

    #####label bg of qr
    lb_bg2 = Label(root, bg="#E8E8E8")
    lb_bg2.place(x=505, y=55, width=355, height=375)

    ##### qr container
    lb_qr = Label(root, bg="white", font=("verdana", 10, "bold"), text="Preview Not Available", borderwidth=1,
                  relief="solid")
    lb_qr.place(x=575, y=85, width=216, height=216)

    ####download and share qr
    capture_btn = Button(root, text="Capture", cursor="hand2", font=("tahoma", 10, "bold"), bg="green",
                         fg="white", border=1, command=capture_img)
    # download_btn.place(x=620, y=320, width=120, height=35)
    upload_btn = Button(root, text="Upload", cursor="hand2", font=("tahoma", 10, "bold"), bg="blue",
                        fg="white", border=1, command=upload_img)
    # upload_btn.place(x=620, y=370, width=120, height=35)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

# qrcodegen()
