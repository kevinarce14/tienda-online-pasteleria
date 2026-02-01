-- ============================================
-- Base de datos: pasteleria
-- ============================================
-- =========================
-- PRODUCTOS
-- =========================
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    precio NUMERIC(10,2) NOT NULL CHECK (precio >= 0),
    imagen_url TEXT,
    categoria VARCHAR(50) DEFAULT 'wedding_cake',
    disponible BOOLEAN DEFAULT TRUE,
    destacado BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_productos_categoria ON productos(categoria);
CREATE INDEX idx_productos_disponible ON productos(disponible);
-- =========================
-- ORDENES (ventas)
-- =========================
CREATE TABLE ordenes (
    id SERIAL PRIMARY KEY,
    nombre_cliente VARCHAR(150),
    email_cliente VARCHAR(150),
    total NUMERIC(10,2) NOT NULL CHECK (total >= 0),
    estado VARCHAR(30) DEFAULT 'pendiente',
    codigo_orden VARCHAR(30) NOT NULL UNIQUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_ordenes_estado ON ordenes(estado);
-- =========================
-- ORDEN_ITEMS
-- =========================
CREATE TABLE orden_items (
    id SERIAL PRIMARY KEY,
    orden_id INTEGER NOT NULL,
    producto_id INTEGER,
    nombre_producto VARCHAR(150) NOT NULL,
    precio_unitario NUMERIC(10,2) NOT NULL CHECK (precio_unitario >= 0),
    cantidad INTEGER NOT NULL DEFAULT 1 CHECK (cantidad > 0),
    subtotal NUMERIC(10,2) NOT NULL CHECK (subtotal >= 0),

    CONSTRAINT fk_orden
        FOREIGN KEY (orden_id)
        REFERENCES ordenes(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_producto
        FOREIGN KEY (producto_id)
        REFERENCES productos(id)
        ON DELETE SET NULL
);
CREATE INDEX idx_orden_items_orden_id ON orden_items(orden_id);
-- =========================
-- CONSULTAS PERSONALIZADAS
-- =========================
CREATE TABLE consultas_custom (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    fecha_evento DATE NOT NULL,
    invitados VARCHAR(50),
    detalles TEXT,
    estado VARCHAR(30) DEFAULT 'nueva',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_consultas_estado ON consultas_custom(estado);
