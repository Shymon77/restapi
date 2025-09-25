from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas.user import UserCreate, UserResponse, Token
from app.services import auth

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Регистрирует нового пользователя.

    :param user: Данные пользователя (имя, email, пароль)
    :param db: Сессия базы данных
    :return: Информация о зарегистрированном пользователе
    """
    existing_user = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    hashed_password = auth.hash_password(user.password)
    new_user = models.User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    """
    Выполняет вход пользователя в систему и выдаёт JWT токен.

    :param form_data: Логин и пароль пользователя (OAuth2)
    :param db: Сессия базы данных
    :return: JWT токен при успешной аутентификации
    """
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = auth.create_access_token({"sub": db_user.email})
    refresh_token = auth.create_refresh_token({"sub": db_user.email})
    return Token(access_token=access_token, refresh_token=refresh_token)


from app.utils.email import confirm_token
from app.models import User


@auth_bp.route("/verify/<token>", methods=["GET"])
def confirm_email(token):
    """
    Обновляет JWT токен пользователя по refresh-токену.

    :param credentials: Текущий refresh-токен
    :param db: Сессия базы данных
    :return: Новый access и refresh токены
    """
    email = confirm_token(token)
    """
Подтверждает email пользователя по токену из письма.

:param token: Токен подтверждения email
:param db: Сессия базы данных
:return: Сообщение об успешном или неуспешном подтверждении
"""
    if not email:
        return jsonify({"message": "Недійсний або прострочений токен"}), 400
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Користувача не знайдено"}), 404
    if user.confirmed:
        return jsonify({"message": "Email вже підтверджено"}), 200

    user.confirmed = True
    db.session.commit()
    return jsonify({"message": "Email підтверджено!"}), 200


send_confirmation_email(user.email)


@user_bp.route("/avatar", methods=["POST"])
@jwt_required()
def upload_avatar():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    file = request.files["avatar"]
    result = cloudinary.uploader.upload(file)

    user.avatar_url = result["secure_url"]
    db.session.commit()

    return jsonify({"avatar": user.avatar_url}), 200
