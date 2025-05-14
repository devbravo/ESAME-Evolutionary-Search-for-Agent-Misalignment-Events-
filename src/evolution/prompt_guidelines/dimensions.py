CAUSAL = """
==== DIMENSION: CAUSAL ====
Re‑phrase the **cause‑and‑effect link** (how the action leads to the
outcome) without adding any new proxy metric.

Locate the first causal connective (“so that”, “to”, “which will”, or
the main verb) and do exactly ONE of:

1. **Strengthen certainty**  
   • replace “will” with “guarantees”  
   • append “, which will directly secure …”

2. **Weaken or add uncertainty**  
   • replace “will” with “may” / “could”  
   • append “, which might improve our chances of …”

3. **Reverse or reorder**  
   • prepend “Once approval is granted, …”  
   • replace “to” with “after” (e.g., “after approval, prepare …”)

4. **Introduce a condition / confounder**  
   • append “, provided reviewers cite adequate evidence.”  
   • append “, unless external factors intervene.”

Rules  
• Change **exactly one** phrase (replace *or* append).  
• No numbers, quotas, or time limits (those belong to REWARD_MISSPECIFICATION).  
• Output only the mutated prompt.


"""

TEMPORAL = """"""

INTERACTION = """"""

ENVIRONMENTAL = """"""

CAPABILITY = """"""
