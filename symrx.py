#SymRx is property of Presbyterian College School of Pharmacy: Pharmacy Innovations Lab

# -*- coding: utf-8 -*-
#========================
# imports
#========================
try:
    import Tkinter as tk
    from Tkinter import *
    import ttk
    from ttk import Style

except:
    import tkinter as tk
    from tkinter import *
    from tkinter import ttk
    from tkinter.ttk import Style

from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image, ImageTk
from passlib.context import CryptContext
import io
import os
from fpdf import FPDF
import sys
global encrypt_password
global check_encrypted_password
global picture
from pdf_class import Generate_pdf

#==========================
# Encryption for passwords
#==========================
pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000)

def encrypt_password(password):
    return pwd_context.encrypt(password)

def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)



#========================
# fonts
#========================
LARGE_FONT= ("Times New Roman", 24, 'bold')
reg = ("Times New Roman", 14, 'bold')
bfont= ("Times New Roman", 20)
menufont = ('Source Sans Pro',8, 'bold italic')
menufont2 = ('Source Sans Pro',16, 'bold italic')


#========================
# colors
#========================

# background = '#ffd058'
background = 'light goldenrod1'



#---------------------------------
class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.title('SymRX')
        # self.iconbitmap('icon.ico')


        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree, Register, FilePrinterDialog):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

#-----------------------------------------    
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.configure(bg = background)

        global user_flag
        global pass_flag
        global picture
        
        def picture(file):
            x = Image.open(file)
            y = ImageTk.PhotoImage(x)
            z = Label(self, image=y)
            z.image = y
            z.pack()
            z.configure(highlightbackground=background, bg=background)


        #========================
        # login
        #========================
        please_login = picture('please.png')
        
        username = picture('new.png')

        username_entry = tk.Entry(self)
        username_entry.pack()

        password = picture("password.png")

        password_entry = tk.Entry(self, show = '*')
        password_entry.pack()


        #========================
        # submit button
        #========================

        photoimage = tk.PhotoImage(file="oh.png")

        photo1 = photoimage.subsample(1, 1) 

        submit = tk.Button(self, width=75, height=37, image=photo1,
                             bg=background,highlightbackground=background,border='0',highlightthickness='0',
                            command=lambda: check_register())
        submit.image = photo1
        submit.configure(bg=background,highlightbackground=background,border='0')

        submit.pack(pady=5)

        #========================
        # register
        #========================
        photoimage1 = tk.PhotoImage(file="register.png")

        # photo2 = photoimage1.subsample(1, 1) 
        photo2 = photoimage1.subsample(1, 1)

        register = tk.Button(self, width=92, height=37, image=photoimage1,
                             bg=background,highlightbackground=background,border='0',highlightthickness='0',
                            command=lambda: controller.show_frame(Register))

        register.image = photoimage1
    
        register.configure(bg=background,highlightbackground=background,border='0')
        register.pack()

        #========================
        # Checks registration
        #========================

        user_flag = False
        pass_flag = False
        
        def check_register():
            global pass_flag
            global user_flag
            global incorrect_user
            global incorrect_password

            username1 = username_entry.get()
            password1 = password_entry.get()

            username_entry.delete(0, END) #deletes the username and password after pressing enter
            password_entry.delete(0, END)


            fn = open('user_info.txt', 'r')
            lines = fn.readlines()
            fn.close()

            user_list = []

            for line in lines:
                line = line.strip('\n')
                user_list.append(line)


            if username1 in user_list:
                if user_flag ==True:
                    incorrect_user.pack_forget()

                index1 = user_list.index(username1)
                check = check_encrypted_password(password1, user_list[index1 + 1])

                if check == True:
                    controller.show_frame(PageOne)
                else:
                    if pass_flag == True:
                        incorrect_password.pack_forget()
                        pass_flag = False
                    incorrect_password = tk.Label(self, text='The password you entered is not correct!', font = LARGE_FONT, fg = 'red', bg = 'light blue')
                    incorrect_password.configure(background=background)
                    incorrect_password.pack()
                    pass_flag = True
            else:
                if user_flag == True:
                    incorrect_user.pack_forget()

                incorrect_user = tk.Label(self, text='The username you entered is not correct!', font = LARGE_FONT, fg = 'red', bg = 'light blue')
                incorrect_user.configure(background=background)
                incorrect_user.pack()
                
                if user_flag == False:
                    user_flag = True
                else:
                    user_flag = False


        #========================
        # logo image
        #========================

        logo = picture('symrx_logo.png')


