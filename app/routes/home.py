from flask import (
    Blueprint, render_template, g
)
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