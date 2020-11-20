from models.entities import Customers, cur_datetime
from app import app
from flask import request, render_template,  redirect, url_for, jsonify, session, Response


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