from datetime import datetime
from pytz import timezone
from app import db



def cur_datetime():
    return datetime.now(tz=timezone('America/Sao_Paulo'))


class Customers(db.Model):
    """
    Esta tabela pega todos os dados que foram coletados 
    """
    __tablename__ = 'Clients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DATETIME, default=cur_datetime)
    updated = db.Column(db.DATETIME, default=cur_datetime, onupdate=cur_datetime)

    # insumos
    name = db.Column('name', db.String(40), nullable=True)
    email = db.Column('email', db.String(40), nullable=True)
    message = db.Column('message', db.String(300), nullable=True)


    def __repr__(self) -> str:
        return f"<Nome: {self.name}, Mensagem:{self.message}>"


    def __init__(self,
                 name: str,
                 email: str,
                 message: str):
        self.name = name
        self.email = email
        self.message = message


    @classmethod
    def inserting(cls, name: str, email: str, message: str):
       new_message = Customers(name=name,
                                  email=email,
                                  message=message)
       new_message.save()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise Exception(f'Error to save on database!! {e}')