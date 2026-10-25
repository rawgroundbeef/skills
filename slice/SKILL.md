---
name: slice
description: One-file planning for a change — brief, evidence, architecture check, decisions, threats when money or keys are involved, acceptance, build plan and bootstrap in a single plan.md — then fresh-context implementation and review orchestrated by the planner. Use when starting feature work, shaping a change, or preparing a fresh-context agent to implement from a durable document.
---

# Slice

One change, one plan file, one fresh implementer, one independent review.
The plan file is the source of truth once it exists; do not rely on
conversation memory after writing it, and do not add other planning files
unless they hold evidence (a mock, a captured log, a probe result).

The planner is the frontier, deep-thinking model. It writes the plan, spawns
the implementer, reviews the result and routes fixes. It never implements.
Implementation always runs in a fresh context on a cheaper, capable model
(the repo or the user's memory may name it). The implementer never reviews
its own work.

## Why one file

Multi-file pipelines (discovery, decisions, UAT, PRD, bootstrap, review
loops over prose) optimise each slice on its own surface and go stale
quickly. On memeputer-reboot they produced tools that were locally correct,
each with a passing eval, and jointly wrong: every slice added its own
pipeline, its own regexes, its own canned lines. The one thing those docs
earned was the decision log with reasons, which is what lets a later reader
trace a bug to the decision that caused it. Keep that; drop the ceremony;
add the check the pipeline never asked.

## The plan file

`.planning/{NNNN-slug}/plan.md`. `NNNN` is the next four-digit number after
the highest in `.planning/` (check remote branches too); the number belongs
to the change, not to its PRs. Create the directory with the plan; add
evidence files beside it only when they hold something prose cannot (a
mock image, a probe output, a transcript).

Write these sections, in this order. Short is fine; missing is not.

1. **Brief.** The ask in the person's own words, the date, who asked, and
   the integration-branch commit the plan was read against.
2. **Evidence.** What the code does today and what exists to reuse, cited
   by file path and symbol name, never by line number (lines go stale the
   week a file moves). Production facts when they shaped the plan, with
   how they were read. Say what was verified by reading and what is
   assumed.
3. **Architecture check.** Answer in a few lines, every time:
   - Which tool, module or route does this become or change?
   - What does it return to the caller (for an agent tool: facts the model
     needs for its next sentence, never a status word with a mandated
     line)?
   - On which turns, surfaces or callers is it offered, and is that set
     fixed?
   - What does the application enforce at the boundary (ids, amounts,
     authority, money), and does any of it parse the person's language?
     The answer to the last part must be "none"; if it is not, the plan
     is wrong.
4. **Decisions.** Numbered `D1`, `D2`, …: the choice, the reason, the
   alternative rejected. Mark the human's own decisions with their name
   and the date. Decisions win over every other section; when a later
   section disagrees, fix the later section.
5. **Threats.** Only when the change touches money, keys, secrets, auth,
   PII or adds a surface (endpoint, webhook, deep link, autonomous action):
   load the repo's `threat-model` skill and record assets, sinks, sources,
   ranked threats, the control for each and the residual. Controls become
   acceptance lines and build items, not afterthoughts.
6. **Acceptance.** Five to ten lines of observable behaviour a person can
   check, one pass criterion that makes the change demo-ready, explicit
   non-goals, and what cannot be tested in the available environment with
   its residual risk. No regression suite for unrelated areas.
7. **Build.** The PR sequence when there is more than one. For each PR:
   what changes, named by module and symbol; tests to add or extend; the
   verification gates from the repo's `AGENTS.md`; evals and their cost
   rule; environment gotchas (local services, flags, credentials by name
   only, things that must not be touched).
8. **Bootstrap.** One paragraph the implementer receives verbatim: read
   this file and `AGENTS.md`; the PR it owns and the branch base; execute
   from the document, stop and report rather than guess when the document
   is insufficient; the repo's standing rules (for memeputer-reboot: never
   kill processes it did not start, never stop or take over the running
   local stack, never push or open a pull request unless this plan says
   so); report back with the branch, a diff summary and the gate results.
9. **Follow-ups.** Dated items found along the way that do not belong in
   this change: bugs seen, deferred ideas, questions, cleanup, environment
   notes. Remove an item only when it is scheduled or rejected. After the
   change ships, add a dated "Shipped" line here with the PR numbers.

## Pipeline

1. **Grill while writing.** Challenge the ask against the code it lands on:
   open the schemas, the unique constraints, the dispatch and approval
   paths, the route allowlists, the persistence sites, and confirm the
   mechanism each decision assumes exists. Answer from code and docs
   wherever possible; ask the human only for decisions the repo cannot
   settle, and ask them together, with a recommendation first. Load the
   `grill` skill when the ask collides with existing domain language or an
   ADR; load `threat-model` for anything in section 5's list.
2. **Write `plan.md`** and commit it on a branch cut from the fetched
   integration branch (`plan/NNNN-slug`). Preserve unrelated local files.
3. **Report in two lines:** ready, or the decisions still needed. Do not
   wait for a manual handoff when it is ready.
4. **Implement.** Spawn a fresh-context subagent (never a fork) on the
   implementation-tier model with exactly the bootstrap paragraph and the
   plan path, in its own worktree cut from the integration branch. It
   builds its PR, runs the gates, and reports. If it says the plan is
   insufficient, fix the plan and dispatch a new implementer; never answer
   it from conversation memory.
5. **Review.** Run the `review` skill in a fresh-context subagent over the
   diff against the integration branch, giving it the plan path and the
   raw scope, never the implementer's conclusions. Every **Request
   changes** finding goes to a *new* implementer with the branch, the
   findings and the plan path. Repeat until **APPROVE**. Accepted
   non-blocking findings go to Follow-ups.
6. **Ship** by the repo's rules (`pr` skill, bot reviews, CI, merge
   policy), then record the outcome in Follow-ups and move to the next PR
   the same way.

## Midstream rules

- Amend the plan; never regenerate it. The human's decisions are not
  reopened without them.
- A finding from implementation or review that changes a decision goes
  into the plan first, then into code.
- Durable architecture decisions still go to ADRs; link them from the
  plan. Reusable glossary goes to `CONTEXT.md`.
- A lower-tier planning model stops after step 3 and hands the plan path
  to the human instead of orchestrating.
- The human can interrupt at any point; the loop is a default, not a lock.

## Done

Planning is ready when the plan's sections agree with each other and with
the code it cites. A PR is done when its code is complete, the repo's
gates pass, and an independent review of a fresh implementer's work
returns **APPROVE** with no Request changes findings.
