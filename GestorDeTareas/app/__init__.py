from flask import Flask
from crud.crudTareas import tareas_bp
from crud.crudEmpleados import empleados_bp
from crud.crudEquipos import equipos_bp
from crud.db import close_db

def create_app():
    app = Flask(__name__)

    # Registrar los blueprints
    app.register_blueprint(tareas_bp, url_prefix='/tareas')
    app.register_blueprint(empleados_bp, url_prefix='/empleados')
    app.register_blueprint(equipos_bp, url_prefix='/equipos')
    app.teardown_appcontext(close_db)
    return app