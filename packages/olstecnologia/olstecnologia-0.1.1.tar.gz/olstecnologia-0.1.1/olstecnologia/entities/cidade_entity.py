from .base_declative_entity import Base
from sqlalchemy import Column, Integer, String, Float


class Cidade(Base):
    __tablename__ = "TCIDADE"
    
    id = Column(Integer, primary_key =  True)
    cidade = Column(String)
    estado = Column(String)
    inativo = Column(String)
    ibge = Column(Float)
    