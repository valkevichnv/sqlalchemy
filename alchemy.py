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
12 + Найдите и распечатайте отделы, в которых работает больше 3-х служащих.
'''

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


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

    # manager = relationship('Emp',back_populates='parent')
    # employee = relationship("Parent", back_populates="children")

    def __init__(self, name):
        self.__name__ = name


class Salgrade(Base):
    __tablename__ = "salgrade"
    grade = Column(Integer, primary_key=True)
    losal = Column(Integer)
    hisal = Column(Integer)

    def __init__(self, name):
        self.__name__ = name


def create(echoing=False):
    # Connect to DB, catch exceptions
    from sqlalchemy.exc import ArgumentError
    from sqlalchemy import create_engine
    engine = None
    error = None
    try:
        engine = create_engine('sqlite:////home/valkevich/PycharmProjects/sqlalchemy/sqlite.db', echo=echoing)

    except ModuleNotFoundError:
        error = 'Module not found'
    except ArgumentError:
        error = "Invalid Arguments for create_engine"
    return engine, error


def setup(engine):
    from sqlalchemy.exc import OperationalError
    db = engine.connect()
    with open('data/data.sql', 'r') as queryfile:
        for query in queryfile.read().split('\n'):

            try:
                db.execute(query.replace(',to_date(', ',date('))
            except OperationalError:
                print("Error in:", query)
    db.close()


def create_session(engine):
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    return (session)


def close_session(session):
    session.close()


def print_query(query):
    for instance in query:
        print(instance)


def get_annual_income():
    from sqlalchemy.sql import func
    return session.query(Emp.ename, Emp.sal + func.ifnull(Emp.comm, 0))


def get_positions_by_department():
    # query = 'SELECT JOB,DEPTNO FROM EMP ORDER BY DEPTNO'
    return session.query(Emp.job, Emp.deptno).group_by(Emp.deptno,Emp.job)


def get_employees_between():
    from sqlalchemy import or_
    return session.query(Emp.ename, Emp.hiredate).filter(
        or_(Emp.hiredate <= 19790101, Emp.hiredate >= 19810201)).order_by(Emp.hiredate.desc())


def get_self_employed_workers():
    return session.query(Emp.ename, Emp.mgr).filter(Emp.mgr == None)


def get_workers():
    from sqlalchemy.sql import func, and_, or_

    return session.query(Emp.ename, Emp.sal + func.ifnull(Emp.comm, 0)).filter(and_(Emp.deptno == 10),
                                                                               or_(Emp.job == 'MANAGER',
                                                                                   (Emp.sal + func.ifnull(Emp.comm,
                                                                                                          0)) > 3000))
    # Hugging PyCharm hugged up my formatting!!!!


def get_query_result(query):
    conn = engine.connect()
    result = conn.execute(query)
    conn.close()
    return result.fetchall()


def get_workers_hierarchy():
    hierarchy = []
    mgrs = [None]
    while mgrs != []:
        for mgr in mgrs:
            hierarchy.append([x for x in session.query(Emp.empno, Emp.ename, Emp.mgr).filter(Emp.mgr == mgr)])
            mgrs = [mgr[0] for mgr in hierarchy[-1]]
    hierarchy.pop()
    return hierarchy
   


def get_salary_by_department():
    from sqlalchemy.sql import func
    return session.query(func.max(Emp.sal), func.avg(Emp.sal), func.min(Emp.sal), Emp.deptno).group_by(Emp.deptno)


def get_workers_quantity_by_department():
    from sqlalchemy.sql import func

    return session.query(func.count(Emp.ename), Emp.deptno).group_by(Emp.deptno)


def get_departments_with_3plus_workers():
    from sqlalchemy.sql import func

    return session.query(func.count(Emp.ename), Emp.deptno).group_by(Emp.deptno).having(func.count(Emp.ename) > 3)


if __name__ == "__main__":

    engine, error = create(False)
    if error is not None:
        raise Exception(error)

    Base.metadata.create_all(engine)
    setup(engine)
    session = create_session(engine)
    #print_query(get_salary_by_department())

    close_session(session)
