from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.src.database.db import get_db
from backend.src.database.models.producto import Producto
from backend.src.database.models.orden import Orden

from backend.src.database.schemas.producto import (
    ProductoCreate,
    ProductoResponse
)
from backend.src.database.schemas.orden import (
    OrdenCreate,
    OrdenResponse
)
from backend.src.database.models.orden_item import OrdenItem
from backend.src.database.schemas.orden_item import (
    OrdenItemCreate,
    OrdenItemResponse
)

app = FastAPI(title="API Tienda Online Pastelería 🎂")


# -------------------------
# ROOT
# -------------------------

@app.get("/")
def root():
    return {"mensaje": "API de Tienda Online Pastelería funcionando 🚀"}


# =========================
# PRODUCTOS
# =========================

@app.get("/productos", response_model=list[ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()


@app.post("/productos", response_model=ProductoResponse)
def crear_producto(
    producto: ProductoCreate,
    db: Session = Depends(get_db)
):
    nuevo = Producto(**producto.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# =========================
# ORDENES
# =========================

@app.get("/ordenes", response_model=list[OrdenResponse])
def listar_ordenes(db: Session = Depends(get_db)):
    return db.query(Orden).all()


@app.post("/ordenes", response_model=OrdenResponse)
def crear_orden(
    orden: OrdenCreate,
    db: Session = Depends(get_db)
):
    nueva = Orden(
        nombre_cliente=orden.nombre_cliente,
        email_cliente=orden.email_cliente,
        total=orden.total,
        estado="pendiente"
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


# =========================
# ORDEN_ITEMS
# =========================

@app.post(
    "/ordenes/{orden_id}/items",
    response_model=OrdenItemResponse
)
def agregar_item_a_orden(
    orden_id: int,
    item: OrdenItemCreate,
    db: Session = Depends(get_db)
):
    orden = db.query(Orden).filter(Orden.id == orden_id).first()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    subtotal = item.precio_unitario * item.cantidad

    nuevo_item = OrdenItem(
        orden_id=orden_id,
        producto_id=item.producto_id,
        nombre_producto=item.nombre_producto,
        precio_unitario=item.precio_unitario,
        cantidad=item.cantidad,
        subtotal=subtotal
    )

    orden.total += subtotal  # 🔥 importante

    db.add(nuevo_item)
    db.commit()
    db.refresh(nuevo_item)

    return nuevo_item