from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
import csv
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/inventario'
app.config['SECRET_KEY'] = 'Even99'  # Cambiar esto por una clave secreta real
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo_producto = db.Column(db.String(8), unique=True, nullable=False)
    nombre_producto = db.Column(db.String(50), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    ubicacion = db.Column(db.String(20), nullable=False)
    
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False)
    contraseña = db.Column(db.String(100), nullable=False)   
    
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))     

# Cargar datos del CSV y almacenarlos en la base de datos
def cargar_datos_csv():
    with open('bd/inventario.csv', 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        # Antes de cargar datos, eliminar todos los registros existentes
        Producto.query.delete()
        db.session.commit()
        for row in csv_reader:
            producto = Producto(
                codigo_producto=row['Codigo Producto'],
                nombre_producto=row['Nombre Producto'],
                cantidad=row['Cantidad'],
                ubicacion=row['Ubicacion']
            )
            db.session.add(producto)

    db.session.commit()
    
# Ruta para el login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        contraseña = request.form['contraseña']
        
        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
        if usuario and bcrypt.checkpw(contraseña.encode('utf-8'), usuario.contraseña.encode('utf-8')):
            login_user(usuario)
            return redirect(url_for('mostrar_productos'))
        else:
            flash('Credenciales inválidas. Por favor, inténtalo nuevamente.', 'error')
    
    return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Ruta para cargar los datos del CSV a la base de datos
@app.route('/cargar_datos')
def cargar_datos():
    with app.app_context():
        cargar_datos_csv()
    return 'Datos cargados exitosamente en la base de datos.'

# Ruta para mostrar los productos en la interfaz web
@app.route('/')
def mostrar_productos():
    productos = Producto.query.all()
    return render_template('productos.html', productos=productos)

# Ruta para agregar los productos en la interfaz web
@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    codigo = request.form.get('codigo')
    nombre = request.form.get('nombre')
    cantidad = request.form.get('cantidad')
    ubicacion = request.form.get('ubicacion')

    nuevo_producto = Producto(
        codigo_producto=codigo,
        nombre_producto=nombre,
        cantidad=cantidad,
        ubicacion=ubicacion
    )

    db.session.add(nuevo_producto)
    db.session.commit()

    return redirect(url_for('mostrar_productos'))

if __name__ == '__main__':
    with app.app_context():
        # Crear la base de datos y cargar datos del CSV
        db.create_all()
        cargar_datos_csv()

    # Iniciar la aplicación Flask
    app.run(debug=True)