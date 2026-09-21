# Pythology upstream-sync policy

Upstream `xai-org/grok-build` is treated as an external software supplier.

## Invariant

No upstream commit is accepted directly into `main`.

The only supported path is:

```text
xai-org/grok-build:main
        |
        v
automation/upstream-sync
        |
        v
Pull Request
        |
        +--> Pythology security invariant checks
        +--> upstream/repository CI where available
        +--> human review
        |
        v
main
```

## Required review

Treat changes in these areas as security-sensitive:

- telemetry, trace/session upload, feedback upload and cloud-storage code;
- remote settings, model-catalog and managed-config fetches;
- shell/process execution and environment inheritance;
- sandbox and network policy;
- permissions and auto-approval logic;
- plugins, hooks, skills, MCP and marketplace installation/trust;
- credential/auth/token handling;
- Git/worktree/clone operations;
- dependency, build, release and GitHub Actions changes;
- binaries, generated artifacts and native-code dependencies.

Upstream conflicts **fail closed**. Never resolve a conflict by dropping a Pythology lockdown change merely to make the sync green.

## Pythology divergence

The Pythology fork intentionally differs from upstream in security defaults. The invariants are documented in `PYTHOLOGY_SECURITY.md` and enforced by `scripts/check-pythology-security-invariants.py`.

## GitHub branch protection target

Enable the following on `main`:

- require pull request before merge;
- at least one approving review;
- dismiss stale approvals;
- require Code Owner review;
- require conversation resolution;
- require the Pythology Security workflow and other existing CI checks;
- require the branch to be up to date where practical;
- block force pushes;
- block deletion;
- apply rules to administrators except for a documented emergency process;
- do not auto-merge upstream-sync PRs.
