-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS inventario;

-- Seleccionar la base de datos
USE inventario;

-- Crear la tabla de productos
CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_producto VARCHAR(8) UNIQUE NOT NULL,
    nombre_producto VARCHAR(50) NOT NULL,
    cantidad INT NOT NULL,
    ubicacion VARCHAR(20) NOT NULL
);

-- Insertar datos iniciales
INSERT INTO productos (codigo_producto, nombre_producto, cantidad, ubicacion)
VALUES 
    ('001', 'Producto 1', 10, 'Almacen A'),
    ('002', 'Producto 2', 15, 'Almacen B');

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password_hash VARCHAR(100) NOT NULL
);

INSERT INTO users (username, password_hash) VALUES ('admin', 'Even99');

