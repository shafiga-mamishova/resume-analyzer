# TODO: Similarity score and missing keywords

from sentence_transformers import SentenceTransformer
import torch
import spacy

model=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
nlp=spacy.load("en_core_web_sm")

def matching_score(text1,text2):
    text1_embedding = model.encode(text1,convert_to_tensor=True)
    text2_embedding = model.encode(text2,convert_to_tensor=True)
    cosine_similarities = torch.nn.functional.cosine_similarity(text1_embedding.unsqueeze(0),text2_embedding.unsqueeze(0))
    print(cosine_similarities.item())
    return cosine_similarities.item()

def missing_keywords(text1,text2):
    text1_doc=nlp(text1)
    text2_doc=nlp(text2)
    job_keywords=set()
    resume_keywords=set()
    for token1 in text1_doc:
        if (token1.pos_=="PROPN" or token1.pos_=="NOUN" or token1.pos_=="VERB"):
            token1_lower=token1.text.lower()
            if token1_lower not in job_keywords:
                job_keywords.add(token1_lower)
    for token2 in text2_doc:
        if (token2.pos_=="PROPN" or token2.pos_=="NOUN" or token2.pos_=="VERB"):
            token2_lower=token2.text.lower()
            if token2_lower not in resume_keywords:
                resume_keywords.add(token2_lower)
    missing_keywords=job_keywords-resume_keywords
    return missing_keywords

    