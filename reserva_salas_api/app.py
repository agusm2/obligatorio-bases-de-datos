from flask import Flask, jsonify, request
from routes.salas import salas_bp

app = Flask(__name__)

# Registrar rutas
app.register_blueprint(salas_bp)

@app.route('/')
def home():
    return jsonify({"message": "Sistema de reserva de salas activo."})

if __name__ == '__main__':
    app.run(debug=True)
