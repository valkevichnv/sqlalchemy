from flask import request, jsonify
from init import *


@app.route('/emp', methods=['GET'])
def get_all_emps():
    all_emps = Emp.query.all()
    result = emps_schema.dump(all_emps)
    return jsonify(result.data)


@app.route('/emp/<empno>', methods=['GET'])
def get_emp(empno):
    emp = Emp.query.get(empno)
    return emp_schema.jsonify(emp)


@app.route('/emp', methods=['POST'])
def add_emp():
    ename = request.json['ename']
    job = request.json['job']
    mgr = request.json['mgr']
    hiredate = request.json['hiredate']
    sal = request.json['sal']
    deptno = request.json['deptno']
    comm = request.json['comm']

    new_emp = Emp(ename, job, mgr, hiredate, sal, deptno, comm)
    db.session.add(new_emp)
    db.session.commit()
    return emp_schema.jsonify(new_emp)


@app.route('/emp/<empno>', methods=['PUT'])
def update_emp(empno):
    emp = Emp.query.get(empno)

    ename = request.json['ename']
    job = request.json['job']
    mgr = request.json['mgr']
    hiredate = request.json['hiredate']
    sal = request.json['sal']
    deptno = request.json['deptno']
    comm = request.json['comm']

    emp.ename = ename
    emp.job = job
    emp.mgr = mgr
    emp.hiredate = hiredate
    emp.deptno = deptno
    emp.comm = comm
    emp.sal = sal

    db.session.commit()
    return emp_schema.jsonify(emp)


@app.route('/emp/<empno>', methods=['DELETE'])
def delete_emp(empno):
    emp = Emp.query.get(empno)
    db.session.delete(emp)
    db.session.commit()
    return emp_schema.jsonify(emp)
