from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/contacts/", response_model=schemas.ContactOut)
def create(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db, contact)


@router.get("/contacts/", response_model=list[schemas.ContactOut])
def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_contacts(db, skip, limit)


@router.get("/contacts/{contact_id}", response_model=schemas.ContactOut)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.get_contact(db, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/contacts/{contact_id}", response_model=schemas.ContactOut)
def update(
    contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)
):
    return crud.update_contact(db, contact_id, contact)


@router.delete("/contacts/{contact_id}")
def delete(contact_id: int, db: Session = Depends(get_db)):
    return crud.delete_contact(db, contact_id)


@router.get("/contacts/search/", response_model=list[schemas.ContactOut])
def search(query: str, db: Session = Depends(get_db)):
    return crud.search_contacts(db, query)


@router.get("/contacts/birthdays/", response_model=list[schemas.ContactOut])
def upcoming_birthdays(db: Session = Depends(get_db)):
    return crud.get_upcoming_birthdays(db)
