"""Controlador que gestiona las rutas de Flask"""

from flask import Blueprint, redirect, render_template, request, session, url_for

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/login", methods=["GET"])
def login_form():
    return render_template("login.html")


@main.route("/login", methods=["POST"])
def login_submit():
    username = request.form.get("user")
    if not username:
        return "Debes enviar un usuario", 400

    # TODO logica comprobar usuario y añadirlo a la sesion
    # Si no existe redirigir a login con error
    session["user"] = username

    # Si existe redirige a landing/dashboard
    return redirect(url_for("main.landing"))


@main.route("/register", methods=["GET"])
def register_form():
    return render_template("register.html")


@main.route("/register", methods=["POST"])
def register_submit():
    nombre = request.form.get("nombre")
    dni = request.form.get("dni")
    email = request.form.get("email")
    if not nombre or not dni or not email:
        return "Faltan datos", 400

    # TODO logica comprobar registro usuario y añadirlo a la sesion
    # Si no existe redirigir a login con error
    session["user"] = nombre

    # Si existe redirige a landing/dashboard
    return redirect(url_for("main.landing"))


@main.route("/landing")
def landing():
    user = session.get("user")
    if not user:
        return redirect(url_for("main.login_form"))

    return render_template("landing.html", username=user)
