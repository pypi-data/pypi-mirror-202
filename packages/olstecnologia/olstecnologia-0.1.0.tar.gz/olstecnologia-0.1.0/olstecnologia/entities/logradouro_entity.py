from .base_declative_entity import Base
from sqlalchemy import Column, Integer, String, Float


class Logradouro(Base):
    __tablename__ = "TLOGRADOURO"

    id = Column(Integer, primary_key =  True)
    cod_logradouro = Column(String)
    descricao = Column(String)
    inativo = Column(String)