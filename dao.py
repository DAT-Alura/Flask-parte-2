from flask_pymongo import ObjectId

from models import Jogo, Usuario


class JogoDao:
    def __init__(self, tabela):
        self.tabela = tabela

    def salvar(self, jogo):
        if jogo.id != None:
            self.tabela.update_one(
                {'_id': ObjectId(jogo.id)},
                {'$set': {
                    'nome': jogo.nome, 'categoria': jogo.categoria, 'console': jogo.console
                }}
            )
        else:
            response = self.tabela.insert_one({
                'nome': jogo.nome, 'categoria': jogo.categoria, 'console': jogo.console
            })
            jogo.id = response.inserted_id
        return jogo

    def listar(self):
        return self.tabela.find()

    def busca_por_id(self, id):
        return self.tabela.find_one({'_id': ObjectId(id)})

    def deletar(self, id):
        return self.tabela.delete_one({'_id': ObjectId(id)})


class UsuarioDao:
    def __init__(self, tabela):
        self.tabela = tabela

    def busca_por_id(self, id):
        return self.tabela.find_one({'id': id})
