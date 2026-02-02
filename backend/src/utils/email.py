import smtplib
from email.message import EmailMessage


def enviar_email_consulta(
    nombre: str,
    email_cliente: str,
    fecha_evento: str,
    invitados: str | None,
    detalles: str
):
    msg = EmailMessage()
    msg["Subject"] = "Nueva consulta personalizada"
    msg["From"] = "kevinfeo2002@gmail.com"
    msg["To"] = "kevindamian1702@gmail.com"

    cuerpo = f"""
    Nueva consulta personalizada recibida

    Nombre: {nombre}
    Email: {email_cliente}
    Fecha del evento: {fecha_evento}
    Invitados: {invitados or "No especificado"}

    Detalles:
    {detalles}
    """

    msg.set_content(cuerpo)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("kevinfeo2002@gmail.com", "tnej orar wvya jcda")
        smtp.send_message(msg)
