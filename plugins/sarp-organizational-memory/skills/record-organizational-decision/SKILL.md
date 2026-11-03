---
name: record-organizational-decision
description: Record or supersede a governed organizational decision in SARP. Use when the user asks to preserve a decision, replace a standing decision, or request human authorization for one.
---

# Record an organizational decision

Use SARP's governed command path. A draft in the conversation is not a stored
decision until SARP accepts the write.

Before any write:

1. Translate the matter into a concise recall query. Leave organization and
   tenant identifiers out of the tool input.
2. Call `recall_decisions`.
3. Call `check_contradictions` on the candidate decision.
4. Report standing decisions, superseded decisions, contradictions, and
   unresolved context separately. Cite the record IDs SARP returned.

An empty recall means the readable projection returned no matching decision.
It is not proof that no decision exists. Say that, then continue only if the
user still wants a record created.

Treat `potential-conflicts-only` and candidates without an explicit
`contradicts` or `corrects` lineage edge as potential conflicts. Say
"potentially conflicts" or "may conflict" in that case. Show the result to
the user before writing. Continue with the write when the user still wants
the decision preserved.

Prepare the decision from the user's request and from records SARP returned.
Use this template. Leave a field empty when the user did not supply it and
SARP did not return it:

- Context:
- Options considered:
- Decision:
- Evidence:
- Owner:
- Review date:

Evidence is the explicit evidence references the user supplied or SARP
returned. Do not fabricate source references. Use `record_evidence` only when
the user explicitly asks to preserve supplied evidence.

Then write through the matching tool:

1. When the new decision replaces a standing decision, call
   `supersede_decision`. Supersession keeps the earlier decision and its
   lineage. Preserve that history. Do not overwrite or delete the earlier
   decision.
2. When no standing decision is being replaced, call `record_decision` and
   include the explicit evidence references.
3. Include the completed template in the decision you send. Pass only
   arguments the tool accepts.

After the write, call `request_authorization`. That call creates a governance
request. It does not approve the request. Stop there and wait for a person to
approve it in SARP. Report the request as pending. A created request is not
authorization, execution, or a final decision.

Leave access tokens, organization IDs, and tenant IDs out of tool inputs.
