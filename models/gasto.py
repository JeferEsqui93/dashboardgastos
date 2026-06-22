from models.db_manager import DBManager
from datetime import datetime

class Gasto:
    def __init__(self, id_usuario, id_categoria, costo, descripcion_gasto=None, fecha=None, id_gasto=None):
        self.id_gasto = id_gasto
        self.id_usuario = id_usuario
        self.id_categoria = id_categoria
        self.descripcion_gasto = descripcion_gasto
        self.costo = costo
        # Si no envían fecha, usamos la de hoy en formato ISO (YYYY-MM-DD)
        self.fecha = fecha if fecha else datetime.now().strftime('%Y-%m-%d')
        self.db = DBManager()

    def registrar(self):
        """Guarda un nuevo gasto. Retorna True si tuvo éxito."""
        query = """
            INSERT INTO Gasto (id_usuario, id_categoria, descripcion_gasto, fecha, costo)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (self.id_usuario, self.id_categoria, self.descripcion_gasto, self.fecha, self.costo)
        
        nuevo_id = self.db.ejecutar_consulta(query, params)
        if nuevo_id:
            self.id_gasto = nuevo_id
            return True
        return False

    def actualizar(self):
        """Actualiza un registro. Retorna True si tuvo éxito."""
        if not self.id_gasto:
            return False  # Si no tiene ID, no podemos actualizar nada
        
        query = """
            UPDATE Gasto 
            SET id_categoria = ?, descripcion_gasto = ?, costo = ?, fecha = ?
            WHERE id_gasto = ?
        """
        params = (self.id_categoria, self.descripcion_gasto, self.costo, self.fecha, self.id_gasto)
        
        nuevo_id = self.db.ejecutar_consulta(query, params)
        if nuevo_id:
            self.id_gasto = nuevo_id
            return True
        return False        

    @classmethod
    def obtener_por_id_usuario(cls, id_usuario):
        """
        Trae todos los gastos de un usuario.
        Usamos un JOIN para traer el nombre de la categoría de una vez.
        """
        db = DBManager()
        query = """
            SELECT g.*, c.nombre_categoria 
            FROM Gasto g
            JOIN Categoria c ON g.id_categoria = c.id_categoria
            WHERE g.id_usuario = ?
            ORDER BY g.fecha DESC
        """
        # Aquí retornamos la lista de resultados directamente (objetos Row)
        # para que el controlador decida cómo mostrarlos.
        return db.consultar(query, (id_usuario,))

    @classmethod
    def obtener_por_id_gasto(cls, id_gasto):
        db = DBManager()
        query = "SELECT * FROM Gasto WHERE id_gasto = ?"
        res = db.consultar(query, (id_gasto,))

        if not res:
            return None

        res = res[0]
        return cls(
            id_gasto = res['id_gasto'],
            id_usuario = res['id_usuario'],
            id_categoria = res['id_categoria'],
            descripcion_gasto = res['descripcion_gasto'],
            costo = res['costo'],
            fecha = res['fecha']
        )

    @classmethod
    def eliminar(cls, id_gasto):
        """Borra un gasto por su ID."""
        db = DBManager()
        query = "DELETE FROM Gasto WHERE id_gasto = ?"
        # Si la consulta devuelve algo distinto a None, es que se ejecutó
        return db.ejecutar_consulta(query, (id_gasto,)) is not None

    @classmethod
    def obtener_gastos_por_categoria(cls, id_usuario, fecha_desde=None):
        db = DBManager()
        # Iniciamos la lista de parámetros con el id_usuario (que siempre es obligatorio)
        parametros = [id_usuario]
        
        # 1. Separamos el inicio de la consulta (Antes del GROUP BY)
        query_base = """
            SELECT c.nombre_categoria, SUM(g.costo) as total
            FROM Gasto g
            JOIN Categoria c ON g.id_categoria = c.id_categoria
            WHERE g.id_usuario = ?
        """
               
        # 2. SI EL USUARIO ELIGIÓ UNA FECHA FILTRO, LE INYECTAMOS EL EXTRA AL WHERE
        if fecha_desde:
            query_base += " AND g.fecha >= ?"
            parametros.append(fecha_desde)  # Agregamos la fecha a la lista de parámetros
            
        # 3. Cerramos la consulta con el agrupamiento y ordenamiento obligatorio
        query_final = query_base + """
            GROUP BY c.nombre_categoria
            ORDER BY total DESC
        """
        
        # Convertimos la lista de parámetros en una tupla para tu db.consultar
        resultado = db.consultar(query_final, tuple(parametros))
        
        # Si el resultado es None o un entero por error, devolvemos lista vacía
        if not isinstance(resultado, list):
            return []
        
        return resultado