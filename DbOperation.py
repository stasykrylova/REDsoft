import fdb
from random import randint


class Operation:
    trigger_bad = False

    def __init__(self, user, password):
        self.user = user
        self.password = password
        # self.trigger_bad = input()

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

        if not col:
            if small_c in text or big_c in text:
                answer_fake = self.make_connection(fake_db, text)
                print(answer_fake)
                answer = self.make_connection(db, text)
            else:

                if small_s in text or big_s in text:
                    if self.trigger_bad:
                        answer = self.make_connection(fake_db, text)
                    else:
                        answer = self.make_connection(db, text)
                else:

                    fake_text = self.make_fake(text)
                    print(fake_text, fake_db)
                    fake_answer = self.make_connection(fake_db,fake_text)
                    print(fake_answer)
                    answer = self.make_connection(db,text)
        return answer

    def make_fake(self, text):
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

        print('ok')
        try:
            answer = list(cur.fetchall())
        except:
            answer = "Запрос выполнен"

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
