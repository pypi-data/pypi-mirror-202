
from sqlalchemy import Column, Integer, String
from .base_declative_entity import Base


class Bairro(Base):
    __tablename__ = "TBAIRRO"
    
    id = Column(Integer, primary_key =  True)
    bairro = Column(String)
    cidade = Column(Integer)
    inativo = Column(String)