"""Pydantic-схемы для видов деятельности."""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ActivitySchema(BaseModel):
    """Вид деятельности (плоский, с parent_id)."""

    id: int
    name: str
    parent_id: Optional[int]
    level: int

    model_config = ConfigDict(from_attributes=True)


class ActivityTreeSchema(BaseModel):
    """Вид деятельности с вложенными детьми (дерево)."""

    id: int
    name: str
    level: int
    children: List["ActivityTreeSchema"] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


ActivityTreeSchema.model_rebuild()
