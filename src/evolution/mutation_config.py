# Example mutation configurations
mutation_configs = {
    "explorer": {
        "temperature": 0.9,
        "top_p": 0.95,
        "frequency_penalty": 0.6,
        "presence_penalty": 0.4
    },
    "refiner": {
        "temperature": 0.6,
        "top_p": 0.9,
        "frequency_penalty": 0.1,
        "presence_penalty": 0.2
    },
    "specialist": {
        "temperature": 0.7,
        "top_p": 0.9,
        "frequency_penalty": 0.3,
        "presence_penalty": 0.3,
        "logit_bias": {
            # Token IDs would go here to bias toward certain concepts
        }
    }
}

# Dynamic adaptation based on evolutionary progress
def get_mutation_config(generation, diversity_score):
    """Return appropriate config based on evolutionary state"""
    if diversity_score < 0.3:  # Low diversity detected
        return mutation_configs["explorer"]
    elif generation > 20:  # Later in evolution
        return mutation_configs["refiner"]
    else:
        return mutation_configs["specialist"]