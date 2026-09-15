---
name: slice
description: Vertical-slice planning pipeline that turns rough requirements into slice-local discovery, decisions, UAT, PRD, follow-ups, and a bootstrap prompt before implementation. Use when starting feature work, shaping a vertical slice, converting rough requirements into acceptance criteria, or preparing a fresh-context agent to implement from durable artifacts.
---

# Slice

Use this as the planning-to-implementation pipeline for one coherent vertical
slice. The artifacts are the source of truth; do not rely on conversation
memory once an artifact exists.

Companion skills this pipeline loads: `$grill`, `$uat`, `$prd`, `$review` (and
a repo-specific `threat-model` skill when the repo has one). Repo-specific
conventions — the integration branch name, verification gates, code layout, and
which zone skills to load — come from the repo's `AGENTS.md`.

## Pipeline

### 1. Establish the branch and scope

When the user wants a PR proposal or implementation off a fresh integration branch:

- Read `AGENTS.md` for the repo's conventions (integration branch, verification
  gates, code layout, zone skills).
- Check `git status --short --branch`.
- Fetch the latest integration branch (e.g. `main`) when permitted, then create
  or confirm a feature branch from it.
- Preserve unrelated local files and untracked planning docs.

Name the feature early and choose a stable slug for artifacts. Slice
directories are numbered so the progression of slices is visible at a glance:

- `.planning/{NNNN-feature-slug}/discovery.md`
- `.planning/{NNNN-feature-slug}/decisions.md`
- `.planning/{NNNN-feature-slug}/uat.md`
- `.planning/{NNNN-feature-slug}/prd.md`
- `.planning/{NNNN-feature-slug}/bootstrap.md`
- `.planning/{NNNN-feature-slug}/follow-ups.md`
- `.planning/{NNNN-feature-slug}/mock/` — optional; only when the slice has a
  visual target (design mock, reference screenshots)

`NNNN` is a zero-padded four-digit sequence number. Pick the next number after
the highest existing prefix in `.planning/` (the first slice is `0001`). The
number belongs to the slice, not to PRs — a multi-PR slice keeps one number.

Create the `.planning/{NNNN-feature-slug}/` directory lazily when the first
planning artifact for the slice is written. Keep filenames stable inside the
directory; the number and slug belong to the directory, not each file.

When the slice has a visual target, capture it into `mock/` at kickoff —
pasted screenshots and external design links are perishable and not readable
by a fresh implementation context. Use descriptive kebab-case names
(`mock-1-history-top.png`), referenced by path from `discovery.md` (with the
living design link alongside) and from `uat.md` as the visual pass reference.
The agent's shell may be unable to read screenshot temp dirs or `~/Desktop`
(macOS TCC) — ask the user to drag files in when copying fails. Prose
extraction in `discovery.md` still happens; the pixels back it up.

### 2. Grill first

Load `$grill` and run it against the kickoff brief, ticket, rough
requirements, existing PRD, or current code behavior. Keep grilling until the
problem, constraints, domain terms, and non-goals are clear enough that a human
and agent are using the same language.

Use code and docs to answer questions whenever possible. Ask the user only for
decisions that cannot be resolved from the repo.

Before a decision leaves the grill, probe it against the code it will land
on: open the seams it touches (the schemas, the unique constraints, the
dispatch or approval paths, the route allowlists, the persistence sites) and
confirm the mechanism the decision assumes actually exists. A decision that
describes what the code cannot do is the most expensive kind of finding to
catch later; most blocking adversarial-review findings are this kind.

Write `.planning/{NNNN-feature-slug}/discovery.md` as the slice-local grill
artifact. Use it for:

- The original requirement set or kickoff brief.
- The refined problem statement.
- Resolved slice-specific terms and constraints.
- Non-goals and open questions.
- Evidence from code or docs that shaped the plan.

Write `.planning/{NNNN-feature-slug}/decisions.md` as the slice-local decision
log. Use it for choices made during the grill, rejected alternatives, and links
to any durable ADRs.

When the slice touches money movement, auth or secrets, PII, or introduces a
new attack surface (new endpoint, webhook, deep link, privileged action), and
the repo has a `threat-model` skill, load it during the grill and run it over
the slice's surface. Record the ranked threats and chosen controls in
`discovery.md` and the accept/mitigate decisions in `decisions.md`; controls
become UAT guardrails and PRD requirements, not afterthoughts.

Update `CONTEXT.md` only when the grill resolves reusable domain glossary
language. Create or update ADRs under `docs/adr/` only when the
`grill` ADR threshold is met. Link those repo-level updates from
`decisions.md`; do not treat `CONTEXT.md` or `docs/adr/` as the slice artifact.

### 3. Write UAT before PRD

Load `$uat` before writing the PRD. Use the grilled context to define the
outside-in acceptance surface: what a human sees, does, verifies, and should not
mistake for a bug.

