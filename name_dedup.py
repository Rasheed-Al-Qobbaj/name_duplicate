import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Global placeholder for lazy loading
_st_model = None

def _get_st_model():
    """Lazy load SentenceTransformer"""
    global _st_model
    if _st_model is None:
        from sentence_transformers import SentenceTransformer
        print("Loading SentenceTransformer Model...")
        _st_model = SentenceTransformer("google/embeddinggemma-300m")
        print("SentenceTransformer Ready.")
    return _st_model

def process_duplicates(raw_data, threshold=0.90):
    """
    Processes a list of [row_index, name] pairs and returns grouped duplicates.
    """
    df = pd.DataFrame(raw_data, columns=['row_index', 'name'])
    names = df['name'].tolist()
    
    model = _get_st_model()
    embeddings = model.encode(names)
    similarity_matrix = cosine_similarity(embeddings)
    
    processed_indexes = set()
    groups =[]
    
    for i in range(len(names)):
        if i in processed_indexes:
            continue
            
        nodes_to_check =[i]
        current_group = set()
        
        while nodes_to_check:
            curr = nodes_to_check.pop()
            current_group.add(curr)
            
            sim_scores = similarity_matrix[curr]
            neighbors =[idx for idx, score in enumerate(sim_scores) if score > threshold]
            
            for n in neighbors:
                if n not in current_group:
                    nodes_to_check.append(n)
        
        processed_indexes.update(current_group)
        
        if len(current_group) > 1:
            group_data = [{
                "row_index": int(df.iloc[idx]['row_index']),
                "name": df.iloc[idx]['name']
            } for idx in current_group]
            groups.append(group_data)

    return groups