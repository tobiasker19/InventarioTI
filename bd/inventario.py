import csv
import random
from faker import Faker

# Utilizamos la librería Faker para generar datos ficticios
fake = Faker()

# Definimos la cantidad de productos en el inventario
num_productos = 20

# Creamos una lista para almacenar los productos
inventario = []

# Generamos datos ficticios y los almacenamos en la lista
for _ in range(num_productos):
    codigo_producto = fake.uuid4()[:8].upper()  # Generamos un código de producto ficticio
    nombre_producto = fake.word().capitalize()
    cantidad_producto = random.randint(1, 100)
    ubicacion_producto = fake.random_element(["Pasillo A", "Pasillo B", "Pasillo C"])

    inventario.append({
        'Codigo Producto': codigo_producto,
        'Nombre Producto': nombre_producto,
        'Cantidad': cantidad_producto,
        'Ubicacion': ubicacion_producto
    })

# Escribimos la lista en un archivo CSV
csv_filename = 'inventario.csv'
csv_columns = inventario[0].keys()

with open(csv_filename, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for producto in inventario:
        writer.writerow(producto)

print(f'Se ha generado el archivo "{csv_filename}" con éxito.')
