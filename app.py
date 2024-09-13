from flask import Flask

from flask import render_template
from flask import request

import pusher

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    matricula      = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]
    return f"Matrícula: {matricula} Nombre y Apellido: {nombreapellido}"

@app.route("/evento")
def evento():
    pusher_client = pusher.Pusher(
        app_id='1767930',
        key='e6d3475eaa59a14fec17',
        secret='c9dd4d864a7413ae936d',
        cluster='us2',
        ssl=True
    )
    
    pusher_client.trigger("conexion", "evento", {"txtTemperatura": 35, "txtHumedad": 0.6, "dpFechaHora": "2024-09-12 20:13:00"})
