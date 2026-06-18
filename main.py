# main.py
from flask import Flask, redirect, url_for
from controllers.auth_controller import auth_bp
from controllers.main_controller import main_bp

app = Flask(__name__)
app.secret_key = 'tu_llave_secreta_aqui' # Vital para usar session y flash

# Registramos el blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(main_bp)

@app.route('/')
def root():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
