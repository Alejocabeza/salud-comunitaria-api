from ..models.request_medicines import RequestMedicine
from pydantic import BaseModel
from typing import Optional

class ResourceRequestMedicine(BaseModel):
    id: int
    name: str
    reason: Optional[str] = None
    send_email_at: Optional[str] = None
    is_sent_email: bool = False
    quantity: int
    doctor_id: int

    @classmethod
    def from_array(cls, requestMedicine: RequestMedicine, **kwargs) -> "ResourceRequestMedicine":
        return cls(
            id=requestMedicine.id,
            name=requestMedicine.name,
            reason=requestMedicine.reason,
            quantity=requestMedicine.quantity,
            doctor_id=requestMedicine.doctor_id,
            send_email_at=requestMedicine.send_email_at,
            is_sent_email=requestMedicine.is_sent_email,
        )
