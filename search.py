import json
from sklearn.neighbors import NearestNeighbors
import pandas as pd
from transformers import AutoTokenizer,AutoModel
import torch

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

embeds = pd.read_csv('embeddings.csv')
nbrs = NearestNeighbors(n_neighbors = 3, algorithm = 'ball_tree').fit(embeds.values)

def ask(pergunta):
    if not pergunta:
        return []
    enc = embed([pergunta])
    distances,indices = nbrs.kneighbors(enc)
    return [parags[i] for i in indices[0]]