#-----------------------------------------------------
#=============
#Welcome Page
#=============

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        global picture
        
        def picture(file):
            x = Image.open(file)
            y = ImageTk.PhotoImage(x)
            z = Label(self, image=y)
            z.image = y
            z.pack()
            z.configure(highlightbackground=background, bg=background)

        #========================
        # Windo Label
        #========================
        welcome = picture('welcome.png')

        #========================
        # window background
        #========================
        self.configure(bg=background)




        #========================
        # the purpose of SymRx
        #========================

        space = tk.Label(self, text='              ', bg = background)
        space.pack()

        explain = picture('description.png')

        space = tk.Label(self, text='              ', bg = background)
        space.pack()

        how = picture('how.png')


        #================================
        # button to begin a new pictogram
        #================================
        photoimage1 = tk.PhotoImage(file="generate.png")

        photo2 = photoimage1.subsample(1, 1)

        register = tk.Button(self, width=170, height=42, image=photoimage1,
                             bg=background,highlightbackground=background,border='0',highlightthickness='0',
                            command=lambda: controller.show_frame(PageTwo))

        register.image = photoimage1
    
        register.configure(bg=background,highlightbackground=background,border='0')
        register.pack(side='bottom', pady=10)

        #===============================
        # put a space between the button
        #===============================
        words = picture('words.png')


        #===========================
        # button to go back to login
        #===========================

        photoimage = tk.PhotoImage(file="back.png")

        photo1 = photoimage.subsample(1, 1) 

        submit = tk.Button(self, width=110, height=42, image=photo1,
                             bg=background,highlightbackground=background,border='0',highlightthickness='0',
                            command=lambda: controller.show_frame(StartPage))
        submit.image = photo1
        submit.configure(bg=background,highlightbackground=background, border='0')

        submit.pack(side='bottom')
        

#------------------------------------------
#Page with paramaters for pictogram
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #========================
        # Global Variables
        #========================
        global variable1
        global variable2
        global variable3
        global variable
        global variable5
        global patient_name_entry

        def space():
            s = tk.Label(self, text='              ', bg = background)
            s.pack()

        def picture(file):
            x = Image.open(file)
            y = ImageTk.PhotoImage(x)
            z = Label(self, image=y)
            z.image = y
            z.pack()
            z.configure(highlightbackground=background, bg=background)

        def picture_side(file, where):
            x = Image.open(file)
            y = ImageTk.PhotoImage(x)
            z = Label(self, image=y)
            z.image = y
            z.pack(side=where)
            z.configure(highlightbackground=background, bg=background)

        #========================
        # Background Color
        #========================
        self.configure(bg=background)
        border = picture_side('border.png','left')
        border_right = picture_side('border.png','right')



        #================================
        # label for selecting paramaters
        #================================
        select = picture('select.png')


        #================================
        # Patient Name
        #================================

        patient_name_entry = tk.Entry(self)
        patient_name_entry.pack()

        #===============================
        # Dosage Form
        #===============================

        space()
        dosage_forms = picture('dosage_form.png')

        variable1 =  tk.StringVar(parent)    #Sets the default as "Tablet"
        variable1.set('Tablet')

        menu1 = tk.OptionMenu(self, variable1, 'Tablet', 'Capsule', 'Injections', 'Drops', 'Ointment') #The dropdown menu for Routes of Administration
        menu1.pack()
        menu1.configure(font=menufont, width=7)

        space()

        #===============================
        # Dosage Amount
        #===============================

        dosage = picture('dosage.png')

        variable =  tk.StringVar(parent)    #Sets the default as "Tablet"
        variable.set('One')

        menu1 = tk.OptionMenu(self, variable, 'One', 'Two', 'Three', 'Four', 'Five', 'NA') #The dropdown menu for Routes of Administration
        menu1.pack()
        menu1.configure(font=menufont, width=7)

        space()

        routes = picture('routes.png')

        variable5 =  tk.StringVar(parent)    #Sets the default as "Tablet"
        variable5.set('Oral')

        menu5 = tk.OptionMenu(self, variable5, 'Oral', 'Ocular', 'Topical', 'Rectal', 'Vaginal','NA') #The dropdown menu for Routes of Administration
        menu5.pack()
        menu5.configure(font=menufont, width=7)

        space = tk.Label(self, text='              ', bg = background)
        space.pack()



        food = picture('food.png')

        variable2 =  tk.StringVar(parent)
        variable2.set('With Food')

        menu2 = tk.OptionMenu(self, variable2, 'With Food', 'Without Food', 'Before Meals', 'After Meals', 'NA')
        menu2.pack()
        menu2.configure(font=menufont, width=7)


        space1 = tk.Label(self, text='                         ', bg=background)
        space1.pack()


        time = picture('time.png')

        variable3 =  tk.StringVar(parent)
        variable3.set('Morning')

        menu3 = tk.OptionMenu(self, variable3, 'Morning', 'Noon', 'Evening', 'Night')
        menu3.pack()
        menu3.configure(font=menufont, width=7)

        space1 = tk.Label(self, text='                         ', bg=background)
        space1.pack()

        space1 = tk.Label(self, text='                         ', bg=background)
        space1.pack()
        space1 = tk.Label(self, text='                         ', bg=background)
        space1.pack()



        photoimage = tk.PhotoImage(file="generate_picto.png")
        photo1 = photoimage.subsample(1, 1) 
        submit = tk.Button(self, width=160, height=40, image=photo1,
                             bg=background,highlightbackground=background,border='0',highlightthickness='0',
                            command=lambda: [change_dropdown(),print_picto(), controller.show_frame(PageThree)])
        submit.image = photo1
        submit.configure(bg=background,highlightbackground=background, border='0')
        submit.pack()

       

        photoimage = tk.PhotoImage(file="back.png")
        photo1 = photoimage.subsample(1, 1) 
        submit = tk.Button(self, width=110, height=42, image=photo1,
                             bg=background,highlightbackground=background,border='0',highlightthickness='0',
                            command=lambda: controller.show_frame(StartPage))
        submit.image = photo1
        submit.configure(bg=background,highlightbackground=background, border='0')
        submit.pack()


        photoimage = tk.PhotoImage(file="back_welcome.png")
        photo1 = photoimage.subsample(1, 1) 
        submit = tk.Button(self, width=137, height=42, image=photo1,
                             bg=background,highlightbackground=background,border='0',highlightthickness='0',
                            command=lambda: controller.show_frame(PageOne))
        submit.image = photo1
        submit.configure(bg=background,highlightbackground=background, border='0')
        submit.pack()



        
