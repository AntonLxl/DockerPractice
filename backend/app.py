from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.json_util import dumps
import json
from os import environ

app = Flask(__name__)
app.config["MONGO_URI"] = environ.get('MONGO_URI')
# print(app.config["MONGO_URI"])
mongo = PyMongo(app)

# jsonify all responses
@app.after_request
def after_request(response):
    # Asegurarse de que la respuesta sea JSON
    if response.content_type == "application/json":
        return response

    # Si no es JSON, convertir la respuesta a JSON
    try:
        response_data = json.loads(response.get_data())
        response.set_data(json.dumps(response_data))
        response.mimetype = "application/json"
    except json.JSONDecodeError:
        pass
    return response

# Ruta para obtener todos los libros
@app.route('/books', methods=['GET'])
def get_books():
    books = mongo.db.books.find()
    return dumps(books)

# Ruta para obtener un libro por su ID
@app.route('/books/<id>', methods=['GET'])
def get_book(id):
    book = mongo.db.books.find_one({"_id": ObjectId(id)})
    if book:
        return dumps(book)
    else:
        return jsonify({"error": "Libro no encontrado"}), 404

# Ruta para agregar un nuevo libro
@app.route('/books', methods=['POST'])
def create_book():
    data = request.json
    result = mongo.db.books.insert_one(data)
    return jsonify({"id": str(result.inserted_id)}), 201

# Ruta para actualizar un libro por su ID
@app.route('/books/<id>', methods=['PUT'])
def update_book(id):
    data = request.json
    result = mongo.db.books.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.modified_count == 1:
        return jsonify({"message": "Libro actualizado exitosamente"})
    else:
        return jsonify({"error": "Libro no encontrado"}), 404

# Ruta para eliminar un libro por su ID
@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    result = mongo.db.books.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return jsonify({"message": "Libro eliminado exitosamente"})
    else:
        return jsonify({"error": "Libro no encontrado"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
