from flask import Blueprint, render_template

views_bp = Blueprint("views", __name__)

@views_bp.route("/")
def home():
    return render_template("index.html")

@views_bp.route("/login")
def login_page():
    return render_template("login.html")