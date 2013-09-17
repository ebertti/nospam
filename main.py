# coding: utf-8
import configuracao
from separar import Separar


def main():
    separar = Separar(
        configuracao.DATASET_COMPLETO,
        configuracao.DATASET_TREINO,
    )
    separar.rodar()



if __name__ == '__main__':
    main()