import re
from flask_bcrypt import Bcrypt
from flask import Flask, redirect, render_template, render_template, request, session, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from datetime import datetime, timedelta
from crud.crudTareas import tareas_bp
from crud.crudEmpleados import empleados_bp
from crud.crudEquipos import equipos_bp
from crud.db import close_db, get_db

# Número máximo de intentos fallidos
MAX_ATTEMPTS = 2
# Tiempo de bloqueo en minutos
BLOCK_TIME = 15

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username
    
    def get_id(self):
        return self.id
login_manager = LoginManager() 

def create_app():
    app = Flask(__name__)
    bcrypt = Bcrypt(app)
    app.secret_key = 'supersecretkey'  # Necesario para manejar las sesiones
    login_manager.login_view = 'login'
    # Inicializar LoginManager
    login_manager.init_app(app)
    
    # Registrar los blueprints
    app.register_blueprint(tareas_bp, url_prefix='/tareas')
    app.register_blueprint(empleados_bp, url_prefix='/empleados')
    app.register_blueprint(equipos_bp, url_prefix='/equipos')
    app.teardown_appcontext(close_db)

    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            contrasenia = request.form['contrasenia']
            if not validar_contrasenia(contrasenia):
                session['error'] = 'La contraseña debe tener al menos 8 caracteres, una letra mayúscula, una letra minúscula, un número y un símbolo.'
                return redirect(url_for('register'))
        
            # Verifica si el usuario ya existe
            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                session['error'] = 'El nombre de usuario ya existe'
                return redirect(url_for('register'))

            # Crea una nueva cuenta con contraseña encriptada
            hashed_password = bcrypt.generate_password_hash(contrasenia).decode('utf-8')  # Encriptar la contraseña
            print(f"Tipo de hashed_password: {type(hashed_password)}")
            print(f"Valor del hashed_password: {hashed_password}")

            cursor.execute("INSERT INTO users (username, contrasenia) VALUES (%s, %s)", (username, hashed_password))
            db.commit()
            
            return redirect(url_for('login'))

        return render_template('register.html')
    # Al iniciar sesión, verifica la contraseña hasheada
    def check_user_password(user_input_password, db_stored_password):
        return bcrypt.check_password_hash(db_stored_password, user_input_password)
    
    def validar_contrasenia(contrasenia):
        # Verifica si la contraseña tiene al menos 8 caracteres, al menos una letra mayúscula, una letra minúscula, un número y un símbolo
        regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!$%^&*?])[A-Za-z\d!$%^&*?]{8,}$'
        return re.match(regex, contrasenia) is not None

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

            # Verifica si el usuario existe
            if user:
                # Verifica si el usuario está bloqueado
                if 'login_attempts' in session and session['login_attempts'] >= MAX_ATTEMPTS:
                    # Convertir el tiempo bloqueado a naive para la comparación
                    time_locked = session.get('locked_until', datetime.now()).replace(tzinfo=None)
                    if time_locked > datetime.now():
                        session['error'] = f"Cuenta bloqueada. Intenta de nuevo después de {BLOCK_TIME} minutos."
                        return redirect(url_for('login'))
                    else:
                        # Si el tiempo de bloqueo ha pasado, resetea los intentos
                        session.pop('login_attempts', None)
                        session.pop('locked_until', None)

                # Verifica la contraseña (usando la función de bcrypt que ya tienes)
                if check_user_password(contrasenia, user['contrasenia']):
                    # Si la contraseña es correcta, resetea los intentos de login
                    session.pop('login_attempts', None)
                    session.pop('locked_until', None)
                    
                    # Crear un usuario y guardarlo en la sesión
                    user_obj = User(user['id'], user['username'])
                    login_user(user_obj)
                    return redirect(url_for('index'))
                else:
                    # Si la contraseña es incorrecta, incrementa el contador de intentos
                    session['login_attempts'] = session.get('login_attempts', 0) + 1
                    if session['login_attempts'] >= MAX_ATTEMPTS:
                        session['locked_until'] = datetime.now() + timedelta(minutes=BLOCK_TIME)
                        session['error'] = f"Has alcanzado el número máximo de intentos fallidos. Tu cuenta será bloqueada por {BLOCK_TIME} minutos."
                    else:
                        session['error'] = 'Usuario o contraseña incorrectos'
                    return redirect(url_for('login'))

            else:
                session['error'] = 'Usuario no encontrado'
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