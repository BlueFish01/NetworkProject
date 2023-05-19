from KeyGen import *
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad

publicKey,privateKey = KeyPairGenerator()

##working with pdf
datafile = open("contextDiagram.pdf",'rb')
pdfBytes = datafile.read()
datafile.close()

HashedPDF1 = SHA256.new(pdfBytes)

HashedPDF = HashedPDF1.digest()


HashedPDF = int.from_bytes(HashedPDF,'big')


print("before encrypting = ",HashedPDF)

encryptedPDF = DecryptPDF(privateKey,publicKey,HashedPDF)

print("encryptedPDF =",encryptedPDF)


# verifier

verifierHashedPDF = SHA256.new(pdfBytes)
verifierHashedPDF = verifierHashedPDF.digest()
verifierHashedPDF = int.from_bytes(verifierHashedPDF,'big')

encryptedPDF = EncryptPDF(publicKey,encryptedPDF)
print("after de = ",encryptedPDF)
print("verifier pdf= ",verifierHashedPDF)

#check
if(verifierHashedPDF==encryptedPDF):
    print("match")
else:
    print("not match")


##AES encryption


