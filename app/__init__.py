from flask_cors import CORS
from flask import Flask
from dotenv import load_dotenv
import os

from .extensions import mongo, jwt, bcrypt
from .routes.auth import auth_bp
from .routes.users import users_bp
from .routes.posts import posts_bp
from .routes.views import views_bp

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
print("MONGO_URI EN RENDER:", os.getenv("MONGO_URI"))
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

mongo.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)

# Registro blueprints

app.register_blueprint(views_bp) 
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(users_bp, url_prefix="/api")
app.register_blueprint(posts_bp, url_prefix="/api")