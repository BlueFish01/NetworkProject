import sqlite3

conn = sqlite3.connect('./user.db')
c = conn.cursor()


# c.execute("""CREATE TABLE users(
#             email text,
#             password text,
#             publicKey text
#             )""")

# c.execute("""CREATE TABLE pdf(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             receiver text,
#             sender text,
#             filePath text,
#             certificate text
#             )""")

# conn.commit()


# c.execute("INSERT INTO users VALUES('AAA@mail.com', '1234', 'MTIzNDI1MzczNDkxMjc1OTY2MDQyMzYyODgxMTM3MDA2ODgzOTM5NjM3ODc4MzUxODgxMzU3MTAxMDkwMTQ5MDg2NjUxNzkzNTM4MTEwNTY4NjkzOTQ1MjQxMjA4NjU1NjE2Nzg5NTk0MzY4MTgwNjY0NDc4NTIzOTI0NDIwODY0MDk0NTA2NzU1OTY3NjQ1Mjk4MTYwNjgwODM3NDM4NTc1NTQ0Mzk1MDkyNzkzNjkxOTQ0ODcxNTE5NTAzNDE3OTQ5NTg1MDQ0MDkwMjY2ODg4MzIzMDExODQwMzkzMTM2MjE2ODIxODI1NDYxODQyNTc2NTcyOTY5MjgyODQ0MjA2MDc4MDM2NjkyNTIyOTAzOTU2NDA0MzY1NzcxMzA2ODMzNzg2ODQxMjc4ODA4MDkwMTEx')")
# c.execute("INSERT INTO users VALUES('BBB@mail.com', '4321', '')")

# conn.commit()
# conn.close()

def Get_User_By_Email(email):
    
    c.execute("SELECT * FROM users WHERE email=:email", {'email':email})
    return c.fetchone()

def uploadPDF(id,receiver,sender,filePath,certificate):
    c.execute("INSERT INTO pdf VALUES(?, ?, ?, ?, ?)",(id,receiver,sender,filePath,certificate))
    conn.commit()
    return

def inbox(receiver):
    c.execute("SELECT * FROM pdf WHERE receiver=:receiver",{'receiver':receiver})
    return c.fetchall()

def pdfquery(id):
    c.execute("SELECT * FROM pdf WHERE id=:id",{'id':id})
    return c.fetchone()

def getKey(sender):
    c.execute("SELECT publicKey FROM users WHERE email=:email",{'email':sender})
    return c.fetchone()

def CloseConnection():
    conn.close()