from typing_extensions import Annotated
from fastapi import FastAPI, Form
from database import Get_User_By_Email

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


