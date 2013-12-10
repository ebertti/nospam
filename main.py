# coding: utf-8
import logging
import scipy
from sklearn import metrics, svm, linear_model, naive_bayes, pipeline, grid_search
from classificacao import Classificacao
from classificacao_crua import ClassificacaoCrua
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
    logger.info("_" * 30 + 'NOVA RODADA' + "_" * 30)
    separar = Separar(
        configuracao.DATASET_COMPLETO,
        configuracao.DATASET_TREINO,
    )
    #separar.rodar()

    classificar = Classificacao()
    treino, teste = classificar.rodar('es', matriz=True,)

    logger.debug("dados carregados")

    #best_score(treino)

    for algoritimo in (
        linear_model.SGDClassifier(),
        linear_model.Perceptron(),
        svm.LinearSVC(),
    ):
        benchmark(algoritimo, treino, teste)

    logger.debug("Finalizou")


def best_score(treino):
    tuned_parameters = {
        'loss': ['hinge'],
        'power_t': scipy.stats.expon(scale=.01),
    }

    clf = grid_search.RandomizedSearchCV(linear_model.SGDClassifier(), tuned_parameters, scoring='accuracy', n_iter=50)
    clf.fit(treino.data, treino.target)
    print(clf.best_estimator_)
    for params, mean_score, scores in sorted(clf.grid_scores_, key=lambda x: x[1]):
        print("%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std() / 2, params))

    exit()



def benchmark(clf, treino, teste):
    logger.info('ALGORITMO: %s', clf)
    logger.info("DATASET: treino: %d, teste:%d n_features: %d", treino.data.shape[0], teste.data.shape[0], teste.data.shape[1])
    t0 = time()
    clf.fit(treino.data, treino.target)
    train_time = time() - t0
    t0 = time()
    pred = clf.predict(teste.data)
    test_time = time() - t0
    logger.info("TEMPO: treino: %0.3fs teste: %0.3fs", train_time, test_time)
    for metric_method in ('accuracy_score', 'precision_score', 'recall_score', 'f1_score', 'confusion_matrix',):
        score = getattr(metrics, metric_method)(teste.target, pred)
        logger.info("%s: %s", metric_method, score)

if __name__ == '__main__':
    #preparar.apagar_temporarios(configuracao.DATASET_TREINO)
    preparar.log(configuracao.LOGGING)
    main()