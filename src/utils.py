import re
from typing import Dict, List
from difflib import SequenceMatcher

def compute_diff(old: str, new: str) -> Dict[str, List[str]]:
    """
    Return a token-level diff summary between two strings.
    Args:
        old: Original text
        new: Modified text

    Returns:
        Dictionary with 'insertions' and 'deletions' lists of tokens
    """
    old_tokens = sanitize_text(old)
    new_tokens = sanitize_text(new)

    old_tokens_cleaned = old_tokens.split()
    new_tokens_cleaned = new_tokens.split()
    s = SequenceMatcher(None, old_tokens_cleaned, new_tokens_cleaned)

    insertions, deletions = [], []
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == "replace":
            deletions.extend(old_tokens_cleaned[i1:i2])
            insertions.extend(new_tokens_cleaned[j1:j2])
        elif tag == "insert":
            insertions.extend(new_tokens_cleaned[j1:j2])
        elif tag == "delete":
            deletions.extend(old_tokens_cleaned[i1:i2])

    return {"insertions": insertions, "deletions": deletions}


# PRE-COMPILED REGULAR EXPRESSIONS FOR PERFORMANCE
_PUNCT = re.compile(r'[^a-z0-9\s]')
_SPACE = re.compile(r'\s+')

def sanitize_text(text: str) -> str:
    text = text.lower()
    text = _PUNCT.sub(' ', text)  # ← Use pre-compiled pattern
    text = _SPACE.sub(' ', text)
    text = text.strip()

    return text


def calculate_parent_similarity(parent1: str, parent2: str, child: str) -> Dict[str, float]:
    p1_tokens = set(sanitize_text(parent1).split())
    p2_tokens = set(sanitize_text(parent2).split())
    child_tokens = set(sanitize_text(child).split())

    p1_similarity = len(child_tokens & p1_tokens) / len(child_tokens | p1_tokens)
    p2_similarity = len(child_tokens & p2_tokens) / len(child_tokens | p2_tokens)

    return {
        "parent1_similarity": round(p1_similarity, 3),
        "parent2_similarity": round(p2_similarity, 3)
    }


