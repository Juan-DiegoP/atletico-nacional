from flask import render_template
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..extensions import mongo, bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId

auth_bp = Blueprint("auth", __name__) 

@auth_bp.route("/")
def home():
    return render_template("index.html") 

@auth_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    nombre = data.get("nombre")
    email = data.get("email")
    password = data.get("password")

    if not nombre or not email or not password:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    if mongo.db.users.find_one({"email": email}):
        return jsonify({"error": "El usuario ya existe"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    user = {
        "nombre": nombre,
        "email": email,
        "password": hashed_password
    }

    mongo.db.users.insert_one(user)

    return jsonify({"mensaje": "Usuario registrado exitosamente 💚"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    user = mongo.db.users.find_one({"email": email})

    if not user or not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"error": "Credenciales incorrectas"}), 401

    access_token = create_access_token(identity=str(user["_id"]))

    return jsonify({
        "mensaje": "Login exitoso 💚",
        "token": access_token
    })

@auth_bp.route("/perfil", methods=["GET"])
@jwt_required()
def perfil():
    user_id = get_jwt_identity()

    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        return {"error": "Usuario no encontrado"}, 404

    return {
        "nombre": user["nombre"],
        "email": user["email"]
    }