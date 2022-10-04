from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def principal():
    return render_template("principal.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/registrarse")
def registrarse():
    return render_template("registro.html")

@app.route("/registro", methods=["post"])
def registro():
    correo = request.form["txtcorreo"]
    edad = request.form["txtedad"]
    usuario = request.form["txtusuario"]
    contrasena = request.form["txtcontrasena"]
    selec_pregunta = request.form["select"]
    res_pregunta = request.form["txtrespuestapregunta"]
    with sqlite3.connect("redsocial.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO usuarios (correo,edad,usuario,contraseña,preguntaseguridad,respuestapreseguridad) VALUES (?,?,?,?,?,?)",[correo,edad,usuario,contrasena,selec_pregunta, res_pregunta])
        con.commit()
    return "Guardado"

@app.route("/login/perfil")
def perfil():
    return render_template("perfil.html")

@app.route("/login/perfil/configuraciones")
def configuracion():
    return render_template("configuraciones.html")

@app.route("/login/perfil/configuraciones/información")
def información():
    return render_template("informacion.html")
    
@app.route("/login/perfil/configuraciones/cambio-contraseña")
def cambioContrasena():
    return render_template("cambio_contrasena.html")

@app.route("/login/perfil/comentarios")
def comentarios():
    return render_template("comentarios.html")

@app.route("/login/perfil/publicación")
def publicacion():
    return render_template("publicacion.html")

@app.route("/login/perfil/publicación/subir-imagen")
def subirImagen():
    return render_template("subir_imagen.html")

@app.route("/login/perfil/mensajes")
def mensajes():
    return render_template("mensajes.html")

@app.route("/login/perfil/mensajes/nuevo-mensaje")
def nuevoMensaje():
    return render_template("nuevo_mensaje.html")

if __name__ == "__main__":
    app.run(debug=True)
