from flask import Blueprint, request, jsonify, abort
from app import crud
from app.schemas import (
    schemas,
)
from app.database import SessionLocal

contacts_bp = Blueprint("contacts", __name__, url_prefix="/contacts")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contacts_bp.route("/", methods=["POST"])
def create_contact():
    db = next(get_db())
    data = request.get_json()
    contact = crud.create_contact(db, data)
    return jsonify(contact), 201


@contacts_bp.route("/", methods=["GET"])
def read_contacts():
    db = next(get_db())
    skip = int(request.args.get("skip", 0))
    limit = int(request.args.get("limit", 100))
    contacts = crud.get_contacts(db, skip, limit)
    return jsonify(contacts), 200


@contacts_bp.route("/<int:contact_id>", methods=["GET"])
def read_contact(contact_id):
    db = next(get_db())
    contact = crud.get_contact(db, contact_id)
    if contact is None:
        abort(404, description="Contact not found")
    return jsonify(contact), 200


@contacts_bp.route("/<int:contact_id>", methods=["PUT"])
def update_contact(contact_id):
    db = next(get_db())
    data = request.get_json()
    updated_contact = crud.update_contact(db, contact_id, data)
    if updated_contact is None:
        abort(404, description="Contact not found")
    return jsonify(updated_contact), 200


@contacts_bp.route("/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    db = next(get_db())
    success = crud.delete_contact(db, contact_id)
    if not success:
        abort(404, description="Contact not found")
    return "", 204


@contacts_bp.route("/search/", methods=["GET"])
def search_contacts():
    db = next(get_db())
    query = request.args.get("query", "")
    results = crud.search_contacts(db, query)
    return jsonify(results), 200


@contacts_bp.route("/birthdays/", methods=["GET"])
def upcoming_birthdays():
    db = next(get_db())
    results = crud.get_upcoming_birthdays(db)
    return jsonify(results), 200
