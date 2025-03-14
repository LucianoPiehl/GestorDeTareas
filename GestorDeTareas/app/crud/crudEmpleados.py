from flask import Blueprint, jsonify, request
from crud.db import get_db

empleados_bp = Blueprint('empleados', __name__)

@empleados_bp.route('/obtenerEmpleados', methods=['GET'])
def obtenerEmpleados():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM empleado")

    column_names = [desc[0] for desc in cursor.description]
   
    lista = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    return jsonify(lista)

@empleados_bp.route('/obtenerEmpleado/<int:id>', methods=['GET'])
def obtenerEmpleado(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM empleado WHERE idEmpleado = %s", (id,))
    empleado = cursor.fetchone()
    
    if not empleado:
        return jsonify({"error": "Empleado no encontrado"}), 404

    return jsonify({
        "idEmpleado": empleado[0],
        "nombreEmpleado": empleado[1],
        "apellidoEmpleado": empleado[2],
        "rol": empleado[3]

    })

@empleados_bp.route('/insertarEmpleado',methods=['POST'])
def insertarEmpleado():
    data = request.get_json() 
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400
    id = data.get('id')
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    rol = data.get('rol')
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""INSERT into empleado (idEmpleado, nombre, apellido, rol)
               VALUES (%s, %s, %s, %s);""",(id, nombre, apellido, rol))
    db.commit()
    return jsonify({"mensaje": "Empleado creado", "id": id, "nombreEmpleado": nombre, "apellido":apellido, "rol":rol})


@empleados_bp.route('/eliminarEmpleado/<int:id>',methods=['DELETE'])
def eliminarEmpleado(id):
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""DELETE FROM empleado WHERE idEmpleado = %s""",(id,))
    db.commit()
    return jsonify({"mensaje": "Empleado eliminada", "id": id})


@empleados_bp.route('/actualizarEmpleado/<int:id>',methods=['PUT'])
def actualizarEmpleado(id):
    data = request.get_json()  # Recibir JSON
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400

    nombre = data.get('nombre')
    apellido = data.get('apellido')
    rol = data.get('rol')
    id = data.get('id')


    db = get_db()
    cursor = db.cursor()
    cursor.execute("""UPDATE empleado set nombre=%s,apellido=%s,rol=%s
                    WHERE idEmpleado = %s;""",(nombre, apellido, rol, id))
    db.commit()
    return jsonify({"mensaje": "Empleado actualizada", "id": id, "nombre": nombre, "apellido": apellido,"rol": rol})

@empleados_bp.route('/asociarTarea/<int:idEmpleado>', methods=['POST'])
def asociarTareaAEmpleado(idEmpleado):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400

    idTarea = data.get('idTarea')
    if not idTarea:
        return jsonify({"error": "idTarea es obligatorio"}), 400

    db = get_db()
    cursor = db.cursor()
    rol = data.get('rol')

    # Verificar si existen el empleado y la tarea
    cursor.execute("SELECT 1 FROM empleado WHERE idEmpleado = %s", (idEmpleado,))
    if not cursor.fetchone():
        return jsonify({"error": "Empleado no encontrado"}), 404

    cursor.execute("SELECT 1 FROM tarea WHERE idTarea = %s", (idTarea,))
    if not cursor.fetchone():
        return jsonify({"error": "Tarea no encontrada"}), 404

    # Asociar la tarea al empleado
    cursor.execute("INSERT INTO tareaxempleado (idEmpleado, idTarea, rol) VALUES (%s, %s, %s)", (idEmpleado, idTarea,rol))
    db.commit()

    return jsonify({"mensaje": "Tarea asociada correctamente", "idEmpleado": idEmpleado, "idTarea": idTarea})

@empleados_bp.route('/<int:idEmpleado>/eliminarTarea/<int:idTarea>', methods=['DELETE'])
def eliminarAsociacionTareaEmpleado(idEmpleado, idTarea):
    db = get_db()
    cursor = db.cursor()

    # Verificar si la asociación existe
    cursor.execute("SELECT 1 FROM tareaxempleado WHERE idEmpleado = %s AND idTarea = %s", (idEmpleado, idTarea))
    if not cursor.fetchone():
        return jsonify({"error": "La asociación no existe"}), 404

    # Eliminar la asociación
    cursor.execute("DELETE FROM tareaxempleado WHERE idEmpleado = %s AND idTarea = %s", (idEmpleado, idTarea))
    db.commit()

    return jsonify({"mensaje": "Asociación eliminada correctamente", "idEmpleado": idEmpleado, "idTarea": idTarea})