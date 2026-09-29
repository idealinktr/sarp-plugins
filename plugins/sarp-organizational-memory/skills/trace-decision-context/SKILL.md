---
name: trace-decision-context
description: Trace the governed context and lineage of a SARP decision. Use when the user asks why a decision was made, what evidence supported it, who authorized it, what action followed, or what outcome was recorded.
---

# Trace decision context

Use the SARP `trace_decision` tool for the decision identified by the user or
returned by `recall_decisions`.

Present only lineage returned by SARP. Organize available records in this
order:

1. evidence,
2. decision,
3. authorization,
4. action,
5. outcome.

Explain the explicit relationships between the records and include their IDs.
Call out missing stages as missing; never infer or invent a relationship to
make the trace look complete. A governance request is not an approval, and an
approval is not execution. Preserve supersession history when the decision has
been replaced.
