# coding: utf-8
import os
from contator import Contadores
import langid


class Separar(object):

    def __init__(self, arquivo_origem, pasta_destino, tamanho=1000):
        self.arquivo_origem = arquivo_origem
        self.pasta_destino = pasta_destino
        self.tamanho = tamanho
        self.contador = Contadores()
        self.arquivos_destino = {}


    def rodar(self):
        with open(self.arquivo_origem, 'r') as stream_origem:
            linha = stream_origem.readline()
            while linha:
                if self.contador.qtd < self.tamanho:
                    texto = linha.split(',')[3]
                    com_link = self.tem_link(texto)
                    idioma = langid.classify(texto)[0]
                    stream_destino = self.stream_destino(idioma)
                    stream_destino.write(idioma + ',' + str(com_link) + ',' + linha)
                    self.contador.mais_um(idioma, com_link)
                    linha = stream_origem.readline()
                else:
                    break

        self.finalizar()

    def tem_link(self, texto):
        return "?v=" in texto

    def stream_destino(self, idioma):
        if idioma not in self.arquivos_destino:
            arquivo_destino = os.path.join(self.pasta_destino, idioma + '.csv')
            self.arquivos_destino[idioma] = open(arquivo_destino, 'w')
        return self.arquivos_destino[idioma]

    def finalizar(self):
        for stream in self.arquivos_destino.values():
            stream.close()
