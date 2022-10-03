from unicodedata import name
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def principal():
    return render_template("principal.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/registrarse")
def registro():
    return render_template("registro.html")

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
    app.run()
