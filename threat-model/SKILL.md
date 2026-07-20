---
name: threat-model
description: Runs a STRIDE threat model over software that holds, moves, or authorizes value — payments, wallets, crypto/on-chain, ledgers, billing, trading, custody, treasury automation — including agent/LLM-in-the-loop systems that can take value-affecting actions. Produces assets, actors, source→sink attack paths, ranked risks, and controls. Use when designing something that touches money or secrets, evaluating a new attack surface, hardening an autonomous/agentic money flow, or asked "what could go wrong and who could cause it."
---

# Threat Model (STRIDE) for value-handling software

Structured "what could go wrong and who could cause it," for systems where a
failure moves money, leaks a secret, or forges a record. Enumerate, rank by
impact × likelihood, recommend controls worst-first, and state the residual risk
that remains after each control.

## Activation triggers
- "threat model this", a new sensitive feature or attack surface
- "what could go wrong / who could attack this"
- before shipping anything that touches money, keys, auth, or PII
- an autonomous or agentic flow that can spend, sign, publish, or authorize

## Methodology

1. **Assets.** What is valuable here: funds and on-chain positions; private keys
   and API credentials; PII; the integrity of ledgers/records; availability of
   the money path; and — for anything published — brand and legal standing.
2. **Actors.** External attacker, malicious insider, compromised account,
   compromised dependency (SDK, RPC, data provider), and — for agent surfaces —
   **untrusted text reaching a model that can act.** Treat every input the system
   did not author as potentially adversarial.
3. **Map source → sink.** For money software, the productive move is to enumerate
   the *sinks* (the actions that affect value: transfer, sign, launch, approve,
   publish, grant) and the *sources* (every input that can reach a sink:
   webhooks, API params, oracle/price feeds, user content, and any text an agent
   reads). A threat is a path from an attacker-controlled source to a sink.
4. **STRIDE walk** across the surface — full definitions, money examples, and
   mitigations in [`references/stride.md`](references/stride.md):
   Spoofing · Tampering · Repudiation · Information disclosure · Denial of service · Elevation of privilege.
5. **Agent-in-the-loop pass.** If a model/agent sits between a source and a sink,
   run the dedicated lens in [`references/agent-surfaces.md`](references/agent-surfaces.md):
   prompt injection, secret exfiltration, memory/knowledge poisoning, and the
   publication sink. Prefer **source/sink invariants that make the worst outcomes
   impossible** over output filters that try to catch them.
6. **Rank** each real threat by impact × likelihood.
7. **Control per threat, worst-first.** Favor deterministic controls in code the
   model cannot influence over controls that depend on the model behaving. State
   the residual risk that remains.

## The invariant test (money software)

Before writing controls, check whether each catastrophic outcome is *possible at
all* by construction. The strongest control is an outcome that cannot happen:

- **Secrets never enter a context that can be exfiltrated.** Keys and credentials
  live where the value-moving code runs, never in a model's prompt/context, logs,
  or any published surface. A secret that is never present cannot leak.
- **No capability = no abuse.** If the system has no "transfer to an arbitrary
  destination" primitive, no input can trigger one. Grant only the specific,
  bounded value actions the job requires; destinations are fixed in code.
- **Guardrails execute outside the model.** Blacklists, spend caps, allow-listed
  destinations, and rate limits enforced in deterministic code hold even if the
  model is fully manipulated; the same rule in a prompt does not.
- **Blast radius is bounded.** Hot/online key holds a small float; the bulk of
  value sits behind a separate, offline authority. One compromise loses the
  float, not the treasury.

Name, for each catastrophic outcome, whether it is *prevented by construction* or
*only mitigated* — and push toward the former.

## Output

```
## threat-model — <surface>
**Assets:** <list>
**Actors:** <list>
**Sinks:** <value-affecting actions>   **Sources:** <untrusted inputs>

### Threats (ranked, impact × likelihood)
1. [HIGH] [S/T/R/I/D/E] <threat> — <source → sink path>
   - Path: <how an attacker gets from source to sink>
   - Control: <mitigation; note if deterministic/outside-model or model-dependent>
   - Class: prevented-by-construction | mitigated | accepted
   - Residual: <what still remains>
```

Separate confirmed exposure from theoretical. Note where a control is missing vs.
present-but-weak, and flag every guardrail that currently lives only in a prompt.
