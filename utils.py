from typing import List

def get_embedding(model, texts: List[str]):
    text_embeddings = model.encode_documents(texts)
    text_embeddings_dense = text_embeddings['dense']
    return text_embeddings_dense
