from tkinter import ttk,Toplevel,PhotoImage,StringVar,Frame,Label,LabelFrame,Button,RIGHT,BOTTOM,Entry
import dialog
from PIL import Image, ImageTk
import cv2
from configparser import ConfigParser


def open_settings(win):
    root = Toplevel(win)

    def setwindowwh(width, height):
        screen_width = root.winfo_screenwidth()  # Width of the screen
        screen_height = root.winfo_screenheight()  # Height of the screen
        # Calculate Starting X and Y coordinates for Window
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2) - 20

        root.geometry('%dx%d+%d+%d' % (width, height, x, y))

    setwindowwh(320, 580)
    root.title("Settings")
    root.configure(bg="#C0C4C3")
    root.resizable(False, False)
    img = PhotoImage(file='Resources/setting.png')
    root.iconphoto(False, img)
    global config, file

    def getcameralist():
         index = 0
         arr = []
         while True:
             cap = cv2.VideoCapture(index)
             if cap.isOpened():
                arr.append(f"Camera {index}")
                cap.release()
             else:
                break
             index += 1
         last_index = index - 1
         return arr, last_index

    def getcameraindex(val):
         index = 0
         device_list, _ = getcameralist()
         for camera_name in device_list:
            if val == camera_name: 
                return index
            index += 1
            return 0

    def getsettings():
        global databasedata, file,config,btnstatus
        file = 'data/config.ini'
        config = ConfigParser()
        config.read(file)
        optioncam = config['camera']
        if optioncam['welsound']:
            btnstatus = True
        else:
            btnstatus = False
        optionst = config['storage']
        databasedata = {}
        if config.has_section('database'):
            databas = config['database']
            databasedata["host"] = databas['host']
            databasedata["username"] = databas['username']
            databasedata["password"] = databas['password']
            databasedata["database"] = databas['database']
        return optioncam['index'], optionst['type'], databasedata

    def initialize():
        cameras, lastindex = getcameralist()
        camera_index, storetype, databasedata = getsettings()
        cb1['values'] = cameras
        cb1.set(cameras[int(camera_index)])
        cb2['values'] = ['CSV', 'MYSQL','SQLLITE']
        cb2.set(storetype)
        if (cb2.get() == "CSV"):
            wrapper3.pack_forget()
            setwindowwh(320, 430)
            lb_bg1.place(height=370)
        elif (cb2.get() == "MYSQL"):
            wrapper3.pack(padx=10, pady=10, fill="both", expand=False)
            setwindowwh(320, 630)
            lb_bg1.place(height=570)
        if databasedata:
            hos.set(databasedata["host"])
            usernam.set(databasedata["username"])
            passwor.set(databasedata["password"])
            databas.set(databasedata["database"])

    def savesettings():
        global file,config
        index = getcameraindex(cb1.get())
        config['camera']['index'] = str(index)
        type = cb2.get()
        config['storage']['type'] = type
        if (type == "MYSQL"):
            host = hos.get()
            dbuser = usernam.get()
            dbpass = passwor.get()
            database = databas.get()
            datas = [host, dbuser, dbpass, database]
            keys = ['host', 'username', 'password', 'database']
            if not config.has_section('database'):
                config.add_section('database')
            for x in range(len(datas)):
                config['database'][keys[x]] = datas[x]
        if usernams.get() != "" and passwors.get()!= "":
            config['credential']['username']= usernams.get()
            config['credential']['password']=passwors.get()
        with open(file, 'w') as configfile:
            config.write(configfile)
        dialog.success_dlg(root, "Settings Saved", "Settings are Successfully Updated!!")

    global btnstatus
    def changebtn():
        global btnstatus
        if btnstatus:
            switchbtn.config(image=btnoff)
            btnstatus = False
        else:
            switchbtn.config(image=btnon)
            btnstatus = True


    selcam = StringVar()
    selstorage = StringVar()
    usernam = StringVar()
    passwor = StringVar()
    hos = StringVar()
    databas = StringVar()
    usernams = StringVar()
    passwors = StringVar()
    #####top label 1
    title_lb1 = Label(root, text="Settings", font=("verdana", 12, "bold"),
                      fg="#F7F3F3", bg="#615F7A")
    title_lb1.place(x=4, y=10, width=310, height=45)

    #####label bg of detail
    lb_bg1 = Frame(root, bg="#E8E8E8")
    lb_bg1.place(x=5, y=55, width=310, height=520)

    wrapper = LabelFrame(lb_bg1, text="General Settings")
    wrapper.pack(padx=10, pady=10, fill="both", expand=False)

    ###label for camera selection
    Label(wrapper, text="Select Camera", font=("verdana", 8)).grid(row=0, column=0, pady=10, padx=10)

    ##select camera
    cb1 = ttk.Combobox(wrapper, width=20, textvariable=selcam, state="readonly", font=('Microsoft YaHei Ui Light', 8))
    cb1.grid(row=0, column=1, pady=10, padx=10)

    ###label welcome sound
    Label(wrapper, text="Welcome Sound", font=("verdana", 8)).grid(row=1, column=0, pady=10, padx=10)

    ##select camera
    btnonr = Image.open('Resources/on.png')
    btnonr = btnonr.resize((51, 27))
    btnon = ImageTk.PhotoImage(btnonr)
    btnoffr = Image.open('Resources/off.png')
    btnoffr = btnoffr.resize((51, 27))
    btnoff = ImageTk.PhotoImage(btnoffr)
    switchbtn = Button(wrapper, image=btnon, bg='#E8E8E8', bd=0, border=0,command=changebtn)
    switchbtn.grid(row=1, column=1, pady=10, padx=10)

    wrapper2 = LabelFrame(lb_bg1, text="Storage Settings")
    wrapper2.pack(padx=10, pady=10, fill="both", expand=False)

    ###label for storage type
    Label(wrapper2, text="Storage Type", font=("verdana", 8)).grid(row=0, column=0, pady=10, padx=10)

    ##select storage type
    cb2 = ttk.Combobox(wrapper2, width=20, textvariable=selstorage, state="readonly", font=('Mead Bold', 8))
    cb2.grid(row=0, column=1, pady=10, padx=16)

    wrapper3 = LabelFrame(lb_bg1, text="MySql Database")
    wrapper3.pack(padx=10, pady=10, fill="both", expand=False)

    ###label for host
    Label(wrapper3, text="Host", font=("verdana", 8)).grid(row=0, column=0, pady=10, padx=10)

    ##select storage type
    host = Entry(wrapper3, width=20, textvariable=hos, font=('Mead Bold', 8))
    host.grid(row=0, column=1, pady=10, padx=16)

    ###label for username
    Label(wrapper3, text="Username", font=("verdana", 8)).grid(row=1, column=0, pady=10, padx=10)

    ##entry username
    username = Entry(wrapper3, width=20, textvariable=usernam, font=('Mead Bold', 8))
    username.grid(row=1, column=1, pady=10, padx=16)

    ###label for password
    Label(wrapper3, text="Password", font=("verdana", 8)).grid(row=2, column=0, pady=10, padx=10)

    ##entry password
    password = Entry(wrapper3, width=20, textvariable=passwor, font=('Mead Bold', 8))
    password.grid(row=2, column=1, pady=10, padx=16)

    ###label for database
    Label(wrapper3, text="Database", font=("verdana", 8)).grid(row=3, column=0, pady=10, padx=10)

    ##entry database
    database = Entry(wrapper3, width=20, textvariable=databas, font=('Mead Bold', 8))
    database.grid(row=3, column=1, pady=10, padx=16)

    wrapper4 = LabelFrame(lb_bg1, text="Login Credentials")
    wrapper4.pack(padx=10, pady=10, fill="both", expand=False)

    ###label for username
    Label(wrapper4, text="Username", font=("verdana", 8)).grid(row=0, column=0, pady=10, padx=10)

    ##entry username
    database = Entry(wrapper4, width=20, textvariable=usernams, font=('Mead Bold', 8))
    database.grid(row=0, column=1, pady=10, padx=16)

    ###label for password
    Label(wrapper4, text="Password", font=("verdana", 8)).grid(row=1, column=0, pady=10, padx=10)

    ##entry password
    database = Entry(wrapper4, width=20, textvariable=passwors, font=('Mead Bold', 8))
    database.grid(row=1, column=1, pady=10, padx=16)

    bg = Frame(root, bg="#E8E8E8")
    bg.pack(pady=13, side=BOTTOM)

    capture_btn = Button(bg, text="Save", cursor="hand2", font=("tahoma", 10, "bold"), bg="green",
                         fg="white", border=1, command=savesettings)
    capture_btn.pack(pady=5, side=RIGHT, ipady=5, ipadx=15)

    def on_select(event):
        if (event.widget.get() == "CSV"):
            wrapper3.pack_forget()
            setwindowwh(320, 430)
            lb_bg1.place(height=370)
        elif (event.widget.get() == "MYSQL"):
            wrapper3.pack(padx=10, pady=10, fill="both", expand=False)
            setwindowwh(320, 630)
            lb_bg1.place(height=570)

    cb2.bind('<<ComboboxSelected>>', on_select)
    initialize()

    root.mainloop()