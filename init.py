from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/valkevich/PycharmProjects/sqlalchemy/sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Dept(db.Model):
    deptno = db.Column(db.Integer, primary_key=True)
    dname = db.Column(db.String)
    loc = db.Column(db.String)

    def __init__(self, dname, loc):
        self.dname = dname
        self.loc = loc


class DeptSchema(ma.Schema):
    class Meta:
        fields = ('deptno', 'dname', 'loc')


class Emp(db.Model):
    empno = db.Column(db.Integer, primary_key=True)
    ename = db.Column(db.String)
    job = db.Column(db.String)
    mgr = db.Column(db.Integer)
    hiredate = db.Column(db.Integer)
    sal = db.Column(db.Integer)
    comm = db.Column(db.Integer)
    deptno = db.Column(db.ForeignKey("dept.deptno"))

    def __init__(self, ename, job, mgr, hiredate, sal, deptno, comm):
        self.ename = ename
        self.job = job
        self.mgr = mgr
        self.hiredate = hiredate
        self.sal = sal
        self.deptno = deptno
        self.comm = comm


class EmpSchema(ma.Schema):
    class Meta:
        fields = ('empno', 'ename', 'job', 'mgr', 'hiredate', 'sal', 'comm', 'deptno')


class Salgrade(db.Model):
    grade = db.Column(db.Integer, primary_key=True)
    losal = db.Column(db.Integer)
    hisal = db.Column(db.Integer)

    def __init__(self, losal, hisal):
        self.losal = losal
        self.hisal = hisal


class SalgradeSchema(ma.Schema):
    class Meta:
        fields = ('grade', 'losal', 'hisal')


dept_schema = DeptSchema(strict=True)
depts_schema = DeptSchema(many=True, strict=True)
emp_schema = EmpSchema(strict=True)
emps_schema = EmpSchema(many=True, strict=True)
salgrade_schema = SalgradeSchema(strict=True)
salgrades_schema = SalgradeSchema(many=True, strict=True)
