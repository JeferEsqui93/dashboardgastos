from models.db_manager import DBManager

class Permisos:
    def __init__(self, nombre_permiso, slug, id_permiso=None):
        self.id_permiso = id_permiso
        self.slug = slug
        self.nombre_permiso = nombre_permiso
        self.db = DBManager()

    @classmethod
    def obtener_por_id(cls, id_permiso):
        db = DBManager()
        query = """
            SELECT * FROM Permisos WHERE id_permiso = ?
        """
        res = db.consultar(query, (id_permiso,))

        if not res:
            return None

        return cls(
            nombre_permiso=res[0]['nombre_permiso'],
            slug=res[0]['slug'],
            id_permiso=res[0]['id_permiso']
        )