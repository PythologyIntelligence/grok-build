# Pythology Grok Build security profile

This fork is an **experimental agent-runtime research dependency**, not a trusted production component.

Pythology intentionally keeps useful harness concepts from upstream while changing defaults that are too permissive for access to Pythology repositories, credentials and intelligence systems.

## Current hard invariants

The security branch establishes these invariants:

1. **Session / repository trace upload is disabled in code.**
   - `AgentConfig::resolve_trace_upload()` always resolves to `false`.
   - The normal ACP feedback trace-upload handler rejects requests.
2. **The upstream internal OTLP trace exporter is disabled in code.**
   - Pythology-owned observability may be added later as a separately reviewed destination.
3. **Remote backend catalog/settings fetch fails closed by default.**
   - No remote xAI settings/model-catalog fetch occurs unless an explicit trusted configuration enables it.
4. **Strict sandbox is the default profile.**
   - The default uses the built-in strict profile, including child-process network restriction where the platform enforcement supports it.
5. **Subprocess environment inheritance is restrictive by default.**
   - Only core platform environment names are inherited.
   - names matching `*KEY*`, `*SECRET*`, or `*TOKEN*` are excluded by default.
6. **Plugin paths are never auto-trusted merely because they live under the user home directory.**
   - Executable plugin capabilities require explicit trust.

These are **Pythology fork invariants**. An upstream sync must not silently revert them.

## What this does not yet mean

This is not certification that the whole upstream codebase is safe.

Before any connection to Prometheus, Atlas, EarthNet, ARCUS, Oracle or production credentials:

- run the focused security CI successfully;
- audit outbound HTTP call sites and remaining upload/storage helpers;
- audit MCP server launch and credential inheritance;
- audit plugin/hook/skill install/update paths;
- audit permission bypass and auto-approval paths;
- audit sandbox behaviour on the actual deployment OS;
- test that child processes cannot read production secret stores;
- test that network denial behaves as expected;
- use disposable repositories and synthetic data first.

## Initial deployment boundary

First execution should be in a disposable environment with:

- no production GitHub token;
- no cloud provider credentials;
- no browser profile/cookies;
- no payment credentials;
- no SSH private keys;
- no production database secrets;
- no writable production mounts;
- no access to Pythology secret stores;
- synthetic or public test repositories only.

Prometheus should eventually request work through explicit capability contracts. The harness must never inherit every capability of the parent process simply because the parent has them.

## Agent Reach / external research

If this runtime is later used to host Agent Reach or another internet research worker:

- read-only public research by default;
- network destinations constrained by policy;
- downloads quarantined;
- no execution of retrieved content;
- no purchase/payment capability;
- no account mutation capability;
- no arbitrary credential access;
- immutable provenance returned with evidence.

Wide eyes. Short leash.
