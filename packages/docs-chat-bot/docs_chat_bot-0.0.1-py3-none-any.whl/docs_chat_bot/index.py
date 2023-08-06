import os
import time
import pickle
import numpy as np
import openai
import pandas as pd

EMBEDDING_MODEL = "text-embedding-ada-002"

def get_embedding(text: str, model: str=EMBEDDING_MODEL) -> list[float]:
    result = openai.Embedding.create(
      model=model,
      input=text
    )
    return result["data"][0]["embedding"]

openai.api_key = os.environ['openai_api_key']

tunks = []

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.codon'):
            with open(os.path.join(root, file), 'r') as f:
                code = f.read()
                tunks.append(code)
        elif file.endswith('.md'):
            with open(os.path.join(root, file), 'r') as f:
                code = f.read()
                pieces = code.split(' '*100+'\n')
                for piece in pieces:
                    tunks.append(piece.strip())

embeddings = {}
progress = 0
start = time.time()
for tunk in tunks:
    progress += 1
    if time.time() - start > 1:
        start = time.time()
        print(f'progress: %.2f%%' % (progress / len(tunks) * 100), end='\r')
    embedding = get_embedding(tunk)
    embeddings[tunk] = embedding

with open('embeddings.pickle', 'wb') as f:
    pickle.dump(embeddings, f)
