# coding=utf-8
import csv
import logging
import os
import re
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction import text
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
import configuracao

logger = logging.getLogger()

stopwords = u"""
a
à
adeus
agora
aí
ainda
além
algo
algumas
alguns
ali
ano
anos
antes
ao
aos
apenas
apoio
após
aquela
aquelas
aquele
aqueles
aqui
aquilo
área
as
às
assim
até
atrás
através
baixo
bastante
bem
bom
breve
cá
cada
catorze
cedo
cento
certamente
certeza
cima
cinco
coisa
com
como
conselho
contra
custa
da
dá
dão
daquela
daquele
dar
das
de
debaixo
demais
dentro
depois
desde
dessa
desse
desta
deste
deve
deverá
dez
dezanove
dezasseis
dezassete
dezoito
dia
diante
diz
dizem
dizer
do
dois
dos
doze
duas
dúvida
e
é
ela
elas
ele
eles
em
embora
entre
era
és
essa
essas
esse
esses
esta
está
estar
estas
estás
estava
este
estes
esteve
estive
estivemos
estiveram
estiveste
estivestes
estou
eu
exemplo
faço
falta
favor
faz
fazeis
fazem
fazemos
fazer
fazes
fez
fim
final
foi
fomos
for
foram
forma
foste
fostes
fui
geral
grande
grandes
grupo
há
hoje
horas
isso
isto
já
lá
lado
local
logo
longe
lugar
maior
maioria
mais
mal
mas
máximo
me
meio
menor
menos
mês
meses
meu
meus
mil
minha
minhas
momento
muito
muitos
na
nada
não
naquela
naquele
nas
nem
nenhuma
nessa
nesse
nesta
neste
nível
no
noite
nome
nos
nós
nossa
nossas
nosso
nossos
nova
nove
novo
novos
num
numa
número
nunca
o
obra
obrigada
obrigado
oitava
oitavo
oito
onde
ontem
onze
os
ou
outra
outras
outro
outros
para
parece
parte
partir
pela
pelas
pelo
pelos
perto
pode
pôde
podem
poder
põe
põem
ponto
pontos
por
porque
porquê
posição
possível
possivelmente
posso
pouca
pouco
primeira
primeiro
próprio
próximo
puderam
qual
quando
quanto
quarta
quarto
quatro
que
quê
quem
quer
quero
questão
quinta
quinto
quinze
relação
sabe
são
se
segunda
segundo
sei
seis
sem
sempre
ser
seria
sete
sétima
sétimo
seu
seus
sexta
sexto
sim
sistema
sob
sobre
sois
somos
sou
sua
suas
tal
talvez
também
tanto
tão
tarde
te
tem
têm
temos
tendes
tenho
tens
ter
terceira
terceiro
teu
teus
teve
tive
tivemos
tiveram
tiveste
tivestes
toda
todas
todo
todos
trabalho
três
treze
tu
tua
tuas
tudo
um
uma
umas
uns
vai
vais
vão
vários
vem
vêm
vens
ver
vez
vezes
viagem
vindo
vinte
você
vocês
vos
vós
vossa
vossas
vosso
vossos
zero""".split('\n')
stopwords = set([text.strip_accents_ascii(w) for w in stopwords])

class Classificar(object):
    pass

import hashlib
class Classificacao(object):

    def rodar(self, idioma, matriz=False, balancear=False):
        preparado_caminho = os.path.join(configuracao.DATASET_PREPARADO, idioma + '.csv')
        tuplas_ehspam = []
        tuplas_nao_ehspam = []
        comentarios = []
        ehspam = []
        logger.debug("abrindo arquivo")

        set_spam = set()
        with open(preparado_caminho, 'r') as preparado_origem:
            leitor = csv.reader(preparado_origem)
            for linha in leitor:
                if linha[6] == "True":
                    tuplas_ehspam.append(linha[5])
                    set_spam.add(hashlib.md5(linha[5]).hexdigest())
                else:
                    tuplas_nao_ehspam.append(linha[5])

            remover = []

            for comentario in tuplas_nao_ehspam:
                if hashlib.md5(comentario).hexdigest() in set_spam:
                    remover.append(comentario)

            logger.info('spans nao marcados: %s', len(remover))
            for comentario in remover:
                tuplas_nao_ehspam.remove(comentario)
                tuplas_ehspam.append(comentario)

        qtd = len(tuplas_ehspam)
        if balancear:
            ehspam = [True for i in range(qtd)] + [False for i in range(qtd)]
            comentarios = tuplas_ehspam + tuplas_nao_ehspam[0:qtd]
        else:
            ehspam = [True for i in range(qtd)] + [False for i in range(len(tuplas_nao_ehspam))]
            comentarios = tuplas_ehspam + tuplas_nao_ehspam

        del tuplas_ehspam
        del tuplas_nao_ehspam

        logger.debug("separando bases")
        comentarios_treino, comentarios_teste, ehspam_treino, ehspam_teste = train_test_split(comentarios, ehspam, train_size=0.8, test_size=0.2)
        logger.debug("Bases separadas")
        treino = Classificar()

        treino.data = comentarios_treino
        treino.target = ehspam_treino
        treino.target_names = (True, False)

        teste = Classificar()
        teste.data = comentarios_teste
        teste.target = ehspam_teste
        teste.target_names = (True, False)

        if matriz:
            logger.debug("Criando Matriz")
            vectorizer = text.TfidfVectorizer(
                 strip_accents='ascii',
                 stop_words=stopwords,
                 tokenizer=tokanaizer,
                 lowercase=True,
                 min_df=3,
            )
            treino.data = vectorizer.fit_transform(treino.data)
            logger.debug("Matriz de treino criada")

            teste.data = vectorizer.transform(teste.data)
            logger.debug("Matriz de teste criada")

        return treino, teste



token_pattern = re.compile(r'(?u)\b\w\w+\b')
def tokanaizer(texto):

    palavras = token_pattern.findall(texto)
    novas_palavras = []
    for palavra in palavras:
        if 'user' in palavra:
            palavra = u'UUUUUUUUUUUUUUSER'
        elif palavra.isnumeric():
            palavra = u'NNNNNNNNNNNNUMBER'
        if palavra[-1] == palavra[-2]:
            ultima = 99
            for i in range(len(palavra) - 1, 0, -1):
                if palavra[-1] != palavra[i]:
                    ultima = i
                    break
            palavra = palavra[:ultima]
        novas_palavras.append(palavra)

    if "?v=" in texto:
        novas_palavras.append(u'LLLLLLLLLLLLLLINK')

    return novas_palavras