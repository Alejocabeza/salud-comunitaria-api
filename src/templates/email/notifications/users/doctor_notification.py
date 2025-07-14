from ...email_base_service import EmailBaseService

class DoctorNotification:
    """
    Email service for doctor registration
    
    Handles sending welcome emails with credentials to newly registered doctor
    """
    
    @staticmethod
    def send_welcome_email(email: str, name: str, password: str) -> dict:
        """
        Send welcome email with credentials to doctor
        
        Args:
            email (str): Recipient email address
            name (str): Doctor name
            password (str): Generated password for the account
            
        Returns:
            dict: Response indicating email status
        """
        subject = "Bienvenido a Salud Comunitaria API - Credenciales de Acceso"
        
        body = f"""
        <html>
        <body>
            <h2>¡Bienvenido a Salud Comunitaria API!</h2>
            <p>Hola <strong>{name}</strong>,</p>
            <p>Tu cuenta de doctor ha sido registrada exitosamente en nuestro sistema.</p>
            <p>Aquí están tus credenciales de acceso:</p>
            <ul>
                <li><strong>Email:</strong> {email}</li>
                <li><strong>Contraseña:</strong> {password}</li>
            </ul>
            <p><strong>Importante:</strong> Por seguridad, te recomendamos cambiar tu contraseña después del primer inicio de sesión.</p>
            <p>Puedes acceder al sistema a través de: <a href="http://localhost:8000/docs">http://localhost:8000/docs</a></p>
            <p>Si tienes alguna pregunta, no dudes en contactarnos.</p>
            <br>
            <p>Saludos,<br>Equipo de Salud Comunitaria API</p>
        </body>
        </html>
        """
        
        email_service = EmailBaseService(
            subject=subject,
            recipients=[email],
            body=body
        )
        
        return email_service.send_email() 