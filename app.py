from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify, make_response

import pusher
import mysql.connector
import datetime
import pytz

con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    con.close()
    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    con.close()
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    con.close()
    matricula      = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]
    return f"Matrícula {matricula} Nombre y Apellido {nombreapellido}"

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("""
    SELECT Id_Log, Nombre_Apellido, Numero_Telefono, DATE_FORMAT(Fecha_Hora, '%d/%m/%Y') AS Fecha FROM contactos_log
    ORDER BY Id_Log DESC
    LIMIT 10 OFFSET 0
    """)
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))

@app.route("/editar", methods=["GET"])
def editar():
    if not con.is_connected():
        con.reconnect()

    id = request.args["id"]
    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT Id_Log, Nombre_Apellido, Numero_Telefono FROM contactos_log
    WHERE Id_Log = %s
    """
    val    = (id,)
    cursor.execute(sql, val)
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))

@app.route("/guardar", methods=["POST"])
def guardar():
    if not con.is_connected():
        con.reconnect()

    id             = request.form["id"]
    nombreapellido = request.form["nombreapellido"]
    numerotelefono = request.form["numerotelefono"]
    fechahora      = datetime.datetime.now(pytz.timezone("America/Matamoros"))
    
    cursor = con.cursor()

    if id:
        sql = """
        UPDATE contactos_log SET
        Nombre_Apellido = %s,
        Numero_Telefono = %s
        WHERE Id_Log = %s
        """
        val = (nombreapellido, numerotelefono, id)
    else:
        sql = """
        INSERT INTO contactos_log (Nombre_Apellido, Numero_Telefono, Fecha_Hora)
                        VALUES (%s,              %s,              %s)
        """
        val =                 (nombreapellido, numerotelefono, fechahora)
    
    cursor.execute(sql, val)
    con.commit()
    con.close()

    pusher_client = pusher.Pusher(
        app_id="1767930",  # Cambia esto a tu nueva app_id de Pusher
        key="e6d3475eaa59a14fec17",
        secret="c9dd4d864a7413ae936d",
        cluster="us2",
        ssl=True
    )

    pusher_client.trigger("canalRegistrosContactos", "registroContactos", {})

    return jsonify({})
