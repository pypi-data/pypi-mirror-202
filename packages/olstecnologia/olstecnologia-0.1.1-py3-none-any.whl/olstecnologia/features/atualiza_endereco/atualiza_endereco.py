
from olstecnologia.config import Conn
from olstecnologia.services.utils import for_dict
from sqlalchemy import select, update, bindparam
from olstecnologia.entities import Paciente, Logradouro, Rua, Bairro, Cidade
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm
import json
import urllib.parse

def atualizando(connect_string):

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

def atualiza_endereco():

    print("a => Pegar dados do arquivo.\nb => digitar a string de conexão.")
    opt = input("Digite sua opção ou tecla enter para selecionar a opção A: ")

    if opt == 'b':
        
        print("Exemplo: (firebird://user:password@host/database)")
        connect_string = input("String de conexão: ")
        
        atualizando(connect_string)
    else:
        
        file_name = input("Caminho do arquivo com extensão .json: ")
        file = open(file_name, "r")

        data_dict = json.loads(file.read())

        if len(data_dict['content']) > 1:
            for x in range(len(data_dict['content'])):
                user = data_dict['content'][x]['user_nameBD']
                password = urllib.parse.quote_plus(data_dict['content'][x]['PassWordBD'])
                host = data_dict['content'][x]['Server']
                port = data_dict['content'][x]['Porta']
                database = data_dict['content'][x]['Database']

                connect_string = f"firebird://{user}:{password}@{host}:{port}/{database}"

                atualizando(connect_string)
        else:

            user = data_dict['content'][0]['user_nameBD']
            password = urllib.parse.quote_plus(data_dict['content'][0]['PassWordBD'])
            host = data_dict['content'][0]['Server']
            port = data_dict['content'][0]['Porta']
            database = data_dict['content'][0]['Database']

            connect_string = f"firebird://{user}:{password}@{host}:{port}/{database}"
            
            atualizando(connect_string)