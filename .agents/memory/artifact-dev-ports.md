---
name: Artifact dev port must be a reserved .replit port
description: Why a web artifact workflow fails to start despite vite reporting "ready"
---

A custom/manually-registered artifact whose `[[services]] localPort` (and `[services.env] PORT`) is NOT one of the localPorts reserved in `.replit` under `[[ports]]` will fail to start: the workflow reports `DIDNT_OPEN_A_PORT` (timeout) even though vite logs `ready` and binds the port, and curl to that port locally works.

**Why:** the workflow port detector / preview proxy only watches localPorts that have a `[[ports]]` localPort→externalPort mapping in `.replit`. An unmapped high port (e.g. an auto-assigned 20517) is invisible to it. Port assignment is normally automatic via `createArtifact`; a hand-rolled `artifact.toml` (tell-tale sign: `id` like `"artifacts/<slug>"` instead of a random id) can drift onto an unmapped port.

**How to apply:** check `.replit` `[[ports]]` for the reserved localPorts (commonly 8080, 8081, 8082, 8098, 8099). Pick a FREE one — probe with `curl localhost:<port>/` (000 = free, anything else = taken; e.g. 8082 was already taken returning 302). Set BOTH `[[services]] localPort` and `[services.env] PORT` to that port via `verifyAndReplaceArtifactToml`, then restart. The path router still routes "/" to it regardless of which external port it maps to.
