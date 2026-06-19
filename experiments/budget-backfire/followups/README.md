# Follow-up controls (planned, not yet run)

The main package covers two Anthropic models on the faithful pen scenario. Two follow-ups are
planned to harden the finding. Neither has run yet, so this folder is a placeholder.

**1. Disguised, agent-native scenario.** Larson and Hamilton's pen study is well known, so a
capable model might recognize the paradigm. The plan reruns the same step-structure design on a
fresh shopping task with no published human baseline (for example, choosing a software tier or a
hardware component), mirroring how the metaphor study pairs a canonical replication with a novel
control. If the flat, no-backfire result holds on text the model has never seen, recognition
isn't doing the work.

**2. Cross-model comparison.** The current package is Anthropic-only. Adding the GPT-5 family
needs an OpenAI multi-turn tool path, whose API differs from Anthropic's. That run would show
whether the null is specific to these models or general.

When these run, each will land here with its own `summary.csv`, raw runs, and analysis, and the
top-level README will link them.
