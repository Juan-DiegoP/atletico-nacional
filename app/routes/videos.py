import os
import cloudinary
import cloudinary.uploader

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from ..extensions import mongo

videos_bp = Blueprint("videos", __name__)

# 🔥 Configuración Cloudinary (usa variables de entorno en Render)
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

@videos_bp.route("/videos", methods=["POST"])
@jwt_required()
def subir_video():
    user_id = get_jwt_identity()

    if "video" not in request.files:
        return {"error": "No se envió ningún video"}, 400

    video = request.files["video"]

    if video.filename == "":
        return {"error": "Nombre de archivo vacío"}, 400

    # 🔥 Subir directamente a Cloudinary
    result = cloudinary.uploader.upload(
        video,
        resource_type="video"
    )

    video_url = result["secure_url"]

    data = request.form

    nuevo_video = {
        "autor_id": ObjectId(user_id),
        "titulo": data.get("titulo"),
        "partido": data.get("partido"),
        "minuto": data.get("minuto"),
        "categoria": data.get("categoria"),
        "video_url": video_url
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