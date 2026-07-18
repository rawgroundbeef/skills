# Agent Skills

Reusable, repo-native workflows for planning, building, reviewing, and shipping
software with coding agents.

This is the source registry for a small set of opinionated agent skills. Each
skill is a self-contained package of instructions and optional references that
an agent loads only when the work calls for it. They are designed to preserve
decisions in the repository, operate against real code and diffs, and leave
behind artifacts another session can pick up cold.

## Skills

| Skill | What it does |
| ----- | ------------ |
| [`slice`](./slice/) | Turns rough requirements into discovery, decisions, UAT, a PRD, follow-ups, and an implementation bootstrap. |
| [`grill`](./grill/) | Stress-tests a plan against the project's domain language and durable architecture decisions. |
| [`prd`](./prd/) | Builds a product requirements document through interview, codebase exploration, and module design. |
| [`review`](./review/) | Reviews diffs for correctness, architecture, security, performance, maintainability, and testing risks. |
| [`pr`](./pr/) | Derives PR copy from the final diff and triages review feedback into address, defer, or dismiss. |
| [`typescript-cli`](./typescript-cli/) | Builds, migrates, and reviews reliable, distributable Node.js CLIs in TypeScript. |
| [`product-website`](./product-website/) | Builds and audits clear, credible, conversion-focused product marketing sites. |

The core software-delivery loop is:

```text
slice → implement → review → pr
```

`grill` and `prd` also work independently when a full slice is unnecessary.

## Use with skillfoo

[skillfoo](https://github.com/rawgroundbeef/skillfoo) syncs selected skills
from this registry into a project as committed, repo-local files.

Add `.skillfoo.yml` to the consumer repository:

```yaml
registry: github.com/rawgroundbeef/skills
skills:
  - slice
  - review
  - pr
```

Then reconcile the project:

```sh
skillfoo status
skillfoo sync
```

The project receives neutral copies under `.agents/skills/`, a managed skills
index in `AGENTS.md`, and tool-specific discovery adapters. Pinning the copied
files and lockfile in the consumer repository makes agent behavior reviewable
and keeps registry upgrades intentional.

## Skill structure

Every skill has one required file and may add progressively disclosed resources:

```text
skill-name/
├── SKILL.md             # Trigger metadata and core workflow
├── agents/openai.yaml   # Optional UI metadata
├── references/          # Detailed guidance loaded only when needed
├── scripts/             # Repeatable deterministic helpers
└── assets/              # Templates and output resources
```

`SKILL.md` frontmatter contains the skill name and a trigger-rich description.
The body stays focused on procedural knowledge an agent would not reliably
reconstruct on its own.

## Registry principles

- Keep skills portable; discover repository-specific rules from `AGENTS.md`
  and local documentation instead of baking in one application's architecture.
- Prefer evidence from code, diffs, tests, and durable artifacts over
  conversation memory.
- Make safety boundaries explicit, especially around writes, publishing,
  destructive operations, and external systems.
- Put detailed or conditional guidance in `references/` so the core workflow
  remains concise.
- Update skills here, then run `skillfoo sync` in consumer repositories. Do not
  hand-edit managed projections and let them drift from the registry.

## Adding a skill

1. Create a lowercase, hyphenated directory containing `SKILL.md`.
2. Give the frontmatter a concise `name` and a description that explains both
   what the skill does and when it should trigger.
3. Add only the references, scripts, or assets the workflow actually needs.
4. Validate the skill, exercise it on a realistic task, and review the final
   package for application-specific assumptions.
5. Sync it into a consumer repository and inspect the resulting diff before
   committing the projection.
