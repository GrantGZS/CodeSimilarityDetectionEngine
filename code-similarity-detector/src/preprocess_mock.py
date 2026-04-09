import json
import os

def mock_tokenize(file_path):
    """
    Mock preprocessing function that reads token lists from a JSON file.
    
    Args:
        file_path (str): The case name/key from the JSON file (e.g., 'case_1_identical')
    
    Returns:
        tuple: Two lists of tokens (tokens_a, tokens_b) for the specified case
    """
    json_path = os.path.join('data', 'mock_tokens', 'sample_pairs.json')
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    if file_path in data:
        return data[file_path]['file_a'], data[file_path]['file_b']
    else:
        available_cases = list(data.keys())
        raise ValueError(f"Case '{file_path}' not found. Available cases: {available_cases}")