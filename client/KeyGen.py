import math
import base64

from Crypto.Util.number import getStrongPrime
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

e = 65537

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m

def string_to_int(s):
    str = s.encode()
    return int.from_bytes(str, byteorder='little')


def int_to_string(i):
    length = math.ceil(i.bit_length() / 8)
    str = i.to_bytes(length, byteorder='little').decode()
    return str

#MainFunction
def KeyPairGenerator():
    
    while(True):
        p = getStrongPrime(512,e=0 ,false_positive_prob=1e-06, randfunc=get_random_bytes)
        q = getStrongPrime(512,e=0 ,false_positive_prob=1e-06, randfunc=get_random_bytes)
        n = p * q
        phi = (p-1)*(q-1)
        if(math.gcd(e, phi) == 1):
            d = modinv(e, phi)
            publicKey = base64.b64encode(str(n).encode('utf-8'))
            privateKey = base64.b64encode(str(d).encode('utf-8'))
            print("\ne =",e,"\n" )
            ##PrivateKey
            print("---RSA PRIVATE KEY---")
            print(privateKey)
            print("---RSA PRIVATE KEY---\n")

            ##PublicKey
            print("---RSA PUBLIC KEY---")
            print(publicKey)
            print("---RSA PUBLIC KEY---\n")

            
            return publicKey,privateKey;
        else:
            continue

def EncryptText(publicKey,text):
    text = string_to_int(text)
    encryptedText = pow(text,e,mod=int(base64.b64decode(publicKey).decode('utf-8')))
    return encryptedText;

def DecryptText(privateKey,publicKey,encryptedText):
    text = pow(encryptedText,int(base64.b64decode(privateKey).decode('utf-8')),mod=int(base64.b64decode(publicKey).decode('utf-8')))
    return int_to_string(text)

def EncryptPDF(publicKey,text):
    encryptedText = pow(text,e,mod=int(base64.b64decode(publicKey).decode('utf-8')))
    return encryptedText;

def DecryptPDF(privateKey,publicKey,encryptedText):
    text = pow(encryptedText,int(base64.b64decode(privateKey).decode('utf-8')),mod=int(base64.b64decode(publicKey).decode('utf-8')))
    return text




