from flask import Flask, render_template, request, jsonify, redirect, url_for
from entities.user import User
from entities.account import Account
from enums.transaction_type import TransactionType
from enums.value_permission import ValuePermission
from entities.log import Log
from enums.log_type import LogType
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
from functools import wraps
from flask import abort
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "index"

def admin_required(f):
    """Permite el acceso solo si el usuario es ADMIN y está activo."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_active or current_user.profile.value != 1:
            abort(403) # Prohibido
        return f(*args, **kwargs)
    return decorated_function

"""
def permission_required(required_permission: ValuePermission):
    # Permite el acceso si es ADMIN o si el perfil Custom tiene el Enum de permiso específico.
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_active:
                abort(403)
            
            if current_user.profile.value == 1:
                return f(*args, **kwargs)
            
            has_permission = any(p.value == required_permission for p in current_user.permissions)
            
            if not has_permission:
                abort(403)
                
            return f(*args, **kwargs)
        return decorated_function
    return 
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/welcome')
@login_required
def welcome():
    account = Account.get_account_by_id(current_user.id)
    return render_template('welcome.html', account=account)

@app.route('/api/users', methods=["POST"])
def create_user():
    data = request.get_json()
    
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if User.check_email_exists(email):
        return jsonify({"success": False, "message": "El correo electrónico ingresado ya se encuentra registrado."}), 409

    if User.save(name, email, password):
        return jsonify({"success": True, "message": "Su cuenta fue creada correctamente."}), 201
    else:
        return jsonify({"success": False, "message": "Ocurrió un error al crear su cuenta. Intente de nuevo."}), 500
    
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    email = data.get("email")
    password = data.get("password")

    user = User.check_login(email, password)
    if user:
        if user.is_active:
            login_user(user)

            Log.saveLog(user, "Inicio de sesión exitoso", LogType.LOGIN)

            return jsonify({
                "success": True,
                "message": "Sesión iniciada correctamente."
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "El usuario está suspendido, contacte a un administrador para más información."
            }), 403
    else:
        return jsonify({
            "success": False,
            "message": "Los datos de acceso ingresados no son correctos."
        }), 401

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route('/logs')
@login_required
def logs():
    logs_data = Log.get_all()
    return render_template('logs.html', logs=logs_data)

@app.route('/users')
@login_required
@admin_required # Solo ADMIN
def users():
    users_data = User.get_all()
    return render_template('users.html', users=users_data)

if __name__ == '__main__':
    app.run(debug=True)