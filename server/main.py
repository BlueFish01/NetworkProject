from typing_extensions import Annotated
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse
from database import *
import json
import base64

app = FastAPI()

class userClass:
    def __init__(self,email,password):
        self.email = email
        self.password = password  

@app.get("/auth")
async def login(user: Annotated[str, Form()], password: Annotated[str, Form()]):
    if Get_User_By_Email(user):
        user_temp = Get_User_By_Email(user)
        userObj = userClass(user_temp[0],user_temp[1])
        if userObj.password == password:
            return ({'status':'Login success','user':userObj.email})

    return ({'status':'Login fail','user':False})

@app.post("/upload")
async def upload(PDF: UploadFile,data: Annotated[str,Form()],certificate: Annotated[str,Form()]):

    file_location = f"./PDF/{PDF.filename}"
    with open(file_location,"wb+") as file_object:
        file_object.write(PDF.file.read())

    dict = json.loads(data)
    
    uploadPDF(int(dict["TimeStamp"]),
              dict["Receiver"],
              dict["Sender"],
              str(f'{dict["TimeStamp"]}.pdf'),
              certificate)
    
    return {"data":dict["Sender"]}

@app.get("/inbox")
async def getInbox(user: Annotated[str, Form()]):
    inboxQuery = inbox(user)
    inbox_dict = {}
    for i in inboxQuery:
        inbox_dict[f'{str(i[0])}'] = i[2]
    
    return(inbox_dict)

@app.get("/download")
async def getPdfFile(id: Annotated[str, Form()]):
    pdfId = int(id)
    Data = pdfquery(pdfId)
    #send data
    DataDict = {"id":str(Data[0]),"receiver":Data[1],"sender":Data[2],"filePath":Data[3],"certificate":Data[4]}
    #send file

    pdf = open(f'./PDF/{DataDict["filePath"]}',"rb")
    pdfBytes = pdf.read()
    pdfStr = base64.b64encode(pdfBytes)

    File = pdfStr
    #send key
    key = getKey(DataDict["sender"])
    DataDict["key"] = key[0]

    
    return(DataDict,File)
    

    
