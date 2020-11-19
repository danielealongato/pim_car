import pypyodbc
from urllib.parse import quote_plus

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# String de conexão Windows Server.
parametros = (
    # Driver que será utilizado na conexão
    DRIVER={ODBC Driver 17 for SQL Server};
    # IP ou nome do servidor\Versão do SQL.
    'SERVER=DESKTOP-NMV9682\SQLEXPRESS;'
    # Porta
    'PORT=1433;'
    # Banco que será utilizado.
    'DATABASE=Blockchain;'
    # Nome de usuário.
    'UID=DESKTOP-NMV9682\Usuário;'
    # Senha.
    'PWD=root')

# String de conexão Docker imagem Linux.
# parametros = (
#     # Driver que será utilizado na conexão
#     'DRIVER={ODBC Driver 17 for SQL Server};'
#     # IP ou nome do servidor\
#     'SERVER=192.168.100.118;'
#     # Porta
#     'PORT=1433;'
#     # Banco que será utilizado (Criar banco).
#     'DATABASE=PythonMSSQL;'
#     # Nome de usuário (Usuário default da imagem Docker).
#     'UID=SA;'
#     # Senha.
#     'PWD=Python.123456')

# Convertendo a string para um padrão de URI HTML.
url_db = quote_plus(parametros)

# Conexão.
# Para debug utilizar echo=True
engine = create_engine('mssql+pyodbc:///?odbc_connect=%s' % url_db)

# Criando uma classe "Session" já configurada.
# Session é instanciado posteriormente para interação com a tabela.
Session = sessionmaker(bind=engine)

Base = declarative_base()


class CustomerTable(Base):
    """Cada classe representa uma tabela do banco"""
    # Nome da tabela, se a variável não for
    # declarada será utilizado o nome da classe.
    __tablename__ = 'Clientes'

    # Colunas da tabela.
    id = Column(Integer, primary_key=True)
    nome = Column('nome', String(50))
    email = Column('email', String(50))
    cpf = Column('cpf', String(50))

    def __init__(self, nome: str, email: str, cpf: str):
        """Construtor.
        Utilizando o construtor para passar os valores
        no momento em que a classe é instanciada.
        :param nome: (str).
        :param idade: (int).
        :param sexo: (str).
        """
        self.nome = nome
        self.email = email
        self.cpf = cpf


if __name__ == "__main__":
    # Verificando se o driver do MS SQL Server está instalado. ODBC Driver 17 for SQL Server
    print([x for x in pypyodbc.drivers() if x.startswith('ODBC Driver 17 for SQL Server')])

    # Removendo todas as tabelas do banco.
    # Base.metadata.drop_all(engine)

    # Criando todas as tabelas.
    #Base.metadata.create_all(engine)

    # Criando uma sessão (add, commit, query, etc).
    session = Session()

    # Criando os dados que serão inseridos na tabela.
    # Classe com o construtor.
    # usuario = NomeDaTabela('Felipe', 35, 'Masculino')
    # usuarios = [NomeDaTabela('Maria', 20, 'Feminino'), NomeDaTabela('Pedro', 50, 'Masculino')]

    # Caso não seja utilizado o construtor na classe
    # os dados são passados depois de se criar a instancia.
    # usuario = NomeDaTabela()
    # usuario.nome = 'Camila'
    # usuario.idade = 50
    # usuario.sexo = 'Feminino'

    # Inserindo registro na tabela.
    # session.add(usuario)

    # Inserindo vários registros na tabela.
    # session.add_all(usuarios)

    # Persistindo os dados.
    # session.commit()

    # Consultar todos os registros.
    dados = session.query(CustomerTable).all()
    print(dados)
    for cliente in dados:
         print(f'Nome: {cliente.nome} - Email: {cliente.email} - cpf: {cliente.cpf}')

    # Consulta registros com filtro.
    # dados = session.query(NomeDaTabela).filter(NomeDaTabela.idade > 40).all()
    # print(dados)
    # for linha in dados:
    #     print(f'Nome: {linha.nome} - Idade: {linha.idade} - Sexo: {linha.sexo}')

    # Alterar um registro da tabela.
    # print('Nome ANTES da alteração:', session.query(NomeDaTabela).filter(NomeDaTabela.id == 1).one().nome)
    # session.query(NomeDaTabela).filter(NomeDaTabela.id == 1).update({'nome': 'Roberto'})
    # session.commit()
    # print('Nome DEPOIS da alteração:', session.query(NomeDaTabela).filter(NomeDaTabela.id == 1).one().nome)

    # Remover um registro da tabela.
    # print('Registro ANTES da remoção:', session.query(NomeDaTabela).filter(NomeDaTabela.id == 1).one_or_none())
    # session.query(NomeDaTabela).filter(NomeDaTabela.id == 1).delete()
    # session.commit()
    # print('Registro DEPOIS da remoção:', session.query(NomeDaTabela).filter(NomeDaTabela.id == 1).one_or_none())

    # Fechando a sessão.
    session.close()
