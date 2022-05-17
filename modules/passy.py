import secrets
import string	 
import sqlite3
import os
import time
import base64
import hashlib

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

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


#class Utils:
#    def password_generator(self):
#        alphabet = string.ascii_letters + string.digits
#        while True:
#    	    password = ''.join(secrets.choice(alphabet) for i in range(10))
#    	    if (any(c.islower() for c in password)
#                and any(c.isupper() for c in password)
#       	        and sum(c.isdigit() for c in password) >=3):
#                break
#        return password


#    def __init__(self):
#        alphabet = string.printable
#        phrase = "hola amigos!"
#        final_phrase = []
#        print("len of final phrase: " + str(len(final_phrase)))
#        
#        try:
#            while True:
#                for letter in alphabet:
#                    if letter != phrase[i] and len(final_phrase) != len(phrase):
#                        time.sleep(0.001)
#                        print(letter)
#                        continue
#
#                    else:
#                        final_phrase.append(letter)
#                        print(*final_phrase)
#                        time.sleep(0.2)
#                        os.system('cls')
#                        if i < len(phrase):
#                            i += 1
#                            continue
#        except IndexError:
#            print(*final_phrase)


class Passy:
    def encrypter(self, data, salt, userpassword): 
        kdf = PBKDF2HMAC(
                        algorithm=hashes.SHA256(),
                        length=32,
                        salt=bytes(salt, "UTF-8"),
                        iterations=390000
                        )

        key = base64.urlsafe_b64encode(kdf.derive(userpassword))
        f = Fernet(key)
        encrypted_data = f.encrypt(data)
        return encrypted_data

    def decrypter(self, data, salt, userpassword):
        kdf = PBKDF2HMAC(
                        algorithm=hashes.SHA256(),
                        length=32,
                        salt=bytes(salt, "UTF-8"),
                        iterations=390000
                        )

        key = base64.urlsafe_b64encode(kdf.derive(bytes(userpassword, "UTF-8")))
        f = Fernet(key)
        decrypted_data = f.decrypt(data)
        return decrypted_data

    def key_hasher(self, key):
        hashed_object = hashlib.sha256(key)
        hash_digest = hashed_object.hexdigest()
        return hash_digest

if __name__ == '__main__':
    crypto = Passy()
