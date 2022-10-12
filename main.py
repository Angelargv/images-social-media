from flask import Flask, render_template, request, redirect, session
import sqlite3
import hashlib
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

FOLDER = "static/images/"

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
    correo = request.form["txtcorreo"]
    password = request.form["txtpassword"]

    # Validaciones
    if not correo or not password:
        error.append("¡ Correo / Contraseña son requeridos !")
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
            cur.execute("SELECT * FROM usuarios WHERE correo= ? AND contraseña= ?",[correo, pwd])
            row = cur.fetchone()
            if row:
                session["email"] = row["correo"]
                session["foto"] = row["fotoperfil"]
                foto = FOLDER + session["foto"]
                print(foto)
                return redirect("/login/perfil")
            else:
                error.append("Correo o contraseña no existe, por favor registrate")
                return render_template("login.html", error = error) 

        
      


@app.route("/registrarse")
def registrarse():
    return render_template("registro.html")

@app.route("/registro", methods=["post"])
def registro():
    error = []
    correo = request.form["txtcorreo"]
    edad = request.form["txtedad"]
    usuario = request.form["txtusuario"]
    contrasena = request.form["txtcontrasena"]
    comprobar = request.form["txtcomprobacion"]

    if not correo:
        error.append("¡Debe digitar un correo!")
        return render_template("registro.html", error = error)  

    if not edad:
        error.append("¡Debe digitar su edad!")
        return render_template("registro.html", error = error)  

    if not usuario:
        error.append("¡Debe digitar un usuario!")
        return render_template("registro.html", error = error)  

    if not contrasena:
        error.append("¡Debe digitar un contraseña!")
        return render_template("registro.html", error = error) 

    if (contrasena!= comprobar):
        error.append("¡Contraseña no coincide!")
        return render_template("registro.html", error = error) 

    # Aplica la función hash (haslib) al password
    clave = hashlib.sha256(contrasena.encode())
    # Convierte el password a hexadecimal tipo string
    pwd = clave.hexdigest()
    # Se conecta a la BD
    with sqlite3.connect("redsocial.db") as con:
        cur = con.cursor()
        # Consultar si ya existe Usuario
        if siExiste(usuario):
            error.append("¡Ya existe el Usuario!")
            return render_template("registro.html", error = error) 
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
    if "email" in session:
        return render_template("perfil.html")
    return render_template("login.html", error = ["¡Usuario no autorizado!"]) 

@app.route("/login/perfil/subir-imagen")
def subirimagen():
    if "email" in session:
        return render_template("subir_imagen.html")
    return render_template("login.html", error = ["¡Usuario no autorizado!"])

@app.route("/login/perfil/subir-imagen", methods=["post"])
def newimage():
    if "email" in session:
        foto_perfil = request.files["foto_perfil"]
        nom_foto = foto_perfil.filename
        print(nom_foto)
        # Crea la ruta
        ruta = FOLDER + secure_filename(nom_foto)
        #Guarda el archivo en disco duro
        foto_perfil.save(ruta)
        user = session["email"]
        with sqlite3.connect("redsocial.db") as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
        
            # Sentencias preparadas
            cur.execute("SELECT * FROM usuarios WHERE correo= ? ",[user])
            row = cur.fetchone()
            if row:
                succesful =[]
                cur.execute("UPDATE usuarios SET fotoperfil= ? WHERE correo = ?",[nom_foto,user])
                con.commit()
                succesful.append("Se sube la nueva foto de perfil")
                return render_template("subir_imagen.html", sucessful = succesful)
            else:
                error= []
                error.append("No se encontro el usuario")
                return render_template("subir_imagen.html", error = error) 

@app.route("/login/perfil/configuraciones")
def configuracion():
    if "email" in session:
        return render_template("configuraciones.html")
    return render_template("login.html", error = ["¡Usuario no autorizado!"]) 

@app.route("/login/perfil/configuraciones/información")
def información():
    if "email" in session:
        return render_template("informacion.html")
    return render_template("login.html", error = ["¡Usuario no autorizado!"]) 
    
@app.route("/login/perfil/configuraciones/cambio-contraseña")
def cambioContrasena():
    if "email" in session:
        return render_template("cambio_contrasena.html")
    return render_template("login.html", error = ["¡Usuario no autorizado!"])


@app.route("/login/perfil/configuraciones/cambio-contraseña", methods=["post"])
def change_pass():
    error = []
    check_email = request.form["txtconfir_correo"]
    pass_cur = request.form["txtpass_cur"]
    pass_new = request.form["txtpass_new"]
    check_new = request.form["txtcheck"]

    if not check_email:
        error.append("¡Se requiere confirmar correo!")
        return render_template("cambio_contrasena.html", error = error)  

    if not pass_cur:
        error.append("¡Se requiere contraseña actual!")
        return render_template("cambio_contrasena.html", error = error)  

    if not pass_new:
        error.append("¡Debe digitar la nueva contraseña!")
        return render_template("cambio_contrasena.html", error = error)  

    if (pass_new!= check_new):
        error.append("¡Nueva contraseña no coincide!")
        return render_template("cambio_contrasena.html", error = error) 
    else:

        # Aplica la función hash (haslib) al password
        clave_actual = hashlib.sha256(pass_cur.encode())  
        clave_nueva = hashlib.sha256(pass_new.encode())
        # Convierte el password a hexadecimal tipo string
        pwdold = clave_actual.hexdigest()
        pwdnew = clave_nueva.hexdigest()

        #Conexión a BD
        with sqlite3.connect("redsocial.db") as con:
            # Convierte el registro en un diccionario
            con.row_factory = sqlite3.Row
            cur = con.cursor()
        
            # Sentencias preparadas
            cur.execute("SELECT * FROM usuarios WHERE correo= ? AND contraseña= ?",[check_email, pwdold])
            row = cur.fetchone()
            if row:
                succesful =[]
                cur.execute("UPDATE usuarios SET contraseña= ? WHERE correo = ?",[pwdnew,check_email])
                con.commit()
                succesful.append("¡La contraseña a sido cambiada con exito!")
                return render_template("cambio_contrasena.html", succesful = succesful)
            else:
                error.append("Correo o contraseña anterior no corresponden, por favor ingrese los datos correctos")
                return render_template("cambio_contrasena.html", error = error) 

    
@app.route("/login/perfil/comentarios")
def comentarios():
    if "email" in session:
        return render_template("comentarios.html")
    return render_template("login.html", error = ["¡Usuario no autorizado!"])
    

@app.route("/login/perfil/publicación")
def publicacion():
    if "email" in session:
        return render_template("publicacion.html")
    return render_template("login.html", error = ["¡Usuario no autorizado!"])
    

@app.route("/login/perfil/mensajes")
def mensajes():
    if "email" in session:
        return render_template("mensajes.html")
    return render_template("login.html", error = ["¡Usuario no autorizado!"])
    

@app.route("/login/perfil/mensajes/nuevo-mensaje")
def nuevoMensaje():
    if "email" in session:
        return render_template("nuevo_mensaje.html")
    return render_template("login.html", error = ["¡Usuario no autorizado!"])
    

@app.route("/logout")
def Logout():
    session.pop("email",None)
    return render_template("principal.html")

if __name__ == "__main__":
    app.run(debug=True, port=4443, ssl_context=('micertificado.pem','llaveprivada.pem'))
