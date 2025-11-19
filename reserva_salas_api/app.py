from flask import Flask, jsonify
from flask_cors import CORS

from routes.classroom import classroom_bp
from routes.participant import participant_bp

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Registrar rutas
app.register_blueprint(classroom_bp)
app.register_blueprint(participant_bp)

@app.route('/')
def home():
    return jsonify({"message": "Sistema de reserva de aulas activo."})

if __name__ == '__main__':
    app.run(debug=True)
