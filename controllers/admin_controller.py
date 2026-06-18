from flask import Blueprint, render_template, session, redirect, url_for

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/usuarios')
def ver_usuarios():
    # Aquí luego validaremos: if session['rol'] != 'Admin': abort(403)
    return render_template('admin/usuarios.html')