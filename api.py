import numpy as np
from fastapi import FastAPI, Request, HTTPException
from pymilvus.model.hybrid import BGEM3EmbeddingFunction

import utils

app = FastAPI()

bge_m3_ef = BGEM3EmbeddingFunction(
    model_name = 'bge-m3',
    device = 'cpu', # Specify the device to use, e.g., 'cpu' or 'cuda:0'
    use_fp16 = False # Specify whether to use fp16. Set to `False` if `device` is `cpu`.
)

@app.post("/embeddings")
async def generate_embeddings(request: Request):
    try:
        json_post = await request.json()
        strings = json_post["strings"]
        embeddings = utils.get_embedding(bge_m3_ef, strings)
        embeddings = np.array(embeddings).tolist()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"vectors": embeddings}
