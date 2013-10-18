# coding: utf-8
import os
import glob
import logging
import logging.config


def log(log_config):
    logging.config.dictConfig(log_config)
    logger = logging.getLogger()
    logger.debug('Log configurado')


def apagar_temporarios(pasta):
    arquivos = glob.glob(pasta + '*')
    for arquivo in arquivos:
        if '.existo' not in arquivo:
            os.remove(arquivo)