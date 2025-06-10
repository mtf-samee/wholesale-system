from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Enum, Text, func
)
from sqlalchemy.orm import relationship
from app.database import Base  # ← THIS LINE IS THE FIX
import enum

# Enum for User Roles
class UserRole(enum.Enum):
    admin = "admin"
    staff = "staff"
    client = "client"

# Enum for Order Status
class OrderStatus(enum.Enum):
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

# Enum for Payment Status
class PaymentStatus(enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"

# User Model - stores all types of users (admin, staff, client)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # PK
    email = Column(String, unique=True, index=True, nullable=False)  # login email
    hashed_password = Column(String, nullable=False)  # password hash for security
    full_name = Column(String, nullable=True)  # optional full name
    role = Column(Enum(UserRole), default=UserRole.client, nullable=False)  # user type

    # Relationships to orders and price list requests made by this user (if client)
    orders = relationship("Order", back_populates="client")
    price_list_requests = relationship("PriceListRequest", back_populates="client")

# Product Model - inventory items to sell
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)  # PK
    name = Column(String, unique=True, index=True, nullable=False)  # product name
    description = Column(Text, nullable=True)  # optional description
    price = Column(Float, nullable=False)  # current unit price
    quantity_in_stock = Column(Integer, nullable=False, default=0)  # inventory count

    # Relation to order items referencing this product
    order_items = relationship("OrderItem", back_populates="product")

# Order Model - client purchase orders, tracks status & timestamps
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)  # PK
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # FK to user (client)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # order timestamp
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)  # current order status

    # Relationships back to client, order items, payments, invoice
    client = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order", cascade="all, delete-orphan")
    invoice = relationship("Invoice", uselist=False, back_populates="order", cascade="all, delete-orphan")

# OrderItem Model - line items within an order, stores quantity and unit price snapshot
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)  # PK
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)  # FK to order
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)  # FK to product
    quantity = Column(Integer, nullable=False)  # units ordered
    unit_price = Column(Float, nullable=False)  # price at time of order (snapshot)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

# Payment Model - supports multiple payments per order (partial or full)
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)  # PK
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)  # FK to order
    amount = Column(Float, nullable=False)  # payment amount
    payment_date = Column(DateTime(timezone=True), server_default=func.now())  # timestamp of payment
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending, nullable=False)  # payment status
    method = Column(String, nullable=True)  # e.g., card, bank transfer, cash

    order = relationship("Order", back_populates="payments")

# Invoice Model - one invoice per order with total amount and payment status
class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)  # PK
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True)  # FK to order (one-to-one)
    invoice_number = Column(String, unique=True, nullable=False)  # unique invoice ID (human readable)
    invoice_date = Column(DateTime(timezone=True), server_default=func.now())  # invoice creation date
    total_amount = Column(Float, nullable=False)  # total cost (sum of all order items)
    paid = Column(Boolean, default=False)  # invoice payment completed or not

    order = relationship("Order", back_populates="invoice")

# PriceListRequest Model - clients request price lists; admins/staff respond
class PriceListRequest(Base):
    __tablename__ = "price_list_requests"

    id = Column(Integer, primary_key=True, index=True)  # PK
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # FK to client user
    requested_at = Column(DateTime(timezone=True), server_default=func.now())  # request timestamp
    status = Column(String, default="pending")  # request status: pending, sent, declined

    client = relationship("User", back_populates="price_list_requests")
