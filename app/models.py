from sqlalchemy import Column, Integer, String, Enum
from .database import Base

class Usuario(Base):
    __tablename__ = "USUARIOS"
    UserID = Column(Integer, primary_key=True, index=True)
    Nome = Column(String)
    Email = Column(String, unique=True, index=True)
    SenhaHash = Column(String, nullable=False)
    Role = Column(Enum('professor', 'orientador', 'coordenador'), nullable=False)
