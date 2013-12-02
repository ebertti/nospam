# coding=utf-8
import os
import glob
import configuracao


def main():
    for arquivo in glob.glob(configuracao.DATASET_PREPARADO + '/*.csv'):
        linhas = 0
        spam = 0
        with open(arquivo, 'r') as arquivo_aberto:
            tupla = arquivo_aberto.readline()
            while tupla:
                linhas += 1
                if str(tupla).endswith('True"\n'):
                    spam += 1
                tupla = arquivo_aberto.readline()
        print os.path.basename(arquivo)[:2] + ',' + str(linhas) + ',' + str(spam)

if __name__ == "__main__":
    main()