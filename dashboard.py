from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import Settings
# import TrainFace
# import takeattendence
import GenerateQr
import QrAttendence

root = Tk()
width = 870
height = 450
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

########################
img = Image.open("Resources/banner.jpg")
img = img.resize((870, 60))
img = ImageTk.PhotoImage(img)
Label(root, image=img, bg='white').place(x=0, y=0)

########################
imgs = Image.open("Resources/bg3.jpg")
imgs = imgs.resize((870, 390))
imgs = ImageTk.PhotoImage(imgs)
bg_img = Label(root, image=imgs, bg='white').place(x=0, y=60)


# functions
def open_face_attn():
    messagebox.showerror("Maintenance Mode", "Not Available Right Now")
    # if not any(isinstance(x, Toplevel) for x in root.winfo_children()):
    #     takeattendence.takeattn(root)
    # else:
    #     messagebox.showerror("Already open", "Please close the another window to open new window")


def open_gen_qr():
    if not any(isinstance(x, Toplevel) for x in root.winfo_children()):
        GenerateQr.qrcodegen(root)
    else:
        messagebox.showerror("Already open", "Please close the another window to open new window")


def open_attd_qr():
    if not any(isinstance(x, Toplevel) for x in root.winfo_children()):
        QrAttendence.attdqr(root)
    else:
        messagebox.showerror("Already open", "Please close the another window to open new window")

def open_face_train():
      messagebox.showerror("Maintenance Mode", "Not Available Right Now")
    # if not any(isinstance(x, Toplevel) for x in root.winfo_children()):
    #     TrainFace.facecamgen(root)
    # else:
    #     messagebox.showerror("Already open", "Please close the another window to open new window")

def open_setting():
    if not any(isinstance(x, Toplevel) for x in root.winfo_children()):
        Settings.open_settings(root)
    else:
        messagebox.showerror("Already open", "Please close the another window to open new window")


# title section
title_lb1 = Label(bg_img, text="Attendance Managment System Using Facial Recognition", font=("verdana", 15, "bold"),
                  fg="navyblue")
title_lb1.place(x=0, y=60, width=870, height=45)

# student button 1
std_img_btn = Image.open("Resources/std1.jpg")
std_img_btn = std_img_btn.resize((120, 120))
std_img1 = ImageTk.PhotoImage(std_img_btn)
std_b1 = Button(bg_img, image=std_img1, cursor="hand2")
std_b1.place(x=70, y=130, width=120, height=120)
std_b1_1 = Button(bg_img, text="Student Pannel", cursor="hand2", font=("tahoma", 10, "bold"), bg="white", fg="navyblue")
std_b1_1.place(x=70, y=240, width=120, height=25)

# face attendence button 2
fat_img_btn = Image.open("Resources/det1.jpg")
fat_img_btn = fat_img_btn.resize((120, 120))
fat_img1 = ImageTk.PhotoImage(fat_img_btn)
fat_b2 = Button(bg_img, image=fat_img1, cursor="hand2", command=open_face_attn)
fat_b2.place(x=270, y=130, width=120, height=120)
fat_b2_1 = Button(bg_img, text="Face Attendence", cursor="hand2", font=("tahoma", 10, "bold"), bg="white",
                  fg="navyblue", command=open_face_attn)
fat_b2_1.place(x=270, y=240, width=120, height=25)

# qr attendence button 3
qrat_img_btn = Image.open("Resources/qrdet.png")
qrat_img_btn = qrat_img_btn.resize((120, 120))
qrat_img1 = ImageTk.PhotoImage(qrat_img_btn)
qrat_b3 = Button(bg_img, image=qrat_img1, cursor="hand2",command=open_attd_qr)
qrat_b3.place(x=470, y=130, width=120, height=120)
qrat_b3_1 = Button(bg_img, text="Qr Attendence", cursor="hand2", font=("tahoma", 10, "bold"), bg="white", fg="navyblue", command=open_attd_qr)
qrat_b3_1.place(x=470, y=240, width=120, height=25)

# manual attendence button 4
mat_img_btn = Image.open("Resources/att.jpg")
mat_img_btn = mat_img_btn.resize((120, 120))
mat_img1 = ImageTk.PhotoImage(mat_img_btn)
mat_b3 = Button(bg_img, image=mat_img1, cursor="hand2")
mat_b3.place(x=670, y=130, width=120, height=120)
mat_b3_1 = Button(bg_img, text="Take Attendence", cursor="hand2", font=("tahoma", 10, "bold"), bg="white",
                  fg="navyblue")
mat_b3_1.place(x=670, y=240, width=120, height=25)

########################################### ground level
# student button 5
rtd_img_btn = Image.open("Resources/atreport.png")
rtd_img_btn = rtd_img_btn.resize((120, 120))
rtd_img1 = ImageTk.PhotoImage(rtd_img_btn)
rtd_b1 = Button(bg_img, image=rtd_img1, cursor="hand2")
rtd_b1.place(x=70, y=300, width=120, height=120)
rtd_b1_2 = Button(bg_img, text="Attendence Reports", cursor="hand2", font=("tahoma", 8, "bold"), bg="white",
                  fg="navyblue")
rtd_b1_2.place(x=70, y=410, width=120, height=25)

# face attendence button 2
tf_img_btn = Image.open("Resources/tf.jpg")
tf_img_btn = tf_img_btn.resize((120, 120))
tf_img1 = ImageTk.PhotoImage(tf_img_btn)
tf_b2 = Button(bg_img, image=tf_img1, cursor="hand2",command=open_face_train)
tf_b2.place(x=270, y=300, width=120, height=120)
tf_b2_1 = Button(bg_img, text="Train Face", cursor="hand2", font=("tahoma", 10, "bold"), bg="white", fg="navyblue",command=open_face_train)
tf_b2_1.place(x=270, y=410, width=120, height=25)

# qr generate button 3
gq_img_btn = Image.open("Resources/gq.jpg")
gq_img_btn = gq_img_btn.resize((120, 120))
gq_img1 = ImageTk.PhotoImage(gq_img_btn)
gq_b3 = Button(bg_img, image=gq_img1, cursor="hand2", command=open_gen_qr)
gq_b3.place(x=470, y=300, width=120, height=120)
gq_b3_2 = Button(bg_img, text="Generate Qr", cursor="hand2", font=("tahoma", 10, "bold"), bg="white", fg="navyblue",
                 command=open_gen_qr)
gq_b3_2.place(x=470, y=410, width=120, height=25)

# manual attendence button 4
set_img_btn = Image.open("Resources/setting.png")
set_img_btn = set_img_btn.resize((120, 120))
set_img1 = ImageTk.PhotoImage(set_img_btn)
set_b3 = Button(bg_img, image=set_img1, cursor="hand2",command=open_setting)
set_b3.place(x=670, y=300, width=120, height=120)
set_b3_2 = Button(bg_img, text="Settings", cursor="hand2", font=("tahoma", 10, "bold"), bg="white", fg="navyblue",command=open_setting)
set_b3_2.place(x=670, y=410, width=120, height=25)

root.mainloop()
