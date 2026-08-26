from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path
import qrcode

import Crypto


def qrcodegen(win):
    root = Toplevel(win)
    width = 880
    height = 450
    screen_width = root.winfo_screenwidth()  # Width of the screen
    screen_height = root.winfo_screenheight()  # Height of the screen
    # Calculate Starting X and Y coordinates for Window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2) - 20

    root.geometry('%dx%d+%d+%d' % (width, height, x, y))
    root.title("QR Generator")
    root.configure(bg="#C0C4C3")
    root.resizable(False, False)
    img = PhotoImage(file='Resources/qrdet.png')
    root.iconphoto(False, img)

    # varaibles
    opts = StringVar(value='Select Student name')
    stdid = StringVar()

    ##########functionss
    def make_qrcode():
        global qr_img,QRcode,Qrimg
        show_result.place_forget()
        lb_qr.config(image='')
        logo_link = "Resources/scllogo.png"

        logo = Image.open(logo_link)

        # taking base width
        basewidth = 75

        # image size
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int(float(logo.size[1]) * float(wpercent))
        logo = logo.resize((basewidth, hsize))
        QRcode = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )

        # url or text
        text = Crypto.encrypt_id("123456")

        # adding text to code
        QRcode.add_data(text)

        # generating Qr code
        QRcode.make(fit=True)

        # take color name from user
        QRcolor = 'Black'

        # adding color to Qr code
        Qrimg = QRcode.make_image(
            fill_color=QRcolor, back_color="white").convert('RGB')

        # set size of Qrcode
        pos = ((Qrimg.size[1] - logo.size[0]) // 2,
               (Qrimg.size[1] - logo.size[1]) // 2)
        Qrimg.paste(logo, pos)

        # save the generated qr code
        # Qrimg.save('Qrimages/rohanqr.png')
        # qr_img = Image.open("Qrimages/rohanqr.png")
        qr_img = Qrimg.resize((240, 240))
        qr_img = ImageTk.PhotoImage(qr_img)
        lb_qr.config(image=qr_img)
        download_btn.place(x=620, y=320, width=120, height=35)
        upload_btn.place(x=620, y=370, width=120, height=35)
        show_result.place(x=120, y=355, height=35)
        show_result.config(text="QR Code Succesfully Generated!!!")

    def make_clear():
        show_result.place_forget()
        download_btn.place_forget()
        upload_btn.place_forget()
        lb_qr.config(image='')

    def download_qr():
        show_result.place_forget()
        downloads_path = str(Path.home() / "Downloads" / "123.png")
        Qrimg.save(downloads_path)
        messagebox.showinfo("Successfully Saved!","Image is successfully downloaded, check your download folder")


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
    generate_btn = Button(lb_bg1, text="Generate QR", cursor="hand2", font=("tahoma", 10, "bold"), bg="#2196F3",
                          fg="white", border=1, command=make_qrcode)
    generate_btn.place(x=40, y=250, width=120, height=35)

    ###clear button
    clear_btn = Button(lb_bg1, text="Clear", cursor="hand2", font=("tahoma", 10, "bold"), bg="#607D8B",
                       fg="white", border=1, command=make_clear)
    clear_btn.place(x=250, y=250, width=120, height=35)

    ########show result label
    show_result = Label(root, font=("verdana", 11), fg="green",bg="#E8E8E8")

    ##################################################

    #####top label 2
    title_lb2 = Label(root, text="Student QR Code", font=("verdana", 12, "bold"),
                      fg="#F7F3F3", bg="#615F7A")
    title_lb2.place(x=505, y=10, width=355, height=45)

    #####label bg of qr
    lb_bg2 = Label(root, bg="#E8E8E8")
    lb_bg2.place(x=505, y=55, width=355, height=375)

    ##### qr container
    lb_qr = Label(root, bg="white", font=("verdana", 10, "bold"),text="Preview Not Available",borderwidth = 1, relief="solid")
    lb_qr.place(x=585, y=100, width=195, height=195)


    ####download and share qr
    download_btn = Button(root, text="Download", cursor="hand2", font=("tahoma", 10, "bold"), bg="green",
                          fg="white", border=1,command=download_qr)
    # download_btn.place(x=620, y=320, width=120, height=35)
    upload_btn = Button(root, text="Upload", cursor="hand2", font=("tahoma", 10, "bold"), bg="blue",
                          fg="white", border=1)
    # upload_btn.place(x=620, y=370, width=120, height=35)
    root.mainloop()


# qrcodegen()