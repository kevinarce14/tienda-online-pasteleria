from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pathlib import Path
from datetime import datetime, date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from backend.src.database.db import get_db
from backend.src.database.models.producto import Producto
from backend.src.database.models.orden import Orden
from backend.src.database.models.consulta_custom import ConsultaCustom

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
from backend.src.database.schemas.consulta_custom import (
    ConsultaCustomCreate,
    ConsultaCustomResponse
)
from backend.src.utils.email import enviar_email_consulta

app = FastAPI(title="API Tienda Online Pastelería 🎂")

# -------------------------
# CORS - IMPORTANTE PARA CONECTAR CON FRONTEND
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# CONFIGURAR ARCHIVOS ESTÁTICOS
# -------------------------
# Obtener la ruta al directorio frontend
BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

# Montar archivos estáticos (si tienes CSS, JS, imágenes en frontend)
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


# -------------------------
# ROOT - SERVIR INDEX.HTML
# -------------------------

@app.get("/")
def root():
    """Servir el archivo index.html"""
    index_path = FRONTEND_DIR / "index.html"
    return FileResponse(index_path)


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
        total=0,  # ✅ Iniciar en 0, se actualizará al agregar items
        estado="pendiente",
        codigo_orden="TEMP"  # placeholder
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    # generar código real
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

    orden.total += subtotal  # 🔥 Se suma correctamente aquí

    db.add(nuevo_item)
    db.commit()
    db.refresh(nuevo_item)

    return nuevo_item


# # =========================
# # CONFIGURACIÓN DE EMAIL
# # =========================

# # ⚠️ CONFIGURAR CON TUS CREDENCIALES
# EMAIL_CONFIG = {
#     "smtp_server": "smtp.gmail.com",  # Para Gmail
#     "smtp_port": 587,
#     "sender_email": "kevinfeo2002@gmail.com",  # ⚠️ CAMBIAR
#     "sender_password": "tnej orar wvya jcda",  # ⚠️ CAMBIAR
#     "receiver_email": "kevindamian1702@gmail.com"  # ⚠️ Email de Nadines
# }

# def enviar_email_consulta(consulta: ConsultaCustom):
#     """
#     Envía un email con los detalles de la consulta personalizada
#     """
#     try:
#         # Crear el mensaje
#         mensaje = MIMEMultipart("alternative")
#         mensaje["Subject"] = f"🎂 Nueva Consulta Personalizada - {consulta.nombre}"
#         mensaje["From"] = EMAIL_CONFIG["sender_email"]
#         mensaje["To"] = EMAIL_CONFIG["receiver_email"]

#         # Crear el contenido HTML
#         html = f"""
#         <html>
#             <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
#                 <div style="background-color: #ff7f50; padding: 20px; text-align: center;">
#                     <h1 style="color: white; margin: 0;">🎂 Nueva Consulta Personalizada</h1>
#                 </div>
                
#                 <div style="padding: 30px; background-color: #f9f9f9;">
#                     <h2 style="color: #ff7f50;">Datos del Cliente</h2>
#                     <table style="width: 100%; border-collapse: collapse;">
#                         <tr>
#                             <td style="padding: 10px; font-weight: bold; width: 40%;">Nombre:</td>
#                             <td style="padding: 10px;">{consulta.nombre}</td>
#                         </tr>
#                         <tr style="background-color: white;">
#                             <td style="padding: 10px; font-weight: bold;">Email:</td>
#                             <td style="padding: 10px;">
#                                 <a href="mailto:{consulta.email}">{consulta.email}</a>
#                             </td>
#                         </tr>
#                         <tr>
#                             <td style="padding: 10px; font-weight: bold;">Fecha del Evento:</td>
#                             <td style="padding: 10px;">{consulta.fecha_evento.strftime('%d/%m/%Y')}</td>
#                         </tr>
#                         <tr style="background-color: white;">
#                             <td style="padding: 10px; font-weight: bold;">Número de Invitados:</td>
#                             <td style="padding: 10px;">{consulta.invitados or 'No especificado'}</td>
#                         </tr>
#                         <tr>
#                             <td style="padding: 10px; font-weight: bold;">Estado:</td>
#                             <td style="padding: 10px;">
#                                 <span style="background-color: #ffd700; padding: 5px 10px; border-radius: 5px;">
#                                     {consulta.estado}
#                                 </span>
#                             </td>
#                         </tr>
#                     </table>

#                     <h2 style="color: #ff7f50; margin-top: 30px;">Detalles de la Consulta</h2>
#                     <div style="background-color: white; padding: 20px; border-radius: 10px; border-left: 4px solid #ff7f50;">
#                         <p style="white-space: pre-wrap; line-height: 1.6;">
#                             {consulta.detalles or 'No se proporcionaron detalles adicionales.'}
#                         </p>
#                     </div>

#                     <div style="margin-top: 30px; padding: 15px; background-color: #fff5f2; border-radius: 10px;">
#                         <p style="margin: 0; color: #666;">
#                             <strong>📋 ID de Consulta:</strong> {consulta.id}
#                         </p>
#                         <p style="margin: 5px 0 0 0; color: #666;">
#                             <strong>📅 Fecha de Registro:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}
#                         </p>
#                     </div>
#                 </div>
                
#                 <div style="background-color: #4d2a20; padding: 20px; text-align: center; color: white;">
#                     <p style="margin: 0;">Nadines Cakes - Sistema de Gestión de Consultas</p>
#                 </div>
#             </body>
#         </html>
#         """

#         # Adjuntar el HTML
#         parte_html = MIMEText(html, "html")
#         mensaje.attach(parte_html)

#         # Enviar el email
#         with smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"]) as server:
#             server.starttls()
#             server.login(EMAIL_CONFIG["sender_email"], EMAIL_CONFIG["sender_password"])
#             server.send_message(mensaje)
        
#         return True
    
#     except Exception as e:
#         print(f"Error al enviar email: {e}")
#         return False


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
    if consulta.invitados and (int(consulta.invitados) < 10 or int(consulta.invitados) > 10000):
        raise HTTPException(status_code=400, detail="El número de invitados debe estar entre 10 y 10000")
    
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
    
        # Enviar email al negocio
    enviar_email_consulta(
        nombre=consulta.nombre,
        email_cliente=consulta.email,
        fecha_evento=str(consulta.fecha_evento),
        invitados=consulta.invitados,
        detalles=consulta.detalles
    )
    
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