# api/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, date
import sys
import os
import logging

# Configurar logging para ver errores
logging.basicConfig(level=logging.INFO)

# ============================================
# FIX CRÍTICO PARA VERCEL: Ajustar path
# ============================================
# Agrega el directorio raíz del proyecto al path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.insert(0, project_root)

print(f"Current directory: {current_dir}")
print(f"Project root: {project_root}")
print(f"Python path: {sys.path}")

try:
    # Intenta importar desde la nueva ubicación
    from backend.src.database.db import get_db
    from backend.src.database.models.producto import Producto
    from backend.src.database.models.orden import Orden
    from backend.src.database.models.consulta_custom import ConsultaCustom
    from backend.src.database.models.orden_item import OrdenItem
    
    from backend.src.database.schemas.producto import (
        ProductoCreate,
        ProductoResponse
    )
    from backend.src.database.schemas.orden import (
        OrdenCreate,
        OrdenResponse
    )
    from backend.src.database.schemas.orden_item import (
        OrdenItemCreate,
        OrdenItemResponse
    )
    from backend.src.database.schemas.consulta_custom import (
        ConsultaCustomCreate,
        ConsultaCustomResponse
    )
    from backend.src.utils.email import enviar_email_consulta
    
    print("✅ Todos los imports funcionaron correctamente")
    
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print(f"Intentando importar desde ubicaciones alternativas...")
    
    # Fallback: intenta importar directamente
    try:
        # Agrega backend/src al path
        backend_src_path = os.path.join(project_root, 'backend', 'src')
        sys.path.insert(0, backend_src_path)
        
        from backend.src.database.db import get_db
        from backend.src.database.models.producto import Producto
        from backend.src.database.models.orden import Orden
        from backend.src.database.models.consulta_custom import ConsultaCustom
        from backend.src.database.models.orden_item import OrdenItem
        
        from backend.src.database.schemas.producto import (
            ProductoCreate,
            ProductoResponse
        )
        from backend.src.database.schemas.orden import (
            OrdenCreate,
            OrdenResponse
        )
        from backend.src.database.schemas.orden_item import (
            OrdenItemCreate,
            OrdenItemResponse
        )
        from backend.src.database.schemas.consulta_custom import (
            ConsultaCustomCreate,
            ConsultaCustomResponse
        )
        from backend.src.utils.email import enviar_email_consulta
        
        print("✅ Imports funcionaron con path alternativo")
    except ImportError as e2:
        print(f"❌ Error crítico en imports: {e2}")
        # Define funciones dummy para que la app al menos cargue
        get_db = None
        enviar_email_consulta = lambda *args, **kwargs: None

app = FastAPI(title="API Tienda Online Pastelería 🎂")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# ROOT
# -------------------------

@app.get("/")
def root():
    return {
        "mensaje": "API de Tienda Online Pastelería funcionando 🚀",
        "endpoints": {
            "productos": "/productos",
            "ordenes": "/ordenes",
            "consultas": "/consultas",
            "docs": "/docs"
        }
    }


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
        total=0,
        estado="pendiente",
        codigo_orden="TEMP"
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    nueva.codigo_orden = generar_codigo_orden(nueva.id)
    db.commit()
    db.refresh(nueva)

    return nueva

def generar_codigo_orden(id_orden: int) -> str:
    anio = datetime.now().year
    return f"ORD-{anio}-{str(id_orden).zfill(6)}"


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

    orden.total += subtotal

    db.add(nuevo_item)
    db.commit()
    db.refresh(nuevo_item)

    return nuevo_item


# =========================
# CONSULTAS PERSONALIZADAS
# =========================

@app.get("/consultas", response_model=list[ConsultaCustomResponse])
def listar_consultas(db: Session = Depends(get_db)):
    """Listar todas las consultas personalizadas"""
    return db.query(ConsultaCustom).all()


@app.post("/consultas", response_model=ConsultaCustomResponse)
def crear_consulta(
    consulta: ConsultaCustomCreate,
    db: Session = Depends(get_db)
):
    """
    Crear una nueva consulta personalizada y enviar email de notificación
    """
    # Validaciones
    if not consulta.nombre or len(consulta.nombre.strip()) < 2:
        raise HTTPException(status_code=400, detail="El nombre debe tener al menos 2 caracteres")
    
    if not consulta.email or "@" not in consulta.email:
        raise HTTPException(status_code=400, detail="Email inválido")
    
    # Validar que la fecha no sea en el pasado
    if consulta.fecha_evento < date.today():
        raise HTTPException(status_code=400, detail="La fecha del evento no puede ser en el pasado")
    
    # Validar número de invitados si se proporciona
    if consulta.invitados and (int(consulta.invitados) < 1 or int(consulta.invitados) > 10000):
        raise HTTPException(status_code=400, detail="El número de invitados debe estar entre 1 y 10000")
    
    # Crear la consulta
    nueva_consulta = ConsultaCustom(
        nombre=consulta.nombre.strip(),
        email=consulta.email.strip().lower(),
        fecha_evento=consulta.fecha_evento,
        invitados=consulta.invitados,
        detalles=consulta.detalles.strip() if consulta.detalles else None,
        estado="pendiente"
    )
    
    db.add(nueva_consulta)
    db.commit()
    db.refresh(nueva_consulta)
    
    # Enviar email de notificación (solo si está configurado)
    try:
        enviar_email_consulta(
            nombre=consulta.nombre,
            email_cliente=consulta.email,
            fecha_evento=str(consulta.fecha_evento),
            invitados=consulta.invitados,
            detalles=consulta.detalles
        )
    except Exception as e:
        print(f"⚠️ No se pudo enviar email: {e}")
    
    return nueva_consulta


@app.get("/consultas/{consulta_id}", response_model=ConsultaCustomResponse)
def obtener_consulta(
    consulta_id: int,
    db: Session = Depends(get_db)
):
    """Obtener una consulta específica por ID"""
    consulta = db.query(ConsultaCustom).filter(ConsultaCustom.id == consulta_id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")
    return consulta


@app.put("/consultas/{consulta_id}/estado")
def actualizar_estado_consulta(
    consulta_id: int,
    estado: str,
    db: Session = Depends(get_db)
):
    """Actualizar el estado de una consulta (pendiente, en_proceso, completada)"""
    estados_validos = ["pendiente", "en_proceso", "completada", "cancelada"]
    
    if estado not in estados_validos:
        raise HTTPException(
            status_code=400,
            detail=f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}"
        )
    
    consulta = db.query(ConsultaCustom).filter(ConsultaCustom.id == consulta_id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")
    
    consulta.estado = estado
    db.commit()
    db.refresh(consulta)
    
    return {"mensaje": f"Estado actualizado a '{estado}'", "consulta": consulta}


# =========================
# IMPORTANTE: PRUEBA SIMPLE
# =========================
@app.get("/test")
def test_endpoint():
    return {"message": "✅ API funcionando en Vercel", "status": "ok"}

@app.get("/debug")
def debug_info():
    return {
        "python_path": sys.path,
        "current_dir": current_dir,
        "project_root": project_root,
        "files_in_root": os.listdir(project_root) if os.path.exists(project_root) else []
    }

# =========================
# HANDLER PARA VERCEL - SIN MANGUM
# =========================
# Vercel detecta FastAPI automáticamente, no necesitas Mangum
# Comenta o elimina esta línea:
# handler = Mangum(app, lifespan="off")

# En su lugar, exporta la app directamente
app = app