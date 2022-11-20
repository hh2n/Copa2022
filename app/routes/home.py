from flask import (
    Blueprint, render_template, g, request, jsonify, redirect, url_for, session, flash
)
from datetime import datetime, timedelta
from app.models.grupos import Grupos
from app.models.user import Usuario
from app.routes.auth import login_required


bp = Blueprint('home', __name__, url_prefix='/')

dbgrupo = Grupos()
user = Usuario()

@bp.route('/', methods=['GET'])
@login_required
def index():
    rows = []
    partidos = []
    posiciones = dbgrupo.get_catGrupos() 
    encuentros = dbgrupo.get_catFechas()
    usuarios = user.get_allUsuarios()
    if posiciones:
        for item in posiciones:
            content = {
                'idGrupo': item['id'],
                'digito': item['digito'],
                'nomGrupo': item['nomGrupo'],
                'equipos': dbgrupo.get_grupos(item['id'])
            }
            rows.append(content)
            
    if encuentros:
        for item in encuentros:
            content = {
                'idFase': item['idFase'],
                'fase': item['fase'],
                'fecha': item['fecha'],
                'partidos': dbgrupo.get_partidos(item['fecha'])
            }
            partidos.append(content)  
        
    return render_template(
        'home/index.html', 
        grupos=rows,  
        encuentros=partidos,
        usuarios=usuarios
    )

@bp.route('/partido', methods=['GET','POST'])
@login_required
def partido():
    data = []
    response = False
    msg = 'Sin acciones'
    if request.method == 'POST':
        params = request.get_json()
        data = dbgrupo.get_partidoId(params['id'])
        if data:
            idUser = session['user_id']
            pronostico = dbgrupo.get_miPronostico(params['id'], idUser)
            response = True
            msg='success'
        
        return jsonify({'success': response, 'msg':msg, 'data':data, 'pronostico':pronostico })

    return jsonify({'success': response, 'msg': msg})

@bp.route('/savepros', methods=['GET','POST'])
@login_required
def savePronostico():
    message = None
    category = 'danger'
    if request.method == 'POST':
        ###############  ############### ############################## ###############
        id = request.form['idpartido']
        golesEq1 = request.form['txt_resulEq1']
        golesEq2 = request.form['txt_resulEq2']
        idEq1 = request.form['idEquipo1']
        idEq2 = request.form['idEquipo2']
        idUser = session['user_id']

        if golesEq1 == '' or golesEq2 == '':
            message = 'Recuerda no dejar ningun campo vacio para ninguno de los equipos.'

        if id and message is None:
            dbgrupo.update_partido(id, golesEq1, golesEq2, idEq1, idEq2, idUser)
            response = True
            message='Tu pronóstico ha sido almacenado con exito !!!'
            category = 'success'
        
        flash(message, category)
        
        return redirect(url_for('home.index'))

    return render_template('home/index.html')