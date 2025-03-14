from flask import Flask, redirect, render_template, render_template, request, session, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

from crud.crudTareas import tareas_bp
from crud.crudEmpleados import empleados_bp
from crud.crudEquipos import equipos_bp
from crud.db import close_db, get_db

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username
    
    def get_id(self):
        return self.id
login_manager = LoginManager() 
def create_app():
    app = Flask(__name__)
  
    app.secret_key = 'supersecretkey'  # Necesario para manejar las sesiones
    login_manager.login_view = 'login'
    # Inicializar LoginManager
    login_manager.init_app(app)

    # Registrar los blueprints
    app.register_blueprint(tareas_bp, url_prefix='/tareas')
    app.register_blueprint(empleados_bp, url_prefix='/empleados')
    app.register_blueprint(equipos_bp, url_prefix='/equipos')
    app.teardown_appcontext(close_db)

    @login_manager.user_loader
    def load_user(user_id):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        if user:
            return User(user['id'], user['username'])
        return None

    # Ruta de login
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            contrasenia = request.form['contrasenia']
            
            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()
            
            # Validación de usuario
            if user and user['contrasenia'] == contrasenia:
                # Crear un usuario y guardarlo en la sesión
                user_obj = User(user['id'], user['username'])
                login_user(user_obj)
                return redirect(url_for('index'))
            else:
                session['error'] = 'Usuario o contraseña incorrectos'
                return redirect(url_for('login'))
        
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login'))



    @app.route('/')
    @login_required
    def index():
        print("Accediendo a /index")
        return render_template('index.html')
    
    @app.route('/empleados')   
    @login_required 
    def empleados():
        return render_template('empleados.html')

    @app.route('/tareas')
    @login_required
    def tareas():
        return render_template('tareas.html')
    
    @app.route('/equipos')
    @login_required
    def equipos():
        return render_template('equipos.html')
    
 
    return app