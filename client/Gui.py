from tkinter import *
from KeyGen import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
from Crypto.Hash import SHA256
import init
import requests
import json
import calendar
import time
import base64


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
    global session 
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

        global PdfPath
        PdfPath = filename
        return PdfPath
    
    else :
        showinfo(
            title='Error',
            message='No File is Selected'
        )

#function to sign PDF
def SignPDF():
    
    if PdfPath :
        PdfFile = open(PdfPath,'rb') 
        PdfBytes = PdfFile.read()
        PdfFile.close()
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)
       
        #prepare data_dict that will be encrypted
        datablock = {'Pdf':PdfBytes,'Sender':session["user"],'Receiver': 'BBB@mail.com', 'TimeStamp':time_stamp}
        datablock_str = str(datablock)
        datablock_ascii = datablock_str.encode('ascii')
        datablock_byte = base64.b64encode(datablock_ascii)

        HashedData0 = SHA256.new(datablock_byte)
        HashedData1 = HashedData0.digest()
        HashDataInt = int.from_bytes(HashedData1,'big')
        
        #encrypt hashed pdf
        file = open('./Keypair.key','r')
        data = file.read()
        data_dict = json.loads(data)
        Pk = data_dict["PrivateKey"]
        Pu = data_dict["PublicKey"]
        BytesPk = bytes(Pk,'utf-8')
        BytesPu = bytes(Pu,'utf-8')

        encryptHashData = EncryptPDF(BytesPk,BytesPu,HashDataInt)

        payloadBlock = {"Sender":session["user"],"Receiver": "BBB@mail.com", "TimeStamp":time_stamp}
        
        #send post request to upload file

        url = "http://localhost:8000/upload"

        payload = {'data': json.dumps(payloadBlock),
                    'certificate': hex(encryptHashData)}
        
        files=[
        ('PDF',(f'{time_stamp}.pdf',open(PdfPath,'rb'),'application/pdf'))
        ]
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        print(response.text)

    else :
        print ("Path is not defined")
        return

#Verify function 
def VerifyThis(id):
    url = "http://localhost:8000/download"

    payload = {'id': id}
    files=[
    ]
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    
   
    
    datatemp = json.loads(response.text)
    
    pdfBytes = base64.b64decode(datatemp[1])

    dataDict = datatemp[0]

    datablock = {'Pdf':pdfBytes,'Sender':dataDict["sender"],'Receiver': dataDict["receiver"], 'TimeStamp': int(dataDict["id"])}
    datablock_str = str(datablock)
    datablock_ascii = datablock_str.encode('ascii')
    datablock_byte = base64.b64encode(datablock_ascii)

    HashedData0 = SHA256.new(datablock_byte)
    HashedData1 = HashedData0.digest()
    HashDataInt = int.from_bytes(HashedData1,'big')
    
    certificate = int(dataDict["certificate"],16)
    key = dataDict["key"]
    Pu = bytes(key,'utf-8')
    DecryptedCertificate = DecryptPDF(Pu,int(certificate))

    if(HashDataInt == DecryptedCertificate):

        with open(f'./Download/{dataDict["filePath"]}',"wb+") as file_object:
            file_object.write(pdfBytes)

        #send delete request via API

        showinfo(
            title='verified',
            message= f'The Pdf is Verified \n from: {dataDict["sender"]} \n To: {dataDict["receiver"]} \n timestamp: {dataDict["id"]}'
        )

    

    return   

def VerifyPDF():

    url = "http://localhost:8000/inbox"

    payload = {'user': session["user"]}
    files=[

    ]
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload, files=files)

    Inboxdict = json.loads(response.text)

    for key, value in Inboxdict.items():
        Button(VerifyPage_Frame,text="From: "f'{value}'"\n id :"f'{key}',command=lambda: VerifyThis({key})).pack(pady=10)   
    
    return



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
    command = SignPDF
)

open_button.pack(pady=50)


#create  Verifyframes inside notebook
VerifyPage_Frame = Frame(notebook)

notebook.add(SignPage_Frame,text= 'Sign')
notebook.add(VerifyPage_Frame,text= 'Verify')



def on_tab_change(event):
    tab = event.widget.tab('current')['text']
    if tab == 'Verify':
        
        inboxLabel = Label(VerifyPage_Frame,text="inbox",fg='#787878',font=('Georgia 20'))
        inboxLabel.pack(pady=15)
        VerifyPDF()
        
        return
    elif tab == 'Sign':

        for widget in VerifyPage_Frame.winfo_children():
            widget.destroy()
        return

notebook.bind('<<NotebookTabChanged>>', on_tab_change)



Login_frame.pack(fill=BOTH,expand=True)
Main_frame.pack(fill=BOTH,expand=True)
    
    






#runing login age
root.mainloop()