import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtWidgets import QErrorMessage
from mainW import Ui_MainWindow
from PyQt5.QtGui import QPixmap
import fdb
from avtoriseDia import Authorise_Ui_Dialog
from AddingDBDia import Adding_DB_Ui_Dialog
from DbOperation import Operation
import os


class AddDB(QDialog, Adding_DB_Ui_Dialog):

    def __init__(self, mainwindow):
        QDialog.__init__(self)
        self.setupUi(self)
        self.mainwindow = mainwindow
        self.pushButton.clicked.connect(self.save_data)

    def save_data(self):
        name_db = self.lineEdit.text()
        if name_db == '':
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Сначала введите название!')
            error_dialog.exec_()
        else:
            name_correct = name_db + ".fdb"
            str_creation = 'create database \'{}\' user \'{}\' password \'{}\''.format(name_correct, self.mainwindow.user,
                                                                                       self.mainwindow.password)
            fake = name_db + "_FAKE.fdb"
            fake_creation = 'create database \'{}\' user \'{}\' password \'{}\''.format(fake, self.mainwindow.user,
                                                                                        self.mainwindow.password)

            try:
                con = fdb.create_database(str_creation)
                con.commit()
                con = fdb.create_database(fake_creation)
                con.commit()
                con = fdb.connect(dsn='DataBases.fdb', user=self.mainwindow.user, password=self.mainwindow.password)
                cur = con.cursor()
                dir_ = str(os.getcwd())
                print(dir_)
                str_adding = "INSERT INTO dbs VALUES (\'{}\',\'{}\');".format(name_db, dir_)
                cur.execute(str_adding)
                cur.transaction.commit("""commit;""")
                con.commit()
                self.mainwindow.update_box()

                self.close()

            except fdb.fbcore.DatabaseError:
                error_dialog = QErrorMessage()
                error_dialog.showMessage('Возникла ошибка!')
                error_dialog.exec_()


class Authorise(QDialog, Authorise_Ui_Dialog):
    close_ev = True

    def __init__(self, mainwindow):
        QDialog.__init__(self)
        self.setupUi(self)
        self.mainwindow = mainwindow
        self.pushButton.clicked.connect(self.save_data)

    def save_data(self):
        self.close_ev = False
        self.mainwindow.user = self.lineEdit.text()
        self.mainwindow.password = self.lineEdit_2.text()
        self.close()
        self.close_ev = True

    def closeEvent(self, event):
        if self.close_ev:
            sys.exit()


class MainWindow(QMainWindow, Ui_MainWindow):
    user = ''
    password = ''
    dbs_list = []
    cur_box = ''

    def __init__(self, parent=None, *args, **kwargs):
        QMainWindow.__init__(self)
        self.setupUi(self)
        while self.user == '' or self.password == '':
            self.get_authorise()
        self.label_3.setPixmap(QPixmap('logo.PNG'))
        str_creation = 'create database \'DataBases.fdb\' user \'{}\' password \'{}\''.format(self.user, self.password)
        try:
            con = fdb.create_database(str_creation)
            con.commit()
        except fdb.fbcore.DatabaseError:
            print('already created')
        con = fdb.connect(dsn='DataBases.fdb', user=self.user, password=self.password)
        cur = con.cursor()
        try:
            cur.execute("""CREATE TABLE dbs (name VARCHAR(20),location VARCHAR(100));""")
            cur.transaction.commit("""commit;""")
            con.commit()
        except fdb.fbcore.DatabaseError:
            print('already created')

        # cur.execute("""INSERT INTO dbs VALUES ('l', 'disk');""")
        # cur.transaction.commit("""commit;""")
        # con.commit()

        self.update_box()
        self.comboBox.activated[str].connect(self.onActivated)
        self.pushButton_2.clicked.connect(self.create_new_db)
        self.pushButton.clicked.connect(self.execute_str)

    def update_box(self):
        self.comboBox.clear()
        con = fdb.connect(dsn='DataBases.fdb', user=self.user, password=self.password)
        cur = con.cursor()
        cur.execute("""SELECT name FROM dbs ;""")
        list_ = list(cur.fetchall())
        con.commit()
        self.dbs_list = []
        if list_:
            self.cur_box = list_[0][0]
            self.cur_box += ".fdb"
        for i in list_:
            self.dbs_list.append(i[0])
        self.comboBox.addItems(self.dbs_list)

    def onActivated(self, text):
        self.cur_box = text
        print(self.cur_box)

    def get_authorise(self):
        DialogSecondIns = Authorise(self)
        DialogSecondIns.show()
        DialogSecondIns.exec()

    def create_new_db(self):
        DialogSecondIns = AddDB(self)
        DialogSecondIns.show()
        DialogSecondIns.exec()

    def execute_str(self):
        request = self.lineEdit.text()
        bd = self.cur_box
        operation = Operation(self.user, self.password)
        answer = operation.execute(request, bd)
        print(answer)
        if answer == "Exception_db":
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Возникла ошибка!')
            error_dialog.exec_()
        else:
            text = str(answer) + '\n'
            self.textEdit.setText(text)


if __name__ == '__main__':
    app = QApplication([])
    application = MainWindow()
    application.show()
    sys.exit(app.exec())

# SYSDBA 5075566
