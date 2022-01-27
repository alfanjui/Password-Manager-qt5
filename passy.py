import secrets
import argparse 
import bcrypt
import string	 
import sqlite3
import os
import time
from cryptography.fernet import Fernet

class DBase:
    def __init__(self):
        if not os.path.isfile("master.db"):
            self.master_con = sqlite3.connect("master.db")
            self.master_cur = self.master_con.cursor()
            self.master_cur.execute('''CREATE TABLE IF NOT EXISTS crypted 
                                       (user TEXT NOT NULL PRIMARY KEY, master_password TEXT NOT NULL)''')
        else:
            print("Master database already exists")
            pass

class Passy:
    def delete_account(self):
        os.remove("databases/" + username + ".db")

    def password_generator(self):
        alphabet = string.ascii_letters + string.digits
        while True:
    	    password = ''.join(secrets.choice(alphabet) for i in range(10))
    	    if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
       	        and sum(c.isdigit() for c in password) >=3):
                break
        return password

    def hasher(self): 
        salt = bcrypt.gensalt(16)
        hashed = bcrypt.hashpw(pwd_to_hash, salt)
        return hashed


class Effects:
    def __init__(self):
        alphabet = string.printable
        i = 0
        phrase = "hola amigos!"
        final_phrase = []
        print("len of final phrase: " + str(len(final_phrase)))
        
        try:
            while True:
                for letter in alphabet:
                    if letter != phrase[i] and len(final_phrase) != len(phrase):
                        time.sleep(0.001)
                        print(letter)
                        continue

                    else:
                        final_phrase.append(letter)
                        print(*final_phrase)
                        time.sleep(0.2)
                        os.system('cls')
                        if i < len(phrase):
                            i += 1
                            continue
        except IndexError:
            print(*final_phrase)


if __name__ == '__main__':
    #key = Fernet.generate_key()
    #f = Fernet(key)
    #
    #encrypted_data = f.encrypt(b"boyyy")
    #print(encrypted_data)

    Effects()
            
