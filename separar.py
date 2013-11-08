# coding: utf-8
import csv
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
            leitor = csv.reader(stream_origem)
            for linha in leitor:
                texto = linha[3]
                com_link = self.tem_link(texto)
                idioma = langid.classify(texto)[0]
                stream_destino = self.stream_destino(idioma)
                stream_destino.writerow([idioma, com_link] + linha)
                self.contador.mais_um(idioma, com_link)

        self.finalizar()

    def tem_link(self, texto):
        return "?v=" in texto

    def stream_destino(self, idioma):
        if idioma not in self.arquivos_destino:
            arquivo_destino = os.path.join(self.pasta_destino, idioma + '.csv')
            self.arquivos_destino[idioma] = csv.writer(
                open(arquivo_destino, 'w'),
                lineterminator='\n',
                quoting=csv.QUOTE_ALL,
            )
        return self.arquivos_destino[idioma]

    def finalizar(self):
        for stream in self.arquivos_destino.values():
            stream.close()
