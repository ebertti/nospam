# coding=utf-8
import csv
import logging
import os
import re
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction import text
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
import configuracao

logger = logging.getLogger()

class Classificar(object):
    pass


class ClassificacaoCrua(object):

    def rodar(self, matriz=False, balancear=False):
        preparado_caminho = os.path.join(configuracao.DATASET_COMPLETO)
        tuplas_ehspam = []
        tuplas_nao_ehspam = []
        comentarios = []
        ehspam = []
        logger.debug("abrindo arquivo")

        with open(preparado_caminho, 'r') as preparado_origem:
            leitor = csv.reader(preparado_origem)
            for linha in leitor:
                if linha[4] == "True":
                    tuplas_ehspam.append(linha[3].decode('utf-8'))
                else:
                    tuplas_nao_ehspam.append(linha[3].decode('utf-8'))
                if len(tuplas_ehspam) + len(tuplas_nao_ehspam ) == 100000:
                    break

        qtd = len(tuplas_ehspam)
        if balancear:
            ehspam = [True for i in range(qtd)] + [False for i in range(qtd)]
            comentarios = tuplas_ehspam + tuplas_nao_ehspam[0:qtd]
        else:
            ehspam = [True for i in range(qtd)] + [False for i in range(len(tuplas_nao_ehspam))]
            comentarios = tuplas_ehspam + tuplas_nao_ehspam

        del tuplas_ehspam
        del tuplas_nao_ehspam

        logger.debug("separando bases")
        comentarios_treino, comentarios_teste, ehspam_treino, ehspam_teste = train_test_split(comentarios, ehspam, train_size=0.5, test_size=0.5)
        logger.debug("Bases separadas")
        treino = Classificar()

        treino.data = comentarios_treino
        treino.target = ehspam_treino
        treino.target_names = (True, False)

        teste = Classificar()
        teste.data = comentarios_teste
        teste.target = ehspam_teste
        teste.target_names = (True, False)

        if matriz:
            logger.debug("Criando Matriz")
            vectorizer = text.TfidfVectorizer(
            )
            treino.data = vectorizer.fit_transform(treino.data)
            logger.debug("Matriz de treino criada")

            teste.data = vectorizer.transform(teste.data)
            logger.debug("Matriz de teste criada")

        return treino, teste



token_pattern = re.compile(r'(?u)\b\w\w+\b')
def tokanaizer(texto):

    palavras = token_pattern.findall(texto)
    novas_palavras = []
    for palavra in palavras:
        if 'user' in palavra:
            palavra = u'UUUUUUUUUUUUUUSER'
        elif palavra.isnumeric():
            palavra = u'NNNNNNNNNNNNUMBER'
        if palavra[-1] == palavra[-2]:
            ultima = 99
            for i in range(len(palavra) - 1, 0, -1):
                if palavra[-1] != palavra[i]:
                    ultima = i
                    break
            palavra = palavra[:ultima]
        novas_palavras.append(palavra)

    if "?v=" in texto:
        novas_palavras.append(u'LLLLLLLLLLLLLLINK')

    return novas_palavras