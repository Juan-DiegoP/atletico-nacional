from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from ..extensions import mongo

posts_bp = Blueprint("posts", __name__)

# 📝 Crear publicación
@posts_bp.route("/posts", methods=["POST"])
@jwt_required()
def crear_post():
    user_id = get_jwt_identity()
    data = request.json

    contenido = data.get("contenido")

    if not contenido:
        return {"error": "El contenido es obligatorio"}, 400

    post = {
        "autor_id": ObjectId(user_id),
        "contenido": contenido
    }

    mongo.db.posts.insert_one(post)

    return {"mensaje": "Publicación creada 💚"}, 201


# 📋 Obtener todas las publicaciones
@posts_bp.route("/posts", methods=["GET"])
def obtener_posts():

    posts = []

    for post in mongo.db.posts.find():
        autor = mongo.db.users.find_one({"_id": post["autor_id"]})

        posts.append({
            "id": str(post["_id"]),
            "contenido": post["contenido"],
            "autor": autor["nombre"] if autor else "Desconocido"
        })

    return posts