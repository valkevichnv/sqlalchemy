from flask import request, jsonify
from init import *


@app.route('/dept', methods=['GET'])
def get_all_depts():
    all_depts = Dept.query.all()
    result = depts_schema.dump(all_depts)
    return jsonify(result.data)


@app.route('/dept/<deptno>', methods=['GET'])
def get_dept(deptno):
    dept = Dept.query.get(deptno)
    return dept_schema.jsonify(dept)


@app.route('/dept', methods=['POST'])
def add_dept():
    dname = request.json['dname']
    loc = request.json['loc']

    new_dept = Dept(dname, loc)
    db.session.add(new_dept)
    db.session.commit()
    return dept_schema.jsonify(new_dept)


@app.route('/dept/<deptno>', methods=['PUT'])
def update_dept(deptno):
    dept = Dept.query.get(deptno)

    dname = request.json['dname']
    loc = request.json['loc']

    dept.dname = dname
    dept.loc = loc

    db.session.commit()
    return dept_schema.jsonify(dept)


@app.route('/dept/<deptno>', methods=['DELETE'])
def delete_dept(deptno):
    dept = Dept.query.get(deptno)
    db.session.delete(dept)
    db.session.commit()
    return dept_schema.jsonify(dept)
