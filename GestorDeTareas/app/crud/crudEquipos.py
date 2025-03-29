from flask import Blueprint, jsonify, request
from crud.db import get_db

equipos_bp = Blueprint('equipos', __name__)

@equipos_bp.route('/obtenerEquipos', methods=['GET'])
def obtenerEquipos():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM equipo")

    column_names = [desc[0] for desc in cursor.description]
   
    lista = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    return jsonify(lista)

@equipos_bp.route('/obtenerEquipo/<int:id>', methods=['GET'])
def obtenerEquipo(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM equipo WHERE idEquipo = %s", (id,))
    equipo = cursor.fetchone()
    
    if not equipo:
        return jsonify({"error": "Equipo no encontrado"}), 404

    return jsonify({
        "idEquipo": equipo[0],
        "nombreEquipo": equipo[1]
    })

@equipos_bp.route('/insertarEquipo',methods=['POST'])
def insertarEquipo():
    data = request.get_json() 
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400
    id = data.get('id')
    nombreEquipo = data.get('nombreEquipo')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""INSERT into equipo (idEquipo, nombreEquipo)
               VALUES (%s, %s);""",(id, nombreEquipo))
    db.commit()
    return jsonify({"mensaje": "Equipo creado", "id": id, "nombreEquipo": nombreEquipo})


@equipos_bp.route('/eliminarEquipo/<int:id>',methods=['DELETE'])
def eliminarEquipo(id):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""DELETE FROM equipo WHERE idEquipo = %s""",(id,))
    db.commit()
    return jsonify({"mensaje": "Equipo eliminado", "id": id})


@equipos_bp.route('/actualizarEquipo/<int:id>',methods=['PUT'])
def actualizarEquipo(id):
    data = request.get_json()  # Recibir JSON
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400

    nombreEquipo = data.get('nombreEquipo')


    db = get_db()
    cursor = db.cursor()
    cursor.execute("""UPDATE equipo set nombreEquipo=%s
                    WHERE idEquipo = %s;""",(nombreEquipo, id))
    db.commit()
    return jsonify({"mensaje": "Equipo actualizado", "id": id, "nombreEquipo": nombreEquipo})


@equipos_bp.route('/asociarEmpleadoAEquipo/<int:idEquipo>', methods=['POST'])
def asociarEmpleadoAEquipo(idEquipo):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400

    idEmpleado = data.get('idEmpleado')
    if not idEmpleado:
        return jsonify({"error": "idEmpleado es obligatorio"}), 400

    db = get_db()
    cursor = db.cursor()
    rol = data.get('rol')

    # Verificar si existen el empleado y la tarea
    cursor.execute("SELECT 1 FROM empleado WHERE idEmpleado = %s", (idEmpleado,))
    if not cursor.fetchone():
        return jsonify({"error": "Empleado no encontrado"}), 404

    cursor.execute("SELECT 1 FROM equipo WHERE idEquipo = %s", (idEquipo,))
    if not cursor.fetchone():
        return jsonify({"error": "Equipo no encontrado"}), 404

    # Asociar la tarea al empleado
    cursor.execute("INSERT INTO empleadoxequipo (idEmpleado, idEquipo, rol) VALUES (%s, %s, %s)", (idEmpleado, idEquipo,rol))
    db.commit()

    return jsonify({"mensaje": "Equipo asociado correctamente", "idEmpleado": idEmpleado, "idEquipo": idEquipo})

@equipos_bp.route('/<int:idEmpleado>/eliminarEmpleadoDeEquipo/<int:idEquipo>', methods=['DELETE'])
def eliminarAsociacionEmpleadoEquipo(idEmpleado, idEquipo):
    db = get_db()
    cursor = db.cursor()

    # Verificar si la asociación existe
    cursor.execute("SELECT 1 FROM empleadoxequipo WHERE idEmpleado = %s AND idEquipo = %s", (idEmpleado, idEquipo))
    if not cursor.fetchone():
        return jsonify({"error": "La asociación no existe"}), 404

    # Eliminar la asociación
    cursor.execute("DELETE FROM empleadoxequipo WHERE idEmpleado = %s AND idEquipo = %s", (idEmpleado, idEquipo))
    db.commit()

    return jsonify({"mensaje": "Asociación eliminada correctamente", "idEmpleado": idEmpleado, "idEquipo": idEquipo})