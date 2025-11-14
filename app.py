from flask import Flask, request, jsonify, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# -------------------------
#   BASE DE DATOS
# -------------------------

# Creamos 132 espacios vacíos
parqueadero = [
    {
        "id": i + 1,
        "id_vehiculo": None,
        "placa": None,
        "tipo_usuario": "Propietario",
        "estado": "Disponible",
        "hora_ingreso": None,
        "hora_salida": None
    }
    for i in range(132)
]

# Señal de sensor para disparar formularios
evento_sensor = None   # "entrada" o "salida"

# -------------------------
#  RUTAS API DESDE LA PICO
# -------------------------

@app.route("/sensor", methods=["POST"])
def sensor_event():
    """
    La Raspberry Pico envía:
    { "evento": "entrada" }  o  { "evento": "salida" }
    """
    global evento_sensor
    data = request.get_json()
    evento_sensor = data["evento"]
    print("Evento recibido:", evento_sensor)
    return jsonify({"status": "ok"})

# -------------------------
#  FORMULARIOS
# -------------------------

@app.route("/registrar_entrada", methods=["POST"])
def registrar_entrada():
    placa = request.form["placa"]

    # Buscar el primer espacio disponible
    for espacio in parqueadero:
        if espacio["estado"] == "Disponible":
            espacio["estado"] = "Ocupado"
            espacio["placa"] = placa
            espacio["id_vehiculo"] = espacio["id"]
            espacio["hora_ingreso"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return redirect(url_for("index"))

    return "No hay espacios disponibles"

@app.route("/registrar_salida", methods=["POST"])
def registrar_salida():
    placa = request.form["placa"]

    # Buscar el espacio ocupado por esa placa
    for espacio in parqueadero:
        if espacio["placa"] == placa and espacio["estado"] == "Ocupado":
            espacio["estado"] = "Disponible"
            espacio["hora_salida"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            espacio["placa"] = None
            espacio["id_vehiculo"] = None
            espacio["hora_ingreso"] = None
            return redirect(url_for("index"))

    return "Placa no encontrada"

# -------------------------
#  VISTA PRINCIPAL (PAGINADA)
# -------------------------

@app.route("/")
def index():
    global evento_sensor

    # PAGINACIÓN
    page = int(request.args.get("page", 1))
    per_page = 25
    start = (page - 1) * per_page
    end = start + per_page

    total_pages = (len(parqueadero) + per_page - 1) // per_page
    lista = parqueadero[start:end]

    # Detectar evento del sensor y mostrar formulario
    formulario = None
    if evento_sensor == "entrada":
        formulario = "entrada"
        evento_sensor = None
    elif evento_sensor == "salida":
        formulario = "salida"
        evento_sensor = None

    return render_template(
        "index.html",
        lista=lista,
        page=page,
        total_pages=total_pages,
        formulario=formulario
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
