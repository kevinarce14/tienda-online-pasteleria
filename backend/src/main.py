from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

#from database.db import SessionLocal
from database.db import get_db
from database.models.producto import Producto
from database.models.cliente import Cliente
from database.models.orden import Orden


app = FastAPI(title="API Tienda Online Pastelería")




# -------------------------
# ENDPOINTS DE PRUEBA
# -------------------------

@app.get("/")
def root():
    return {"mensaje": "API de Tienda Online Pastelería funcionando 🚀"}


# -------------------------
# PRODUCTOS
# -------------------------

@app.get("/productos")
def listar_productos(db: Session = Depends(get_db)):
    productos = db.query(Producto).all()
    return productos


@app.post("/productos")
def crear_producto(
    nombre: str,
    precio: float,
    db: Session = Depends(get_db),
    descripcion: str | None = None,
    categoria: str = "wedding_cake"
):
    nuevo_producto = Producto(
        nombre=nombre,
        precio=precio,
        descripcion=descripcion,
        categoria=categoria
    )

    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)

    return nuevo_producto


# -------------------------
# CLIENTES
# -------------------------

@app.get("/clientes")
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()


@app.post("/clientes")
def crear_cliente(
    nombre: str,
    email: str,
    db: Session = Depends(get_db),
    telefono: str | None = None
):
    # Validar email único
    existe = db.query(Cliente).filter(Cliente.email == email).first()
    if existe:
        raise HTTPException(status_code=400, detail="El email ya existe")

    cliente = Cliente(
        nombre=nombre,
        email=email,
        telefono=telefono
    )

    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    return cliente


# -------------------------
# ORDENES
# -------------------------

@app.get("/ordenes")
def listar_ordenes(db: Session = Depends(get_db)):
    return db.query(Orden).all()
