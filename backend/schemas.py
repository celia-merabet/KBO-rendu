from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class EstablishmentBase(BaseModel):
    establishment_number: int
    status: Optional[str] = None
    start_date: Optional[date] = None

class EstablishmentCreate(EstablishmentBase):
    pass

class Establishment(EstablishmentBase):
    class Config:
        orm_mode = True

class EnterpriseBase(BaseModel):
    enterprise_number: int
    status: Optional[str] = None
    juridical_form: Optional[str] = None
    type: Optional[str] = None
    language: Optional[str] = None
    start_date: Optional[date] = None

class EnterpriseCreate(EnterpriseBase):
    establishments: Optional[List[EstablishmentCreate]] = []

class Enterprise(EnterpriseBase):
    establishments: List[Establishment] = []

    class Config:
        orm_mode = True
