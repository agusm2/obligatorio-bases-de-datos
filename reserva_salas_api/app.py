from flask import Flask, jsonify
from flask_cors import CORS

from routes.classroom import classroom_bp
from routes.participant import participant_bp
from routes.reservation import reservations_bp

app = Flask(__name__)

<<<<<<< Updated upstream
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Registrar rutas
=======
# Register blueprints
>>>>>>> Stashed changes
app.register_blueprint(classroom_bp)
app.register_blueprint(participant_bp)
app.register_blueprint(reservations_bp)

@app.route('/')
def home():
    return jsonify({"message": "Room reservation system is active."})

if __name__ == '__main__':
    app.run(debug=True)
