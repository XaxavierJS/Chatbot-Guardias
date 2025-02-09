from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    return "¡Hola, mundo! La aplicación se desplegó correctamente."

# Definir la ruta para el webhook (ejemplo: "/incoming")
@app.route("/incoming", methods=["POST"])
def incoming():
    # Procesar la información del mensaje de Twilio
    data = request.form  # O use request.get_json() si espera JSON
    # Aquí puede incluir la lógica para manejar el mensaje recibido
    return "Mensaje recibido", 200

if __name__ == "__main__":
    app.run()
