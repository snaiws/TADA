from typing import List, Dict, Optional  

import numpy as np  
import faiss  
from sentence_transformers import SentenceTransformer  



class DocumentStore:  
    def __init__(self):  
        # 문장 임베딩 모델 초기화  
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')  
        
        # FAISS 인덱스 초기화  
        self.dimension = self.model.get_sentence_embedding_dimension()  
        self.index = faiss.IndexFlatL2(self.dimension)  
        
        # 문서 저장  
        self.documents = []  
        

    def add_documents(self, texts: List[str], metadata: Optional[List[Dict]] = None):  
        """문서 추가"""  
        if not texts:  
            return  
            
        # 임베딩 생성  
        embeddings = self.model.encode(texts)  
        
        # FAISS 인덱스에 추가  
        self.index.add(np.array(embeddings).astype('float32'))  
        
        # 문서 저장  
        self.documents.extend(texts)


    def search(self, query: str, n_results: int = 3) -> List[str]:  
        """질문과 관련된 문서 검색"""  
        # 쿼리 임베딩  
        query_embedding = self.model.encode([query])  
        
        # 유사도 검색  
        D, I = self.index.search(np.array(query_embedding).astype('float32'), n_results)  
        
        # 관련 문서 반환  
        return [self.documents[i] for i in I[0]]