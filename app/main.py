from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import (
    users,
    auth,
    products,
    orders,
    payments,
    invoices,
    price_list_requests,
)

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(payments.router, prefix="/payments", tags=["Payments"])
app.include_router(invoices.router, prefix="/invoices", tags=["Invoices"])
app.include_router(price_list_requests.router, prefix="/price-list-requests", tags=["Price List Requests"])

@app.get("/")
def read_root():
    return {"message": "Wholesale system backend is live!"}
