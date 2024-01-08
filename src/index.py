from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/inventario'
db = SQLAlchemy(app)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo_producto = db.Column(db.String(8), unique=True, nullable=False)
    nombre_producto = db.Column(db.String(50), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    ubicacion = db.Column(db.String(20), nullable=False)

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

if __name__ == '__main__':
    with app.app_context():
        # Crear la base de datos y cargar datos del CSV
        db.create_all()
        cargar_datos_csv()

    # Iniciar la aplicación Flask
    app.run(debug=True)
