import difflib
from typing import Dict, List

def compute_diff(old: str, new: str) -> Dict[str, List[str]]:
    """
    Return a token-level diff summary between two strings.
    Args:
        old: Original text
        new: Modified text

    Returns:
        Dictionary with 'insertions' and 'deletions' lists of tokens
    """
    old_tokens = old.split()
    new_tokens = new.split()
    s = difflib.SequenceMatcher(None, old_tokens, new_tokens)

    insertions, deletions = [], []
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == "insert":
            insertions.extend(new_tokens[j1:j2])
        elif tag == "delete":
            deletions.extend(old_tokens[i1:i2])
    return {"insertions": insertions, "deletions": deletions}

def compute_char_diff(old: str, new: str) -> Dict[str, List[str]]:
    """Character-level diff for more fine-grained analysis"""
    # Could add this later for more precise tracking
    pass