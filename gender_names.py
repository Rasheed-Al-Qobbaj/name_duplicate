import json
import re

# Global placeholder for lazy loading
_llm_model = None

def _get_llm_model():
    """Lazy load quantized Gemma via llama_cpp"""
    global _llm_model
    if _llm_model is None:
        from llama_cpp import Llama
        print("Loading Gemma GGUF Model...")
        _llm_model = Llama.from_pretrained(
            repo_id="codegood/gemma-2b-it-Q4_K_M-GGUF",
	        filename="gemma-2b-it.Q4_K_M.gguf",
            n_ctx=2048,      # Context window
            n_threads=4,     # Hardware dependent: adjust for CPU optimization
            verbose=False    # Suppress verbose C logs
        )
        print("Gemma Model Ready.")
    return _llm_model

def process_gender(raw_data):
    """
    Processes a list of [row_index, name] pairs.
    Returns a list of dicts: {"row_index": int, "name": str, "gender": str}
    """
    llm = _get_llm_model()
    results =[]
    BATCH_SIZE = 25 
    
    for i in range(0, len(raw_data), BATCH_SIZE):
        batch = raw_data[i:i + BATCH_SIZE]
        names = [item[1] for item in batch]
        
        names_str = json.dumps(names, ensure_ascii=False)
        
        # Gemma instruction format focusing on strict JSON output
        prompt = (
            f"<start_of_turn>user\n"
            f"Classify the gender of the following Arabic first names.\n"
            f"Valid responses are strictly 'Male', 'Female', or 'Unknown'.\n"
            f"Output ONLY a valid JSON dictionary mapping each name to its gender.\n"
            f"Names: {names_str}<end_of_turn>\n"
            f"<start_of_turn>model\n{{"
        )
        
        response = llm(
            prompt,
            max_tokens=1024,
            stop=["<end_of_turn>"],
            temperature=0.0 # Greedy decoding for structural tasks
        )
        
        # Prepend the opening brace omitted in the prompt
        text_output = "{" + response['choices'][0]['text'].strip()
        
        # Robust JSON extraction to ignore trailing text
        json_match = re.search(r'\{.*?\}', text_output, re.DOTALL)
        
        batch_results_dict = {}
        if json_match:
            try:
                batch_results_dict = json.loads(json_match.group(0))
            except json.JSONDecodeError:
                print(f"Failed to parse JSON for batch {i}. Raw output: {text_output}")
                
        # Map predictions back to the original rows
        for item in batch:
            row_idx, name = item
            
            # Default to Unknown if the name was skipped or malformed
            gender = batch_results_dict.get(name, "Unknown")
            
            if gender not in ["Male", "Female", "Unknown"]:
                gender = "Unknown"
                
            results.append({
                "row_index": row_idx,
                "name": name,
                "gender": gender
            })

    return results