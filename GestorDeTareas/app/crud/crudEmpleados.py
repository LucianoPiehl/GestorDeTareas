from flask import Blueprint

empleados_bp = Blueprint('empleados', __name__)

@empleados_bp.route('/empleados')
def obtener_empleados():
    # Lógica de obtención de empleados
    return "Lista de empleados"
