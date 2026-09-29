# SARP Plugins

Official public distribution repository for SARP plugins.

This repository contains installable client configuration and usage guidance
only. SARP's canonical domain model, Command Runtime, Query Runtime,
authorization rules, and organizational data remain in the governed SARP
service and are not duplicated here.

## Claude Code

Add this repository as a marketplace:

```sh
claude plugin marketplace add idealinktr/sarp-plugins
```

Install the organizational memory plugin:

```sh
claude plugin install sarp-organizational-memory@sarp-plugins
```

Start a new Claude Code session, run `/mcp`, select
`plugin:sarp-organizational-memory:sarp-memory`, and complete the browser sign-in
flow.

The plugin connects to the public SARP MCP service at
<https://mcp.getsarp.com/mcp>. Authentication and organization scope are
derived from the signed-in actor; never place access tokens, organization IDs,
or tenant IDs in prompts or plugin configuration.

See the [plugin guide](plugins/sarp-organizational-memory/README.md) for the
eight public tools, example prompts, and verification steps.

## Distribution boundary

The files in this repository may configure a client to call SARP, but they do
not grant authority or bypass governance. All writes pass through SARP's
governed command path. Authorization requests cannot approve themselves, and
superseding a decision preserves its history and lineage.

