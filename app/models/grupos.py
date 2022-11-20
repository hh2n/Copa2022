
from app.db.db import get_db
from app.models.config_db import Config


class Grupos(Config):

    def get_catGrupos(self):
        db, c = get_db()
        c.execute(
            'SELECT cg.id, cg.nombre as nomGrupo, cg.digito FROM '+self.catGrupos+' cg WHERE estado = 1'
        )
        return c.fetchall()
    
    def get_catFechas(self):
        db, c = get_db()
        c.execute(
            'SELECT cf.idFase , cf.fase  , tp.fecha '
            'FROM cat_fase cf '
            'INNER JOIN tbl_partido tp ON tp.fkFase = cf.idFase '
            'WHERE cf.estado=1 AND cf.idFase = 1 '
            'GROUP BY tp.fecha '
        )
        return c.fetchall()
    
    def get_grupos(self, idGrupo):
        db, c = get_db()
        c.execute(
            'SELECT te.logo , te.nombre as nombreEquipo  '
            'FROM  '+self.tblGrupos+' tg  '
            'INNER JOIN '+self.tblEquipos+' te ON te.idEquipo = tg.fkEquipo '
            'WHERE tg.fkTorneo = 1 AND tg.fkGrupo = %s',
            (idGrupo, )
        )
        return c.fetchall()
    
    def get_partidos(self, fecha):
        db, c = get_db()
        c.execute(
            'SELECT tp.idPartido, eq1.nomGrupo as grupoEq1, eq1.nomEquipo as nomEquipo1, eq1.logo as logoEq1, '
            'eq2.nomGrupo as grupoEq2, eq2.nomEquipo as nomEquipo2, eq2.logo as logoEq2, '
            'tp.fecha , tp.horario , tp.goles_e1 , tp.goles_e2 , tp.estado  '
            'FROM tbl_partido tp '
            'INNER JOIN View_Grupos eq1 ON eq1.idGrupo = tp.fkEquipo_1 '
            'INNER JOIN View_Grupos eq2 ON eq2.idGrupo = tp.fkEquipo_2 '
            'WHERE tp.fecha = %s '
            'ORDER BY tp.fecha, tp.horario  ASC ',
            (fecha, )
        )
        return c.fetchall()
    
    def get_partidoId(self, id):
        db, c = get_db()
        c.execute(
            'SELECT tp.idPartido, eq1.idGrupo as idEq1, eq1.nomEquipo as nomEquipo1, eq1.logo as logoEq1, '
            'eq2.idGrupo as idEq2, eq2.nomEquipo as nomEquipo2, eq2.logo as logoEq2, '
            'tp.fecha , tp.goles_e1 , tp.goles_e2 , tp.estado '
            'FROM '+self.tblPartidos+' tp '
            'INNER JOIN View_Grupos eq1 ON eq1.idGrupo = tp.fkEquipo_1 '
            'INNER JOIN View_Grupos eq2 ON eq2.idGrupo = tp.fkEquipo_2 '
            'WHERE tp.idPartido = %s '
            'ORDER BY tp.fecha, tp.horario  ASC ',
            (id, )
        )
        return c.fetchone()
    
    def get_miPronostico(self, id, idUser):
        db, c = get_db()
        c.execute(
            'SELECT tp.idPronostico , tp.goles_equipo1 , tp.goles_equipo2  '
            'FROM '+self.tblPronostico+' tp '
            'WHERE tp.fkPartido = %s AND tp.fkUser = %s',
            (id, idUser)
        )
        return c.fetchone()

    def update_partido(self, id, golsEq1, golsEq2, idEq1, idEq2, idUser):
        db, c = get_db()
        c.execute(
            'INSERT INTO '+self.tblPronostico+' (`fkUser`, `fkPartido`, `fkGrupoEq1`, `fkGrupoEq2`, `goles_equipo1`, `goles_equipo2`) '
            'VALUES (%s, %s, %s, %s, %s, %s)',
            (idUser, id,  idEq1, idEq2, golsEq1, golsEq2)
        )
        db.commit()