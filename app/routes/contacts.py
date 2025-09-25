from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Contact, User
from app.schemas import ContactCreate, ContactResponse
from app.routes.auth import get_current_user
from app.extensions import limiter
from fastapi.security import OAuth2PasswordBearer

contacts_bp = APIRouter(prefix="/contacts", tags=["contacts"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@contacts_bp.post("/", response_model=ContactResponse)
@limiter.limit("5/minute")
async def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_contact = Contact(**contact.dict(), owner_id=current_user.id)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


@contacts_bp.get("/", response_model=List[ContactResponse])
async def get_contacts(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    contacts = db.query(Contact).filter(Contact.owner_id == current_user.id).all()
    return contacts


@contacts_bp.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = (
        db.query(Contact)
        .filter(Contact.id == contact_id, Contact.owner_id == current_user.id)
        .first()
    )
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@contacts_bp.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int,
    contact_update: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = (
        db.query(Contact)
        .filter(Contact.id == contact_id, Contact.owner_id == current_user.id)
        .first()
    )
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    for key, value in contact_update.dict().items():
        setattr(contact, key, value)
    db.commit()
    db.refresh(contact)
    return contact


@contacts_bp.delete("/{contact_id}")
async def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = (
        db.query(Contact)
        .filter(Contact.id == contact_id, Contact.owner_id == current_user.id)
        .first()
    )
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    db.delete(contact)
    db.commit()
    return {"detail": "Contact deleted successfully"}
