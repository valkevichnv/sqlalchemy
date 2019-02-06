#!/usr/bin/python3.7
'''
Задания

Предварительное задание - установить базу данных (SQLite, Postgres, Mysql), создать базу данных/схему/пользователя.

1 + создать функцию для соединения с базой. Функция должна выводить ошибку соединения,
если параметры соединения неверны или база недоступна. Использовать эту функцию в остальных задачах.
2 + создать таблицы в базе данных из файла schema.sql, используя Metadata
3 + прочесть файл с данными data.sql, выполнить sql-запросы, пропустить комментариии. Если в запросе
ошибка - вывести проблемный запрос и ошибку, после этого выполнить оставшиеся запросы.

4 + Распечатайте имена всех служащих и их годовой доход (годовая зарплата плюс премия),
используйте в качестве имен столбцов комментарии к полям из файла schema.sql

5 + Распечатайте список должностей по отделам
6 + Распечатать список сотрудников, которые были зачислены на работу до января 1979 и
после февраля 1981 годов. Результаты упорядочить в порядке убывания даты зачисления на работу.
7 + Вывести сотрудников, которыми никто не руководит.
8 + Определить сотрудников 10 отдела, занимающих должность менеджера или имеющих годовой доход более 3000.
9 - Вывести всех служащих в иерархическом порядке, определяемом должностной подчиненностью.
10 + Вычислите и выведите максимальную, среднюю и минимальную зарплату для каждой должности в отделе.
11 + Определите количество служащих в каждом отделе компании.
12 - Найдите и распечатайте отделы, в которых работает больше 3-х служащих.
'''

from sqlalchemy.orm import sessionmaker, relationships


def create(echoing=False):
    # Connect to DB, catch exceptions
    from sqlalchemy.exc import ArgumentError
    from sqlalchemy import create_engine
    engine = None
    error = None
    try:
        engine = create_engine('sqlite:///:memory:', echo=echoing)

    except ModuleNotFoundError:
        error = 'Module not found'
    except ArgumentError:
        error = "Invalid Arguments for create_engine"
    return engine, error


def setup(engine):
    create_tables(engine)
    make_queries(engine)


def create_tables(engine):
    from sqlalchemy import Column, Integer, String, Date, ForeignKey
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()

    class Dept(Base):
        __tablename__ = "dept"
        deptno = Column(Integer, primary_key=True)
        dname = Column(String)
        loc = Column(String)

        def __init__(self, name):
            self.__name__ = name

    class Emp(Base):
        __tablename__ = "emp"
        empno = Column(Integer, primary_key=True)
        ename = Column(String)
        job = Column(String)
        mgr = Column(Integer)
        hiredate = Column(Integer)
        sal = Column(Integer)
        comm = Column(Integer)
        deptno = Column(ForeignKey("dept.deptno"))

        def __init__(self, name):
            self.__name__ = name

    class Salgrade(Base):
        __tablename__ = "salgrade"
        grade = Column(Integer, primary_key=True)
        losal = Column(Integer)
        hisal = Column(Integer)

        def __init__(self, name):
            self.__name__ = name

    Base.metadata.create_all(engine)


def make_queries(engine):
    from sqlalchemy.exc import OperationalError
    db = engine.connect()
    with open('data/data.sql', 'r') as queryfile:
        for query in queryfile.read().split('\n'):

            try:
                db.execute(query.replace(',to_date(', ',date('))
            except OperationalError:
                print("Error in:", query)
    db.close()


def get_query_result(engine, query):
    conn = engine.connect()
    result = conn.execute(query)
    conn.close()
    return result.fetchall()


def get_annual_income(engine):
    query = 'SELECT ENAME,SAL+IFNULL( COMM, 0 ) FROM EMP;'
    return get_query_result(engine, query)


def get_positions_by_department(engine):
    # SELECT POSITION, DEPARTMENT FROM WORKERS SORT BY DEPARTMENT
    query = 'SELECT JOB,DEPTNO FROM EMP GROUP BY DEPTNO,JOB'
    return get_query_result(engine, query)


def get_employees_between(engine):
    # SELECT NAME, EMPLOY_DATE FROM WORKERS WHERE  EMPLOY_DATE <= 01.01.1979
    # OR EMPLOY_DATE >= 01.02.1981 SORT BY EMPLOY_DATE DESCENDING
    query = 'SELECT ENAME,HIREDATE FROM EMP WHERE (HIREDATE <=19790101 OR ' \
            'HIREDATE >=19810201) ORDER BY HIREDATE DESC'
    return get_query_result(engine, query)


def get_self_employed_workers(engine):
    # SELECT NAME, CHIEF FROM WORKERS WHERE CHIEF == ''
    query = 'SELECT ENAME,MGR FROM EMP WHERE MGR IS NULL'
    return get_query_result(engine, query)


def get_workers(engine):
    # SELECT NAME, DEPARTMENT, POSITION, INCOME FROM WORKERS WHERE DEPARTMENT == 10 AND
    # (POSITION == 'manager' OR INCOME > 3000)
    # if department==10 and (position == 'manager' or min_income>3000): query = True
    query = 'SELECT ENAME,JOB,SAL+IFNULL(COMM,0) AS INCOME FROM EMP WHERE (DEPTNO = 10 ' \
            'AND (JOB = "MANAGER" OR INCOME>3000))'

    return get_query_result(engine, query)


def get_workers_hierarchy():
    # Hug knows how to query this @LinusTorwalds
    pass


def get_salary_by_position(engine):
    # max, min, avg
    query = 'SELECT MIN(SAL),AVG(SAL),MAX(SAL),DEPTNO FROM EMP GROUP BY DEPTNO'
    return get_query_result(engine, query)


def get_workers_quantity_by_department(engine):
    query = 'SELECT COUNT(ENAME),DEPTNO FROM EMP GROUP BY DEPTNO'
    return get_query_result(engine, query)


def get_departments_with_3plus_workers():
    pass


if __name__ == "__main__":
    engine, error = create(False)
    if error != None: raise Exception(error)
    setup(engine)
    print(get_workers_quantity_by_department(engine))
