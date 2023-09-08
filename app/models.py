from passlib.hash import bcrypt
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func

Base = declarative_base()

# Clase que representa la tabla 'people' en la base de datos.
class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    cel_number = Column(String)
    dress = Column(String)
    city = Column(String)


# Clase que representa la tabla 'users' en la base de datos.
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    tokens = relationship("Token", back_populates="user")


# Clase que representa la tabla 'tokens' en la base de datos.
class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String)
    token_type = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="tokens")
    user_id = Column(Integer, ForeignKey("users.id"))
