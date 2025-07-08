from ..models.role import Roles
from pydantic import BaseModel
from typing import Optional

class ResourceRole(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    @classmethod
    def from_array(cls, role: Roles, **kwargs) -> "ResourceRole":
        return cls(
            id=role.id,
            name=role.name,
            description=role.description or kwargs.get("description", None)
        )
