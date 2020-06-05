from flask import render_template, request, session, flash, redirect, url_for, send_from_directory
import time

from helpers import recupera_arquivo, deleta_arquivo
from jogoteca import app, mongo
from models import Jogo
from dao import JogoDao, UsuarioDao

JOGO_DAO = JogoDao(mongo.db.jogo)
USUARIO_DAO = UsuarioDao(mongo.db.usuario)


@app.route('/')
def index():
    jogos = JOGO_DAO.listar()
    return render_template('lista.html', titulo='Jogos', jogos=jogos)


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
        timestamp = time.time()
        arquivo.save(f'{upload_path}/{jogo.id}-{timestamp}.jpg')
    return redirect(url_for('index'))


@app.route('/editar/<string:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    jogo = JOGO_DAO.busca_por_id(id)
    nome_arquivo = recupera_arquivo(id) if recupera_arquivo(id) else 'capa_padrao.jpg'
    return render_template('editar.html', titulo='Editar', jogo=jogo, nome_arquivo=nome_arquivo)


@app.route('/atualizar', methods=['POST'])
def atualizar():
    id = request.form['id']
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console, id)
    JOGO_DAO.salvar(jogo)
    if request.files['arquivo']:
        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(jogo.id)
        arquivo.save(f'{upload_path}/{jogo.id}-{timestamp}.jpg')
    return redirect(url_for('index'))


@app.route('/uploads/<string:nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)


@app.route('/deletar/<string:id>')
def deletar(id):
    JOGO_DAO.deletar(id)
    flash('O jogo foi removido com sucesso!')
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    flash(session['usuario_logado'] + ' foi deslogado!')
    session['usuario_logado'] = None
    return redirect(url_for('index'))
