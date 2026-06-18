from models.db_manager import DBManager

class Categoria:
    def __init__(self, nombre_categoria, descripcion_categoria=None, id_categoria=None):
        self.id_categoria = id_categoria
        self.nombre = nombre_categoria
        self.descripcion = descripcion_categoria
        self.db = DBManager()

    @classmethod
    def obtener_todas(cls):
        """
        Consulta todas las categorías disponibles.
        Útil para llenar los Selects/Dropdowns en el frontend.
        """
        db = DBManager()
        query = "SELECT * FROM Categoria ORDER BY nombre_categoria ASC"
        return db.consultar(query)

    @classmethod
    def obtener_por_id(cls, id_categoria):
        """Busca una categoría específica."""
        db = DBManager()
        query = "SELECT * FROM Categoria WHERE id_categoria = ?"
        res = db.consultar(query, (id_categoria,))
        
        if not res:
            return None
            
        c = res[0]
        return cls(
            nombre_categoria=c['nombre_categoria'],
            descripcion_categoria=c['descripcion_categoria'],
            id_categoria=c['id_categoria']
        )

    def registrar(self):
        """Permite crear nuevas categorías (ej: 'Suscripciones Digitales')."""
        query = """
            INSERT INTO Categoria (nombre_categoria, descripcion_categoria)
            VALUES (?, ?)
        """
        params = (self.nombre, self.descripcion)
        nuevo_id = self.db.ejecutar_consulta(query, params)
        
        if nuevo_id:
            self.id_categoria = nuevo_id
            return True
        return False