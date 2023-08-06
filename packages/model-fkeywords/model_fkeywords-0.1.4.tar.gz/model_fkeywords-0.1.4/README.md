# Model of Find KeyWords In Text

[![CircleCI](https://circleci.com/gh/EneasJr-Rodrigues/model_fkeywords.svg?style=svg&circle-token=616f1a5503dbf230d7aa84a7bfd60e9cb166c834)](https://app.circleci.com/pipelines/github/EneasJr-Rodrigues/model_fkeywords)
[![Python required version: 3.8.10](https://img.shields.io/badge/python-3.8.10-blue.svg?style=flat-square)](https://www.python.org/downloads/release/python-3810)
[![pre-commit](https://img.shields.io/badge/pre--commit-disabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This project was created by the [Eneas Rodrigues](https://github.com/EneasJr-Rodrigues).
Contact them for instruction on how to build, run and test it.
This project generates wheel file, and allows installation in other IDE or Google Colab
The project's internal directories have a Python notebook to use for testing.

## Install Model of API

```shell

Install:
pip install model-fkeywords

```


## Basic Usage

* Step_1: import a class
  
```shell

from api_model.nlsuper import NlExtractorProcess ## using to clean text
from api_model.nlvisualization import NlVisualization ## libs of data visualization (metplotlib and seaborn)

```

* Step_2: declare variables using the exemple:

```shell

filename = 'results_100_call' ## file name
prefix = 'csv' ## extension of file
prefix_sep = ',' ## delimitator
column_text = 'TEXT' ## column to process data
whats_process = 'complete' ## kind of process
# whats_process = 'partial'
# whats_process = 'only_keywords'
id_database = 'ID' ## id of database
type_find = 'aproximado' ## kind of find words (aproximado = synonyms or close words or fixo = words fix)
activate_stopwords = 'sim' ## não if you want to use stopwords in your process
encoding = 'UTF-8' ## UTF-8 encoding of file exemple UTF-8 or ANSI

```

* whats_process: explanation

```shell
##### Description of process
        whats_process = 'complete'
            return: process all pipeline
        whats_process = 'partial'
            return: findkeywords and process bigrams
        whats_process = 'only_keywords'
            return: findkeywords  
```

* Step_3: Creation of json format (column and text) to want find in the text
  
```shell
text_finds = {
    'negatividade': ['a desejar', 'abrir uma reclamacao', 'absurd', 'aguento mais', 'boceta', 'bosta', 'brigaram', 'buceta', 'burocra', 'cansad', 'caralho', 'conflito', 'constrang', 'decepcao', 'decepcionad', 'quanta demora', 'que demora', 'tentando resolver', 'descontent', 'descrenca', 'descrente', 'desrespeit', 'fdp', 'filha da ****', 'filha de uma ****', 'filho da ****', 'filho de uma ****', 'frustracao', 'frustrad', 'humilhacao', 'humilhad', 'ignorad', 'ignoram', 'incompet', 'inferno', 'informa nada', 'injuria', 'ironia', 'ironic', 'irreponsaveis', 'irresponsabilidade', 'irresponsavel', 'ma vontade', 'mal a pior', 'mal atendid', 'mal educad', 'mal respondem', 'mal tratad', 'mau atendid', 'mau educad', 'mau respondem', 'mau tratad', 'merda', 'nao podemos arcar', 'nao posso arcar', 'nao sabe', 'ninguem resolve', 'ofenderam', 'ofendid', 'orrivel', 'pelo amor de deus', 'pessimo', 'pessimu', 'porra', 'poxa', 'pqp', '**** que pariu', 'reclamacao', 'reclamar', 'ridicul', 'ruim', 'sabe nada', 'sem educacao', 'ta dificil', 'trata mal', 'trata mau', 'tratou mal', 'tratou mau', 'triste', 'vergonh', 'vagabund', 'raiva', 'detest', 'nao quero mais', 'odeio', 'safad', 'deus me livre', 'vergonh'],
    're****cao': ['advogad', 'consumidor.gov', 'entrar com processo', 'facebook', 'instagram', 'judiciais', 'judicial', 'justica', 'meu direito', 'meus direito', 'ouvidoria', 'pequenas causas', 'processar voces', 'procon', 'reclame aqui', 'reclameaqui', 'twitter'],
    'rechamada': ['ainda nao', 'alguma posicao', 'ate agora', 'ate o momento', 'atraso', 'chamado aberto', 'consigo resolver', 'contato novamente', 'continuo sem acesso', 'de novo', 'demora', 'desde ontem', 'desde semana', 'diversas vezes', 'duas vezes', 'em andamento', 'entrei em contato', 'era pra ter', 'faz um mes', 'faz uma semana', 'ja abri', 'ja enviei', 'ja liguei', 'ja mandei', 'liguei pra central', 'mesmo erro', 'muitas vezes', 'nao chegou', 'nao e a primeira vez', 'ocorrencia aberta', 'posicionamento', 'segunda vez', 'sem sucesso', 'tentativa', 'terceira vez', 'todo dia', 'varias vezes', 'chamado aberto'],
    'satisfacao': ['adorei', 'adoro', 'ageis', 'agil', 'agilidade', 'amei', 'atendimento perfeito', 'bem atendid', 'carisma', 'diferenciad', 'educad', 'eficacia', 'eficas', 'eficaz', 'elogiar', 'elogio', 'excelente atendimento', 'feliz', 'gostei', 'impecavel', 'me ajudou', 'merito', 'motivacao', 'motivad', 'muito 10', 'muito bom', 'muito dez', 'nota 10', 'nota dez', 'otimo atendimento', 'parabenizar', 'parabens', 'pela ajuda', 'personalizad', 'preparad', 'prestativ', 'profissional', 'qualidade', 'rapidez', 'resolveu', 'satisfacao', 'satisfatori', 'satisfeit', 'solucionou', 'ate que enfim', 'ate que em fim'],
    'concorrencia': ['ifood', 'caju', 'vee', 'flash', 'bem', 'up', 'VR', 'ticket', 'alelo', 'swile'],
    'contencao': ['desculpa', 'desculpe', 'sinto muito', 'desculpe a demora', 'lamento', 'lamentamos', 'perdoa', 'perdao', 'pelo ocorrido', 'o ocorrido', 'fique tranquil'],
    'ocorrencia': ['chamado', 'ocorrencia', 'registrada com sucesso'],
    'direcionamento': ['central de atedimento', 'ligar na central', 'somente na central', 'sodexo.com', 'ligue na central'],
    'pedefacil': ['clique no', 'clique em', 'menu servicos', 'do menu', 'pede facil', 'clica no', 'clica em', 'diretamente no site', 'visualizar em', 'no menu', 'menu'],
    'ativo': ['analista pode entrar em contato', 'o analista entrara em contato', 'para te auxiliar na proposta', 'solicitei o contato', 'deixe seu contato']

          }
```

* Step_4: optional: if you want to add new stopwords to remove of text
  
```shell
additional_stop_words = ['porque','bom','dia','tres','três','alo','alô']
```

* Step_5: adicional columns of formated

```shell
interlocutor = {'CANAL': ['LEFT', 'RIGHT']} ## column of separation (when use bigram and trigram)
response_time = 'STARTTIME' ## column to format datetime
format_data = '%d/%m/%Y %H:%M:%S|%d/%m/%Y %H:%M|%Y-%m-%d %H:%M:%S|%d-%m-%Y %H:%M|%d%m%Y %H:%M:%S|%d%b%Y:%H:%M:%S' # 03MAR2022:12:01:33
```

* Step_6: Using the function to process

```shell
df = NlExtractorProcess.call_process(filename, prefix, prefix_sep,\
                                     column_text, whats_process,\
                                     text_finds, id_database, type_find,\
                                     additional_stop_words, activate_stopwords,\
                                    interlocutor, response_time, format_data) ## Return to dataframe with results
```

## Data Visualization

* Step_1: Define variables from process to wordCloud

```shell
filename = 'results_100_call' ## Name of file
column_filter = '' ## optional if you want to filter some column to visualized in wordCloud
column_text = 'all_messages' ## column process / text
whats_process = 'trigram' ## kind of Ngram trigram or bigram
```

* Step_2: Function to WordCloud

```shell
NlVisualization.wordCloud_Topics(filename,column_filter,column_text,whats_process)
```

* Step_3: Function of Word Frequency:

```shell
NlVisualization.plot_10_most_common_words(filename,column_filter,column_text)
```

* Step_4: Function of Pareto Graph:

```shell
### parameters: filename = variable defined before, x = column process, y = column count to agroup data. title = title of graph, limite = limit of words in graph
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (46, 9)
NlVisualization.pareto_plot(filename, x='countent_bigram', y='count', title='Alias Pareto Distribution', limite=20)
```

* Step_4: plot semantic words

```shell
### parameters: filename = variable defined before, column_text = column_text, 'pagamento' = word semantic (it can be any words), 40 = numbers of words in graph, vector_size = size of vector words, min_count = words min of count, window = size of dimension graph
### it is a machine learning model (word2Vec)
NlVisualization.tsne_plot(filename, column_text, 'pagamento', 40, n_iter=300, vector_size=300, min_count=20, window=30)
```

* Step_5: plot a clustering model kmeans machine learning

```shell
### parameters: filename = variable defined before,
### column_text = column_text
### model kind of clustering
### max_k = number max of clusterized text (the function find the best number of clustering automatic)
### return: clst = model vectorized, 
### optimal_k = numbers of cluster finded
### df = dataframe with result
clst, optimal_k, df = NlVisualization.clustering_model(filename, column_text, model='kmeans', plot=True, max_k=20)
```

## Important

Have some notebooks with exemple to usage this project


## Usually Functios

* Cleaner
* Remove_special_characters
* Tokenizer
* Filter_stop_words
* Stemmer
* Lemmatizer
* NGrams
* Histogram (Word Frequency)
* Anonymizer
* Pattern Matching
* NER (Named Entity Recognition)
* Machine Learning Model unsupervised (Word2Vec and Kmeans) to cluster text

## Main Contributors (until Mai/2022)

* Eneas Rodrigues de Souza Junior - eneas.rodrigues25@gmail.com