The point of writing UAT here is alignment. The human should be able to read the
UAT and confirm: yes, this is how the feature should work from a user's
perspective. If that is true, treat it as evidence that the discovery and
decisions are good enough to turn into a PRD. If it is not true, return to the
grill and fix discovery or decisions before writing the PRD.

Write `.planning/{NNNN-feature-slug}/uat.md` unless the user asks for another
location. Make the UAT concrete enough to prove shared understanding before any
implementation plan hardens.

**STOP HERE and ask the human.** Present the UAT and get an explicit "yes,
this is how it should behave" before writing the PRD. Do not proceed on
momentum or inferred approval — the UAT is the alignment gate, and skipping
the human's read defeats its purpose.

The UAT should answer:

- What user-visible workflow proves the slice works?
- What durable side effects must exist or explicitly not exist?
- What guardrails, non-goals, and environment gotchas matter?
- What single pass criterion makes the PR demo-ready?

### 4. Write the PRD from discovery and decisions

Load `$prd` after the UAT is agreed or at least stable enough to guide
acceptance. The PRD is grounded in the grill output: discovery, decisions,
shared domain language, and code evidence. Use the UAT as the human-approved
user-perspective contract that keeps the PRD honest about observable behavior
and pass criteria.

If the PRD and UAT disagree, do not force one to fit the other. Revisit the
upstream artifact that is wrong: discovery may be incomplete, a decision may be
unclear, or the UAT may have accepted the wrong behavior. Resolve the mismatch
before moving on.

Write `.planning/{NNNN-feature-slug}/prd.md` unless the user asks for another
location. Ground it in:

- `.planning/{NNNN-feature-slug}/discovery.md`.
- `.planning/{NNNN-feature-slug}/decisions.md`.
- `CONTEXT.md` terms when the slice relies on shared domain language.
- Relevant ADRs when the slice relies on durable architecture decisions.
- The UAT file by path as acceptance guidance.
- Existing code and module boundaries.
- Explicit non-goals and follow-up slices.

If the work needs multiple PRs, record the slice shape in the PRD and name the
branch order.

### 5. Produce the bootstrap prompt

Write `.planning/{NNNN-feature-slug}/bootstrap.md` only after discovery,
decisions, UAT, and PRD are coherent enough for a fresh implementation session.

The bootstrap is not another PRD. It is the cold-start prompt for a clean
context. Reference artifacts by path instead of inlining them.

Include:

- A short statement of what is being built.
- The artifact read order with one line explaining each path.
- Decisions and constraints that must not be violated.
- The intended PR or branch sequence when the work is split.
- Implementation pointers that were verified from code.
- Any repo-specific zone skills to load before editing relevant areas.
- Required verification gates from `AGENTS.md`.
- Environment gotchas needed to smoke-test the slice.
- Out-of-scope work and follow-ups.
- A final instruction to execute from the documents, not conversation memory.

If the bootstrap cannot be written cleanly, stop and fix the upstream artifact
that is vague or contradictory.

### 6. Adversarial review before handoff

After the bootstrap is written, run an adversarial pass over the full artifact
set before sending the user into a fresh context. Do not treat the bootstrap as
the completed handoff. The reviewer's job is to break the plan, not to polish
prose. Use a fresh-context subagent when available so the review is not
contaminated by conversation memory.

- Read the artifacts cold, in the bootstrap's stated read order.
- Hunt for contradictions between discovery, decisions, UAT, PRD, and
  bootstrap.
- Challenge every implementation pointer that is not backed by code evidence —
  verify it against the codebase or remove it.
- Probe for gaps a cold agent would trip on: missing constraints, unstated
  environment setup, acceptance criteria that cannot actually be observed.
- Ask the closing question: could a fresh context implement this without
  asking the user anything the artifacts should have answered?
- Tag each finding blocking or non-blocking: blocking means a genuine gap a
  cold implementer cannot resolve alone; a judgement call an implementer can
  reasonably make is non-blocking.

Route each finding to the upstream artifact that is wrong and fix it there —
do not patch over it in the bootstrap. The review passes when it stops
producing blocking findings.

Keep the loop short. Give the second and later reviewers the previous report
so they re-verify its pointers quickly and spend their effort hunting beyond
it; a cold read of the artifacts is still required, but a cold re-derivation
of every pointer is not. Cap the loop at three passes: if the third pass still
produces blocking findings, fix them, tell the human the count and the trend,
and proceed to step 7 anyway — the implementation subagent's first report is
the next review, and it is cheaper than a fourth cold read. When a pass finds
only document contradictions or pointer drift, fix and proceed without
another pass.

Report the outcome to the human in one or two lines before any implementation
begins:

- If blocking findings remain, say planning is not ready, summarize the
  blockers, fix the upstream artifacts, and rerun the adversarial review.
- When the review passes, say so, give the bootstrap path, and continue
  straight into step 7. Do not end the turn waiting for a manual handoff.

