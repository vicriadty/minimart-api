from fastapi import FastAPI

from .database import Base, engine
from .routers import products, transactions

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MiniMart API")


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(products.router)
app.include_router(transactions.router)
