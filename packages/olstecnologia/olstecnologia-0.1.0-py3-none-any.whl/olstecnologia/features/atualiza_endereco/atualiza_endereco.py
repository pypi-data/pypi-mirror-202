
from olstecnologia.config import Conn
from olstecnologia.services.utils import cria_list_with_dicts, for_dict
from sqlalchemy import Table, select, update, bindparam, MetaData
import timeit
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from olstecnologia.entities import Paciente, Logradouro, Rua, Bairro, Cidade
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm


def atualiza_endereco():

    print("String de conexão: Exemplo: (firebird://user:password@host/database)")
    connect_string = input("String de conexão: ")
    # connect_string = "firebird://sysdba:masterkey@192.168.100.10/D:/Servidor/Desenvolvimento/BD DOS CLIENTES/BD - Fredson/CLINI7.FDB"

    #Pegando a conexão
    try:
        conexao = Conn(connect_string) 

        conn = conexao.engine()
        session = conexao.session()
        Session = sessionmaker(conn)
    except:
        print("Erro na conexão do banco de dados!")

    # # Criando a consulta com joins
    query = select(Paciente.id,
                    (Logradouro.descricao+" "+Rua.rua),
                    Rua.cep, Bairro.bairro, Cidade.cidade,
                    Cidade.estado, Cidade.ibge)\
                    .join(Paciente, Paciente.rua == Rua.id)\
                        .join(Logradouro, Logradouro.id == Rua.logradouro)\
                            .join(Bairro, Bairro.id == Rua.bairro)\
                                .join(Cidade, Cidade.id == Bairro.cidade)

    
    # # Criando a query de atualização
    stmt = update(Paciente)\
        .where(Paciente.id == bindparam("p_id"))\
            .values(cep=bindparam("cep"), endereco=bindparam("endereco"), bairro=bindparam("bairro"), codmunicipioibge=bindparam("codmunicipioibge"), municipio=bindparam("municipio"), uf=bindparam("uf"))

    # Pegando os dados
    # Tratando os dados
    # Executando a atualização
    with Session() as s:
        data = s.execute(query)
        data_update = [for_dict(x) for x in data] 

        # with tqdm(total=100, desc ="Atualizando o banco: ") as barra_progresso:

        for x in tqdm(range(len(data_update)), desc ="Atualizando o banco: "):
            try:
                session.execute(stmt, data_update[x])
                session.commit()
            except Exception as e:
                print(e)
            # barra_progresso.update(100)

    print("Atualização realizada com sucesso!!!")

