import functools
import time
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf.csrf import generate_csrf
from app.models.user import Usuario

bp = Blueprint('auth', __name__, url_prefix='/auth')

model = Usuario()


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        error = None
        user = model.get_userMail(email)
        if user is None:
            error = 'Usuario y/o contraseña incorrectos.'
        elif not check_password_hash(user['passwordd'], password):
            error = 'Usuario y/o contraseña incorrectos.'

        if error is None:
            session.clear()
            session['user_id'] = user['idUser']
            return redirect(url_for('home.index'))

        flash(error)

    return render_template('auth/index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        ###############  ############### ############################## ###############
        nombre = request.form['txt_name']
        apellido = request.form['txt_apellido']
        email = request.form['txt_mail']
        password = request.form['txt_password']
        error = None
        
        if not nombre:
            error = 'El Nombre es requerido'

        if not apellido:
            error = 'El Apellido es requerido'
        
        if not email:
            error = 'El Correo Electrónico es requerido'
        
        if not password:
            error = 'La contraseña es requerida'

        if error is None:
            user = model.get_userMail(email)
            if user is None:
                try:
                    password = generate_password_hash(password, 'sha256', 30)
                    model.password = generate_password_hash(password, 'sha256', 30)
                    #Insertamos en Base de datos
                    id = model.insert_user(nombre, apellido, email, password)
                    if id:
                        return redirect(url_for('auth.login'))
                    else:
                        error = 'Error al intentar crear el registro, intentalo de nuevo.'

                except Exception as inst:
                    error = 'Error: <i>('+str(inst)+')</i>'

            else:

                error = 'El correo electrónico ingresado ya existe, intenta con uno diferente.'
                
        flash(error)

    return render_template('auth/register.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        session.permanent = True
        session.modified = True
        g.saludo = generar_saludo()
        g.user = model.get_user(user_id)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def generar_saludo():
    d = time.strftime("%p")  # %p - Equivalente de AM o PM

    if d == "AM":
        return "Benos dias"
    else:
        h = int(time.strftime("%H"))
        if h < 18:
            return "Buenas tardes"
        else:
            return "Buenas noches"

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))