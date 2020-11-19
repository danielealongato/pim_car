from datetime import datetime

from pytz import timezone
from PIM_HTML_4SEM.app import db



def cur_datetime():
    return datetime.now(tz=timezone('America/Sao_Paulo'))


class Customers(db):
    """
    Esta tabela pega todos os dados que foram coletados ao longo de todas as consultas entre APIS
    """
    __tablename__ = 'Clients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DATETIME, default=cur_datetime)
    updated = db.Column(db.DATETIME, default=cur_datetime, onupdate=cur_datetime)

    # insumos
    name = db.Column('name', db.String(40), nullable=False)
    phone_number = db.Column('phone_number', db.String(20), nullable=False)
    document_number = db.Column('document_number', db.String(20), nullable=False)
    email = db.Column('email', db.String(40), nullable=False)
    address = db.Column('address', db.String(100), nullable=False)


    def __repr__(self) -> str:
        return f"<Customer id: {self.id}, document:{self.document_number}>"
