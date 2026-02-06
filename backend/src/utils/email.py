import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def enviar_email_consulta(
    nombre: str,
    email_cliente: str,
    fecha_evento: str,
    invitados: str | None,
    detalles: str
):
    """
    Envía un email con los detalles de la consulta personalizada
    Usa variables de entorno para las credenciales
    """
    
    # Obtener configuración de variables de entorno
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
    
    msg = EmailMessage()
    msg["Subject"] = "🎂 Nueva consulta personalizada - Nadines Cakes"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    cuerpo = f"""
    ═══════════════════════════════════════
    🎂 NUEVA CONSULTA PERSONALIZADA
    ═══════════════════════════════════════

    📋 DATOS DEL CLIENTE:
    ───────────────────────────────────────
    Nombre:           {nombre}
    Email:            {email_cliente}
    Fecha del evento: {fecha_evento}
    Invitados:        {invitados or "No especificado"}

    💬 DETALLES:
    ───────────────────────────────────────
    {detalles or "No se proporcionaron detalles adicionales."}

    ═══════════════════════════════════════
    Este mensaje fue generado automáticamente
    por el sistema de Nadines Cakes
    ═══════════════════════════════════════
    """

    msg.set_content(cuerpo)

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"✅ Email enviado exitosamente a {EMAIL_RECEIVER}")
        return True
    except Exception as e:
        print(f"❌ Error al enviar email: {e}")
        # No lanzar excepción, solo registrar el error
        return False