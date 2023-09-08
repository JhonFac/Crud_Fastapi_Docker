from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth import (
    CreateUserRequest,
    OAuth2PasswordRequestForm,
    authenticate_user,
    bcrypt_context,
    create_access_token,
    get_current_user,
    validate_user,
)
from app.crud import delete_person, get_all_people, get_person_by_id, update_person
from app.database import get_db
from app.models import Person, User
from app.schemas import CreateUserRequest, PersonCreate, PersonUpdate, Token

# Configuración de la ruta API '/auth' y creación de la aplicación FastAPI.
router = APIRouter(prefix="/auth", tags=["auth"])
app = FastAPI()
app.description = "Test en FastAPI para autenticación con JWT y CRUD de personas."
app.title = "Test Imagine"

# Anotación para la dependencia que obtiene la sesión de la base de datos.
db_dependency = Annotated[Session, Depends(get_db)]

# Anotación para la dependencia que obtiene el usuario actual.
user_dependency = Annotated[dict, Depends(get_current_user)]
# Seccion de autenticacion JWT


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    existing_user = db.query(User).filter(User.username == create_user_request.username).first()
    if existing_user:
        return {"message": "User already exists"}, status.HTTP_400_BAD_REQUEST

    try:
        new_user = User(
            username=create_user_request.username,
            hashed_password=bcrypt_context.hash(create_user_request.password),
        )
        db.add(new_user)
        db.commit()
        return {"message": "User created successfully"}
    except IntegrityError:
        return {"message": "Error creating user. Duplicate username."}, status.HTTP_400_BAD_REQUEST


# Autentica al usuario y genera un token de acceso JWT.
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    token = create_access_token(user.username, user.id, timedelta(minutes=200))
    return {"access_token": token, "token_type": "bearer"}


# Obtiene información del usuario actual.
@app.get("/", status_code=status.HTTP_200_OK, tags=["User"])
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Autenticaction Fails")
    return {"User": user}


# seccion de crud


# Configura las rutas relacionadas con el CRUD de personas.
app.include_router(router)


# Obtiene una lista de personas desde la base de datos.
@app.get("/people/", tags=["Person"])
async def read_people(user: user_dependency, db: db_dependency):
    validate_user(user)
    return get_all_people(db)


# Obtiene detalles de una persona por su ID.
@app.get("/person/{person_id}/", tags=["Person"])
async def read_person(user: user_dependency, person_id: int, db: db_dependency):
    validate_user(user)
    person = get_person_by_id(db, person_id)
    if person:
        return person
    raise HTTPException(status_code=404, detail="Person not found")


# Crea una nueva persona en la base de datos.
@app.post("/create-person/", tags=["Person"])
async def create_person(user: user_dependency, person: PersonCreate, db: db_dependency):
    validate_user(user)
    person_dict = person.dict()
    new_person = Person(**person_dict)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person


# Actualiza información de una persona por su ID.
@app.put("/update-person/{person_id}/", tags=["Person"])
async def update_person_data(user: user_dependency, person_id: int, person_data: PersonUpdate, db: db_dependency):
    validate_user(user)
    updated_person = update_person(db, person_id, person_data.dict(exclude_unset=True))
    if updated_person:
        return updated_person
    raise HTTPException(status_code=404, detail="Person not found")


# Elimina una persona por su ID.
@app.delete("/delete-person/{person_id}/", tags=["Person"])
async def delete_person_data(user: user_dependency, person_id: int, db: db_dependency):
    validate_user(user)
    deleted_person = delete_person(db, person_id)
    if deleted_person:
        return deleted_person
    raise HTTPException(status_code=404, detail="Person not found")
