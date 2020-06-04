from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from flask_pymongo import PyMongo
import os

from dao import JogoDao, UsuarioDao
from models import Jogo, Usuario

app = Flask(__name__)
app.secret_key = 'daniel'
app.config["MONGO_URI"] = "mongodb://localhost:27017/jogoteca"
app.config["UPLOAD_PATH"] = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
mongo = PyMongo(app)

JOGO_DAO = JogoDao(mongo.db.jogo)
USUARIO_DAO = UsuarioDao(mongo.db.usuario)


@app.route('/')
def index():
    jogos = JOGO_DAO.listar()
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
    jogo = JOGO_DAO.salvar(Jogo(nome, categoria, console))
    if request.files['arquivo']:
        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        arquivo.save(f'{upload_path}/{jogo.id}.jpg')
    return redirect(url_for('index'))


@app.route('/editar/<string:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    jogo = JOGO_DAO.busca_por_id(id)
    return render_template('editar.html', titulo='Editar', jogo=jogo, nome_arquivo=f'{id}.jpg')


@app.route('/atualizar', methods=['POST'])
def atualizar():
    id = request.form['id']
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console, id)
    JOGO_DAO.salvar(jogo)
    return redirect(url_for('index'))


@app.route('/deletar/<string:id>')
def deletar(id):
    JOGO_DAO.deletar(id)
    flash('O jogo foi removido com sucesso!')
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo='Login', proxima=proxima)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = USUARIO_DAO.busca_por_id(request.form['id'])
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


@app.route('/uploads/<string:nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)


app.run(debug=True, port=8080)
