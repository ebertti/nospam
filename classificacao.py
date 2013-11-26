# coding=utf-8
import csv
import logging
import os
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import configuracao

logger = logging.getLogger()


class Classificar(object):
    pass


class Classificacao(object):

    def rodar(self, idioma, matriz=False):
        preparado_caminho = os.path.join(configuracao.DATASET_PREPARADO, idioma + '.csv')
        comentarios = []
        ehspam = []
        logger.info("abrindo arquivo")

        with open(preparado_caminho, 'r') as preparado_origem:
            leitor = csv.reader(preparado_origem)
            for linha in leitor:
                comentarios.append(linha[5].decode('utf-8'))
                ehspam.append(linha[6] == "True")

        comentarios_treino, comentarios_teste, ehspam_treino, ehspam_teste = train_test_split(comentarios, ehspam, train_size=0.5, test_size=0.5)

        treino = Classificar()

        treino.data = comentarios_treino
        treino.target = ehspam_treino
        treino.target_names = (True, False)

        teste = Classificar()
        teste.data = comentarios_teste
        teste.target = ehspam_teste
        teste.target_names = (True, False)

        if matriz:
            logger.info("Criando Matriz")
            vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5)
            treino.data = vectorizer.fit_transform(treino.data)
            logger.info("Matriz de treino criada")

            teste.data = vectorizer.transform(teste.data)
            logger.info("Matriz de teste criada")

        return treino, teste




