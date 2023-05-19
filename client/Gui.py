from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
import init
import requests
import json


root = Tk()
root.title("myGui")
root.resizable(False,False)

#display setting
w = 600 # Width 
h = 400 # Height
screen_width = root.winfo_screenwidth()  # Width of the screen
screen_height = root.winfo_screenheight() # Height of the screen

# Calculate Starting X and Y coordinates for Window
x = (screen_width/2) - (w/2)
y = (screen_height/2) - (h/2)


root.geometry('%dx%d+%d+%d' % (w, h, x, y))





# Authentication function
def Authentication(email,password): 

    #send api request to login
    url = "http://localhost:8000/auth"
    payload = {'user': email.get(),
    'password': password.get()}
    files=[]
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    session = json.loads(response.text)
    
    if not session["user"]:
        showinfo(
            title=session["status"],
            message='Invilid email or passowrd'
        )
        return
    else:
        showinfo(
            title="Welcome",
            message=session["status"]
        )
        #KeyGeneration and update Key on Database if necessary
        init.init()
        Login_frame.destroy()
        notebook.pack(fill=BOTH,expand=True)
        return 

# File selection function
def select_file():
    filetypes = (
        ('PDF files', '*.pdf'),
        ('All files', '*.*')
    )

    filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir='./',
        filetypes=filetypes)
    
    if filename :
        showinfo(
            title='Selected File',
            message=filename
        )
        imgPanel.pack(pady = 20)
        sign_button.pack(ipadx=10)
    else :
        showinfo(
            title='Error',
            message='No File is Selected'
        )

    

#<---- Create main frame to store pages ----->
Main_frame = Frame(root,)

#create login frame
Login_frame = Frame(Main_frame)
#<-----Loginpage components---->
#Add TextBox
email = StringVar()
password = StringVar()

#Add button
loginBtn = Button(Login_frame,text="Login",command=lambda: Authentication(email,password)).pack(side=BOTTOM,pady=25)

passwordBox = Entry(Login_frame,textvariable=password,show="*").pack(side=BOTTOM,pady=15)
emailBox = Entry(Login_frame,textvariable=email).pack(side=BOTTOM,pady=15)

emailLabel = Label(Login_frame,text="email",fg='#787878').place(x=205,y=205)
passwaordLabel = Label(Login_frame,text="password",fg='#787878').place(x=205,y=260)

#createNotebook to collect tabs
notebook = ttk.Notebook(Main_frame)
style = ttk.Style()
style.theme_create( "MyStyle", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [0, 0, 0, 0] } },
        "TNotebook.Tab": {"configure": {"padding": [100, 5] },}})
style.theme_use("MyStyle")
style.configure('TNotebook', tabposition='ne')

#create  Signframes inside notebook
SignPage_Frame = Frame(notebook)

open_button = Button(
    SignPage_Frame,
    text="Open a File",
    command=select_file
)

# Add pdf image
img = Image.open("pdf.png")
img = img.resize((100,100),Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)
imgPanel = Label(SignPage_Frame, image = img)

sign_button = Button(
    SignPage_Frame,
    text="Sign PDF",

)

open_button.pack(pady=50)


#create  Signframes inside notebook
VerifyPage_Frame = Frame(notebook)

notebook.add(SignPage_Frame,text= 'Sign')
notebook.add(VerifyPage_Frame,text= 'Verify')

Login_frame.pack(fill=BOTH,expand=True)
Main_frame.pack(fill=BOTH,expand=True)
    
    






#runing login age
root.mainloop()