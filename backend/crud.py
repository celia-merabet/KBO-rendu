# backend/crud.py
from sqlalchemy.orm import Session

from . import models, schemas


# ENTREPRISE
def get_enterprise(db: Session, enterprise_number: int):
    return db.query(models.Enterprise).filter(models.Enterprise.enterprise_number == enterprise_number).first()

def create_enterprise(db: Session, enterprise: schemas.EnterpriseCreate):
    db_enterprise = models.Enterprise(
        enterprise_number=enterprise.enterprise_number,
        status=enterprise.status,
        juridical_form=enterprise.juridical_form,
        type=enterprise.type,
        language=enterprise.language,
        start_date=enterprise.start_date
    )
    db.add(db_enterprise)
    db.commit()
    db.refresh(db_enterprise)

    # Ajouter les établissements si fournis
    for est in enterprise.establishments:
        db_est = models.Establishment(
            establishment_number=est.establishment_number,
            status=est.status,
            start_date=est.start_date,
            enterprise_number=db_enterprise.enterprise_number
        )
        db.add(db_est)
    db.commit()
    return db_enterprise

def delete_enterprise(db: Session, enterprise_number: int):
    db_ent = get_enterprise(db, enterprise_number)
    if db_ent:
        db.delete(db_ent)
        db.commit()
        return True
    return False

# ÉTABLISSEMENT
def get_establishments(db: Session, enterprise_number: int):
    return db.query(models.Establishment).filter(models.Establishment.enterprise_number == enterprise_number).all()

def update_establishment(db: Session, est_number: int, updates: dict):
    est = db.query(models.Establishment).filter(models.Establishment.establishment_number == est_number).first()
    if not est:
        return None
    for key, value in updates.items():
        setattr(est, key, value)
    db.commit()
    db.refresh(est)
    return est
