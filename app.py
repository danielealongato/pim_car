from flask import Flask, render_template, request
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy


app = Flask("Projeto Car")
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:''@127.0.0.1/dani'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.run(debug=True)

db = SQLAlchemy(app)
db.init_app(app=app)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
from models.entities import Customers

def create_app():
    from models.entities import Customers
    db.init_app(app=app)
    migrate = Migrate(app, db)
    return app


@app.route("/home", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('home.html')

    if request.method == 'POST':
        print(request.values.get('name'), request.values.get('email'), request.values.get('message'))
        Customers.inserting(name=request.values.get('name'), email=request.values.get('email'), message=request.values.get('message'))
        return render_template('home.html')


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

@app.route("/atclientes")
def atclientes():
    return render_template("atclientes.html")