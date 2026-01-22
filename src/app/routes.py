"""Controlador que gestiona las rutas de Flask"""

from flask import Blueprint, redirect, render_template, request, session, url_for

from app.logic import (
    es_email_registrado,
    obtener_usuario,
    es_email_valido,
    es_usuario_registrado,
    es_dni_valido,
    registrar_usuario,
)

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
    if not dni or not es_dni_valido(dni):
        return "Debes enviar un DNI válido", 400

    if es_usuario_registrado(dni):
        session["nombre"] = obtener_usuario(dni).nombre
        session["dni"] = dni
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
    elif not es_dni_valido(dni):
        return "Debes enviar un DNI válido", 400
    elif not es_email_valido(email):
        return "Debes enviar un email válido", 400
    elif es_usuario_registrado(dni):
        return "Este DNI ya está registrado", 400
    elif es_email_registrado(email):
        return "Este email ya está registrado", 400
    else:
        registrar_usuario(nombre, dni, email)
        session["user"] = nombre
        return redirect(url_for("main.landing"))


@main.route("/landing")
def landing():
    user = session.get("nombre")
    bicis = obtener_usuario(session.get("dni")).bicis  # type: ignore viene validada por login
    if not user:
        return redirect(url_for("main.login_form"))

    return render_template("landing.html", username=user, bicis=bicis)


@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))


@main.route("/delete", methods=["POST"])
def delete():
    # TODO implementar borrado seguro con auth de usuario
    return "BORRARIAS: " + str(request.form.get("num_serie"))
