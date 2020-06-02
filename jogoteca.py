from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_pymongo import PyMongo

from dao import JogoDao, UsuarioDao
from models import Jogo, Usuario

app = Flask(__name__)
app.secret_key = 'daniel'
app.config["MONGO_URI"] = "mongodb://localhost:27017/jogoteca"
mongo = PyMongo(app)

jogo_dao = JogoDao(mongo.db.jogo)
usuario_dao = UsuarioDao(mongo.db.usuario)


@app.route('/')
def index():
    jogos = jogo_dao.listar()
    return render_template('lista.html', titulo='Jogos', jogos=jogos)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo')


@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    jogo_dao.salvar(jogo)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo='Login', proxima=proxima)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = usuario_dao.busca_por_id(request.form['id'])
    if usuario != None and request.form['senha'] == usuario['senha']:
        session['usuario_logado'] = usuario['id']
        flash(usuario['nome'] + ' logou com sucesso!')
        proxima = request.form['proxima']
        return redirect(proxima)
    flash(request.form['id'] + ' não logado, tente novamente!')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    flash(session['usuario_logado'] + ' foi deslogado!')
    session['usuario_logado'] = None
    return redirect(url_for('index'))


app.run(debug=True, port=8080)
