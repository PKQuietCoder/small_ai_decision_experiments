---
name: Detached shell processes are killed when the bash call returns
description: Why nohup/setsid background jobs die early in this environment
---

Background processes launched from the bash tool (even with `nohup ... &` or
`setsid ... &` + `disown`, output redirected to a file, stdin `/dev/null`) are
killed shortly after the originating bash call returns. They do NOT survive into
later tool calls. Symptom: the job's log stops after the first few lines and the
process is gone from `ps` on the next poll.

**Why:** the sandbox tears down the process tree spawned by a bash invocation
when that invocation completes; detaching from the controlling terminal is not
enough to escape it.

**How to apply:** run long jobs to completion inside a SINGLE foreground bash
call (max ~120s), or make them fast enough to fit (e.g. parallelize independent
API calls). Do not rely on launch-then-poll-across-calls for work that must keep
running. Also note: `pkill`/`kill` with a pattern that matches the bash shell
itself will kill your own call (exit 143) — target specific PIDs instead.
