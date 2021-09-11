import sqlite3
import random
import timeit
from russian_names import RussianNames

conn = sqlite3.connect("testDatabase.db")
cursor = conn.cursor()


def create_table(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS people 
    (
        full_name text, 
        date_of_birthday text, 
        gender text
    )
    """)


def create_record(full_name, date_of_birthday, gender, cursor):
    cursor.execute(f"""INSERT INTO people VALUES 
    (
        '{full_name}', 
        '{date_of_birthday}', 
        '{gender}'
    )
    """)


def get_all_records(cursor):
    sql = "SELECT DISTINCT full_name, date_of_birthday, gender," \
          " (SELECT(strftime('%Y', 'now') - strftime('%Y', date_of_birthday))" \
          " - (strftime('%m-%d', 'now') < strftime('%m-%d', date_of_birthday))" \
          " AS'full_years')" \
          "  FROM people ORDER BY full_name"
    for el in cursor.execute(sql):
        print(el[0], el[1], el[2], el[3])


def filling_records(cursor, conn):
    counter = 0
    while counter < 100:
        full_name = 'F' + RussianNames(transliterate=True).get_person()[1:]

        year = random.randint(1970, 2021)
        month = random.randint(1, 12)
        day = random.randint(1, 31)
        date_of_birthday = f'{year}-{month}-{day}'

        gender = random.choice(['male', 'female'])
        create_record(full_name, date_of_birthday, gender, cursor)
        counter += 1

    count = 0
    while count < 900:
        full_name = RussianNames(transliterate=True).get_person()

        year = random.randint(1970, 2021)
        month = random.randint(1, 12)
        day = random.randint(1, 31)
        date_of_birthday = f'{year}-{month}-{day}'

        gender = random.choice(['male', 'female'])
        create_record(full_name, date_of_birthday, gender, cursor)
        count += 1

    conn.commit()


def fetch_from_table(cursor):
    sql = "SELECT * FROM people WHERE full_name LIKE 'F%' AND gender " \
          "LIKE 'male'"
    for el in cursor.execute(sql):
        print(el[0], el[1], el[2])


if __name__ == '__main__':
    print(
        '1. Создание таблицы с полями представляющими ФИО,'
        ' дату рождения, пол.\n'
        '2. Создание записи.\n'
        '3. Вывод всех строк с уникальным значением ФИО+дата,'
        ' отсортированным по ФИО\n'
        '4. Заполнение автоматически 1000000 строк.\n'
        '5. Результат выборки из таблицы по критерию: пол мужской,'
        ' ФИО  начинается с "F"'
    )

    choice = (input("Введите номер желаемого действия:"))
    if choice == '1':
        create_table(cursor)
    elif choice == '2':
        full_name = input('Введите ФИО (на английском):')
        date_of_birthday = input('Введите дату рождения (формат YYYY-MM-DD):')
        gender = input('Введите пол (male/female):')
        create_record(full_name, date_of_birthday, gender, cursor)
        conn.commit()
    elif choice == '3':
        get_all_records(cursor)
    elif choice == '4':
        filling_records(cursor, conn)
    elif choice == '5':
        fetch_from_table(cursor)
        t = timeit.Timer()
        print(f'Время выполнения запроса {t.timeit()}')
    else:
        print('Неверное действие')
