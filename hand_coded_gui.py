import sys, os, base64
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

from modules import passy
import sqlite3

#background-color = "#FBE698"

style = '''*{background-color: #FBE698;
        border: 4px solid #6DECE0;
        border-radius: 15px;
        font-size: 20px;
        color: #15B5B0;
        padding: 5px;}
        *:hover{background: #6DECE0; color: black;}'''

background_style = "background: #F9BDC0;"

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        
        #CODE BODY
        self.setWindowTitle("Password Manager")
        self.setStyleSheet(background_style)
        self.setFixedWidth(400)
        self.setFixedHeight(300)

        self.welcome_banner = qtw.QLabel('Password Manager!')
        self.welcome_banner.setStyleSheet(
                "font-size: 30px;" +
                "color: ;" +
                "margin-top: 20px;"
                )
        self.welcome_banner.setAlignment(qtc.Qt.AlignCenter)

        self.main_login_button = qtw.QPushButton( # Login button
                "Login",
                clicked=self.change_to_login
                )
        self.main_login_button.setStyleSheet(style) 
        self.main_login_button.setCursor(qtg.QCursor(qtc.Qt.PointingHandCursor)) 

        self.signup_button = qtw.QPushButton( # Register button
                "Sign up",
                clicked=self.change_to_signup
                )
        self.signup_button.setStyleSheet(style)

        self.config_button = qtw.QPushButton( # Configuration button
                "Configuration",
                clicked=self.change_to_config
                )
        self.config_button.setStyleSheet(style)
        self.config_button.setCursor(qtg.QCursor(qtc.Qt.PointingHandCursor))

        ########## LAYOUT #############
        grid = qtw.QGridLayout()

        ########## WIDGET #############
        grid.addWidget(self.welcome_banner, 0, 0)
        grid.addWidget(self.main_login_button, 1, 0)
        grid.addWidget(self.signup_button, 2, 0)
        grid.addWidget(self.config_button, 3, 0)
        self.setLayout(grid)

        self.show()

    def change_to_signup(self):
        self.signup_dialog = SignupWindow()
        self.hide()
        self.signup_dialog.show()

    def change_to_login(self):
        self.login_dialog = DialogWindow()
        self.hide()
        self.login_dialog.show()

    def change_to_config(self):
        self.config_dialog = ConfigWindow()
        self.config_dialog.show()

    def open_file(self):
        filename, _ = qtw.QFileDialog.getOpenFileName()
        if filename:
            with open(filename, 'r') as handle:
                text = handle.read()


class DialogWindow(qtw.QWidget):
    submitted = qtc.pyqtSignal(str, str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #CODE BODY
        self.setWindowTitle("Password Manager")
        self.setStyleSheet(background_style)
        self.setFixedWidth(400)
        self.setFixedHeight(300)

        self.username_input = qtw.QLineEdit()
        self.username_input.setStyleSheet(style)

        self.password_input = qtw.QLineEdit()
        self.password_input.setEchoMode(qtw.QLineEdit.Password)
        self.password_input.setStyleSheet(style)

        self.salt_input = qtw.QLineEdit()
        self.salt_input.setEchoMode(qtw.QLineEdit.Password)
        self.salt_input.setStyleSheet(style)

        self.cancel_button = qtw.QPushButton(
                'Cancel',
                clicked=self.change_to_main
                )
        self.cancel_button.setStyleSheet(style)
 
        self.login_button  = qtw.QPushButton(
                'Login',
                clicked=self.authenticate
                )
        self.login_button.setStyleSheet(style)

        #LAYOUT
        layout = qtw.QGridLayout()
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)

        button_widget = qtw.QWidget()
        button_widget.setLayout(qtw.QHBoxLayout())
        button_widget.layout().addWidget(self.cancel_button)
        button_widget.layout().addWidget(self.login_button)

        layout.addWidget(button_widget)
        self.setLayout(layout)

        #BUTTONS
        self.username_input.textChanged.connect(self.set_button_text)

    @qtc.pyqtSlot(str)
    def set_button_text(self, text):
        if text:
            self.login_button.setText(f'Log in {text}')
        else:
            self.login_button.setText('Log In')

    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if len(username)==0 or len(password)==0:
            qtw.QMessageBox.critical(self, 'Error', 'Please fill all the fields')

        if os.path.isfile(str(username) + ".db"):
            hashed_password = passy.Passy.key_hasher(self, bytes(password, "UTF-8"))
            con = sqlite3.connect("master.db")
            cur = con.cursor()
            cur.execute('''SELECT user, master_password FROM crypted 
                        WHERE user=?''', (username,))
            userdata_checked = cur.fetchone()
            user_salt = userdata_checked[1]
            db_password = userdata_checked[1]
            user_salt = user_salt[:24]
            db_password = db_password[24:]

            if userdata_checked[0] == username and db_password == hashed_password:
                qtw.QMessageBox.information(self, 'Access granted', 'Access granted')
                with open(username + ".db", 'rb') as f:
                    data = f.read()
                    decrypted_data = passy.Passy.decrypter(self, data, user_salt, password)

                with open(str(username)+".db", 'wb') as d:
                    d.write(decrypted_data)

                self.change_to_table(username)

            else:
                qtw.QMessageBox.critical(self, 'Error', 'Credentials given are not correct')
                print(db_password)
                print(user_salt)
                print(hashed_password)
        else:
            qtw.QMessageBox.critical(self, 'Error', "Database doesn't exist")
            print("DB does not exist")

    def change_to_main(self):
        self.main_window = MainWindow()
        self.close()
        self.main_window.show()

    def change_to_table(self, user):
        self.table_window = TableWindow(user=user)
        self.close()
        self.table_window.show()


