from models.db_manager import DBManager
from models.rol import Rol

class Usuario:
    def __init__(self, nombres, apellidos, documento, correo, password_hash, celular=None, fecha_nacimiento=None, id_usuario=None):
        self.id_usuario = id_usuario
        self.nombres_usuario = nombres
        self.apellidos_usuario = apellidos
        self.documento = documento
        self.celular = celular
        self.correo = correo
        self.fecha_nacimiento = fecha_nacimiento
        self.password_hash = password_hash
        
        # Instanciamos el manager para usarlo en los métodos
        self.db = DBManager()

    @classmethod
    def validar_credenciales(cls, documento, password):
        """Retorna True o False de acuerdo a la validación de credenciales"""
        db = DBManager()
        query = """
            SELECT * FROM Usuario WHERE documento = ?
        """
        res = db.consultar(query, (documento,))

        if not res:
            return False

        user_data = res[0]
        if user_data["password_hash"] == password:
            usuario = cls(
                nombres=user_data['nombres_usuario'],
                apellidos=user_data['apellidos_usuario'],
                documento=user_data['documento'],
                celular=user_data['celular'],
                correo=user_data['correo_usuario'],
                fecha_nacimiento=user_data['fecha_nacimiento'],
                password_hash=None # No necesitamos el password plano aquí
            )
            # Asignamos el ID que viene de la DB (importante para FKs)
            usuario.id_usuario = user_data['id_usuario']
            return usuario
        return False

    @classmethod
    def obtener_por_id(cls, id_usuario):
        """Busca un usuario por su ID y retorna una instancia de la clase."""
        db = DBManager()
        query = "SELECT * FROM Usuario WHERE id_usuario = ?"
        resultado = db.consultar(query, (id_usuario,))
        
        if resultado:
            u = resultado[0]
            return cls(
                nombres=u['nombres_usuario'],
                apellidos=u['apellidos_usuario'],
                documento=u['documento'],
                correo=u['correo_usuario'],
                password_hash=u['password_hash'],
                celular=u['celular'],
                fecha_nacimiento=u['fecha_nacimiento'],
                id_usuario=u['id_usuario']
            )
        return None

    def registrar(self):
        """Guarda el usuario y le asigna el rol genérico."""
        # 1. Insertar el usuario
        query_user = """
            INSERT INTO Usuario (nombres_usuario, apellidos_usuario, documento, celular, correo_usuario, fecha_nacimiento, password_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params_user = (
            self.nombres_usuario, self.apellidos_usuario, self.documento, 
            self.celular, self.correo, self.fecha_nacimiento, self.password_hash
        )
        id_usuario = self.db.ejecutar_consulta(query_user, params_user)
        
        if id_usuario:
            self.id_usuario = id_usuario
            # 2. Asignar rol genérico (ID 2) por defecto en la tabla intermedia
            query_rol = "INSERT INTO Usuario_Rol (id_usuario, id_rol, descripcion_usuario_rol) VALUES (?, ?, ?)"
            params_rol = (self.id_usuario, 2, 'Asignación automática')
            
            self.db.ejecutar_consulta(query_rol, params_rol)
            return True
        return False    

    def actualizar(self):
        """Actualiza la información del usuario en la base de datos."""
        if not self.id_usuario:
            return False

        query = """
            UPDATE Usuario 
            SET nombre_usuario = ?, celular = ?, correo_usuario = ?
            WHERE id_usuario = ?
        """
        params = (self.nombre, self.celular, self.correo, self.id_usuario)
        self.db.ejecutar_consulta(query, params)
        return True

    def cargar_seguridad(self):
        """Carga el rol y permisos como atributos del usuario actual."""
        # 1. Obtener el id_rol desde la tabla intermedia Usuario_Rol
        # (Asumiendo que tienes un método o consulta para esto en tu clase)
        query = "SELECT id_rol FROM Usuario_Rol WHERE id_usuario = ?"
        resultado = self.db.consultar(query, (self.id_usuario,))
        
        if not resultado:
            self.rol = None
            self.permisos = []
            return self
            
        id_rol = resultado[0]['id_rol']
        
        # 2. Usar tus nuevos métodos de la clase Rol
        obj_rol = Rol.obtener_por_id(id_rol)
        lista_permisos = Rol.obtener_permisos(id_rol) # Pasamos el id_rol
        
        # 3. Asignar los valores al objeto Usuario
        self.rol = obj_rol.nombre_rol
        # Extraemos solo el texto del slug de la lista de objetos usando List Comprehension
        self.permisos = [permiso.slug for permiso in lista_permisos]
        
        return self