# coding: utf-8
import logging
import configuracao
import preparar
from separar import Separar

logger = logging.getLogger()

def main():
    logger.info("iniciando")
    separar = Separar(
        configuracao.DATASET_COMPLETO,
        configuracao.DATASET_TREINO,
    )
    separar.rodar()
    logger.info("Finalizou")


if __name__ == '__main__':
    preparar.apagar_temporarios(configuracao.DATASET_TREINO)
    preparar.log(configuracao.LOGGING)
    main()