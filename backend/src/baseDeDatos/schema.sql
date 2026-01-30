-- =========================
-- Base de datos: pasteleria
-- =========================
-- Productos disponibles en la tienda
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio NUMERIC(10,2) NOT NULL,
    imagen_url TEXT,
    activo BOOLEAN DEFAULT TRUE
);
-- Ventas (una por checkout)
CREATE TABLE ventas (
    id SERIAL PRIMARY KEY,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total NUMERIC(10,2) NOT NULL
);
-- Detalle de cada venta (productos vendidos)
CREATE TABLE venta_detalle (
    id SERIAL PRIMARY KEY,
    venta_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    precio NUMERIC(10,2) NOT NULL,

    CONSTRAINT fk_venta
        FOREIGN KEY (venta_id)
        REFERENCES ventas(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_producto
        FOREIGN KEY (producto_id)
        REFERENCES productos(id)
);
-- Consultas del formulario "Custom Order"
CREATE TABLE consultas_custom (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    fecha_evento DATE NOT NULL,
    invitados VARCHAR(50),
    detalles TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
