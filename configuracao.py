# coding: utf-8
import os

PROJECT_DIR = os.path.dirname(__file__)

DATASET_COMPLETO = os.path.join(PROJECT_DIR, 'dataset/completo/youtube_comments_20120117.csv')
DATASET_TREINO = os.path.join(PROJECT_DIR, 'dataset/treino/')
DATASET_PREPARADO = os.path.join(PROJECT_DIR, 'dataset/preparado/')

HOST_MONITOR = 'localhost'
HOST_PORTA = 8124

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # this fixes the problem
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'NOTSET',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'arquivo': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': "logfile.log",
        },
    },

    'root': {
        'handlers': ['default', 'arquivo'],
        'level': 'NOTSET',
        'propagate': True
    }
}