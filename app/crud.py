from sqlalchemy.orm import Session
from app import models, schemas
from app.utils import get_password_hash

# --- User CRUD ---

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    if user_update.full_name is not None:
        db_user.full_name = user_update.full_name
    if user_update.password is not None:
        db_user.hashed_password = get_password_hash(user_update.password)
    if user_update.role is not None:
        db_user.role = user_update.role
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True

# --- Product CRUD ---

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_name(db: Session, name: str):
    return db.query(models.Product).filter(models.Product.name == name).first()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity_in_stock=product.quantity_in_stock
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    if product.name is not None:
        db_product.name = product.name
    if product.description is not None:
        db_product.description = product.description
    if product.price is not None:
        db_product.price = product.price
    if product.quantity_in_stock is not None:
        db_product.quantity_in_stock = product.quantity_in_stock
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if not db_product:
        return False
    db.delete(db_product)
    db.commit()
    return True

# --- Order CRUD ---

def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(
        client_id=order.client_id,
        status=order.status
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Add order items
    for item in order.items:
        db_item = models.OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price
        )
        db.add(db_item)
    db.commit()
    return db_order

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def update_order_status(db: Session, order_id: int, status: schemas.OrderStatus):
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    db_order.status = status
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    if not db_order:
        return False
    db.delete(db_order)
    db.commit()
    return True

# --- Payment CRUD ---

def create_payment(db: Session, payment: schemas.PaymentCreate):
    db_payment = models.Payment(
        order_id=payment.order_id,
        amount=payment.amount,
        status=payment.status,
        method=payment.method
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payment(db: Session, payment_id: int):
    return db.query(models.Payment).filter(models.Payment.id == payment_id).first()

def get_payments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Payment).offset(skip).limit(limit).all()

def update_payment_status(db: Session, payment_id: int, status: schemas.PaymentStatus):
    db_payment = get_payment(db, payment_id)
    if not db_payment:
        return None
    db_payment.status = status
    db.commit()
    db.refresh(db_payment)
    return db_payment

def delete_payment(db: Session, payment_id: int):
    db_payment = get_payment(db, payment_id)
    if not db_payment:
        return False
    db.delete(db_payment)
    db.commit()
    return True

# --- Invoice CRUD ---

def create_invoice(db: Session, invoice: schemas.InvoiceCreate):
    db_invoice = models.Invoice(
        order_id=invoice.order_id,
        invoice_number=invoice.invoice_number,
        total_amount=invoice.total_amount,
        paid=invoice.paid
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def get_invoice(db: Session, invoice_id: int):
    return db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()

def get_invoices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Invoice).offset(skip).limit(limit).all()

def update_invoice_status(db: Session, invoice_id: int, paid: bool):
    db_invoice = get_invoice(db, invoice_id)
    if not db_invoice:
        return None
    db_invoice.paid = paid
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def delete_invoice(db: Session, invoice_id: int):
    db_invoice = get_invoice(db, invoice_id)
    if not db_invoice:
        return False
    db.delete(db_invoice)
    db.commit()
    return True

# --- Price List Request CRUD ---

def create_price_list_request(db: Session, request: schemas.PriceListRequestCreate):
    db_request = models.PriceListRequest(
        client_id=request.client_id,
        status=request.status
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def get_price_list_request(db: Session, request_id: int):
    return db.query(models.PriceListRequest).filter(models.PriceListRequest.id == request_id).first()

def get_price_list_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PriceListRequest).offset(skip).limit(limit).all()

def update_price_list_request_status(db: Session, request_id: int, status: str):
    db_request = get_price_list_request(db, request_id)
    if not db_request:
        return None
    db_request.status = status
    db.commit()
    db.refresh(db_request)
    return db_request

def delete_price_list_request(db: Session, request_id: int):
    db_request = get_price_list_request(db, request_id)
    if not db_request:
        return False
    db.delete(db_request)
    db.commit()
    return True
