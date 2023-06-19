import psycopg2
import itertools
import time
import csv
import re
import os

from config import connection

def create_table(conn):
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE zno(
                    OUTID UUID NOT NULL,
                    Birth INT2 NOT NULL,
                    SEXTYPENAME VARCHAR(15) NOT NULL,
                    REGNAME VARCHAR(50) NOT NULL,
                    AREANAME VARCHAR(50) NOT NULL,
                    TERNAME VARCHAR(50) NOT NULL,
                    REGTYPENAME VARCHAR(100) NOT NULL,
                    TerTypeName VARCHAR(40) NOT NULL,
                    ClassProfileNAME VARCHAR(50),
                    ClassLangName VARCHAR(20),
                    EONAME TEXT,
                    EOTYPENAME VARCHAR(80),
                    EORegName VARCHAR(50),
                    EOAreaName VARCHAR(50),
                    EOTerName VARCHAR(50),
                    EOParent TEXT,
                    UkrTest VARCHAR(40),
                    UkrTestStatus VARCHAR(30),
                    UkrBall100 NUMERIC(10, 2),
                    UkrBall12 INT2,
                    UkrBall INT2,
                    UkrAdaptScale INT2,
                    UkrPTName TEXT,
                    UkrPTRegName VARCHAR(50),
                    UkrPTAreaName VARCHAR(50),
                    UkrPTTerName VARCHAR(50),
                    histTest VARCHAR(30),
                    HistLang VARCHAR(20),
                    histTestStatus VARCHAR(30),
                    histBall100 NUMERIC(10, 2),
                    histBall12 INT2,
                    histBall INT2,
                    histPTName TEXT,
                    histPTRegName VARCHAR(80),
                    histPTAreaName VARCHAR(50),
                    histPTTerName VARCHAR(50),
                    mathTest VARCHAR(40),
                    mathLang VARCHAR(20),
                    mathTestStatus VARCHAR(30),
                    mathBall100 NUMERIC(10, 2),
                    mathBall12 INT2,
                    mathBall INT2,
                    mathPTName TEXT,
                    mathPTRegName VARCHAR(50),
                    mathPTAreaName VARCHAR(50),
                    mathPTTerName VARCHAR(50),
                    physTest VARCHAR(40),
                    physLang VARCHAR(20),
                    physTestStatus VARCHAR(30),
                    physBall100 NUMERIC(10, 2),
                    physBall12 INT2,
                    physBall INT2,
                    physPTName TEXT,
                    physPTRegName VARCHAR(50),
                    physPTAreaName VARCHAR(50),
                    physPTTerName VARCHAR(50),
                    chemTest VARCHAR(40),
                    chemLang VARCHAR(20),
                    chemTestStatus VARCHAR(30),
                    chemBall100 NUMERIC(10, 2),
                    chemBall12 INT2,
                    chemBall INT2,
                    chemPTName TEXT,
                    chemPTRegName VARCHAR(50),
                    chemPTAreaName VARCHAR(50),
                    chemPTTerName VARCHAR(50),
                    bioTest VARCHAR(40),
                    bioLang VARCHAR(20),
                    bioTestStatus VARCHAR(30),
                    bioBall100 NUMERIC(10, 2),
                    bioBall12 INT2,
                    bioBall INT2,
                    bioPTName TEXT,
                    bioPTRegName VARCHAR(50),
                    bioPTAreaName VARCHAR(50),
                    bioPTTerName VARCHAR(50),
                    geoTest VARCHAR(40),
                    geoLang VARCHAR(20),
                    geoTestStatus VARCHAR(30),
                    geoBall100 NUMERIC(10, 2),
                    geoBall12 INT2,
                    geoBall INT2,
                    geoPTName TEXT,
                    geoPTRegName VARCHAR(50),
                    geoPTAreaName VARCHAR(50),
                    geoPTTerName VARCHAR(50),
                    engTest VARCHAR(40),
                    engTestStatus VARCHAR(30),
                    engBall100 NUMERIC(10, 2),
                    engBall12 INT2,
                    engDPALevel VARCHAR(30),
                    engBall INT2,
                    engPTName TEXT,
                    engPTRegName VARCHAR(50),
                    engPTAreaName VARCHAR(50),
                    engPTTerName VARCHAR(50),
                    fraTest VARCHAR(40),
                    fraTestStatus VARCHAR(30),
                    fraBall100 NUMERIC(10, 2),
                    fraBall12 INT2,
                    fraDPALevel VARCHAR(30),
                    fraBall INT2,
                    fraPTName TEXT,
                    fraPTRegName VARCHAR(50),
                    fraPTAreaName VARCHAR(50),
                    fraPTTerName VARCHAR(50),
                    deuTest VARCHAR(40),
                    deuTestStatus VARCHAR(30),
                    deuBall100 NUMERIC(10, 2),
                    deuBall12 INT2,
                    deuDPALevel VARCHAR(30),
                    deuBall INT2,
                    deuPTName TEXT,
                    deuPTRegName VARCHAR(50),
                    deuPTAreaName VARCHAR(50),
                    deuPTTerName VARCHAR(50),
                    spaTest VARCHAR(40),
                    spaTestStatus VARCHAR(30),
                    spaBall100 NUMERIC(10, 2),
                    spaBall12 INT2,
                    spaDPALevel VARCHAR(30),
                    spaBall INT2,
                    spaPTName TEXT,
                    spaPTRegName VARCHAR(50),
                    spaPTAreaName VARCHAR(50),
                    spaPTTerName VARCHAR(50),
                    ZNOYear INT2
                )""")
    conn.commit()
    cur.close()
    return conn


def drop_table(conn):
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS zno")
    conn.commit()
    cur.close()
    return conn


def is_float(string):
    if re.match('^\\d+,\\d+$', string):
        return True
    return False


def create_formatted_row(old_row, year):
    for i in range(len(old_row)):
        if is_float(old_row[i]):
            old_row[i] = old_row[i].replace(',', '.')

    formatted_row = ';'.join(old_row)

    return formatted_row + ';' + year + '\n'


def insert_data(file_name, conn, size, year):
    start = time.time()

    cur = conn.cursor()
    inserted_parts = 0
    is_final = False

    try:
        os.remove('tmp.csv')
    except OSError:
        pass

    with open(file_name, encoding='cp1251') as f:
        reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_ALL)
        next(reader, None)

        count = 0
        with open('tmp.csv', 'w+') as tmp:
            while not is_final:
                try:
                    for line in reader:
                        tmp.write(create_formatted_row(line, year))
                        count += 1

                        if count == size:
                            tmp.seek(0, 0)
                            cur.copy_from(tmp, 'zno', sep=';', null='null')
                            conn.commit()
                            tmp.seek(0, 0)
                            tmp.truncate(0)
                            inserted_parts += 1
                            count = 0

                    if count != 0:
                        tmp.seek(0, 0)
                        cur.copy_from(tmp, 'zno', sep=';', null='null')
                        conn.commit()
                        is_final = True

                except psycopg2.OperationalError as error:
                    print(error)
                    print("Втрачено підключення до бази даних...\nПовторюємо підключення...\n")
                    is_connected = False
                    while not is_connected:
                        try:
                            conn = psycopg2.connect(**connection)
                            cur = conn.cursor()
                            is_connected = True
                        except psycopg2.OperationalError as error:
                            time.sleep(1)

                    print("Підключення до бази даних відновлено!\nДоопрацьовуємо дані...")
                    f.seek(0, 0)
                    reader = itertools.islice(csv.reader(f, delimiter=';'),
                                              inserted_parts * size + 1, None)
                    tmp.seek(0, 0)
                    tmp.truncate(0)

    cur.close()
    os.remove('tmp.csv')
    end = time.time()

    with open('time-measurements.txt', 'a', encoding='windows-1251') as log:
        log.write(f'Запис та обробка файлу {file_name}: {end - start} секунд.\n')

    return conn


def task(conn):
    query = '''
    SELECT REGNAME, ZNOYear, AVG(mathBall100)
    FROM zno
    WHERE mathTestStatus = 'Зараховано'
    GROUP BY REGNAME, ZNOYear;
    '''

    cur = conn.cursor()
    cur.execute(query)

    with open('results.csv', 'w') as res:
        writer = csv.writer(res, lineterminator='\n')
        writer.writerow(['Регіон', 'Рік', 'Середній бал з математики'])
        for row in cur:
            writer.writerow(row)


def main():

    repeat = 0
    conn = None

    while repeat < 10:
        try:
            print('Спроба з\'єднатися з базою даних...')
            conn = psycopg2.connect(**connection)
            print('З\'єднання встановлено!\n')

            print('Видаляємо таблицю, якщо вона існує...')
            conn = drop_table(conn)
            print('Таблиця видалена!\n')

            print('Створюємо таблицю...')
            conn = create_table(conn)
            print('Таблиця створена!\n')

            print('Опрацьовуємо перший файл...')
            conn = insert_data('./data/Odata2019File.csv', conn, 100, "2019")
            print('Перший файл занесений в базу даних!\n')

            print('Опрацьовуємо другий файл...')
            conn = insert_data('./data/Odata2020File.csv', conn, 100, "2020")
            print('Другий файл занесений в базу даних!\n')

            print("""Виконуємо порівняння середніх балів з математики...\n""")
            task(conn)
            print('Результати доступні в файлі results.csv')

            conn.close()
            break

        except psycopg2.DatabaseError as error:
            print(error)
            print('Помилка з\'єднання з базою даних. Повторюємо спробу...\n')
            time.sleep(2)

        finally:
            repeat += 1
            if repeat == 10:
                print(f'Не вдалося з\'єднатися з базою даних. Всього запитів: {repeat}')
            if conn is not None:
                conn.close()


if __name__ == '__main__':
    main()
