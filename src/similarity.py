# TODO: Similarity score and missing keywords

from sentence_transformers import SentenceTransformer
import torch

model=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def matching_score(text1,text2):
    text1_embedding = model.encode(text1,convert_to_tensor=True)
    text2_embedding = model.encode(text2,convert_to_tensor=True)
    cosine_similarities = torch.nn.functional.cosine_similarity(text1_embedding.unsqueeze(0),text2_embedding.unsqueeze(0))
    print(cosine_similarities.item())
    return cosine_similarities.item()