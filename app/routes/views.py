from flask import Blueprint, render_template

views_bp = Blueprint("views", __name__)

@views_bp.route("/posts")
def posts_page():
    return render_template("posts.html")


@views_bp.route("/login")
def login_page():
    return render_template("login.html")

from flask import render_template

@views_bp.route("/feed")
def feed():
    return render_template("feed.html")