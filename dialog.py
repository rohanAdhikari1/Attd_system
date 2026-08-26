from tkinter import *
from PIL import Image, ImageTk


def success_dlg(win,title,message):
    root = Toplevel(win)
    width = 280
    height = 135
    screen_width = root.winfo_screenwidth()  # Width of the screen
    screen_height = root.winfo_screenheight()  # Height of the screen

    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2) - 20

    root.geometry('%dx%d+%d+%d' % (width, height, x, y))
    root.title(title)
    root.configure(bg="#f1f1f1")
    # root.resizable(False, False)
    img = PhotoImage(file='Resources/login.png')
    root.iconphoto(False, img)
    root.transient(win)

    set_img_btn = Image.open("Resources/suc.png")
    set_img_btn = set_img_btn.resize((38, 38))
    imgs = ImageTk.PhotoImage(set_img_btn)
    ft1 = Frame(root, bg="white")
    ft1.place(height=75, width=265, x=8, y=8)
    takeattn_img = Label(ft1, bg='white', image=imgs)
    takeattn_img.place(height=38, width=38, x=12, y=20)
    Label(ft1, bg='white', text=message, font=("tahoma", 10)).place(height=38, x=55, y=20)
    ft = Frame(root, bg="#52d1e0")
    ft.place(height=25, width=84, x=180, y=99)
    Button(ft, text="OK", bg="#e2f0fd", bd=0, command=root.destroy).place(x=2,y=2,height=21, width=80)
    root.mainloop()
