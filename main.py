from tkinter import *
from configparser import ConfigParser

root = Tk()
width = 870
height = 450
screen_width = root.winfo_screenwidth()  # Width of the screen
screen_height = root.winfo_screenheight()  # Height of the screen

# Calculate Starting X and Y coordinates for Window
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2) - 20

root.geometry('%dx%d+%d+%d' % (width, height, x, y))
root.title("Attendence login")
# root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)

img = PhotoImage(file='Resources/login.png')
root.iconphoto(False, img)
Label(root, image=img, bg='white').place(x=50, y=50)

frame = Frame(root, width=350, height=350, bg="white")
frame.place(x=480, y=40)

error = Label(frame, pady=5, padx=5, text="Invalid! username and password. Please try again", fg='red', bg='#E4E2E2', font=('Microsoft YaHei Ui Light', 10))
error.place(x=20, y=1)
error.place_forget()

heading = Label(frame, text="Sign in", fg='#57a1f8', bg='white', font=('Microsoft YaHei Ui Light', 23, 'bold'))
heading.place(x=100, y=35)


##signin the user
def signin():
    file = 'data/config.ini'
    config = ConfigParser()
    config.read(file)
    crd = config['credential']
    username = user.get()
    password = code.get()
    if username == crd['username'] and password == crd['password']:
        error.place_forget()
        root.destroy()
        import dashboard
    else:
        error.place(x=20, y=1)


################
def on_click(e):
    code.focus_set()


def on_enter(e):
    name = user.get()
    if name == 'Username':
        user.delete(0, 'end')


def on_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, "Username")


user = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei Ui Light', 11))
user.place(x=30, y=110)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)
user.bind('<Return>', on_click)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=137)


########################
def on_click(e):
    signin()


def on_enter(e):
    codes = code.get()
    if codes == 'Password':
        code.delete(0, 'end')


def on_leave(e):
    name = code.get()
    if name == '':
        code.insert(0, "Password")


code = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei Ui Light', 11))
code.place(x=30, y=180)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)
code.bind('<Return>', on_click)

showed = False


def hide():
    global showed
    if showed:
        eyebtn.config(image=closeeye)
        code.config(show="*")
        showed = False
    else:
        eyebtn.config(image=openeye)
        code.config(show="")
        showed = True


openeye = PhotoImage(file='Resources/eye.png')
closeeye = PhotoImage(file='Resources/eye-close-up.png')
eyebtn = Button(frame, image=closeeye, bg='white', bd=0, border=0, command=hide)
code.config(show="*")
eyebtn.place(x=290, y=185)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=207)

#####################
Button(frame, width=39, pady=7, text='Log in', bg="#57a1f8", fg='white', border=0, command=signin).place(x=35, y=245)

root.mainloop()
# takeattendence.takeattn()
