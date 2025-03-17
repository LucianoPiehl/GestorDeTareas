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
    cursor.execute("""
        INSERT INTO empleado (nombre, apellido, rol)
        VALUES (%s, %s, %s);
    """, (nombre, apellido, rol))
    db.commit()
    idEmpleado = cursor.lastrowid

    return jsonify({
        "mensaje": "Empleado creado",
        "id": idEmpleado,
        "nombre": nombre,
        "apellido": apellido,
        "rol": rol
    })


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


    db = get_db()
    cursor = db.cursor()
    cursor.execute("""UPDATE empleado set nombre=%s,apellido=%s,rol=%s
                    WHERE idEmpleado = %s;""",(nombre, apellido, rol, id))
    db.commit()
    return jsonify({"mensaje": "Empleado actualizada", "id": id, "nombre": nombre, "apellido": apellido,"rol": rol})

@empleados_bp.route('/asociarTareaAEmpleado/<int:idEmpleado>', methods=['POST'])
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

@empleados_bp.route('/<int:idEmpleado>/eliminarTareaDeEmpleado/<int:idTarea>', methods=['DELETE'])
def eliminarAsociacionTareaEmpleado(idEmpleado, idTarea):
    db = get_db()
    cursor = db.cursor()

    # Eliminar la asociación
    cursor.execute("DELETE FROM tareaxempleado WHERE idEmpleado = %s AND idTarea = %s", (idEmpleado, idTarea))
    db.commit()

    return jsonify({"mensaje": "Asociación eliminada correctamente", "idEmpleado": idEmpleado, "idTarea": idTarea})

@empleados_bp.route('/<int:idEmpleado>/tareas', methods=['GET'])
def obtenerTareasEmpleado(idEmpleado):
    db = get_db()
    cursor = db.cursor()

    # Obtener las tareas asociadas al empleado junto con el rol (Empleado o Jefe)
    cursor.execute("""
        SELECT t.idTarea, t.nombreTarea, te.rol 
        FROM tarea t 
        JOIN tareaxempleado te ON t.idTarea = te.idTarea 
        WHERE te.idEmpleado = %s
    """, (idEmpleado,))
    tareas = cursor.fetchall()
    
    if not tareas:
        return jsonify([])  # Si no tiene tareas, devolver lista vacía
    
    # Devolver las tareas junto con el rol
    return jsonify(tareas)

@empleados_bp.route('/cambiarRol/<int:id_empleado>/<int:id_tarea>/', methods=['PUT'])
def cambiar_rol_en_tarea(id_empleado, id_tarea):
    try:
        conexion = get_db()
        cursor = conexion.cursor()

        # Consultar el rol actual
        cursor.execute("SELECT rol FROM tareaxempleado WHERE idEmpleado = %s AND idTarea = %s", (id_empleado, id_tarea))
        resultado = cursor.fetchone()

        if not resultado:
            return jsonify({"mensaje": "Registro no encontrado"}), 404

        nuevo_rol = 0 if resultado[0] == 1 else 1  # Cambiar entre 0 y 1

        # Actualizar el rol en la tabla
        cursor.execute("UPDATE tareaxempleado SET rol = %s WHERE idEmpleado = %s AND idTarea = %s", (nuevo_rol, id_empleado, id_tarea))
        conexion.commit()

        return jsonify({"mensaje": "Rol actualizado correctamente"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conexion.close()