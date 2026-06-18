from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from datetime import datetime, timedelta
from models.gasto import Gasto

main_bp = Blueprint('main', __name__)

CATEGORIAS_CONTROL = {
    'alimentación': {'titulo': 'Gasto en Alimentación', 'color': 'success', 'icono': 'utensils'},
    'transporte': {'titulo': 'Gasto en Transporte', 'color': 'info', 'icono': 'motorcycle'}
}

@main_bp.route('/')
@main_bp.route('/index')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    id_usuario = session.get('user_id')
    
    # 1. Capturar la opción elegida por el usuario (por defecto será 'mes')
    temporalidad = request.args.get('temporalidad', 'mes')
    
    # 2. Calcular la fecha de inicio según la opción
    hoy = datetime.today()
    fecha_desde = None  # Si se queda en None, significa "Todos los tiempos"
    
    if temporalidad == 'mes_actual':
        fecha_desde = hoy.replace(day=1).strftime('%Y-%m-%d')  # Primer día del mes actual
    elif temporalidad == 'ultimo_trimestre':
        fecha_desde = (hoy - timedelta(days=90)).strftime('%Y-%m-%d')
    elif temporalidad == 'ultimo_semestre':
        fecha_desde = (hoy - timedelta(days=180)).strftime('%Y-%m-%d')
    elif temporalidad == 'ultimo_año':
        fecha_desde = (hoy - timedelta(days=365)).strftime('%Y-%m-%d')

    # 3. Enviar la fecha calculada al modelo
    datos_db = Gasto.obtener_gastos_por_categoria(id_usuario, fecha_desde)
    
    etiquetas = [fila[0] for fila in datos_db]
    valores = [fila[1] for fila in datos_db]
    gastos_usuario = {fila[0].lower(): fila[1] for fila in datos_db}

    texto_tarjeta = temporalidad.replace("_", " ").upper()

    tarjetas_control = [
        {
            "titulo": f"Total Gastado ({texto_tarjeta})",
            "valor": sum(valores),
            "borde": "primary",
            "texto": "primary",
            "icono": "dollar-sign"
        }
    ]
    
    # Aquí es donde la función "mira" hacia afuera y usa el diccionario global
    for categoria, config in CATEGORIAS_CONTROL.items():
        gasto_real = gastos_usuario.get(categoria, 0)
        
        nueva_tarjeta = {
            "titulo": config['titulo'],
            "valor": gasto_real,
            "borde": config['color'],
            "texto": config['color'],
            "icono": config['icono']
        }
        tarjetas_control.append(nueva_tarjeta)
        
    return render_template(
        'dashboard/index.html', 
        etiquetas=etiquetas, 
        valores=valores, 
        tarjetas=tarjetas_control,
        temporalidad_actual=temporalidad
        )

@main_bp.route('/gastos')
def ver_gastos():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    # Llamamos al método con el ID del usuario en sesión
    lista = Gasto.obtener_por_id_usuario(session['user_id'])
    
    # Pasamos la lista a la plantilla
    return render_template('gastos/ver.html', lista_gastos=lista)

@main_bp.route('/gastos/registrar', methods=['GET', 'POST'])
def registrar_gasto():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        # 1. Capturar datos del formulario
        descripcion = request.form.get('descripcion')
        id_categoria = request.form.get('id_categoria')
        costo = request.form.get('costo')
        id_usuario = session['user_id']

        # 2. lógica para insertar en la DB usando tu DBManager
        registro = Gasto(id_usuario, id_categoria, costo, descripcion).registrar()

        if not registro:
            flash('Ocurrió un error al registrar el gasto', 'danger')
            return return_templates('gastos/registrar.html')

        # Por ahora simularemos el éxito
        flash('¡Gasto registrado correctamente!', 'success')
        return redirect(url_for('main.ver_gastos'))

    # Si es GET, mostramos el formulario
    return render_template('gastos/registrar.html')

@main_bp.route('/gastos/editar/<int:id_gasto>', methods=['GET', 'POST'])
def editar_gasto(id_gasto):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    gasto = Gasto.obtener_por_id_gasto(id_gasto)

    if not gasto:
        flash('Gasto no encontrado', 'danger')
        return redirect(url_for('main.ver_gastos'))
    
    if request.method == 'POST':
        gasto.fecha = request.form.get('fecha')
        gasto.descripcion_gasto = request.form.get('descripcion_gasto')
        gasto.id_categoria = int(request.form.get('id_categoria'))
        gasto.costo = request.form.get('costo')
        
        gasto.actualizar() 
        return redirect(url_for('main.ver_gastos'))
        
    return render_template('gastos/editar.html', gasto=gasto)

@main_bp.route('/gastos/eliminar/<int:id_gasto>', methods=['POST'])
def eliminar_gasto(id_gasto):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    # Llamamos al método del modelo que acabamos de crear
    if Gasto.eliminar(id_gasto):
        flash('El gasto ha sido eliminado correctamente.', 'success')
    else:
        flash('Hubo un error al intentar eliminar el gasto.', 'danger')

    # Siempre regresamos a la lista de gastos
    return redirect(url_for('main.ver_gastos'))