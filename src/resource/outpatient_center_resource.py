from ..models.outpatient_center import OutpatientCenter
from pydantic import BaseModel
from typing import Optional

class ResourceOutpatientCenter(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    rif: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

    @classmethod
    def from_array(cls, outpatient_center: OutpatientCenter, **kwargs) -> "ResourceOutpatientCenter":
        return cls(
            id=outpatient_center.id,
            name=outpatient_center.name,
            email=outpatient_center.email,
            rif=outpatient_center.rif,
            phone=outpatient_center.phone,
            address=outpatient_center.address
        )
