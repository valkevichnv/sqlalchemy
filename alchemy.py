#!/usr/bin/python3.7
'''
Задания

Предварительное задание - установить базу данных (SQLite, Postgres, Mysql), создать базу данных/схему/пользователя.

1 - создать функцию для соединения с базой. Функция должна выводить ошибку соединения,
если параметры соединения неверны или база недоступна. Использовать эту функцию в остальных задачах.
2 - создать таблицы в базе данных из файла schema.sql, используя Metadata
3 - прочесть файл с данными data.sql, выполнить sql-запросы, пропустить комментариии. Если в запросе
ошибка - вывести проблемный запрос и ошибку, после этого выполнить оставшиеся запросы.

4 - Распечатайте имена всех служащих и их годовой доход (годовая зарплата плюс премия),
используйте в качестве имен столбцов комментарии к полям из файла schema.sql

5 - Распечатайте список должностей по отделам
6 - Распечатать список сотрудников, которые были зачислены на работу до января 1979 и
после февраля 1981 годов. Результаты упорядочить в порядке убывания даты зачисления на работу.
7 - Вывести сотрудников, которыми никто не руководит.
8 - Определить сотрудников 10 отдела, занимающих должность менеджера или имеющих годовой доход более 3000.
9 - Вывести всех служащих в иерархическом порядке, определяемом должностной подчиненностью.
10 - Вычислите и выведите максимальную, среднюю и минимальную зарплату для каждой должности в отделе.
11 - Определите количество служащих в каждом отделе компании.
12 - Найдите и распечатайте отделы, в которых работает больше 3-х служащих.
'''

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import ArgumentError


def create():
    # Connect to DB, catch exceptions

    error = None
    try:
        engine = create_engine('sqlite:///:memory:', echo=True)
    except ModuleNotFoundError:
        print("Error: module not found")
        error = 'MNF'
    except ArgumentError:
        print("Error: invalid arguments.")
        error = "IA"
    return engine, error


def setup(engine):
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
        hiredate = Column(Date)
        sal = Column(Integer)
        comm = Column(Integer)
        deptno = ForeignKey("dept.deptno")

        def __init__(self, name):
            self.__name__ = name

    class Salgrade(Base):
        __tablename__ = "salgrade"
        id = Column(Integer, primary_key=True)
        grade = Column(Integer)
        losal = Column(Integer)
        hisal = Column(Integer)

        def __init__(self, name):
            self.__name__ = name

    Base.metadata.create_all(engine)


def disconnect():
    pass


def create_tables():
    # Use schema.sql
    pass


def make_queries():
    # Use data.sql
    pass


def get_annual_income():
    # SELECT NAME, INCOME FROM WORKERS
    pass


def get_positions_by_department():
    # SELECT POSITION, DEPARTMENT FROM WORKERS SORT BY DEPARTMENT
    pass


def get_employees_between(date_1, date_2):
    # SELECT NAME, EMPLOY_DATE FROM WORKERS WHERE  EMPLOY_DATE <= 01.01.1979
    # OR EMPLOY_DATE >= 01.02.1981 SORT BY EMPLOY_DATE DESCENDING
    pass


def get_self_employed_workers():
    # SELECT NAME, CHIEF FROM WORKERS WHERE CHIEF == ''
    pass


def get_workers():
    # SELECT NAME, DEPARTMENT, POSITION, INCOME FROM WORKERS WHERE DEPARTMENT == 10 AND
    # (POSITION == 'manager' OR INCOME > 3000)
    # if department==10 and (position == 'manager' or min_income>3000): query = True
    pass


def get_workers_hierarchy():
    # Hug knows how to query this @LinusTorwalds
    pass


def get_salary_by_position():
    # max, min, avg
    pass


def get_workers_quantity_by_department():
    pass


def get_departments_with_3plus_workers():
    pass


if __name__ == "__main__":
    engine, error = create()
    #    setup(engine)
    if error != None: raise Exception(error)
    setup(engine)
