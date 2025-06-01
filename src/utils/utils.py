import re
from typing import Set, Dict, List
from difflib import SequenceMatcher

# PRE-COMPILED REGULAR EXPRESSIONS FOR PERFORMANCE
_PUNCT = re.compile(r'[^a-z0-9\s]')
_SPACE = re.compile(r'\s+')

def sanitize_text(text: str) -> str:
    text = text.lower()
    text = _PUNCT.sub(' ', text)  # ← Use pre-compiled pattern
    text = _SPACE.sub(' ', text)
    text = text.strip()

    return text


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


class SimilarityCalculator:
    """
    Similarity calculator with internal caching for parent tokens.
    Used when same parents are reused across generations.
    """

    def _init__(self):
        self._token_cache = {}

    def _get_tokens(self, text: str) -> Set[str]:
        """Get tokens with caching"""
        if text not in self._token_cache:
            self._token_cache[text] = sanitize_text(text)
        return self._token_cache[text]

    def calculate_similarity(self, parent1: str, parent2: str, child: str) -> Dict[str, float]:
        """Calculate similarity with automatic caching."""
        p1_tokens = self._get_tokens(parent1)
        p2_tokens = self._get_tokens(parent2)
        child_tokens = self._get_tokens(child)

        if not child_tokens:
            return {"p1_similarity": 0.0, "p2_similarity": 0.0}

        p1_similarity = len(child_tokens & p1_tokens) / len(child_tokens | p1_tokens)
        p2_similarity = len(child_tokens & p2_tokens) / len(child_tokens | p2_tokens)

        return {
            "p1_similarity": round(p1_similarity, 3),
            "p2_similarity": round(p2_similarity, 3)
        }

    def clear_cache(self):
        """Clear the internal token cache."""
        self._token_cache.clear()

    def cache_size(self) -> int:
        """Get the current size of the token cache."""
        return len(self._token_cache)


