from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk

root = Tk()
width = 920
height = 480
screen_width = root.winfo_screenwidth()  # Width of the screen
screen_height = root.winfo_screenheight()  # Height of the screen
# Calculate Starting X and Y coordinates for Window
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2) - 20

root.geometry('%dx%d+%d+%d' % (width, height, x, y))
root.title("Student Details")
root.configure(bg="#C0C4C3")
root.resizable(False, False)
img = PhotoImage(file='Resources/std1.png')
root.iconphoto(False, img)

opts = StringVar(value='Select Student name')

#####top label 1
title_lb1 = Label(root, text="Student Deatils", font=("verdana", 12, "bold"),
                      fg="#F7F3F3", bg="#615F7A")
title_lb1.place(x=7, y=7, width=470, height=45)

#####label bg of detail
lb_bg1 = Frame(root, bg="#E8E8E8")
lb_bg1.place(x=7, y=52, width=470, height=375)

wrapper = LabelFrame(lb_bg1, text="Student Lookup")
wrapper.pack(padx=10, pady=10, fill="both", expand=False)

###label for select
Label(wrapper, text="Select Student", font=("verdana", 8)).grid(row=0, column=0, pady=10, padx=10)

###select student
std_name = ttk.Combobox(wrapper, textvariable=opts, width=30)
std_name.grid(row=0, column=1, pady=10, padx=10)

root.mainloop()