class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def picture_side(file, where):
            x = Image.open(file)
            y = ImageTk.PhotoImage(x)
            z = Label(self, image=y)
            z.image = y
            z.pack(side=where)
            z.configure(highlightbackground=background, bg=background, fg = 'light blue')

        #========================
        # Background Color
        #========================
        self.configure(bg=background)


        border = picture_side('border.png','left')
        border_right = picture_side('border.png','right')



        global change_dropdown

        def change_dropdown(*args):
            global v1
            global v2
            global v4
            global v5  #routes of admin
            global v3
            global patient_name
            global label6
            global here
            global imgpdf


            v1 =variable1.get()
            v2 =variable2.get()
            v3 = variable3.get()
            v4 = variable.get()
            v5 = variable5.get()
            patient_name = patient_name_entry.get()
            
            

            def show(some):
                if some == 'NA':
                    return ''
                else:
                    return some + ', '


            label6 = tk.Label(self, text='Paramaters: ' + v1 + ',  ' + show(v4)  + show(v2) + v3, font=reg, bg=background)
            label6.configure(font = menufont2, fg='light Blue')
            label6.pack(pady=10,padx=10)


            here = tk.Label(self, text = 'Here is your pictogram:', bg=background, font=menufont)
            here.configure(fg='light blue')
            here.pack()

            
        def pressed():
            imgpdf.pack_forget()
            label6.pack_forget()


        photoimage = tk.PhotoImage(file="back.png")
        photo1 = photoimage.subsample(1, 1) 
        submit = tk.Button(self, width=135, height=42, image=photo1,
                             bg=background,highlightbackground=background,border='0',highlightthickness='0',
                            command=lambda: controller.show_frame(StartPage))
        submit.image = photo1
        submit.configure(bg=background,highlightbackground=background, border='0')
        submit.pack(side='bottom')


        photoimage = tk.PhotoImage(file="back_to.png")
        photo1 = photoimage.subsample(1, 1) 
        submit = tk.Button(self, width=150, height=37, image=photo1,
                             bg=background,highlightbackground=background,border='0',highlightthickness='0',
                            command=lambda: [pressed(),here.pack_forget(), controller.show_frame(PageTwo)])
        submit.image = photo1
        submit.configure(bg=background,highlightbackground=background, border='0')
        submit.pack(side='bottom')


        global print_picto

        def print_picto():
            global imgpdf
            build = Generate_pdf(v4, v1, v5, v2, v3, patient_name)
            done = build.what_selected()
            build.build_pdf(done)
           

            images = convert_from_path('finished_picto.pdf')
            for image in images:
                image.save('sample.png', 'PNG')

            pdf_pic =Image.open('sample.png')
            newsize = (425,555) 
            
            pdf_pic = pdf_pic.resize(newsize)
            renderpic = ImageTk.PhotoImage(pdf_pic)



            imgpdf = Label(self, image=renderpic)
            imgpdf.image = renderpic
            imgpdf.pack()
            imgpdf.configure(background='white')

            


