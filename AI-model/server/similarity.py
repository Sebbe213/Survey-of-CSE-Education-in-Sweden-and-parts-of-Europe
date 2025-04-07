import numpy as np


def cosine_similarity(a,b):
    vec1, vec2 = np.array(a), np.array(b)
    vec1_normalised, vec2_normalised = np.linalg.norm(vec1), np.linalg.norm(vec2)
    dot_product = np.dot(vec1, vec2)

    similarity = dot_product / (vec1_normalised * vec2_normalised)
    return similarity


