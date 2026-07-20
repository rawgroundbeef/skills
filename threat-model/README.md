# threat-model

A STRIDE threat model for software that holds, moves, or authorizes value —
payments, wallets, crypto/on-chain, ledgers, billing, trading, custody, treasury
automation — and for agent/LLM-in-the-loop systems that can take value-affecting
actions.

It runs the classic STRIDE walk (Spoofing, Tampering, Repudiation, Information
disclosure, Denial of service, Elevation of privilege), but organizes the hunt
around **source → sink**: enumerate the few actions that affect value (transfer,
sign, launch, approve, publish), then trace which untrusted inputs can reach
each. It ranks threats by impact × likelihood and recommends controls worst-first,
always stating the residual risk.

The distinctive part is the **invariant test** and the **agent-in-the-loop lens**.
Rather than only listing mitigations, it pushes each catastrophic outcome toward
*prevented by construction* — secrets that never enter an exfiltratable context,
capabilities that simply don't exist to be abused, guardrails enforced in
deterministic code the model can't influence, and blast radius bounded to a small
float. For agentic money flows it treats untrusted text as an actor and models
prompt injection, secret exfiltration, memory poisoning, the publication sink, and
unattended-autonomy failure modes.

- [`SKILL.md`](./SKILL.md) — the agent workflow.
- [`references/stride.md`](./references/stride.md) — STRIDE definitions with
  money-software examples, mitigations, and the ranking guide.
- [`references/agent-surfaces.md`](./references/agent-surfaces.md) — the
  source→sink model, the four sinks and how to close each, the two-stage read,
  injection threats, and autonomy failure modes.

## Use it

```text
Use $threat-model on this launch/payment/withdrawal flow before we build it.
```

Point it at a feature, an endpoint, a money path, or an autonomous agent that can
spend, sign, launch, approve, or publish.
