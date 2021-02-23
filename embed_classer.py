import gensim 
import numpy as np


class embed(object):
    def __init__(self, path):
        self.path = path
        self._load_model()
        
    def _load_model(self):
        self.model = gensim.models.Word2Vec.load(self.path)
        self.vector_size = self.model.vector_size

    def _embed_single(self, text, max_len):
        embedding = [self.model.wv[i].reshape(-1, self.vector_size) for i in text.split() if i in self.model.wv]
        if len(embedding) == 0:
            return self._pad(np.zeros((1, self.vector_size)), max_len)
        embedding = np.concatenate(embedding, axis=0)
        return self._pad(embedding, max_len)
                    
    def embed_batch(self, text_list, max_len):
        batch = [self._embed_single(i, max_len) for i in text_list]
        return np.concatenate(batch)
    
    def _pad(self, array, max_len):
        if array.shape[0] >= max_len:
            return np.expand_dims(array[:max_len],0)
        else:
            padding_size = max_len - array.shape[0]
            return np.expand_dims(np.pad(array, [(0, padding_size), (0, 0)], mode='constant', constant_values=0), 0)
