# TODO: Similarity score and missing keywords

from sentence_transformers import SentenceTransformer
from transformers import pipeline
import torch
import spacy
 

model=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
nlp=spacy.load("en_core_web_sm")
# tokenizer=AutoTokenizer.from_pretrained("distilgpt2")
# model_gpt=AutoModelForCausalLM.from_pretrained("distilgpt2")
generator=pipeline("text-generation",model="gpt2")

def matching_score(job_description,resume_text):
    text1_embedding = model.encode(job_description,convert_to_tensor=True)
    text2_embedding = model.encode(resume_text,convert_to_tensor=True)
    cosine_similarities = torch.nn.functional.cosine_similarity(text1_embedding.unsqueeze(0),text2_embedding.unsqueeze(0))
    print(cosine_similarities.item())
    return cosine_similarities.item()

def missing_keywords(job_description,resume_text):
    text1_doc=nlp(job_description)
    text2_doc=nlp(resume_text)
    job_keywords=set()
    resume_keywords=set()
    for token1 in text1_doc:
        if (token1.pos_=="PROPN" or token1.pos_=="NOUN" or token1.pos_=="VERB"):
            token1_lower=token1.lemma_.lower()
            if token1_lower not in job_keywords:
                job_keywords.add(token1_lower)
    for token2 in text2_doc:
        if (token2.pos_=="PROPN" or token2.pos_=="NOUN" or token2.pos_=="VERB"):
            token2_lower=token2.lemma_.lower()
            if token2_lower not in resume_keywords:
                resume_keywords.add(token2_lower)
    missing_keywords=job_keywords-resume_keywords
    return missing_keywords

def suggestion(job_description,resume_text):
    skills=[]
    actions=[]
    skills_suggestions=[]
    actions_suggestions=[]

    missing=missing_keywords(job_description,resume_text)
    print("DEBUG Missing Keywords: ", missing)
    for word in missing:
        doc=nlp(word)
        token=doc[0]
        if token.pos_ == "VERB":
            actions.append(token.text)
        elif token.pos_ == "PROPN":
            skills.append(token.text)
    
    skills=skills[:2]
    actions=actions[:2]

    for skill in skills:
        prompt=f"Give a resume suggestion sentence highlighting the skill '{skill}' for this job: {job_description}"
        result=generator(prompt, max_new_tokens=150, num_return_sequences=1)[0]["generated_text"]
        skills_suggestions.append(result.split("\n")[0])
    for action in actions:
        prompt=f"Give a resume suggestion sentence using the action '{action}' for this job: {job_description}"
        result=generator(prompt, max_new_tokens=150, num_return_sequences=1)[0]["generated_text"]
        actions_suggestions.append(result.split("\n")[0])

    return skills_suggestions,actions_suggestions,missing
        