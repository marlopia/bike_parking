"""Controlador que gestiona las rutas de Flask"""

from flask import Blueprint, redirect, render_template, request, session, url_for

from app.logic import buscar_usuario_por_dni, es_usuario_registrado, es_dni_valido

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/login", methods=["GET"])
def login_form():
    return render_template("login.html")


@main.route("/login", methods=["POST"])
def login_submit():
    dni = request.form.get("dni")
    if not dni or es_dni_valido(dni):
        return "Debes enviar un usuario válido", 400

    if es_usuario_registrado(dni):
        session["dni"] = buscar_usuario_por_dni(dni).nombre
        return redirect(url_for("main.landing"))
    else:
        return redirect(url_for("main.login_form"))


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
