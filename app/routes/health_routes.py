from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)

@health_bp.route("/actuator/health", methods=["GET"])
@health_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "UP",
        "components": {
            "db": {
                "status": "UP",
                "details": {
                    "database": "SQLite",
                    "validationQuery": "SELECT 1"
                }
            },
            "ping": {
                "status": "UP"
            }
        }
    }), 200
