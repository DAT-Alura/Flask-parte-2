import os

from jogoteca import app


def recupera_arquivo(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if id in nome_arquivo:
            return nome_arquivo


def deleta_arquivo(id):
    arquivo = recupera_arquivo(id)
    if arquivo != None:
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))
