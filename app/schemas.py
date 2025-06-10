from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum
from datetime import datetime

# --- Enums ---

class UserRole(str, Enum):
    admin = "admin"
    staff = "staff"
    client = "client"

class OrderStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class PaymentStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"

# --- Authentication ---

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# --- Users ---

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: Optional[UserRole] = UserRole.client

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    role: UserRole

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None

# --- Products ---

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity_in_stock: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity_in_stock: Optional[int] = None

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True

# --- Orders & Items ---

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = None
    unit_price: Optional[float] = None

class OrderItemOut(OrderItemBase):
    id: int
    product: ProductOut

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    status: OrderStatus = OrderStatus.pending

class OrderCreate(OrderBase):
    client_id: int
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None

class OrderOut(OrderBase):
    id: int
    client: UserOut
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        orm_mode = True

# --- Payments ---

class PaymentBase(BaseModel):
    amount: float
    status: PaymentStatus = PaymentStatus.pending
    method: Optional[str] = None

class PaymentCreate(PaymentBase):
    order_id: int

class PaymentUpdate(BaseModel):
    status: Optional[PaymentStatus] = None
    method: Optional[str] = None

class PaymentOut(PaymentBase):
    id: int
    order_id: int
    payment_date: datetime

    class Config:
        orm_mode = True

# --- Invoices ---

class InvoiceBase(BaseModel):
    invoice_number: str
    total_amount: float
    paid: bool = False

class InvoiceCreate(InvoiceBase):
    order_id: int

class InvoiceOut(InvoiceBase):
    id: int
    order_id: int
    invoice_date: datetime

    class Config:
        orm_mode = True

class InvoiceUpdate(BaseModel):
    paid: Optional[bool] = None

# Optional: Used separately in /invoices/{id}/paid
class InvoicePaidUpdate(BaseModel):
    paid: bool

# --- Price List Requests ---

class PriceListRequestBase(BaseModel):
    status: Optional[str] = "pending"

class PriceListRequestCreate(PriceListRequestBase):
    client_id: int

class PriceListRequestUpdate(BaseModel):
    status: Optional[str] = None

class PriceListRequestOut(PriceListRequestBase):
    id: int
    client: UserOut
    requested_at: datetime

    class Config:
        orm_mode = True
