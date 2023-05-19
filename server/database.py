import sqlite3

conn = sqlite3.connect('./user.db')
c = conn.cursor()


# c.execute("""CREATE TABLE users(
#             email text,
#             password text,
#             publicKey text
#             )""")

# c.execute("INSERT INTO users VALUES('AAA@mail.com', '1234', '')")
# c.execute("INSERT INTO users VALUES('BBB@mail.com', '4321', '')")

def Get_User_By_Email(email):
    
    c.execute("SELECT * FROM users WHERE email=:email", {'email':email})
    return c.fetchone()
    


def CloseConnection():
    conn.close()