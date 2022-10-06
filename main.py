from flask import Flask, render_template, request, redirect, session
import sqlite3
import hashlib
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)

@app.route("/")
def principal():
    return render_template("principal.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/loguearse",methods=["post"])
def log():
    error = []
    # Captura los datos enviados
    username = request.form["txtusername"]
    password = request.form["txtpassword"]

    # Validaciones
    if not username or not password:
        error.append("Usuario/Contraseña son requeridos")
        return render_template("login.html", error = error)  
    else:

        clave = hashlib.sha256(password.encode())
        pwd = clave.hexdigest()

        #Conexión a BD
        with sqlite3.connect("redsocial.db") as con:
            # Convierte el registro en un diccionario
            con.row_factory = sqlite3.Row
            cur = con.cursor()
           
            # Sentencias preparadas
            cur.execute("SELECT * FROM usuarios WHERE usuario= ? AND contraseña= ?",[username, pwd])
            # cur.fetchone()
            if cur.fetchone():
                return redirect("/login/perfil")
            else:
                error.append("Usuario o contraseña no existe, por favor registrate")
                return render_template("login.html", error = error) 

        
      


@app.route("/registrarse")
def registrarse():
    return render_template("registro.html")

@app.route("/registro", methods=["post"])
def registro():
    correo = request.form["txtcorreo"]
    edad = request.form["txtedad"]
    usuario = request.form["txtusuario"]
    contrasena = request.form["txtcontrasena"]
    comprobar = request.form["txtcomprobacion"]

    if not correo:
        return "Debe digitar un correo"

    if not edad:
        return "Debe digitar su edad"

    if not usuario:
        return "Debe digitar un usuario"

    if not contrasena:
        return "Debe digitar un contraseña"

    if (contrasena!= comprobar):
        return "Contraseña no coincide"

    # Aplica la función hash (haslib) al password
    clave = hashlib.sha256(contrasena.encode())
    # Convierte el password a hexadecimal tipo string
    pwd = clave.hexdigest()
    # Se conecta a la BD
    with sqlite3.connect("redsocial.db") as con:
        cur = con.cursor()
        # Consultar si ya existe Usuario
        if siExiste(usuario):
            return "Ya existe el Usuario!"
        #Crea el nuevo Usuario
        cur.execute("INSERT INTO usuarios (correo,edad,usuario,contraseña) VALUES (?,?,?,?)",[correo,edad,usuario,pwd])
        con.commit()
        return redirect ("/login/perfil")

def siExiste(user):
     # Se conecta a la BD
    with sqlite3.connect("redsocial.db") as con:
        cur = con.cursor()
        # Consultar si ya existe Usuario
        cur.execute("SELECT usuario FROM usuarios WHERE usuario=?",[user])
        if cur.fetchone():
            return True
    
    return False

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
