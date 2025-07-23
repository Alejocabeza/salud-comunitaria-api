from ..email_base_service import EmailBaseService

class RequestMedicineNotification:
    """
    Email service for request medicine notifications

    Handles sending email notifications for medicine requests
    """
    
    @staticmethod
    def send_request_medicine_email(email: str, name: str, medicine: str, quantity: int, type: str) -> dict:
        """
        Send email notification for medicine request

        Args:
            email (str): Recipient email address
            name (str): Patient name
            medicine (str): Requested medicine name
            quantity (int): Quantity of medicine requested
            
        Returns:
            dict: Response indicating email status
        """
        subject = "Notificación de Solicitud de Medicamento"

        body = f"""
        <html>
        <body>
            <h2>¡Notificación de Solicitud de Medicamento!</h2>
            <p>El {type}, <strong>{name}</strong> ha solicitado el siguiente medicamento:</p>
            <ul>
                <li><strong>Medicamento:</strong> {medicine}</li>
                <li><strong>Cantidad:</strong> {quantity}</li>
            </ul>
            <p>Por favor, revisa la solicitud y toma las acciones necesarias.</p>
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