from flask import Blueprint

equipos_bp = Blueprint('equipos', __name__)

@equipos_bp.route('/equipos')
def obtener_equipos():

    return "Lista de equipos"
