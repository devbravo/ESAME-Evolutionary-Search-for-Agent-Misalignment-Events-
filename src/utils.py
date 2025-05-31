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


def compute_char_diff(old: str, new: str) -> Dict[str, List[str]]:
    """Character-level diff for more fine-grained analysis"""
    # Could add this later for more precise tracking
    pass


def sanitize_text(text: str) -> str:
    """
    Normalize input text for diff computation.:
    - Lowercase everything.
    - Remove all punctuation (anything that isn’t a letter, digit, or whitespace).
    - Collapse multiple whitespace characters into a single space.
    - Strip leading/trailing whitespace.
    Args:
        text: The raw input string.
    Returns:
        A normalized string where tokens are separated by single spaces and
        punctuation has been stripped.
    """

    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    return text


