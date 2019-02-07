from flask import request, jsonify
from init import *


@app.route('/salgrade', methods=['GET'])
def get_all_salgrades():
    all_salgrades = Salgrade.query.all()
    result = salgrades_schema.dump(all_salgrades)
    return jsonify(result.data)


@app.route('/salgrade/<grade>', methods=['GET'])
def get_salgrade(grade):
    salgrade = Salgrade.query.get(grade)
    return salgrade_schema.jsonify(salgrade)


@app.route('/salgrade', methods=['POST'])
def add_salgrade():
    losal = request.json['losal']
    hisal = request.json['hisal']

    new_salgrade = Salgrade(losal, hisal)
    db.session.add(new_salgrade)
    db.session.commit()
    return salgrade_schema.jsonify(new_salgrade)


@app.route('/salgrade/<grade>', methods=['PUT'])
def update_salgrade(grade):
    salgrade = Salgrade.query.get(grade)

    losal = request.json['losal']
    hisal = request.json['hisal']

    salgrade.losal = losal
    salgrade.hisal = hisal

    db.session.commit()
    return salgrade_schema.jsonify(salgrade)


@app.route('/salgrade/<grade>', methods=['DELETE'])
def delete_salgrade(grade):
    salgrade = Salgrade.query.get(grade)

    db.session.delete(salgrade)
    db.session.commit()
    return salgrade_schema.jsonify(salgrade)
