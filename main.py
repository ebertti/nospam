# coding: utf-8
import logging
from sklearn import metrics, svm
from classificacao import Classificacao
import configuracao
import preparar
from separar import Separar
from time import time

logger = logging.getLogger()

class L1LinearSVC(svm.LinearSVC):

    def fit(self, X, y):
        # The smaller C, the stronger the regularization.
        # The more regularization, the more sparsity.
        self.transformer_ = svm.LinearSVC(penalty="l1",
                                      dual=False, tol=1e-3)
        X = self.transformer_.fit_transform(X, y)
        return svm.LinearSVC.fit(self, X, y)

    def predict(self, X):
        X = self.transformer_.transform(X)
        return svm.LinearSVC.predict(self, X)

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

    algoritimo = svm.LinearSVC()
    benchmark(algoritimo, treino, teste)


    logger.info("Finalizou")



def benchmark(clf, treino, teste):
    print('_' * 80)
    print("Training: ")
    print(clf)
    print("treino n_samples: %d, n_features: %d" % treino.data.shape)
    print("teste n_samples: %d, n_features: %d" % teste.data.shape)
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