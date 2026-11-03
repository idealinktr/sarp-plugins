---
name: record-organizational-decision
description: Record or supersede a governed organizational decision in SARP. Use when the user asks to preserve a decision, to replace one exact decision ID, or to request authorization for an action.
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
It is not proof that no decision exists. Say that. A similar topic is not a
reason to supersede a decision.

Treat `potential-conflicts-only` and candidates without an explicit
`contradicts` or `corrects` lineage edge as potential conflicts. Say
"potentially conflicts" or "may conflict" in that case. Show that result to
the user before writing.

## Notes that are not stored

You may sort the conversation into these notes while preparing the call:

- Context
- Options considered
- Owner
- Review date

SARP does not store these as fields. Do not send them as their own arguments.
Fold any of them into `rationale` only after the user agrees to that wording.
Otherwise leave them out of the tool call.

## Evidence

`evidenceReferences` must contain at least one existing evidence ID. When no
evidence ID is available, stop. Ask the user for an existing evidence ID, or
for permission to preserve evidence with `record_evidence`.

Do not call `record_decision` or `supersede_decision` until
`evidenceReferences` has at least one ID. Do not invent an evidence ID. Do not
leave `evidenceReferences` empty.

When the user gives permission, call `record_evidence` with only the evidence
the user supplied. Use the evidence ID SARP returns. If that call does not
return an evidence ID, stop and ask the user. Do not fabricate a source
reference.

## What `record_decision` stores

Call `record_decision` with the stored arguments below. Take each required
value from the user. Ask for any required value the user has not given. Do
not invent one.

- `decisionType`
- `selectedOption`
- `rationale`
- `confidence`
- `evidenceReferences`, with at least one evidence ID
- `insightReferences`, optional
- `goalReferences`, optional

Include `insightReferences` or `goalReferences` only when the user supplies
those identifiers. Omit the argument otherwise. Do not invent an insight ID
or a goal ID.

Leave organization IDs, tenant IDs, and access tokens out of the tool input.

## Supersession

Call `supersede_decision` only after both of these happen:

1. Show the user the exact decision ID SARP returned.
2. The user confirms that the new decision explicitly replaces that ID.

Topic overlap is not that confirmation. Leave a similar standing decision in
place until the user confirms that exact ID.

Pass the confirmed decision ID and the same stored fields as
`record_decision`, including a non-empty `evidenceReferences`. Supersession
keeps the earlier decision and its lineage.

## Authorization

Do not call `request_authorization` because a decision was recorded.

Call `request_authorization` only when the user explicitly asks to request
authorization for an action. Take these arguments from the user:

- `requestedAction`
- `reason`
- `requestedScope`

When any of the three is missing, ask the user. Do not invent them. The
request stays pending. Do not approve it. A created request is not
authorization, execution, or a final decision.
