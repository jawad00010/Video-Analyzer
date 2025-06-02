import json

def load_training_examples(jsonl_path="training_data.jsonl", limit=3):
    examples = []
    try:
        with open(jsonl_path, "r") as f:
            for line in f:
                example = json.loads(line)
                examples.append(example)
        return examples[:limit]
    except Exception as e:
        return []
