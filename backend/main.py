from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import engine, get_db

# Crée les tables si elles n'existent pas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="KBO CRUD API")

@app.post("/enterprises/", response_model=schemas.Enterprise)
def create_enterprise(enterprise: schemas.EnterpriseCreate, db: Session = Depends(get_db)):
    db_ent = crud.get_enterprise(db, enterprise.enterprise_number)
    if db_ent:
        raise HTTPException(status_code=400, detail="Entreprise déjà existante")
    return crud.create_enterprise(db, enterprise)

@app.get("/enterprises/{enterprise_number}", response_model=schemas.Enterprise)
def read_enterprise(enterprise_number: int, db: Session = Depends(get_db)):
    db_ent = crud.get_enterprise(db, enterprise_number)
    if db_ent is None:
        raise HTTPException(status_code=404, detail="Entreprise non trouvée")
    return db_ent

@app.delete("/enterprises/{enterprise_number}")
def delete_enterprise(enterprise_number: int, db: Session = Depends(get_db)):
    success = crud.delete_enterprise(db, enterprise_number)
    if not success:
        raise HTTPException(status_code=404, detail="Entreprise non trouvée")
    return {"detail": "Entreprise supprimée"}

# CRUD ÉTABLISSEMENTS
@app.get("/enterprises/{enterprise_number}/establishments", response_model=List[schemas.Establishment])
def get_establishments(enterprise_number: int, db: Session = Depends(get_db)):
    return crud.get_establishments(db, enterprise_number)

@app.put("/establishments/{est_number}", response_model=schemas.Establishment)
def update_establishment(est_number: int, updates: schemas.EstablishmentCreate, db: Session = Depends(get_db)):
    est = crud.update_establishment(db, est_number, updates.dict())
    if not est:
        raise HTTPException(status_code=404, detail="Établissement non trouvé")
    return est
