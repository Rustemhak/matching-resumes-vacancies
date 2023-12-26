import torch
from sentence_transformers import SentenceTransformer, util


model_id = "cointegrated/rubert-tiny2"
model = SentenceTransformer(model_id)
model.load_state_dict(torch.load("model/last.pt", map_location=torch.device('cpu')))


def cosine_similarity(vacancy, cv):
    """
    Считает косинусное сходство между текстами вакансии и резюме
    Параметры:
    - vacancy: Текст вакансии.
    - cv: Текст резюме.
    """
    cv_emb = model.encode(cv, convert_to_tensor=True)
    vacancy_emb = model.encode(vacancy, convert_to_tensor=True)
    cosine_scores = util.cos_sim(cv_emb, vacancy_emb)
    return float(cosine_scores)
