from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# Database khusus test: SQLite in-memory, terpisah dari minimart.db.
# Tiap pytest run mulai dari kondisi kosong -> test jadi repeatable.
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_create_product_and_transaction():
    p = client.post(
        "/products",
        json={"name": "Indomie", "sku": "IND-001", "price": 3500, "stock": 10},
    )
    assert p.status_code == 201
    pid = p.json()["id"]

    t = client.post("/transactions", json={"product_id": pid, "quantity": 3})
    assert t.status_code == 201
    assert t.json()["total_price"] == 10500

    # stok harus berkurang otomatis: 10 - 3 = 7
    assert client.get(f"/products/{pid}").json()["stock"] == 7


def test_transaction_rejected_when_stock_low():
    p = client.post(
        "/products", json={"name": "Aqua", "sku": "AQ-001", "price": 4000, "stock": 1}
    )
    pid = p.json()["id"]
    t = client.post("/transactions", json={"product_id": pid, "quantity": 5})
    assert t.status_code == 400
