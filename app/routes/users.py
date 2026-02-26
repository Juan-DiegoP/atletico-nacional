from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from ..extensions import mongo

users_bp = Blueprint("users", __name__)

@users_bp.route("/perfil", methods=["GET"])
@jwt_required()
def perfil():
    user_id = get_jwt_identity()

    return jsonify({
        "mensaje": "Acceso autorizado 🔥",
        "user_id": user_id
    })


@users_bp.route("/usuarios", methods=["GET"])
@jwt_required()
def obtener_usuarios():
    usuarios = []

    for user in mongo.db.users.find():
        usuarios.append({
            "id": str(user["_id"]),
            "nombre": user["nombre"],
            "email": user["email"]
        })

    return jsonify(usuarios)


@users_bp.route("/usuario/<id>", methods=["PUT"])
@jwt_required()
def actualizar_usuario(id):
    data = request.json

    mongo.db.users.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "nombre": data.get("nombre"),
            "email": data.get("email")
        }}
    )

    return jsonify({"mensaje": "Usuario actualizado 🔥"})


@users_bp.route("/usuario/<id>", methods=["DELETE"])
@jwt_required()
def eliminar_usuario(id):
    mongo.db.users.delete_one({"_id": ObjectId(id)})

    return jsonify({"mensaje": "Usuario eliminado 💥"})