# STRIDE — definitions, money-software examples, mitigations

STRIDE is a checklist so no threat class is missed. Walk each against the
surface. Examples lean toward software that holds, moves, or authorizes value
(payments, wallets, on-chain, ledgers, billing, custody, treasury automation).

---

**S — Spoofing** (pretending to be someone/something else)
- Examples: forged webhook claiming to be the partner bank or payment processor;
  a fabricated price/oracle feed; a spoofed RPC or data-provider response feeding
  a trade or launch; stolen session token; a chat/social account impersonating a
  verified person; an API caller faking identity.
- Mitigations: strong authentication; MFA; cryptographically signed requests
  (HMAC / webhook signing secrets — verify the raw body, not a re-serialized
  copy); mTLS between services; short-lived tokens; verify external facts against
  an independent source before acting on them. Bind account identity to a
  verified human out-of-band — a channel authenticates the *account*, never the
  person's *intent*.

**T — Tampering** (altering data in transit or at rest)
- Examples: changing a payment amount or destination address in flight; editing a
  stored balance directly; altering an audit record; mutating token/launch
  metadata; poisoning the persistent state an autonomous system learns from.
- Mitigations: TLS in transit; integrity checks / signatures; DB constraints and
  permissions so records can't be edited out of band; append-only ledgers
  (compensating entries, never edits); validate and pin destinations in code so a
  data change can't redirect funds; treat any state derived from untrusted input
  as tainted until validated.

**R — Repudiation** (doing something and denying it, with no proof otherwise)
- Examples: an admin (or an autonomous agent) moves funds or launches an asset
  and there is no record of who/what/when; a user disputes an action you can't
  evidence.
- Mitigations: append-only audit log of every privileged/value action — actor
  (human or agent), inputs, decision, and outcome; tamper-evident logs; signed
  operations; for agent actions, log the exact decision record and the source
  signals that drove it.

**I — Information disclosure** (seeing what you shouldn't)
- Examples: an endpoint returns another user's balance (IDOR); secrets in
  logs/errors; a private key or API credential reaching a prompt, a published
  record, or a model's output; PII over-exposed; cross-tenant leakage.
- Mitigations: authz at the resource; least privilege; encrypt sensitive data;
  scrub secrets/PII from logs and error output; row-level security. **Keep
  secrets out of any context that can be exfiltrated** — a key that is never
  present in a prompt, log, or published surface cannot leak, which beats
  scanning output for it.

**D — Denial of service** (making it unavailable)
- Examples: flooding an expensive endpoint; unbounded query/complexity; resource
  exhaustion; a retry storm; a dependency (RPC, price feed, data provider)
  outage that silently degrades a money flow; draining a hot wallet's gas/float
  so nothing can execute.
- Mitigations: rate limits and quotas; backoff + jitter on retries; input
  size/complexity bounds; circuit breakers; autoscaling with caps; detect
  degraded dependencies and fail safe (stop acting) rather than acting on stale
  or empty data; keep the operating float funded with alerting before exhaustion.

**E — Elevation of privilege** (gaining rights beyond your role)
- Examples: a normal user reaches an admin function; mass assignment sets
  `isAdmin`; a low-tier key performs a high-tier action; **untrusted input steers
  an agent into taking a value action it should not** (prompt injection is an EoP
  against an agent's tools); a forged approval message passes an allowlist.
- Mitigations: deny by default; authz checks at every privileged action; least
  privilege per role/key; tier operations by blast radius; step-up auth and
  multi-party approval for the most sensitive actions; for agents, enforce the
  value-action guardrails in deterministic code outside the model (see
  `agent-surfaces.md`), and require a signed/second-factor confirmation for the
  actions that move the most value.

---

# Ranking guide (impact × likelihood)
- Impact: money loss / key compromise / auth bypass / mass data exposure /
  irreversible on-chain action = high; single-record / cosmetic = low.
- Likelihood: reachable by an unauthenticated external actor, or by untrusted
  input that already flows into the system = high; requires insider + physical
  access = low.
- Rank = the product. Fix high-impact-high-likelihood first; document accepted
  residual risk for the rest. Weight *irreversibility* up — an on-chain transfer
  or a public launch cannot be rolled back like a database row.
