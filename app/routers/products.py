from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=schemas.ProductOut, status_code=201)
def create_product(payload: schemas.ProductCreate, db: Session = Depends(get_db)):
    if db.query(models.Product).filter_by(sku=payload.sku).first():
        raise HTTPException(400, "SKU sudah digunakan")
    product = models.Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("", response_model=list[schemas.ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.get(models.Product, product_id)
    if not product:
        raise HTTPException(404, "Product tidak ditemukan")
    return product


@router.patch("/{product_id}/stock", response_model=schemas.ProductOut)
def update_stock(
    product_id: int, payload: schemas.StockUpdate, db: Session = Depends(get_db)
):
    product = db.get(models.Product, product_id)
    if not product:
        raise HTTPException(404, "Produk tidak ditemukan")
    product.stock = payload.stock
    db.commit()
    db.refresh(product)
    return product
