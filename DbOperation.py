import fdb
from random import randint
import time
import datetime


class Operation:
    time_ans = ''

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.trigger_bad = False
        self.time_out = False

    def execute(self, text, db):
        small_s = 'select'
        big_s = 'SELECT'
        small_c = 'create'
        big_c = 'CREATE'
        fake_db = db.replace('.fdb', '_FAKE.fdb')
        stop_words = ['UPDATE', 'update', 'DELETE', 'delete']
        answer = ''
        col = 0
        for i in stop_words:
            if i in text:
                answer = self.make_connection(db, text)
                col += 1
        if text.lower() == 'system timeout;':
            self.time_ans = " \n Ваш запрос теперь будет обрабатываться раз в минуту."
            self.time_out = True
        elif text.lower() == 'system alright;':
            self.time_ans = " "
            self.time_out = False
        else:
            if self.time_out:
                print('1')
                time.sleep(59)
            if not col:
                if text.lower() == 'system trigger true;':
                    self.trigger_bad = True
                    print('2')
                elif text.lower() == 'system trigger false;':
                    self.trigger_bad = False

                else:
                    if small_c in text or big_c in text:
                        answer_fake = self.make_connection(fake_db, text)
                        print(answer_fake)
                        answer = self.make_connection(db, text)
                    else:

                        if small_s in text or big_s in text:
                            if self.trigger_bad:
                                print('3')
                                answer = self.make_connection(fake_db, text)
                                today = datetime.datetime.today()
                                date = today.strftime("%Y-%m-%d-%H.%M.%S")
                                my_file = open("logs.txt", 'a')
                                t = '\n' + self.user + ' ' + date + '\n' + text
                                my_file.write(t)
                                my_file.close()
                            else:
                                print(self.trigger_bad)
                                answer = self.make_connection(db, text)
                        else:

                            fake_text = self.make_fake(text)
                            print(fake_text, fake_db)
                            fake_answer = self.make_connection(fake_db, fake_text)
                            print(fake_answer)
                            answer = self.make_connection(db, text)
        return answer+self.time_ans

    @staticmethod
    def make_fake(text):
        counter = 0
        fake_text = ''
        exceptions = [',', '.', ';', ':', '(', ')', ' ', '=']
        for i in text:
            cur_ = i
            if is_int(i):
                r = randint(0, 1)
                if counter % 2 == r:
                    cur_ = make_random()
                counter += 1
            if i in exceptions:
                counter = 0
            fake_text += cur_
        print(fake_text)
        return fake_text

    def make_connection(self, db, text):
        try:
            con = fdb.connect(dsn=db, user=self.user, password=self.password)
            cur = con.cursor()
            cur.execute(text)

        except fdb.fbcore.DatabaseError:
            return "Exception_db"

        try:
            str_ = ''
            answer = str(list(cur.fetchall()))
            for i in range(len(answer)):
                if answer[i] != '[' and answer[i] != ']':
                    if answer[i] == '(':
                        str_ += ' '
                    elif answer[i] == ')':
                        str_ += '\n'
                    elif answer[i] == ',':
                        str_ += ''
                    else:
                        str_ += answer[i]
                    print(str_)
            answer = str_

        except:
            answer = "Запрос выполнен"
            print('4')

        cur.transaction.commit("""commit;""")
        con.commit()
        return answer


def is_int(str_):
    try:
        int(str_)
        return True
    except ValueError:
        return False


def make_random():
    generated = randint(0, 9)
    generated = str(generated)
    return generated
