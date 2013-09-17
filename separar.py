# coding: utf-8

class Separar(object):

    def __init__(self, arquivo_origem, arquivo_destino, tamanho=1000):
        self.arquivo_origem = arquivo_origem
        self.arquivo_destino = arquivo_destino
        self.tamanho = tamanho

    def rodar(self):
        qtd = 0
        with open(self.arquivo_origem, 'r') as stream_origem, \
             open(self.arquivo_destino, 'w') as stream_destino :
            linha = stream_origem.readline()
            while linha:
                if qtd < self.tamanho:
                    stream_destino.write(linha)
                    qtd += 1
                    linha = stream_origem.readline()
                else:
                    break
