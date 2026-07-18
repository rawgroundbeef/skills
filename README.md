# Agent Skills

A personal collection of agent workflows I am building and maintaining for the
way I plan, build, review, and ship software.

These are opinionated on purpose. They favor evidence from the repository,
durable decisions over conversation memory, explicit human gates, and output
another agent can pick up cold. I keep changing them as I learn what actually
works.

Feel free to use them, adapt them, fork them, or pull out the pieces that fit
your own workflow.

## The collection

| Skill | What it does |
| ----- | ------------ |
| [⚔️ `slice`](./slice/) | Shapes a rough idea into a fully grilled, acceptance-driven vertical slice and a cold-start implementation handoff. |
| [`grill`](./grill/) | Stress-tests a plan against the project's domain language and durable architecture decisions. |
| [`prd`](./prd/) | Builds a product requirements document through interview, codebase exploration, and module design. |
| [`review`](./review/) | Reviews diffs for correctness, architecture, security, performance, maintainability, and testing risks. |
| [`pr`](./pr/) | Derives PR copy from the final diff and triages review feedback into address, defer, or dismiss. |
| [`typescript-cli`](./typescript-cli/) | Builds, migrates, and reviews reliable, distributable Node.js CLIs in TypeScript. |
| [`product-website`](./product-website/) | Builds and audits clear, credible, conversion-focused product marketing sites. |

Each directory has its own README for humans and a `SKILL.md` containing the
actual agent workflow.

## Using a skill

Copy or link the skill directory into whichever skills location your agent
uses, then invoke it by name—for example:

```text
Use $review to check this branch before I merge it.
```

The descriptions in `SKILL.md` are written to support automatic triggering too,
when the agent environment provides it.

## Anatomy

```text
skill-name/
├── README.md            # Human-facing overview
├── SKILL.md             # Trigger metadata and executable workflow
├── agents/openai.yaml   # Optional UI metadata
├── references/          # Detailed guidance loaded only when needed
├── scripts/             # Repeatable deterministic helpers
└── assets/              # Templates and output resources
```

Not every skill needs every directory. The core workflow stays in `SKILL.md`;
supporting material exists only when it earns its keep.

## Building these

- Keep the workflow portable and discover project-specific rules from the
  repository instead of baking in one application's architecture.
- Prefer code, diffs, tests, and durable artifacts over conversation memory.
- Make write boundaries and human approval gates explicit.
- Use progressive disclosure so specialized guidance does not crowd every task.
- Exercise skills on real work and revise them when reality finds the weak spot.
