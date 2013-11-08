# coding=utf-8
import socket
import json
import logging
import configuracao
logger = logging.getLogger()


class Contadores(object):

    def __init__(self):
        self.idiomas = {}
        self.com_link = 0
        self.sem_link = 0
        # Porta que o Servidor esta
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        destino = (configuracao.HOST_MONITOR, configuracao.HOST_PORTA)
        try:
            self.tcp.connect(destino)
            self.conectado = True
        except:
            self.conectado = False

    @property
    def qtd(self):
        return self.com_link + self.sem_link

    def mais_um(self, idioma, com_link):
        if idioma not in self.idiomas:
            self.idiomas[idioma] = Contador(idioma)
        self.idiomas[idioma].mais_um(com_link)
        if com_link:
            self.com_link += 1
        else:
            self.sem_link += 1

        if self.qtd % 50000 == 0:
            logger.debug(self)

        if self.conectado:
            self.tcp.send(json.dumps({'idioma': idioma, 'com_link':com_link}))


    def __str__(self):
        return "%s idiomas:%s qtd:%s com_link:%s sem_link:%s\n\t%s" % (
            'conectado' if self.conectado else 'erro',
            len(self.idiomas), self.qtd, self.com_link, self.sem_link,
            '\n\t'.join([str(contador) for contador in self.idiomas.values()])
        )

    def __int__(self):
        return self.qtd

    def finalizar(self):
        self.tcp.close()

class Contador(object):

    def __init__(self, idioma):
        self.idioma = idioma
        self.com_link = 0
        self.sem_link = 0

    @property
    def qtd(self):
        return self.com_link + self.sem_link

    def mais_um(self, com_link):
        if com_link:
            self.com_link += 1
        else:
            self.sem_link += 1

    def __str__(self):
        return "idioma:%s qtd:%s com_link:%s sem_link:%s" % (self.idioma, self.qtd, self.com_link, self.sem_link)