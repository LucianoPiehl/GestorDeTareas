from flask import Blueprint, jsonify, request
from crud.db import get_db

tareas_bp = Blueprint('tareas', __name__)
@tareas_bp.route('/obtenerTareas', methods=['GET'])
def obtenerTareas():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM TAREA")

    column_names = [desc[0] for desc in cursor.description]
   
    lista = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    return jsonify(lista)

@tareas_bp.route('/obtenerTarea/<int:id>', methods=['GET'])
def obtenerTarea(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tarea WHERE idTarea = %s", (id,))
    tarea = cursor.fetchone()
    
    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404

    return jsonify({
        "idTarea": tarea[0],
        "nombreTarea": tarea[1],
        "fechaFin": tarea[2],
        "fechaInicio": tarea[3],
        "estado": tarea[4]
    })

@tareas_bp.route('/insertarTareas',methods=['POST'])
def insertarTarea():
    data = request.get_json()  # Recibir JSON
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400
    id = data.get('id')
    nombreTarea = data.get('nombreTarea')
    fechaFin = data.get('fechaFin')
    fechaInicio = data.get('fechaInicio')
    estado = data.get('estado')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""INSERT into tarea (idTarea, nombreTarea, fechaFin, fechaInicio, estado)
               VALUES (%s, %s, %s, %s, %s);""",(id, nombreTarea, fechaFin, fechaInicio, estado))
    db.commit()
    return jsonify({"mensaje": "Tarea creada", "id": id, "nombreTarea": nombreTarea, "fechaFin":fechaInicio, "fechaInicio":fechaInicio, "estado":estado})


@tareas_bp.route('/eliminarTarea/<int:id>',methods=['DELETE'])
def eliminarTarea(id):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""DELETE FROM tarea WHERE idTarea = %s""",(id,))
    db.commit()
    return jsonify({"mensaje": "Tarea eliminada", "id": id})


@tareas_bp.route('/actualizarTarea/<int:id>',methods=['PUT'])
def actualizarTarea(id):
    data = request.get_json()  # Recibir JSON
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400

    nombreTarea = data.get('nombreTarea')
    fechaFin = data.get('fechaFin')
    fechaInicio = data.get('fechaInicio')
    estado = data.get('estado')

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""UPDATE tarea set nombreTarea=%s, fechaFin=%s, fechaInicio=%s, estado=%s
                    WHERE idTarea = %s;""",(nombreTarea, fechaFin, fechaInicio, estado, id))
    db.commit()
    return jsonify({"mensaje": "Tarea actulizada", "id": id, "nombreTarea": nombreTarea, "fechaFin":fechaInicio, "fechaInicio":fechaInicio, "estado":estado})

