"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# obtener los mimebors 
@app.route('/members', methods=['GET'])
def get_all_members():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    
    return jsonify(members), 200

# obtener un mimebro por su id
@app.route('/members/<int:member_id>' , methods=['GET'])
def get_one_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is not None:
        response_body =member
        return jsonify(response_body) ,200
    else:
        response_body = {'error' : ' miembro no encontrado'}
        return jsonify(response_body),404

# agregar un miembro nuevo 

@app.route('/members' ,  methods=['POST'])
def add_new_memeber():
    data = request.get_json()

    if 'first name' not in data or 'age' not in data or 'lucky_numbers' not in data:
        return jsonify({'error':'faltan datos'}) ,400
    
    jackson_family.add_member(data)
    return jsonify({"message": "Miembro agregado correctamente"}), 200

# 4) Eliminar un miembro por ID
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_one_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is not None:
        jackson_family.delete_member(member_id)
        return jsonify({"done": True}), 200
    else:
        return jsonify({"error": "Miembro no encontrado"}), 404



# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
