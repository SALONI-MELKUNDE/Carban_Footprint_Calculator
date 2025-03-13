import os
import sys
from ctypes import windll

import pymysql
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal

import mysql.connector 
import MySQLdb as mdb
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from carbonFootprint.carbon_footprint import CarbonFootprintCalculator


class Ui_Form(CarbonFootprintCalculator):
    def __init__(self):
        QWidget.__init__(self)
        super(CarbonFootprintCalculator, self).__init__()
        self.setObjectName("Form")
        self.resize(625, 565)
        self.widget = QtWidgets.QWidget(self)
        self.widget.setGeometry(QtCore.QRect(30, 30, 550, 500))
        self.widget.setStyleSheet("QPushButton#login, #register, #pushButton_7{\n"
                                  "    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(11, 131, 120, 219), stop:1 rgba(85, 98, 112, 226));\n"
                                  "    color:rgba(255, 255, 255, 210);\n"
                                  "    border-radius:5px;\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton#login:hover, #register:hover, #pushButton_7:hover{\n"
                                  "    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(150, 123, 111, 219), stop:1 rgba(85, 81, 84, 226));\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton#login:pressed, #register:pressed, #pushButton_7:pressed{\n"
                                  "    padding-left:5px;\n"
                                  "    padding-top:5px;\n"
                                  "    background-color:rgba(150, 123, 111, 255);\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton#pushButton_2, #pushButton_3, #pushButton_4, #pushButton_5{\n"
                                  "    background-color: rgba(0, 0, 0, 0);\n"
                                  "    color:rgba(85, 98, 112, 255);\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton#pushButton_2:hover, #pushButton_3:hover, #pushButton_4:hover, #pushButton_5:hover{\n"
                                  "    color: rgba(131, 96, 53, 255);\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton#pushButton_2:pressed, #pushButton_3:pressed, #pushButton_4:pressed, #pushButton_5:pressed{\n"
                                  "    padding-left:5px;\n"
                                  "    padding-top:5px;\n"
                                  "    color:rgba(91, 88, 53, 255);\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton#forgot_btn{\n"
                                  "    background-color: rgba(0, 0, 0, 0);\n"
                                  "    color:rgba(85, 98, 112, 255);\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton#forgot_btn:hover{\n"
                                  "    color: rgba(131, 96, 53, 255);\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton#forgot_btn:pressed{\n"
                                  "    padding-left:5px;\n"
                                  "    padding-top:5px;\n"
                                  "    color:rgba(91, 88, 53, 255);\n"
                                  "}\n"
                                  "\n"
                                  "")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(40, 30, 280, 430))
        # border_image = QPixmap("images/carbonfootprint_login.png")
        # self.label.setStyleSheet(f"border-image: url({border_image});\n"
        #                          "border-top-left-radius: 50px;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(40, 30, 280, 430))
        self.label_2.setStyleSheet("background-color:rgba(0, 0, 0, 300);\n"
                                   "border-top-left-radius: 50px;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(270, 30, 240, 430))
        self.label_3.setStyleSheet("background-color:rgba(255, 255, 255, 255);\n"
                                   "border-bottom-right-radius: 50px;")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.widget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(318, 383, 141, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Social Media Circled")
        font.setPointSize(15)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Social Media Circled")
        font.setPointSize(15)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_4.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Social Media Circled")
        font.setPointSize(15)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.pushButton_5 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_5.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Social Media Circled")
        font.setPointSize(15)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout.addWidget(self.pushButton_5)
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setGeometry(QtCore.QRect(40, 80, 230, 130))
        self.label_6.setStyleSheet("background-color:rgba(0, 0, 0, 75);")
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.title = QtWidgets.QLabel(self.widget)
        self.title.setGeometry(QtCore.QRect(50, 80, 210, 100))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(60)
        self.title.setFont(font)
        self.title.setStyleSheet("color:rgba(255, 255, 255, 200);")
        self.title.setObjectName("title")
        self.title.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.welcome_message = QtWidgets.QLabel(self.widget)
        self.welcome_message.setGeometry(QtCore.QRect(50, 165, 220, 160))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(60)
        self.welcome_message.setFont(font)
        self.welcome_message.setStyleSheet("color:rgba(255, 255, 255, 170);")
        self.welcome_message.setObjectName("welcome_message")
        self.widget_3 = QtWidgets.QWidget(self.widget)
        self.widget_3.setGeometry(QtCore.QRect(280, 70, 220, 315))
        self.widget_3.setObjectName("widget_3")
        self.label_9 = QtWidgets.QLabel(self.widget_3)
        self.label_9.setGeometry(QtCore.QRect(50, 10, 121, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("color:rgba(0, 0, 0, 200);")
        self.label_9.setObjectName("label_9")
        self.username_reg = QtWidgets.QLineEdit(self.widget_3)
        self.username_reg.setGeometry(QtCore.QRect(15, 110, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.username_reg.setFont(font)
        self.username_reg.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                        "border:none;\n"
                                        "border-bottom:2px solid rgba(46, 82, 101, 200);\n"
                                        "color:rgba(0, 0, 0, 240);\n"
                                        "padding-bottom:7px;")
        self.username_reg.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.username_reg.setObjectName("username_reg")
        self.first_name_reg = QtWidgets.QLineEdit(self.widget_3)
        self.first_name_reg.setGeometry(QtCore.QRect(15, 60, 85, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.first_name_reg.setFont(font)
        self.first_name_reg.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                          "border:none;\n"
                                          "border-bottom:2px solid rgba(46, 82, 101, 200);\n"
                                          "color:rgba(0, 0, 0, 240);\n"
                                          "padding-bottom:7px;")
        self.first_name_reg.setObjectName("first_name_reg")
        self.register = QtWidgets.QPushButton(self.widget_3)
        self.register.setGeometry(QtCore.QRect(15, 260, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.register.setFont(font)
        self.register.setObjectName("register")
        self.user_role = QtWidgets.QComboBox(self.widget_3)
        self.user_role.setGeometry(QtCore.QRect(120, 60, 85, 40))
        self.user_role.addItems(["User", "Admin"])
        self.user_role.setCurrentIndex(0)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.user_role.setFont(font)
        self.user_role.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                         "border:none;\n"
                                         "border-bottom:2px solid rgba(46, 82, 101, 200);\n"
                                         "color:rgba(0, 0, 0, 240);\n"
                                         "padding-bottom:7px;")
        self.user_role.setObjectName("user_role")
        self.password_reg = QtWidgets.QLineEdit(self.widget_3)
        self.password_reg.setGeometry(QtCore.QRect(15, 160, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.password_reg.setFont(font)
        self.password_reg.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                        "border:none;\n"
                                        "border-bottom:2px solid rgba(46, 82, 101, 200);\n"
                                        "color:rgba(0, 0, 0, 240);\n"
                                        "padding-bottom:7px;")
        self.password_reg.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_reg.setObjectName("password_reg")
        self.con_pass_reg = QtWidgets.QLineEdit(self.widget_3)
        self.con_pass_reg.setGeometry(QtCore.QRect(15, 210, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.con_pass_reg.setFont(font)
        self.con_pass_reg.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                        "border:none;\n"
                                        "border-bottom:2px solid rgba(46, 82, 101, 200);\n"
                                        "color:rgba(0, 0, 0, 240);\n"
                                        "padding-bottom:7px;")
        self.con_pass_reg.setEchoMode(QtWidgets.QLineEdit.Password)
        self.con_pass_reg.setObjectName("con_pass_reg")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setGeometry(QtCore.QRect(280, 70, 220, 315))
        self.widget_2.setObjectName("widget_2")
        self.label_4 = QtWidgets.QLabel(self.widget_2)
        self.label_4.setGeometry(QtCore.QRect(60, 10, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:rgba(0, 0, 0, 200);")
        self.label_4.setObjectName("label_4")
        self.password = QtWidgets.QLineEdit(self.widget_2)
        self.password.setGeometry(QtCore.QRect(15, 145, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.password.setFont(font)
        self.password.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                    "border:none;\n"
                                    "border-bottom:2px solid rgba(46, 82, 101, 200);\n"
                                    "color:rgba(0, 0, 0, 240);\n"
                                    "padding-bottom:7px;")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.username = QtWidgets.QLineEdit(self.widget_2)
        self.username.setGeometry(QtCore.QRect(15, 80, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.username.setFont(font)
        self.username.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
                                    "border:none;\n"
                                    "border-bottom:2px solid rgba(46, 82, 101, 200);\n"
                                    "color:rgba(0, 0, 0, 240);\n"
                                    "padding-bottom:7px;")
        self.username.setObjectName("username")
        self.login = QtWidgets.QPushButton(self.widget_2)
        self.login.setGeometry(QtCore.QRect(15, 225, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.login.setFont(font)
        self.login.setObjectName("login")
        self.forgot_btn = QtWidgets.QPushButton(self.widget_2)
        self.forgot_btn.setGeometry(QtCore.QRect(21, 275, 181, 16))
        self.forgot_btn.setObjectName("forgot_btn")
        self.pushButton_7 = QtWidgets.QPushButton(self.widget)
        self.pushButton_7.setGeometry(QtCore.QRect(270, 80, 30, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setStyleSheet("border-radius:0px;\n"
                                        "border-top-right-radius:15px;\n"
                                        "border-bottom-right-radius:15px;")
        self.pushButton_7.setCheckable(True)
        self.pushButton_7.setObjectName("pushButton_7")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.login.clicked.connect(self.open_carbonfootprint)
        self.register.clicked.connect(self.register_details)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_2.setText(_translate("Form", "E"))
        self.pushButton_3.setText(_translate("Form", "D"))
        self.pushButton_4.setText(_translate("Form", "M"))
        self.pushButton_5.setText(_translate("Form", "C"))
        self.title.setText(_translate("Form", "CARBON FOOTPRINT\nCALCULATOR"))
        self.welcome_message.setText(_translate("Form",
                                                "Welcome to the Carbon Footprint\nCalculator!\n\nThis tool helps you understand and\nreduce your carbon footprint.\nEvery small action counts toward a\nhealthier planet.\nCalculate your emissions, get insights,\nand track your impact with tables\n& charts  for a sustainable future."))
        self.label_9.setText(_translate("Form", "Register"))
        self.username_reg.setPlaceholderText(_translate("Form", "  User Name"))
        self.first_name_reg.setPlaceholderText(_translate("Form", "  Name"))
        self.register.setText(_translate("Form", "R e g i s t e r"))
        self.user_role.setPlaceholderText(_translate("Form", "  Role"))
        self.password_reg.setPlaceholderText(_translate("Form", "  Password"))
        self.con_pass_reg.setPlaceholderText(_translate("Form", "  Confirm Password"))
        self.label_4.setText(_translate("Form", "Log In"))
        self.password.setPlaceholderText(_translate("Form", "  Password"))
        self.username.setPlaceholderText(_translate("Form", "  User Name"))
        self.login.setText(_translate("Form", "L o g  I n"))
        self.forgot_btn.setText(_translate("Form", "Forgot your User Name or password?"))
        self.pushButton_7.setText(_translate("Form", ">"))

    # def open_carbonfootprint(self):
    #     self.register.blockSignals(True)
    #     self.login.blockSignals(True)
    #
    #     # print("yes")
    #     try:
    #         username = self.username.text()
    #         password = self.password.text()
    #         # db = DatabaseThread(username, password)
    #         # db.run()
    #         mydb = mysql.connector.connect(
    #             host="localhost",
    #             user="",
    #             password=""
    #             database="mydbcf"
    #         )
    #         mycursor = mydb.cursor()
    #         mycursor.execute("select * from login_table where User='"+ username + "' and Password='"+ password + "'")
    #         result = mycursor.fetchone()
    #
    #         if result:
    #             print("entered")
    #             # cfc = CarbonFootprintCalculator()
    #             self.close()
    #             # cfc.show()
    #         else:
    #             print("Username/Password Incorrect")
    #     except mysql.connector.Error as e:
    #         print(f"Database not connected{e}")
    #     self.login.blockSignals(False)
    #     self.register.blockSignals(False)
    #
    # def register_details(self):
    #     try:
    #         username = self.username_reg.text()
    #         password = self.password_reg.text()
    #         role = self.user_role.currentText()
    #         mydb = mysql.connector.connect(host="localhost", user="root", password="25062000", database="mydbcf")
    #         mycursor = mydb.cursor()
    #         mycursor.execute("select * from login_table where User='" + username + "' and Password='" + password + "'")
    #         result = mycursor.fetchone()
    #
    #         if result:
    #             print("Already exists")
    #         else:
    #             mycursor.execute("insert into table values('" + username +"', '" + password +"', '" + role +"')")
    #             mydb.commit()
    #     except mysql.connector.Error as e:
    #         print("Database not connected")

    def open_carbonfootprint(self):
        self.register.blockSignals(True)
        self.login.blockSignals(True)

        try:
            username = self.username.text()
            password = self.password.text()

            mydb = pymysql.connect(
                host="sql.freedb.tech",
                user="freedb_saloni",
                password="Xyk$b8T!MNGQh&T",
                database="freedb_mydbcf"
            )
            print("Successfully connected")
            mycursor = mydb.cursor()
            print("Fetched cursor")

            # Using parameterized query to prevent SQL injection
            query = "SELECT * FROM login_table WHERE User=%s AND Password=%s"
            mycursor.execute(query, (username, password))
            result = mycursor.fetchone()
            role = result[2]

            

            if result:
                print("Login successful")
                cfc = CarbonFootprintCalculator(username, role)
                self.close()
                cfc.showMaximized()
            else:
                QMessageBox.about(self, 'Login Error', 'Username/Password Incorrect')
                print("Username/Password Incorrect")

            mydb.close()  # Always close the database connection after use
        except mdb.Error as e:
            print(f"Database not connected: {e}")
        finally:
            self.login.blockSignals(False)
            self.register.blockSignals(False)

    # def open_carbonfootprint(self):
    #     chrome_options = Options()
    #     chrome_options.add_argument("--headless")
    #     chrome_options.add_argument("--disable-gpu")
    #
    #     # Specify the path to your ChromeDriver
    #     service = Service('chromedriver.exe')  # Replace with your ChromeDriver path
    #
    #     # Initialize the WebDriver
    #     driver = webdriver.Chrome(service=service, options=chrome_options)
    #
    #     # Navigate to the URL
    #     driver.get('http://smmydomain.infinityfreeapp.com/database_api.php?operation=read&table=login_table')
    #
    #     # Get page source or response content
    #     content = driver.page_source
    #
    #     # Extract the JSON part from the content
    #     start = content.find('[')
    #     end = content.rfind(']') + 1
    #
    #     if start != -1 and end != -1:
    #         json_data = content[start:end]
    #         try:
    #             parsed_data = json.loads(json_data)  # Parse the JSON string into Python data
    #             print(parsed_data)  # Print or use the parsed data
    #             # print(type(parsed_data))
    #         except json.JSONDecodeError:
    #             print("Failed to parse JSON data")
    #     else:
    #         print("JSON data not found in the response")
    #
    #     # Close the browser
    #     driver.quit()

    def register_details(self):
        try:
            username = self.username_reg.text()
            password = self.password_reg.text()
            role = self.user_role.currentText()

            # mydb = mdb.connect(
            #     host="localhost",
            #     user="root",
            #     password="25062000",
            #     database="mydbcf"
            # )

            mydb = pymysql.connect(
                host="sql.freedb.tech",
                user="freedb_saloni",
                password="Xyk$b8T!MNGQh&T",
                database="freedb_mydbcf"
            )

            mycursor = mydb.cursor()

            # Check if user already exists
            check_query = "SELECT * FROM login_table WHERE User=%s"
            mycursor.execute(check_query, (username,))
            result = mycursor.fetchone()

            if result:
                QMessageBox.about(self, 'Registration', 'User already exists')
                print("User already exists")
            else:
                # Using parameterized query for insertion
                insert_query = "INSERT INTO login_table (User, Password, Role) VALUES (%s, %s, %s)"
                mycursor.execute(insert_query, (username, password, role))
                mydb.commit()
                print("User registered successfully")

            mydb.close()  # Close the database connection after use
        except mdb.Error as e:
            print(f"Database not connected: {e}")


class LoginApp(Ui_Form):

    def __init__(self):
        super(LoginApp, self).__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.label.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0))
        self.label_3.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0))
        self.login.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=3, yOffset=3))
        self.register.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=3, yOffset=3))

        self.widget_3.hide()
        self.pushButton_7.clicked.connect(lambda: self.changeForm("page_change"))
        self.forgot_btn.clicked.connect(lambda: self.changeForm("forgot"))
        self.register.clicked.connect(lambda: self.changeForm("register"))
        self.offset = None

    def changeForm(self, *args):
        if "page_change" in args:
            if self.pushButton_7.isChecked():
                self.widget_2.hide()
                self.widget_3.show()
                self.pushButton_7.setText("<")
            else:
                self.widget_2.show()
                self.widget_3.hide()
                self.pushButton_7.setText(">")
        elif "register" in args:
            self.widget_2.show()
            self.widget_3.hide()
            self.pushButton_7.setText(">")
        elif "forgot" in args:
            self.widget_2.hide()
            self.widget_3.show()
            self.pushButton_7.setText("<")

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.offset is not None:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.offset = None


if __name__ == "__main__":
  windll.shcore.SetProcessDpiAwareness(0)
  app = QApplication(sys.argv)
  window = LoginApp()
  window.show()
  sys.exit(app.exec_())






    

