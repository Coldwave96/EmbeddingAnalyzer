import numpy as np
from typing import List
from pymilvus import MilvusClient, DataType

def get_embedding(model, texts: List[str]):
    text_embeddings = model.encode_documents(texts)
    text_embeddings_dense = text_embeddings['dense']
    embeddings = np.array(text_embeddings_dense).tolist()
    return embeddings

def create_collection(milvus_client, name_list):
    for collection_name in name_list:
        if not milvus_client.has_collection(collection_name):
            schema = MilvusClient.create_schema(auto_id=True, enable_dynamic_field=False)
            schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
            schema.add_field(field_name="string", datatype=DataType.VARCHAR, max_length=8192)
            schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=1024)
            schema.add_field(field_name="account", datatype=DataType.VARCHAR, max_length=128)
            schema.add_field(field_name="label", datatype=DataType.VARCHAR, max_length=128)
            schema.add_field(field_name="time", datatype=DataType.INT64)

            milvus_client.create_collection(collection_name=collection_name, schema=schema)
