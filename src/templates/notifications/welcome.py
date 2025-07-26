from fastapi_mail import FastMail, MessageSchema
from src.core.email import emailConfig

async def welcome(email_to: str, username: str, password: str):
    html = f"""
    <html>
        <body>
            <h2>Bienvenido al Sistema de Salud Comunitaria (Lazarus)</h2>
            <p>Hola {username},</p>
            <p>Se ha creado una cuenta para ti en el sistema Lazarus. A continuación encontrarás tus credenciales de acceso:</p>
            <ul>
                <li><strong>Usuario:</strong> {username}</li>
                <li><strong>Contraseña:</strong> {password}</li>
            </ul>
            <p>Te recomendamos cambiar tu contraseña después de iniciar sesión por primera vez.</p>
            <p>¡Gracias!</p>
        </body>
    </html>
    """

    message = MessageSchema(
        subject="Bienvenido a Lazarus - Credenciales de Acceso",
        recipients=[email_to],
        body=html,
        subtype="html"
    )

    fm = FastMail(emailConfig)
    await fm.send_message(message)

