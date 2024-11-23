from flask import Flask, render_template, request, jsonify
import requests

# Configuración del modelo
MODEL_URL = "https://proyectfinalv2.australiaeast.inference.ml.azure.com/score"
AUTH_TOKEN = "gwLP4msIkAFASVIjVAhSFlcViCJMVQg7"

headers = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json"
}

# Inicialización de Flask
app = Flask(__name__)

# Ruta principal para la interfaz
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Recibir datos del formulario
        distancia = float(request.form.get("distancia"))
        trafico = int(request.form.get("trafico"))
        clima = request.form.get("clima")
        hora_dia = request.form.get("hora_dia")
        dia_semana = request.form.get("dia_semana")

        # Construir el payload para el modelo
        data = {
            "input_data": {
                "data": [
                    {
                        "distancia": distancia,
                        "trafico": trafico,
                        "clima": clima,
                        "hora_dia": hora_dia,
                        "dia_semana": dia_semana
                    }
                ]
            }
        }

        # Consumir el modelo en Azure
        try:
            response = requests.post(MODEL_URL, headers=headers, json=data)
            prediction = response.json() if response.status_code == 200 else response.text
        except Exception as e:
            prediction = f"Error al conectar con el modelo: {e}"

        # Mostrar el resultado en la página
        return render_template("index.html", prediction=prediction)

    # Renderizar la página inicial
    return render_template("index.html", prediction=None)



# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
