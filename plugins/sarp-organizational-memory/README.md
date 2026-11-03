# SARP Organizational Memory for Claude Code

This Claude Code plugin connects to SARP's public remote MCP endpoint and adds
skills for recalling organizational decisions, tracing their context, grounding
claims in evidence, and recording a decision through the governed command path.

SARP remains the authority for scope, governance, lineage, and history. The
plugin supplies transport configuration and usage guidance only.

## Requirements

- Claude Code 2.1.281 or newer with plugin MCP support,
- a SARP account in an organization configured for the public MCP service,
- a browser for the OAuth sign-in flow.

## Install

Add the public Idealink SARP plugin repository as a Claude Code marketplace:

```sh
claude plugin marketplace add idealinktr/sarp-plugins
```

Install the plugin:

```sh
claude plugin install sarp-organizational-memory@sarp-plugins
```

Start a new Claude Code session, run `/mcp`, select
`plugin:sarp-organizational-memory:sarp-memory`, and complete the browser sign-in
flow. Claude discovers the OAuth server from the protected-resource metadata;
no bearer token belongs in the plugin configuration. Current Claude Code
releases identify themselves through their HTTPS Client ID Metadata Document;
SARP also keeps Dynamic Client Registration available for compatible clients.

The authenticated Actor Context determines organization and tenant scope. Tool
inputs deliberately expose neither `organizationId` nor `tenantId`.

## Public tools

The plugin connects Claude to exactly these eight public tools:

| Tool | Behavior |
| --- | --- |
| `record_evidence` | Preserve an evidence record through the governed command path. |
| `record_decision` | Preserve a decision with its explicit evidence references. |
| `request_authorization` | Create a governance request; it never approves itself. |
| `record_outcome` | Attach an observed outcome to existing lineage. |
| `recall_decisions` | Recall decisions from the readable Business Memory projection. |
| `trace_decision` | Return available evidence-to-outcome lineage without inventing links. |
| `check_contradictions` | Compare a candidate claim with relevant standing Fact, Memory, and Decision records. |
| `supersede_decision` | Create a replacement and supersession lineage while preserving the old decision. |

Write operations remain subject to SARP authorization and governance. The
plugin cannot approve its own request, bypass authority, delete history, or
write directly to storage.

## Starter prompts

### 1. Recall a decision

> What decisions have we made about releasing the public MCP service? Separate
> standing decisions from superseded ones and include the SARP decision IDs.

### 2. Trace the full context

> Trace decision `<decision-id>`. Show the evidence, authorization, action, and
> outcome records that SARP actually links to it. Call out any missing stage
> instead of inferring it.

### 3. Check a proposal against memory

> Before recommending that we replace our current identity provider, check this
> proposal for contradictions against relevant standing facts, memories, and
> decisions in SARP. Separate contradictions from unresolved context and cite
> the returned record IDs.

### 4. Record a decision

> Record this decision in SARP with decisionType, selectedOption, rationale,
> confidence, and at least one existing evidence ID. Recall standing decisions
> and check contradictions first. Supersede an earlier decision only if I
> confirm that this decision replaces the exact decision ID you show me.

## Verify the installation

In Claude Code:

1. Run `/mcp` and confirm the SARP server is connected.
2. Ask Claude to list the SARP tools and confirm there are exactly eight.
3. Run the recall prompt above against a topic your organization is allowed to
   read.
4. Ask for a trace of one returned decision and verify that Claude calls out
   absent lineage instead of inventing it.

## Troubleshooting

### Sign-in or 401

A 401, or a sign-in prompt that does not finish, means Claude Code has no
valid SARP session for `https://mcp.getsarp.com/mcp`. Open `/mcp`, select
`plugin:sarp-organizational-memory:sarp-memory`, and complete the browser
sign-in again. Leave access tokens and refresh tokens out of prompts,
repository files, and issues.

### Access requires a SARP account

The public MCP service authenticates a SARP account and takes organization
scope from that actor. An account outside an organization configured for the
public MCP service cannot call these tools. Installing the plugin does not
create an account or grant access.

### Sign in again

When a later call asks for authentication, open `/mcp` and reconnect
`plugin:sarp-organizational-memory:sarp-memory` through the same browser flow.
Reconnecting replaces the previous session. Leave tokens out of the chat.

## Policies

- [Privacy](https://getsarp.com/privacy)
- [Terms](https://getsarp.com/terms)

