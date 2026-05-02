import smtplib
from email.message import EmailMessage
import os


def enviar_email(email_remetente, senha_email, email_destinatario, caminho_anexo):
    msg = EmailMessage()
    msg["Subject"] = "Áudio codificado"
    msg["From"] = email_remetente
    msg["To"] = email_destinatario

    msg.set_content("""
Olá!

Segue em anexo o arquivo codificado.

Use a senha correta no sistema para recuperar o áudio original.
""")

    with open(caminho_anexo, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename=os.path.basename(caminho_anexo)
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_remetente, senha_email)
        smtp.send_message(msg)