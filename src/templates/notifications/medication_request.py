from fastapi_mail import FastMail, MessageSchema
from src.core.email import emailConfig

async def medication_request(
    email_to: str, 
    center_name: str,
    requester_name: str, 
    requester_type: str,
    medication_name: str, 
    quantity: int, 
    reason: str
):
    html = f"""
    <html>
        <body>
            <h2>Nueva Solicitud de Medicamento - Sistema Lazarus</h2>
            <p>Estimado equipo de {center_name},</p>
            <p>Se ha recibido una nueva solicitud de medicamento en el sistema Lazarus:</p>
            
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3>Detalles de la Solicitud:</h3>
                <ul>
                    <li><strong>Solicitante:</strong> {requester_name} ({requester_type})</li>
                    <li><strong>Medicamento:</strong> {medication_name}</li>
                    <li><strong>Cantidad:</strong> {quantity}</li>
                    <li><strong>Motivo:</strong> {reason}</li>
                    <li><strong>Estado:</strong> Pendiente</li>
                </ul>
            </div>
            
            <p>Por favor, revise la solicitud en el sistema para proceder con la aprobación o rechazo correspondiente.</p>
            <p>Gracias por su atención.</p>
            
            <hr>
            <p><small>Este es un mensaje automático del Sistema de Salud Comunitaria Lazarus.</small></p>
        </body>
    </html>
    """

    message = MessageSchema(
        subject=f"Nueva Solicitud de Medicamento - {medication_name}",
        recipients=[email_to],
        body=html,
        subtype="html"
    )

    fm = FastMail(emailConfig)
    await fm.send_message(message)