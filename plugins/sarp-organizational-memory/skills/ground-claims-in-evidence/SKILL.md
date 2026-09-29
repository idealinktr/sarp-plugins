---
name: ground-claims-in-evidence
description: Ground a proposed claim or decision in SARP evidence and standing memory. Use before recommending a material decision, when the user asks for supporting evidence, or when a proposal may contradict existing facts, memory, or decisions.
---

# Ground claims in evidence

Before presenting a material organizational claim as supported:

1. State the candidate claim precisely.
2. Use `check_contradictions` to compare it with relevant standing Fact,
   Memory, and Decision records in the authenticated actor's scope.
3. Report supporting, contradicting, and unresolved context separately.
4. Use `trace_decision` for any decision whose lineage is material to the
   answer.
5. Label uncertainty and projection warnings exactly as returned by SARP.

Treat `potential-conflicts-only` and candidates without an explicit
`contradicts` or `corrects` lineage edge as potential conflicts, not established
contradictions. Say "potentially conflicts" or "may conflict" in that case.
Only say that records contradict one another when SARP returns an explicit
conflict or correction edge.

Do not turn observations into facts, evidence into approval, or a governance
request into authorization. Never claim a contradiction has been resolved
unless SARP returns a record that establishes that resolution. Use
`record_evidence` only when the user explicitly asks to preserve supplied
evidence; do not fabricate source references.
