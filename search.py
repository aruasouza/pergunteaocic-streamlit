import json
from sklearn.neighbors import NearestNeighbors
import pandas as pd
from transformers import AutoTokenizer,AutoModel
import torch
import re

tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
model = AutoModel.from_pretrained('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

def mean_pooling(model_output,attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def embed(sentences):
    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
    return sentence_embeddings.numpy()

with open('catecismo.json','r',encoding = 'utf-8') as f:
    parags = list(json.load(f).values())

with open('catpio.json','r',encoding = 'utf-8') as f:
    qea = json.load(f)
    respostas = list(qea.values())
    perguntas = list(qea.keys())

embeds = pd.read_csv('embeddings.csv')
nbrs = NearestNeighbors(n_neighbors = 3, algorithm = 'ball_tree').fit(embeds.values)

pio_embeds = pd.read_csv('pio_embeddings.csv')
nbrs_pio = NearestNeighbors(n_neighbors = 1, algorithm = 'ball_tree').fit(pio_embeds.values)

def ask(pergunta):
    if not pergunta:
        return '',[]
    perg = re.sub(r'[^a-z0-9\sáéíóúâêôãõàç-]','',pergunta.lower()).replace('-',' ')
    enc = embed([perg])
    distances,indices = nbrs.kneighbors(enc)
    trechos = [parags[i] for i in indices[0]]
    return ask_pio(enc),trechos

def ask_pio(enc):
    distances,indices = nbrs_pio.kneighbors(enc)
    print(perguntas[indices[0][0]])
    if distances[0][0] <= 2.5:
        return respostas[indices[0][0]]
    return ''