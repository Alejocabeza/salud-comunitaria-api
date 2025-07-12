from ..models.resource import Resource
from pydantic import BaseModel
from typing import Optional

class ResourceResources(BaseModel):
    id: int
    name: str
    dose: Optional[str] = None
    quantity: Optional[int] = None
    in_stock: Optional[bool] = True

    @classmethod
    def from_array(cls, resource: Resource, **kwargs) -> "ResourceResources":
        return cls(
            id=resource.id,
            name=resource.name,
            dose=resource.dose or kwargs.get("dose", None),
            quantity=resource.quantity or kwargs.get("quantity", None),
            in_stock=resource.in_stock or kwargs.get("in_stock", None),
        )
