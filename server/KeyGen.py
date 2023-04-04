import math
import random
import base64
import codecs

from Crypto.Util.number import getStrongPrime
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

#prime generator
p = getStrongPrime(512,e=0 ,false_positive_prob=1e-06, randfunc=get_random_bytes)
q = getStrongPrime(512,e=0 ,false_positive_prob=1e-06, randfunc=get_random_bytes)


n = p * q

phi = (p-1)*(q-1)
e = 2

while (e < phi):
    if(math.gcd(e, phi) == 1):
        break
    else:
        e = e+1

# Took from SO
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

d = modinv(e, phi)

result = (d*e)%phi

publicKey = base64.b64encode(bytes(str(n),'utf-8'))
privateKey = base64.b64encode(bytes(str(d),'utf-8'))


##Private Key
print("---RSA PRIVATE KEY---")
print(privateKey)
print("---RSA PRIVATE KEY---\n")

##PublicKey
print("---RSA PUBLIC KEY---")
print(publicKey)
print("---RSA PUBLIC KEY---\n")
print ("e =",e)

#test
def string_to_int(s):
    str = pad(s.encode(),8,style='pkcs7')
    print(str)
    return int.from_bytes(str, byteorder='little')


def int_to_string(i):
    length = math.ceil(i.bit_length() / 8)
    str = i.to_bytes(length, byteorder='little').decode()
    return str

message = "Hello123498ritug-fkcckckwe22@@@DFDS"

EnM = string_to_int(message) 
print(EnM)


pu = pow(EnM,e,mod=n)
print(pu)

pr = pow(pu,d,mod=n)
print(pr)

DcM = int_to_string(pr)
print(DcM)
