# coding: utf-8
import logging
from sklearn import svm, metrics
from classificacao import Classificacao
import configuracao
import preparar
from separar import Separar
from time import time

logger = logging.getLogger()

def main():
    logger.info("iniciando")
    separar = Separar(
        configuracao.DATASET_COMPLETO,
        configuracao.DATASET_TREINO,
    )
    #separar.rodar()

    classificar = Classificacao()
    treino, teste = classificar.rodar('pt', matriz=True)

    logger.info("dados carregados")

    algoritimo = svm.SVC(kernel='linear', gamma=10)
    benchmark(algoritimo, treino, teste)


    logger.info("Finalizou")



def benchmark(clf, treino, teste):
    print('_' * 80)
    print("Training: ")
    print(clf)
    t0 = time()
    clf.fit(treino.data, treino.target)
    train_time = time() - t0
    print("train time: %0.3fs" % train_time)

    t0 = time()
    pred = clf.predict(teste.data)
    test_time = time() - t0
    print("test time:  %0.3fs" % test_time)

    score = metrics.f1_score(teste.target, pred)
    print("f1-score:   %0.3f" % score)

    print()
    clf_descr = str(clf).split('(')[0]
    return clf_descr, score, train_time, test_time

if __name__ == '__main__':
    #preparar.apagar_temporarios(configuracao.DATASET_TREINO)
    preparar.log(configuracao.LOGGING)
    main()