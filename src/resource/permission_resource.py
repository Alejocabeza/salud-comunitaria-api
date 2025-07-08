from ..models.permission import Permission
from pydantic import BaseModel
from typing import Optional

class ResourcePermission(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    @classmethod
    def from_array(cls, permission: Permission, **kwargs) -> "ResourcePermission":
        return cls(
            id=permission.id,
            name=permission.name,
            description=permission.description or kwargs.get("description", None)
        )
