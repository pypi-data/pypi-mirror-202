from .base_declative_entity import Base
from sqlalchemy import Column, Integer, String, Float


class Rua(Base):
    __tablename__ = 'TRUA'
    
    id = Column(Integer, primary_key =  True)
    rua = Column(String)
    bairro = Column(Integer)
    logradouro = Column(Integer)
    cep = Column(String)
