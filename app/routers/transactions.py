from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("", response_model=schemas.TransactionOut, status_code=201)
def create_transaction(
    payload: schemas.TransactionCreate, db: Session = Depends(get_db)
):
    product = db.get(models.Product, payload.product_id)
    if not product:
        raise HTTPException(404, "Product tidak ditemukan")
    if product.stock < payload.quantity:
        raise HTTPException(400, f"Stok tidak mencukupi (sisa {product.stock})")
    product.stock -= payload.quantity
    trx = models.Transaction(
        product_id=product.id,
        quantity=payload.quantity,
        total_price=payload.quantity * product.price,
    )
    db.add(trx)
    db.commit()
    db.refresh(trx)
    return trx


@router.get("", response_model=list[schemas.TransactionOut])
def list_transactions(db: Session = Depends(get_db)):
    return db.query(models.Transaction).order_by(models.Transaction.id.desc()).all()
