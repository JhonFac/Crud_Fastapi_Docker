from sqlalchemy.orm import Session

from .models import Person


# Función para crear una nueva persona en la base de datos
def create_person(db: Session, person_data: dict):
    new_person = Person(**person_data)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person


# Función para obtener todas las personas en la base de datos
def get_all_people(db: Session):
    return db.query(Person).all()


# Función para obtener una persona por su ID
def get_person_by_id(db: Session, person_id: int):
    return db.query(Person).filter(Person.id == person_id).first()


# Función para actualizar los datos de una persona
def update_person(db: Session, person_id: int, person_data: dict):
    person = db.query(Person).filter(Person.id == person_id).first()
    if person:
        for key, value in person_data.items():
            setattr(person, key, value)
        db.commit()
        db.refresh(person)
        return person
    return None


# Función para eliminar una persona por su ID
def delete_person(db: Session, person_id: int):
    person = db.query(Person).filter(Person.id == person_id).first()
    if person:
        db.delete(person)
        db.commit()
        return person
    return None
