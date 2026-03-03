import os
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from bson import ObjectId
from ..extensions import mongo

videos_bp = Blueprint("videos", __name__)

# Ruta absoluta segura
UPLOAD_FOLDER = os.path.join("app", "static", "uploads")

@videos_bp.route("/videos", methods=["POST"])
@jwt_required()
def subir_video():
    user_id = get_jwt_identity()

    if "video" not in request.files:
        return {"error": "No se envió ningún video"}, 400

    video = request.files["video"]

    if video.filename == "":
        return {"error": "Nombre de archivo vacío"}, 400

    # 🔥 Crear carpeta si no existe (SOLUCIÓN AL 500)
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    filename = secure_filename(video.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    video.save(filepath)

    data = request.form

    nuevo_video = {
        "autor_id": ObjectId(user_id),
        "titulo": data.get("titulo"),
        "partido": data.get("partido"),
        "minuto": data.get("minuto"),
        "categoria": data.get("categoria"),
        "video_url": f"/static/uploads/{filename}"
    }

    mongo.db.videos.insert_one(nuevo_video)

    return {"mensaje": "Video subido correctamente ⚽🔥"}, 201


@videos_bp.route("/videos", methods=["GET"])
def obtener_videos():
    videos = []

    for video in mongo.db.videos.find():
        autor = mongo.db.users.find_one({"_id": video["autor_id"]})

        videos.append({
            "id": str(video["_id"]),
            "titulo": video.get("titulo"),
            "partido": video.get("partido"),
            "minuto": video.get("minuto"),
            "categoria": video.get("categoria"),
            "autor": autor["nombre"] if autor else "Desconocido",
            "video_url": video.get("video_url")
        })

    return videos