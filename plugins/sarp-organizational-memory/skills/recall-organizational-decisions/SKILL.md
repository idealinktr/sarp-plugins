---
name: recall-organizational-decisions
description: Recall governed organizational decisions from SARP. Use when the user asks what was decided, which decisions still stand, or what the organization remembers about a topic.
---

# Recall organizational decisions

Use the SARP `recall_decisions` tool to answer from the authenticated actor's
organizational scope.

1. Translate the user's topic into a concise recall query without adding an
   organization or tenant identifier.
2. Call `recall_decisions`.
3. Distinguish active, superseded, and otherwise non-standing decisions.
4. Preserve provenance, freshness, and warnings returned by SARP.
5. Summarize the result in plain language and cite returned decision IDs so the
   user can request a trace.

Never treat an empty result as proof that no decision exists. State only that
the current readable projection returned no matching decision. Do not create or
change organizational records unless the user explicitly asks for that action.

