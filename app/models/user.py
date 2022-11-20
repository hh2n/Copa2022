from app.db.db import get_db
from app.models.config_db import Config


class Usuario(Config):
    
    def __init__(self):
        self._idUser = ''
        self._estado = ''
        
    ### Setters AND Getters
    ############# id user
    @property
    def id(self):
        return self._idUser
    
    @id.setter
    def id(self, id):
        self._idUser = id

    ############# Estado
    @property
    def estado(self):
        return self._estado
    
    @estado.setter
    def estado(self, estado):
        self._estado = estado

    #############################
    def insert_user(self, nombre, apaterno, email, passwd):
        db, c = get_db()
        c.execute(
            'INSERT INTO `'+self.tblUsers+'` (`pnombre`, `apaterno`,`email`,`passwordd`) VALUES ( %s, %s, %s, %s)', 
            (nombre, apaterno, email, passwd)
        )
        db.commit()
        idLast = c.lastrowid
        return idLast

    def get_allUsuarios(self):
        db, c = get_db()
        c.execute(
            'SELECT tu.idUser, tu.email, tu.telefono, tu.foto	,'
            'CONCAT_WS(" ", tu.pnombre, tu.apaterno) as nombreUser '
            'FROM '+self.tblUsers+' tu WHERE tu.estado = 1 ORDER BY nombreUser ASC '
        )
        return c.fetchall()

    def get_userMail(self, mail):
        db, c = get_db()
        c.execute(
            'SELECT * FROM '+self.tblUsers+' WHERE email= %s AND estado = 1', (mail, )
        )
        return c.fetchone()

    def get_user(self, id):
        db, c = get_db()
        c.execute(
            'SELECT tu.idUser, tu.foto , tu.email , tu.telefono , tu.online ,'
            'CONCAT_WS(" ", TRIM(tu.pnombre) , TRIM(tu.apaterno)) AS shortName '
            'FROM '+ self.tblUsers +' tu '
            'WHERE tu.idUser = %s', 
            (id, )
        )
        return c.fetchone()
    
    def update_estado(self):
        db, c = get_db()
        c.execute(
            'UPDATE '+self.tbl_users+' SET `activo` = %s WHERE `id_usuario` = %s',
            (self.estado, self.id)
        )
        db.commit()
