#!/usr/bin/env python3
"""Fail CI if an upstream sync silently removes Pythology security invariants."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

checks = {
    "trace upload hard-off": (
        "crates/codegen/xai-grok-shell/src/agent/config.rs",
        'pub(crate) fn resolve_trace_upload(&self) -> Resolved<bool> {\n        Resolved::new(false, ConfigSource::Default)',
    ),
    "internal trace export hard-off": (
        "crates/codegen/xai-grok-shell/src/agent/config.rs",
        'pub(crate) fn resolve_traces_export_enabled(&self) -> bool {\n        let _ = self;\n        false',
    ),
    "feedback trace side-channel blocked": (
        "crates/codegen/xai-grok-shell/src/extensions/feedback_trace.rs",
        "trace upload is disabled in the Pythology fork",
    ),
    "remote fetch fail-closed": (
        "crates/codegen/xai-grok-shell/src/util/config/resolve/features.rs",
        ".find_map(remote_fetch_value)\n    // Pythology fork: no backend catalog/settings egress unless explicitly enabled.\n    .unwrap_or(false)",
    ),
    "strict sandbox default": (
        "crates/codegen/xai-grok-sandbox/src/profiles.rs",
        "/// Pythology fork default: filesystem-minimal profile with child-network restriction.\n    #[default]\n    Strict,",
    ),
    "core-only subprocess environment": (
        "crates/codegen/xai-grok-tools/src/util/shell_env_policy.rs",
        "inherit: ShellEnvironmentPolicyInherit::Core,\n            ignore_default_excludes: false,",
    ),
    "plugin auto-trust disabled": (
        "crates/codegen/xai-grok-agent/src/plugins/trust.rs",
        "pub fn is_config_path_auto_trusted(_plugin_root: &Path) -> bool {\n        false",
    ),
}

failed = []
for name, (relpath, needle) in checks.items():
    text = (ROOT / relpath).read_text(encoding="utf-8")
    if needle not in text:
        failed.append(f"{name}: missing expected invariant in {relpath}")

if failed:
    print("Pythology security invariant check FAILED:", file=sys.stderr)
    for failure in failed:
        print(f" - {failure}", file=sys.stderr)
    sys.exit(1)

print(f"Pythology security invariant check passed ({len(checks)} invariants).")
