from flask import Blueprint, jsonify, request
from math import modf
from bson.objectid import ObjectId
from config.database import connection
from random import random
import os

blueprint = Blueprint('users', __name__)

@blueprint.route('/random')
def lotery():

    number = int(random()*100000000)
    hostname = os.uname()[1]

    return jsonify({'number': number, 'hostname': hostname})

@blueprint.route('/user')
def index():
    db = connection()
    users = db.users.find()
    result = []

    for user in users:
        result.append({'_id':  str(user.get('_id')), 'id':  str(user.get('id')),  'nome': user.get('nome'),  'email': user.get('email')})

    return jsonify(result)


@blueprint.route('/user', methods=["POST"])
def add():

    data = request.json
    data['id'] = str(ObjectId())

    db = connection()
    result = db.users.insert_one(data)
    user = db.users.find_one(result.inserted_id)

    return jsonify({'_id':  str(user.get('_id')), 'id':  str(user.get('id')), 'nome': user.get('nome'), 'email': user.get('email')})

@blueprint.route('/user/<id>', methods=["PUT"])
def edit(id):

    db = connection()
    data = request.json
    data['id'] = id

    update_data = { "$set": data }
    db.users.update_one({'id': id}, update_data)
    user = db.users.find_one({ 'id': id })

    if user is None:
        return jsonify({'message': 'Data not found'}), 404

    return jsonify({'_id':  str(user.get('_id')), 'id':  str(user.get('id')), 'nome': user.get('nome'), 'email': user.get('email')})

@blueprint.route('/user/<id>', methods=["DELETE"])
def delete(id):

    db = connection()

    user = db.users.find_one({ 'id': id })

    if user is None:
        return jsonify({'message': 'Data not found'}), 404

    result = db.users.delete_one({'id': id })

    return jsonify({'result': f"{result.deleted_count} row as deleted"})

@blueprint.route('/user/<id>')
def show(id):
    
    db = connection()
    user = db.users.find_one({'id': id})

    if user is None:
        return jsonify({'message': 'Data not found'}), 404

    result = {'_id':  str(user.get('_id')), 'id':  user.get('id'), 'nome': user.get('nome'), 'email': user.get('email')}

    return jsonify(result)