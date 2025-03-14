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
    return jsonify({"mensaje": "Equipo eliminada", "id": id})


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
    return jsonify({"mensaje": "Equipo actualizada", "id": id, "nombreEquipo": nombreEquipo})

