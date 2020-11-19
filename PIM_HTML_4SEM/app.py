from flask import Flask, render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

app = Flask("Projeto Vinicius")
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@127.0.0.1/dani'
# config_database = {'SQLALCHEMY_DATABASE_URI': 'mysql+mysqlconnector://root:@127.0.0.1/dani'}
# app.config.from_mapping(config_database)

db = SQLAlchemy()
manager = Manager(app)
manager.add_command('db', MigrateCommand)

def create_app():
    from PIM_HTML_4SEM.models.entities import Customers

    db.init_app(app=app)
    migrate = Migrate(app, db)
    return app


@app.route("/")
def index():
    return render_template("atclientes.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/bd")
def bd():
    return render_template("bd.html")


@app.route("/bi")
def bi():
    return render_template("bi.html")


@app.route("/diamante")
def diamante():
    return render_template("diamante.html")


@app.route("/mobdados")
def mobdados():
    return render_template("mobdados.html")

