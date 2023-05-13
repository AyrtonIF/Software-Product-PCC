from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()

class Clientes(db.Model):
    __tablename__ = "Clientes"

    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    genero = db.Column(db.String)
    nascimento = db.Column(db.String)
    fone = db.Column(db.Integer)
    cidade = db.Column(db.String)
    estado = db.Column(db.String)
    endereco = db.Column(db.String)

    def __init__(self, cliente, email, fone, genero, nascimento, cidade, estado, endereco):
        self.cliente = cliente
        self.email = email
        self.fone = fone
        self.genero = genero
        self.nascimento = nascimento
        self.cidade = cidade
        self.estado = estado
        self.endereco = endereco

class Produtos(db.Model):
    __tablename__ = "Produtos"

    id = db.Column(db.Integer, primary_key=True)
    nome_produto = db.Column(db.String)
    codigo_produto = db.Column(db.String, unique=True)
    quantidade = db.Column(db.Integer)
    produto = db.Column(db.String)
    data_cadastro = db.Column(db.String)

    def __init__(self, nome_produto, codigo_produto, quantidade, produto, data_cadastro):
        self.nome_produto = nome_produto
        self.codigo_produto = codigo_produto
        self.quantidade = quantidade
        self.produto = produto
        self.data_cadastro = data_cadastro

class User(db.Model, UserMixin):
    __tablename__ = "Users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)
    
class Pedidos(db.Model):
    __tablename__ = "Pedidos"

    id = db.Column(db.Integer, primary_key=True)
    email_cliente = db.Column(db.String)
    codigo_produto = db.Column(db.Integer)
    quantidade = db.Column(db.Integer)
    status = db.Column(db.String)
    data_hora = db.Column(db.String)

    def __init__(self, email_cliente, codigo_produto, quantidade, status, data_hora):
        self.email_cliente = email_cliente
        self.codigo_produto = codigo_produto
        self.quantidade = quantidade
        self.status = status
        self.data_hora = data_hora