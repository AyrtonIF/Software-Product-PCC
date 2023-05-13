from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from flask_mail import Mail, Message
from app import secret

app = Flask(__name__)
app.config.from_object('config')
app.config['SECRET_KEY'] = 'secret'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'software.product.bot@gmail.com'
app.config['MAIL_PASSWORD'] = secret.senha
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

login_manager = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

from app.models import tables
from app.controllers import default