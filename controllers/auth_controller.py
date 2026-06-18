# controllers/auth_controller.py

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.usuario import Usuario

# Creamos el Blueprint para agrupar rutas de autenticación
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        documento = request.form.get('documento')
        password = request.form.get('password')
        
        # 1. El controlador le pide al Modelo que valide
        validacion = Usuario.validar_credenciales(documento, password)
        
        if validacion:
            # 2. Obtenemos el rol y permisos del usuario
            validacion.cargar_seguridad()
            
            # 3. Cargamos el id del usuario en la sesión
            session['user_id'] = validacion.id_usuario
            
            # Guardamos los slugs en la sesión para que el Dashboard sepa qué mostrar
            session['permisos'] = validacion.permisos
            session['nombre'] = validacion.nombres_usuario
            
            flash(f"Bienvenido de nuevo, {validacion.nombres_usuario}", "success")
            return redirect(url_for('main.index'))
        
        # 4. Si falla, notificamos al usuario
        flash("Documento o contraseña incorrectos", "danger")
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear() # Limpia toda la sesión (seguridad)
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 1. Capturar datos del formulario usando el atributo 'name'
        nombres = request.form.get('nombres')
        apellidos = request.form.get('apellidos')
        documento = request.form.get('documento')
        celular = request.form.get('celular')
        correo = request.form.get('correo')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # 2. Validaciones básicas
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return render_template('auth/register.html')

        # 3. Instanciar el modelo Usuario
        # Nota: Asegúrate de que tu __init__ en la clase Usuario reciba estos campos
        nuevo_usuario = Usuario(
            nombres=nombres,
            apellidos=apellidos,
            documento=documento,
            celular=celular,
            correo=correo,
            fecha_nacimiento=fecha_nacimiento,
            password_hash=password # El modelo debería encargarse del hash
        )

        # 4. Intentar el registro (esto activará la inserción doble: Usuario + Rol)
        if nuevo_usuario.registrar():
            flash('"¡Registro exitoso! Por favor inicia sesión', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Error al registrar. El documento o correo ya podrían existir.', 'danger')
            return render_template('auth/register.html')

    # Si es GET, simplemente mostrar el formulario
    return render_template('auth/register.html')