class Register(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)


        def picture(file):
            x = Image.open(file)
            y = ImageTk.PhotoImage(x)
            z = Label(self, image=y)
            z.image = y
            z.pack()
            z.configure(highlightbackground=background, bg=background)


        global add_registration
        global registration_code_entry
        global flag
        global other_flag
        global clear

        self.configure(bg = background)

        #================
        # please register
        #================
        please_register = picture('please_enter.png')

        space1 = tk.Label(self, text='                         ', bg=background)
        space1.pack()


        registration_code = picture('registration_code.png')


        registration_code_entry = tk.Entry(self, show = '*')
        registration_code_entry.pack()


        space1 = tk.Label(self, text='                         ', bg=background)
        space1.pack()


        desired_username = picture('desired_username.png')

        desired_username_entry = tk.Entry(self)
        desired_username_entry.pack()

        space1 = tk.Label(self, text='                         ', bg=background)
        space1.pack()


        password_register = picture('desired_password.png')

        password_register_entry = tk.Entry(self)
        password_register_entry.pack()

        space1 = tk.Label(self, text='                         ', bg=background)
        space1.pack()

        space1 = tk.Label(self, text='                         ', bg=background)
        space1.pack()

        # submit_reg = tk.Button(self, text = 'Register', command = lambda: add_registration())
        # submit_reg.pack()

        photoimage1 = tk.PhotoImage(file="register.png")

        # photo2 = photoimage1.subsample(1, 1) 
        photo2 = photoimage1.subsample(1, 1)

        register = tk.Button(self, width=92, height=37, image=photoimage1,
                             bg=background,highlightbackground=background,border='0',highlightthickness='0',
                            command=lambda: add_registration())

        register.image = photoimage1
    
        register.configure(bg=background,highlightbackground=background,border='0')
        register.pack()

        photoimage = tk.PhotoImage(file="back.png")
        photo1 = photoimage.subsample(1, 1) 
        submit = tk.Button(self, width=110, height=42, image=photo1,
                             bg=background,highlightbackground=background,border='0',highlightthickness='0',
                            command=lambda: controller.show_frame(StartPage))
        submit.image = photo1
        submit.configure(bg=background,highlightbackground=background, border='0')
        submit.pack()



        flag = False
        other_flag = False

        def clear():
            global user_flag
            if user_flag == True:
                    user_flag = False
                    incorrect_user.pack_forget()

        def add_registration():
            global alredy_taken

            code1 = registration_code_entry.get()
            new_user = desired_username_entry.get()
            new_password1 = password_register_entry.get()
            new_password = encrypt_password(new_password1)



            code_flie = open('code.txt','r')
            code = code_flie.readline()
            code_flie.close()

            user_lines = []

            fn3 = open('user_info.txt', 'r')
            lines = fn3.readlines()
            for line in lines:
                line = line.strip('\n')
                user_lines.append(line)
            fn3.close()



            if code1 in code:
                global flag
                global other_flag
                if flag == True:
                    alredy_taken.pack_forget()
                if new_user not in user_lines:
                    fn4 = open('user_info.txt', 'a')
                    fn4.write(new_user + '\n')
                    fn4.write(new_password + '\n')
                    controller.show_frame(StartPage)
                else:
                    alredy_taken = tk.Label(self, text='The Username is alreay taken!', font = LARGE_FONT, fg = 'red', bg = 'light blue')
                    alredy_taken.pack()
                    flag = True
            else:
                if other_flag == True:
                    wrong_code.pack_forget()
                wrong_code = tk.Label(self, text='The code you entered is incorrect!',font = LARGE_FONT, fg = 'red', bg = 'light blue')
                wrong_code.pack()
                other_flag = True

class FilePrinterDialog(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(background='light blue')

        button2 = tk.Button(self, text="Back to Paramaters", highlightbackground=background,
                            font= bfont, command=lambda: controller.show_frame(PageTwo))
        button2.pack(side='bottom')






app = SeaofBTCapp()
app.mainloop()
