import os
import datetime
from flask import Flask 

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY_APP'),
        DATABASE_HOST = os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER = os.environ.get('FLASK_DATABASE_USER'),
        DATABASE = os.environ.get('FLASK_DATABASE')
    )
    ## Import conexion a base de datos 
    from .db import db
    db.init_app(app)

    ## import BluePrint
    from .routes import home

    ## Inscribiendo BluePrint
    app.register_blueprint(home.bp)


    @app.template_filter('strftime_short')
    def date_format_short(value):
        dias = {
            0: "Dom",
            1: "Lun",
            2: "Mar",
            3: "Mié",
            4: "Jue",
            5: "Vie",
            6: "Sáb",
        }
        diaNum = int(value.strftime("%w"))
        dia = dias.get(diaNum)
       
        return "{}, {}/{}".format(dia, value.day, value.month-1)

    return app