class TableWindow(qtw.QWidget):
    def __init__(self, user=None):
        self.user = user

        super().__init__()
        
        #CODE BODY
        self.setWindowTitle(str(self.user) + "'s" + " Database")
        self.setStyleSheet(background_style)
        self.setFixedWidth(1000)
        self.setFixedHeight(400)

        self.password_table = qtw.QTableWidget()
        self.password_table.setColumnCount(4)
        self.password_table.setRowCount(40)
        self.password_table.setHorizontalHeaderLabels(['Network', 'Username', 'E-Mail', 'Password'])

        self.add_network_button = qtw.QPushButton(
                "Add Network",
                clicked=lambda:self.change_to_add_network(self.user)
                )
        self.add_network_button.setStyleSheet(style)
        
        self.logout_button = qtw.QPushButton(
                "Logout",
                clicked=self.change_to_main
                )
        self.logout_button.setStyleSheet(style)

        self.connection_to_db(self.user) 

        #LAYOUT
        table_layout = qtw.QVBoxLayout()
        table_layout.addWidget(self.password_table)
        table_layout.addWidget(self.logout_button) 
        table_layout.addWidget(self.add_network_button)
        self.setLayout(table_layout)

    def apply_user_data(self, data):
        col = 0
        row = 0

        for i in data:
            for x in i:
                if col < 4:
                    self.password_table.setItem(row, col, qtw.QTableWidgetItem(x))
                    col += 1
                    continue
                else:
                    break
            row += 1
            col = 0
        
    def connection_to_db(self, user):
        con = sqlite3.connect(str(self.user) + ".db")
        cur = con.cursor()
        cur.execute("SELECT * FROM CREDENTIALS")
        data = cur.fetchall()
        print("data before apply")
        self.apply_user_data(data) 
        print(data)
        con.close()

    def change_to_add_network(self, user):
        self.add_window = AddNetwork(user=user)
        self.close()
        self.add_window.show()

    def change_to_main(self):
        self.main_window = MainWindow()
        self.close()
        self.main_window.show()


class AddNetwork(qtw.QWidget):
    def __init__(self, user=None):
        self.user = user

        super().__init__()

        #CODE BODY
        self.setWindowTitle("Register new Network in Database")
        self.setStyleSheet(background_style)
        self.setFixedWidth(400)    
        self.setFixedHeight(300)
        
        self.add_network_input = qtw.QLineEdit()
        self.add_network_input.setText("Network")
        self.add_network_input.setStyleSheet(style)

        self.add_username_input = qtw.QLineEdit()
        self.add_username_input.setText("Username")
        self.add_username_input.setStyleSheet(style)

        self.add_email_input= qtw.QLineEdit()
        self.add_email_input.setText("E-Mail")
        self.add_email_input.setStyleSheet(style)

        self.add_password_input = qtw.QLineEdit()
        self.add_password_input.setText("Password")
        self.add_password_input.setEchoMode(qtw.QLineEdit.Password)
        self.add_password_input.setStyleSheet(style)

        self.back_button = qtw.QPushButton(
                "Back to menu",
                clicked=self.go_back
                )
        self.back_button.setStyleSheet(style)

        self.register_button = qtw.QPushButton(
                "Register",
                clicked=lambda:self.register_network_in_userDB(self.user)
                )
        self.register_button.setStyleSheet(style)

        #LAYOUT
        self.buttons_widget = qtw.QWidget()
        self.buttons_widget.setLayout(qtw.QHBoxLayout())
        self.buttons_widget.layout().addWidget(self.back_button)
        self.buttons_widget.layout().addWidget(self.register_button)

        self.layout = qtw.QVBoxLayout()
        self.layout.addWidget(self.add_network_input)
        self.layout.addWidget(self.add_username_input)
        self.layout.addWidget(self.add_email_input)
        self.layout.addWidget(self.add_password_input)
        self.layout.addWidget(self.buttons_widget)
         
        self.setLayout(self.layout)

    def go_back(self):
        table_window = TableWindow(user=self.user)
        self.close()
        table_window.show() 

    def register_network_in_userDB(self, user):
        con = sqlite3.connect(str(user) + ".db")
        cur = con.cursor()

        network_text = self.add_network_input.text()
        user_text = self.add_username_input.text()
        email_text = self.add_email_input.text()
        pass_text = self.add_password_input.text()

        if len(network_text)==0 or len(user_text)==0 or len(email_text)==0 or len(pass_text)==0:
            qtw.QMessageBox.critical(self, 'Error', 'Please fill up all the fields :)')
        else:
            cur.execute("INSERT INTO CREDENTIALS VALUES(?, ?, ?, ?)", (str(network_text), str(user_text), str(email_text), str(pass_text)))
            con.commit()
            print("Personal Query succesfully executed")
            con.close()

            registered_message_box = qtw.QMessageBox()
            registered_message_box.setIcon(qtw.QMessageBox.Information)
            registered_message_box.setText("Data succesfully saved!")
            registered_message_box.exec_()

            self.go_back()

class SignupWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        #CODE BODY
        self.setWindowTitle("Password Manager")
        self.setStyleSheet(background_style)
        self.setFixedWidth(400)
        self.setFixedHeight(300)

        self.username_signup_input = qtw.QLineEdit()
        self.username = self.username_signup_input.text()
        self.username_signup_input.setStyleSheet(style)

        self.password_signup_input = qtw.QLineEdit()
        self.password_signup_input.setEchoMode(qtw.QLineEdit.Password)
        self.password = self.password_signup_input.text()
        self.password_signup_input.setStyleSheet(style)

        self.back_button = qtw.QPushButton(
                "Back to menu",
                clicked=self.change_to_main
                )
        self.back_button.setStyleSheet(style)

        self.register_button = qtw.QPushButton(
                "Register",
                clicked=self.register_in_masterDB
                )
        self.register_button.setStyleSheet(style)

        #LAYOUT
        self.buttons_widget = qtw.QWidget()
        self.buttons_widget.setLayout(qtw.QHBoxLayout())
        self.buttons_widget.layout().addWidget(self.back_button)
        self.buttons_widget.layout().addWidget(self.register_button)

        self.layout = qtw.QVBoxLayout()
        self.layout.addWidget(self.username_signup_input)
        self.layout.addWidget(self.password_signup_input)
        self.layout.addWidget(self.buttons_widget)
         
        self.setLayout(self.layout)

    def change_to_main(self):
        self.main_window = MainWindow()
        self.close()
        self.main_window.show()

    def register_in_masterDB(self):
        user_text = self.username_signup_input.text()
        pass_text = bytes(self.password_signup_input.text(), "UTF-8")
        user_salt = base64.b64encode(os.urandom(16)).decode('utf-8') 

        if len(user_text)==0 and len(pass_text)==0:
            qtw.QMessageBox.critical(self, 'Error', 'Please fill up all the fields :)')

        if not os.path.isfile(str(user_text)+".db"):
            con = sqlite3.connect("master.db")
            cur = con.cursor()

            encrypted_password = passy.Passy.key_hasher(self, pass_text)
            pass_and_salt = user_salt + encrypted_password
            print(user_salt)
            print(pass_and_salt)

            cur.execute("INSERT INTO crypted VALUES(?, ?)", (str(user_text), str(pass_and_salt)))
            con.commit()
            print("Query succesfully executed")
            con.close()

            user_DB_con = sqlite3.connect(str(user_text) + ".db")
            user_DB_con.execute('''CREATE TABLE IF NOT EXISTS CREDENTIALS(
                                network TEXT NOT NULL PRIMARY KEY,
                                user TEXT NOT NULL,
                                'e-mail' TEXT NOT NULL,
                                password TEXT NOT NULL)''')

            with open(str(user_text)+".db", 'rb') as f:
                data = f.read()
                encrypted_data = passy.Passy.encrypter(self, data, user_salt, pass_text)

            with open(str(user_text)+".db", 'wb') as e:
                e.write(encrypted_data)

            registered_message_box = qtw.QMessageBox()
            registered_message_box.setIcon(qtw.QMessageBox.Information)
            registered_message_box.setText("Account succesfully created and encrypted")
            registered_message_box.exec_()

            self.change_to_main()

        else: 
            qtw.QMessageBox.critical(self, 'Error', 'This user already exists')


class ConfigWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        #CODE BODY
        self.animation_checkbox = qtw.QCheckBox('Turn off animations')
        self.save_changes_button = qtw.QPushButton(
                'Save changes'
                )

        #LAYOUT
        self.setLayout(qtw.QFormLayout())
        self.layout().addRow(self.animation_checkbox)
        self.layout().addRow(self.save_changes_button)


if __name__ == '__main__':
    passy.DBase()

    app = qtw.QApplication(sys.argv)
    mainw = MainWindow()

    sys.exit(app.exec_())
