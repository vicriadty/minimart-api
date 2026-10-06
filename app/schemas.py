from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1)
    sku: str = Field(min_length=1)
    price: float = Field(gt=0)
    stock: int = Field(ge=0, default=0)


class ProductOut(ProductCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class StockUpdate(BaseModel):
    stock: int = Field(ge=0)


class TransactionCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class TransactionOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    total_price: float
    created_at: datetime

    class Config:
        from_attributes = True
