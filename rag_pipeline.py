from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
import numpy as np

class RAGPipeline:
    def __init__(self, documents):
        self.documents = documents
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        # semantic embeddings
        self.embeddings = self.model.encode(documents)

        # BM25 keyword index
        tokenized = [doc.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized)

    def retrieve(self, query, top_k=4):
        # semantic
        q_emb = self.model.encode([query])
        sim = cosine_similarity(q_emb, self.embeddings)[0]

        # keyword
        bm = self.bm25.get_scores(query.lower().split())
        bm = bm / (np.max(bm) + 1e-9)

        # hybrid
        score = 0.5 * sim + 0.5 * bm
        idx = np.argsort(score)[-top_k:][::-1]

        return [(self.documents[i], float(score[i])) for i in idx]