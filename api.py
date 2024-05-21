import os
import time
from fastapi import FastAPI, Request, HTTPException
from pymilvus.model.hybrid import BGEM3EmbeddingFunction
from pymilvus import MilvusClient

import utils

device = os.environ.get('DEVICE', 'cpu')
milvus_uri = os.environ.get('MILVUS_URI', "http://192.168.89.129:19530")
name_list = os.environ.get("NAME_LIST", ["command", "url", "payload"])

app = FastAPI()

bge_m3_ef = BGEM3EmbeddingFunction(
    model_name = 'bge-m3',
    device = device, # Specify the device to use, e.g., 'cpu' or 'cuda:0'
    use_fp16 = (lambda d: d != 'cpu')(device) # Specify whether to use fp16. Set to `False` if `device` is `cpu`.
)

@app.post("/embeddings")
async def generate_embeddings(request: Request):
    try:
        json_post = await request.json()
        strings = json_post["strings"]
        embeddings = utils.get_embedding(bge_m3_ef, strings)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"vectors": embeddings}

client = MilvusClient(milvus_uri)
utils.init_collection(client, name_list)

@app.post("/insert")
async def insert(request: Request):
    try:
        json_post = await request.json()
        collention_name = json_post["type"]
        id = json_post["id"]
        string = json_post["string"]
        account = json_post["account"]
        label = json_post["label"]
        vector = utils.get_embedding(bge_m3_ef, [string])[0]
            
        res = client.insert(
            collection_name = collention_name,
            data = {
                'id': id,
                'string': string,
                'vector': vector,
                'account': account,
                'label': label,
                'time': int(time.time())
            }
        )
        ids = int(res['ids'][0])
        client.refresh_load(collection_name=collention_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {'ids': ids}

@app.post("/search")
async def search(request: Request):
    try:
        json_post = await request.json()
        collection_name = json_post["type"]
        strings = json_post["strings"]
        limit = json_post["limit"]
        vector = utils.get_embedding(bge_m3_ef, strings)

        search_params = {
            "metric_type": "COSINE",
            "params": {}
        }

        res = client.search(
            collection_name = collection_name,
            data = vector,
            limit = limit,
            output_fields = ['id', 'string', 'account', 'label', 'time'],
            search_params = search_params
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return res

@app.post("/upsert")
async def upsert(request: Request):
    try:
        json_post = await request.json()
        collection_name = json_post["type"]
        id = json_post["id"]
        string = json_post["string"]
        account = json_post["account"]
        label = json_post["label"]
        vector = utils.get_embedding(bge_m3_ef, [string])[0]

        res = client.upsert(
            collection_name = collection_name,
            data = {
                "id": id,
                "string": string,
                "vector": vector,
                "account": account,
                "label": label,
                "time": int(time.time())
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return res

@app.post("/delete")
async def delete(request: Request):
    try:
        json_post = await request.json()
        collection_name = json_post["type"]
        ids = json_post["ids"]

        res = client.delete(
            collection_name = collection_name,
            ids = ids
        )
    except Exception as e:
        raise HTTPException(status_code=500)
    return res
