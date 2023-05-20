from KeyGen import *
from Crypto.Hash import SHA256
import os
import json


#check if keyFile is exits
def CheckFile():
    for root, dirs, files in os.walk('./'):
        for file in files:
            if file.endswith('.key'):
                return True

#check if keyFile is exits
def init():
    if not CheckFile():

        publicKey,privateKey = KeyPairGenerator()

        data = {"PrivateKey":privateKey.decode(),
                "PublicKey":publicKey.decode()}
        
        with open("Keypair.key","w+") as fileWriter:
            fileWriter.write(json.dumps(data))
        

