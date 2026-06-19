#!/usr/bin/env bash
# Example PreToolUse hook for the Bash tool — DISABLED BY DEFAULT.
#
# This is an inert template: it allows every command (exit 0) and is NOT wired
# into .claude/settings.json, so it does nothing until you opt in. To enable it,
# register it under settings.json -> hooks.PreToolUse (matcher "Bash") and add
# your own checks.
#
# Hook protocol: exit code 2 BLOCKS the command (stderr is shown to Claude);
# any other exit code ALLOWS it. Always fail OPEN (exit 0 on error) so a bug
# here can never wedge the shell. Example checks a maintainer might add: refuse
# `rm -rf` on root/home paths, refuse plain `git push --force`, or enforce pnpm
# over npm/yarn (this workspace is pnpm-only).
exit 0
