from models import Jogo, Usuario


class JogoDao:
    def __init__(self, tabela):
        self.tabela = tabela

    def salvar(self, jogo):
        jogoExiste = self.tabela.find_one({'nome': jogo.nome})
        if jogoExiste != None:
            self.tabela.update_one(
                {'nome': jogo.nome},
                {'$set': {'categoria': jogo.categoria, 'console': jogo.console}}
            )
        else:
            self.tabela.insert_one({
                'nome': jogo.nome, 'categoria': jogo.categoria, 'console': jogo.console
            })
        return jogo

    def listar(self):
        return self.tabela.find()

    def busca_por_id(self, nome):
        return self.tabela.find_one({'nome': nome})

    def deletar(self, nome):
        return self.tabela.delete_one({'nome': nome})


class UsuarioDao:
    def __init__(self, tabela):
        self.tabela = tabela

    def busca_por_id(self, id):
        return self.tabela.find_one({'id': id})
