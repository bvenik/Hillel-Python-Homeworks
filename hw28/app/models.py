from typing import Optional
from sqlmodel import Field, SQLModel


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    price: float
    is_active: bool = True
    owner_id: int = Field(index=True)


class ItemCreate(SQLModel):
    title: str
    description: Optional[str] = None
    price: float
    owner_id: int


class ItemRead(SQLModel):
    id: int
    title: str
    description: Optional[str] = None
    price: float
    is_active: bool
    owner_id: int


class ItemUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None
    owner_id: Optional[int] = None
