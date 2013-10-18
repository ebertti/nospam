# coding: utf-8
import os

PROJECT_DIR = os.path.dirname(__file__)

DATASET_COMPLETO = os.path.join(PROJECT_DIR, 'dataset/completo/youtube_comments_20120117.csv')
DATASET_TREINO = os.path.join(PROJECT_DIR, 'dataset/treino/')

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
    },

    'root': {
        'handlers': ['default'],
        'level': 'NOTSET',
        'propagate': True
    }
}