Never implement in the planning context itself. The planning context is the
orchestrator and reviewer; implementation always runs in a fresh context.

### 7. Orchestrate implementation from the planning context

The planning model is the frontier, deep-thinking model. It does not stop,
clear, and ask the human to paste the bootstrap. Once the adversarial review
passes and the human has been told, the planner provisions the implementation
itself and stays in the loop as reviewer:

1. **Provision a fresh implementation subagent.** Spawn a subagent with no
   conversation context (never a fork) on a cheaper, implementation-tier model
   (capable, but geared to building rather than planning; the repo or the
   user's memory may name it). Its entire prompt is: the bootstrap path, the
   PR or branch it is responsible for, the branch to start from, and the
   instruction to execute from the documents and report back with the branch,
   the diff summary, and verification results. Give it a worktree when the
   planning context's own tree must stay clean.
2. **Let it implement.** It completes the work for its PR, runs the
   repository's verification gates from `AGENTS.md`, and reports. If the docs
   are insufficient to implement cold, it says so instead of guessing; the
   planner fixes the upstream artifact and re-dispatches.
3. **Review from the planning context.** When the subagent reports, the planner
   reviews the branch or diff against its integration branch: load `$review`
   in a fresh-context review subagent when available, giving it the bootstrap
   path and raw review scope, never the implementer's conclusions; otherwise
   the planner runs `$review` itself and discloses that the review was not
   independent. The implementer never reviews its own work.
4. **Loop fixes through new subagents.** Every **Request changes** finding goes
   to a *new* fresh implementation subagent with the branch, the findings, and
   the bootstrap path. It fixes, reruns the gates, and reports. The planner
   reviews again. Repeat until the review returns **APPROVE** with no Request
   changes findings.
5. **Preserve and report.** Accepted non-blocking findings go to the slice's
   `follow-ups.md` using the `$review` skill's durable-follow-up rules. Report
   the review scope, verdict, verification results, and remaining warnings to
   the human, then move to the next PR in the sequence the same way.

A lower-tier or non-frontier planning model should not orchestrate; it stops
after step 6, reports the pass, and hands the bootstrap path to the human for a
fresh frontier or implementation context.

The human can interrupt at any point; the loop is a default, not a lock. Never
push or open a pull request from a subagent unless the human asked for it in
the slice; the `$pr` skill runs when the human says to ship.

## Follow-ups

Maintain `.planning/{NNNN-feature-slug}/follow-ups.md` throughout planning and
implementation. Use it for real findings that should survive the current
session but do not belong in the current slice:

- Bugs discovered while testing or reading adjacent code.
- Deferred slice ideas.
- Product questions.
- Cleanup or refactor notes.
- Environment and testing notes.

Keep each item dated and specific enough to pick up cold. Remove an item only
when it is scheduled into a slice or explicitly rejected.

Use this section order:

- Bugs Discovered
- Deferred Slice Ideas
- Product Questions
- Cleanup / Refactor Notes
- Environment / Testing Notes

## Midstream Rules

- Resume from existing artifacts in pipeline order.
- Do not regenerate an approved artifact unprompted; amend it when it is stale.
- Prefer `.planning/{NNNN-feature-slug}/` artifacts for active PR work.
- Put durable architecture decisions in ADRs, not in bootstrap prose alone.
- Track deferred slices in `.planning/{NNNN-feature-slug}/follow-ups.md` when
  they are real but out of the current PR.
- Keep implementation out of scope until the bootstrap is ready, unless the
  user explicitly asks to skip planning.
- Implementation always runs in a fresh subagent context; the planning context
  orchestrates and reviews, and routes each round of fixes to a new subagent.

## Artifact Map

| Step                     | Artifact                                      |
| ------------------------ | --------------------------------------------- |
| Discovery                | `.planning/{NNNN-feature-slug}/discovery.md`  |
| Decisions                | `.planning/{NNNN-feature-slug}/decisions.md`  |
| UAT                      | `.planning/{NNNN-feature-slug}/uat.md`        |
| PRD                      | `.planning/{NNNN-feature-slug}/prd.md`        |
| Bootstrap                | `.planning/{NNNN-feature-slug}/bootstrap.md`  |
| Deferred work            | `.planning/{NNNN-feature-slug}/follow-ups.md` |
| Visual target (optional) | `.planning/{NNNN-feature-slug}/mock/`         |

## Done Criteria

Planning is ready when discovery, decisions, UAT, PRD, follow-ups, and
bootstrap agree on scope, terms, acceptance, non-goals, and branch order, and
the adversarial review has stopped producing blocking findings. The planner
reports that pass to the human and then provisions implementation itself
(step 7); it does not wait for a manual handoff.

Implementation is done for a PR only after the relevant code is complete, the
repo's verification gates (from `AGENTS.md`) pass, and the latest `$review`
pass, run from the planning context over a fresh implementation subagent's
work, returns **APPROVE** with no Request changes findings.
