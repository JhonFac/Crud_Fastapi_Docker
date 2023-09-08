from pydantic import BaseModel


# Clase para crear una nueva persona (utilizada en el endpoint de creación).
class PersonCreate(BaseModel):
    first_name: str
    last_name: str
    cel_number: str
    dress: str
    city: str


# Clase para actualizar los datos de una persona (utilizada en el endpoint de actualización).
class PersonUpdate(BaseModel):
    first_name: str
    last_name: str
    cel_number: str
    dress: str
    city: str


# Clase para representar una persona (utilizada en respuestas y solicitudes).
class Person(BaseModel):
    id: int
    first_name: str
    last_name: str
    cel_number: str
    dress: str
    city: str


# Clase para representar una persona en la base de datos (configurada para ORM).
class PersonInDB(Person):
    class Config:
        orm_mode = True


# Clase para solicitar la creación de un nuevo usuario.
class CreateUserRequest(BaseModel):
    username: str
    password: str


# Clase para representar un token de acceso.
class Token(BaseModel):
    access_token: str
    token_type: str
