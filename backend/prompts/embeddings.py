import numpy as np
import hashlib

def text_to_embedding(text: str, dim: int = 128):
    """
    Simple embedding function viewd in redit lol
    """
    vec = np.zeros(dim, dtype="float32")
    for word in text.lower().split():
        h = int(hashlib.md5(word.encode()).hexdigest(), 16)
        index = h % dim
        vec[index] += 1
    return vec
