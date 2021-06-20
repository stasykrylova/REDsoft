import fdb
from random import randint
import time
import datetime
import ast


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
        fake_db = db.replace('.fdb', '')
        if '.FDB' in fake_db:
            fake_db = fake_db.replace('.FDB', '')
        fake_db += '_FAKE.fdb'
        if '.FDB' in db:
            db = db.replace('.FDB', '')
        if '.fdb' in db:
            db = db.replace('.fdb', '')
        db += '.fdb'
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
                        print(fake_db, text)
                        answer_fake = self.make_connection(fake_db, text)
                        print('3', answer_fake)
                        print(db)
                        answer = self.make_connection(db, text)
                    else:

                        if small_s in text or big_s in text:
                            if self.trigger_bad:
                                print('4')
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

                            fake_text = self.make_fake(text, fake_db)
                            print(fake_text, fake_db)
                            fake_answer = self.make_connection(fake_db, fake_text)
                            print(fake_answer)
                            answer = self.make_connection(db, text)
        return answer+self.time_ans

    def make_fake(self, text, fake_db):
        print('10', text)
        text = text.lower()
        tabl = "into"
        res = text[text.find(tabl) + len(tabl):].split()[0]
        print('11', res)
        req = "SELECT * FROM {};".format(res)
        print('12', req)
        print(fake_db, req)
        number = self.make_check(fake_db, req)
        print("HERE iS", number)
        print("----------------------")
        print(len(number))
        fake_text = ''
        if len(number) < 2:
            print("here we are")
            counter = 0
            comma = ','
            pos = text.find(comma)
            text_part_f = text[:pos] + ","
            text_part_s = text[pos + 1:]
            print('after coma', text_part_s)
            exceptions = [',', '.', ';', ':', '(', ')', ' ', '=']
            for i in text_part_s:
                cur_ = i
                if is_int(i):
                    r = randint(0, 1)
                    if counter % 2 == r:
                        cur_ = make_random()
                    counter += 1
                if i in exceptions:
                    counter = 0
                fake_text += cur_
            fake_text = text_part_f + fake_text
            print(fake_text)
        else:
            ran_first = randint(0, len(number)-1)
            req = "SELECT * FROM {} WHERE id = {};".format(res, ran_first)
            print(req)
            first = self.make_check(fake_db, req)
            ran_sec = randint(0, len(number) - 1)
            while ran_first == ran_sec:
                ran_sec = randint(0, len(number)-1)
            req = "SELECT * FROM {} WHERE id = {};".format(res, ran_sec)
            print(req)
            second = self.make_check(fake_db, req)
            print("HERE iS", first, second)
            data_first = list(first)[0]
            data_second = list(second)[0]
            print("DATAS:", data_first, data_second)
            l = ''
            for i in range(len(text)):
                if text[i] == '(':
                    while text[i] != ")":
                        l += text[i]
                        i+=1
            l += ')'
            print(l)
            one = ast.literal_eval(l)
            print(one)
            print(one[0])
            print(data_second)
            print(data_first)
            matrix = [
                one[1:],
                data_first[1:],
                data_second[1:]
            ]
            matrix = [list(ele) for ele in matrix]
            print(matrix)
            generated = list(one)
            for i in range(len(one)):
                if i == 0:
                    generated[i] = one[i]
                else:
                    n = randint(0, 2)
                    print('okay')
                    generated[i] = matrix[n][i-1]
                    print('okay')
                    matrix[n][i - 1] = 'mAtRiXnUlL'
            print('matr', matrix)

            changed_first = list(data_first)

            for i in range(len(changed_first)):
                if i == 0:
                    changed_first[i] = data_first[i]
                else:
                    n = randint(0, 2)
                    while matrix[n][i - 1] == 'mAtRiXnUlL':
                        n = randint(0, 2)
                    changed_first[i] = matrix[n][i-1]

                    if isinstance(changed_first[i], str):
                        string = changed_first[i]
                        changed_first[i] = '\''
                        changed_first[i] += string
                        changed_first[i] += '\''

                    matrix[n][i - 1] = 'mAtRiXnUlL'
            print('matr', matrix)

            changed_second = list(data_second)

            for i in range(len(changed_second)):
                if i == 0:
                    changed_second[i] = data_second[i]
                else:
                    n = randint(0, 2)
                    while matrix[n][i - 1] == 'mAtRiXnUlL':
                        n = randint(0, 2)
                    changed_second[i] = matrix[n][i-1]

                    if isinstance(changed_second[i], str):
                        string = changed_second[i]
                        changed_second[i] = '\''
                        changed_second[i] += string
                        changed_second[i] += '\''

                    matrix[n][i - 1] = 'mAtRiXnUlL'
            print('matr', matrix)

            print(generated)
            print(changed_first)
            print(changed_second)



            print("----------------------")
            con = fdb.connect(dsn=fake_db, user=self.user, password=self.password)
            cur = con.cursor()
            text_col = "select * from {}".format(res)
            cur.execute(text_col)
            text_update = ''
            c = 0
            for fieldDesc in cur.description:
                print(fieldDesc[fdb.DESCRIPTION_NAME])
                text_update += str(fieldDesc[fdb.DESCRIPTION_NAME])
                text_update += "="
                text_update += str(changed_first[c])
                c += 1
                text_update += ','
            text_update = text_update[0:-1]
            update_text_first = 'UPDATE {} SET {} WHERE ID = {};'.format(res, text_update, int(changed_first[0]))
            print(update_text_first)
            new_req = self.make_check(fake_db, update_text_first)
            print(new_req)
            fake_text = 'INSERT INTO {} VALUES {};'.format(res, tuple(generated))
            text_update = ''
            c = 0
            for fieldDesc in cur.description:
                print(fieldDesc[fdb.DESCRIPTION_NAME])
                text_update += str(fieldDesc[fdb.DESCRIPTION_NAME])
                text_update += "="
                text_update += str(changed_second[c])
                c += 1
                text_update += ','
            text_update = text_update[0:-1]
            update_text_second = 'UPDATE {} SET {} WHERE ID ={};'.format(res, text_update, changed_second[0])
            print(update_text_second)
            new_req = self.make_check(fake_db, update_text_second)
            print(new_req)

        return fake_text

    def make_check(self, db, text):
        try:
            con = fdb.connect(dsn=db, user=self.user, password=self.password)
            cur = con.cursor()
            cur.execute(text)

        except fdb.fbcore.DatabaseError:
            return "Exception_db"
        try:
            answer = list(cur.fetchall())
        except:
            answer = []
            print('6')

        cur.transaction.commit("""commit;""")
        con.commit()
        return answer

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
