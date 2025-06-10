from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas, crud
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.PriceListRequestOut)
def create_price_list_request(request: schemas.PriceListRequestCreate, db: Session = Depends(get_db)):
    db_request = crud.create_price_list_request(db, request)
    return db_request

@router.get("/{request_id}", response_model=schemas.PriceListRequestOut)
def get_price_list_request(request_id: int, db: Session = Depends(get_db)):
    db_request = crud.get_price_list_request(db, request_id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Price list request not found")
    return db_request

@router.get("/", response_model=List[schemas.PriceListRequestOut])
def list_price_list_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    requests = crud.get_price_list_requests(db, skip=skip, limit=limit)
    return requests

# Fix here: use PriceListRequestUpdate schema (assumed correct)
@router.put("/{request_id}/status", response_model=schemas.PriceListRequestOut)
def update_price_list_request_status(
    request_id: int,
    status_update: schemas.PriceListRequestUpdate,
    db: Session = Depends(get_db)
):
    # Assuming PriceListRequestUpdate contains the status field
    db_request = crud.update_price_list_request_status(db, request_id, status_update.status)
    if not db_request:
        raise HTTPException(status_code=404, detail="Price list request not found")
    return db_request

@router.delete("/{request_id}")
def delete_price_list_request(request_id: int, db: Session = Depends(get_db)):
    success = crud.delete_price_list_request(db, request_id)
    if not success:
        raise HTTPException(status_code=404, detail="Price list request not found")
    return {"detail": "Price list request deleted successfully"}
