from sqlalchemy import BigInteger, Column, Date, ForeignKey, String
from sqlalchemy.orm import relationship

from .database import Base


class Enterprise(Base):
    __tablename__ = "enterprise"
    enterprise_number = Column(BigInteger, primary_key=True, index=True)
    status = Column(String)
    juridical_form = Column(String)
    type = Column(String)
    language = Column(String)
    start_date = Column(Date)

    establishments = relationship("Establishment", back_populates="enterprise", cascade="all, delete")

class Establishment(Base):
    __tablename__ = "establishment"
    establishment_number = Column(BigInteger, primary_key=True, index=True)
    enterprise_number = Column(BigInteger, ForeignKey("enterprise.enterprise_number", ondelete="CASCADE"))
    status = Column(String)
    start_date = Column(Date)

    enterprise = relationship("Enterprise", back_populates="establishments")
