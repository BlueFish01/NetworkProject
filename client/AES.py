from Crypto.Cipher import AES
from dotenv import load_dotenv
import base64
import os


def AESencrypt(dataBytes):

    load_dotenv()

    key = os.getenv('SERVER_AES_KEY')

    keyBytes = base64.b64decode(key)

    if type(dataBytes) == str:
        data = base64.b64decode(dataBytes)
    if type(dataBytes) == bytes:
        data = dataBytes
        

    cipher = AES.new(keyBytes, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    file_out = open("./encrypted.bin", "wb+")
    [ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
    file_out.close()

def AESdecrypt(filepath):

    load_dotenv()

    key = os.getenv('SERVER_AES_KEY')

    keyBytes = base64.b64decode(key)

    file_in = open(filepath, "rb")
    nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
    file_in.close()

    # let's assume that the key is somehow available again
    cipher = AES.new(keyBytes, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    
    return data

