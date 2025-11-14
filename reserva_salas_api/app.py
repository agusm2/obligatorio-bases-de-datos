from flask import Flask, jsonify
from routes.classroom import classroom_bp
from routes.participant import participant_bp

app = Flask(__name__)

# Registrar rutas
app.register_blueprint(classroom_bp)
app.register_blueprint(participant_bp)

@app.route('/')
def home():
    return jsonify({"message": "Sistema de reserva de aulas activo."})

if __name__ == '__main__':
    app.run(debug=True)
