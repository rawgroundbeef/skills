---
name: pr
description: Write and publish clear pull requests, triage review feedback, and babysit a PR through bot reviews and CI. Use when opening or updating a PR, responding to review comments, or asked to babysit a PR until reviewers are satisfied.
---

# PR title & description

Write for a nontechnical teammate by default. They should understand the
problem and resulting behavior without knowing the implementation or reading
the conversation. Ground change claims in the final diff and validation claims
in actual results. Respect the user's chosen format and required repo template.

## When invoked

1. Identify the branch and its base. Base = the repo's default branch unless
   the branch was cut from another base or the user names one. Detect it with
   `gh repo view --json defaultBranchRef -q .defaultBranchRef.name` (fallback:
   `git symbolic-ref --short refs/remotes/origin/HEAD`).
2. Gather the evidence and writing requirements:
   - `git diff {base}...HEAD --stat`, plus the hunks needed to ground claims
   - `git log {base}..HEAD --oneline` (scope check only — never narrate it)
   - `gh pr list --state merged --limit 5` (match the repo's house title style)
   - The repo's PR template and the user's audience or format preferences
   - Actual check output, test logs, CI results, or recorded manual verification;
     distinguish completed checks from suggested verification
   - **If** the branch includes planning docs (e.g. a `.planning/{NNNN-slug}/`
     folder from the `slice` skill), read them for intent and deferred work —
     confirm what shipped against the diff. Use linked issues and surrounding
     code when needed to understand the problem; don't narrate the work session.

## Description guidance

Open with the concrete problem and result: what triggers it, what goes wrong
for the affected person, and what happens after this change. For work without a
direct UI effect, explain who it helps and why, such as a developer whose build
fails. Do not invent a user-facing effect for an internal change.

Scale the detail to the change. A simple PR usually needs one or two short
paragraphs and a concise testing summary. Use headings and bullets when they
help, or when the user's format or repo template requires them. Useful details
include:

- **What changes:** the behavior a reviewer needs to assess. Explain necessary
  technical terms in context; include identifiers, protocols, or implementation
  detail only when they help assess correctness, compatibility, or a tradeoff.
- **Testing:** what was checked, the actual result, and a results link when
  available. Summarize routine checks instead of dumping commands. Include an
  exact command when it helps reproduce a relevant result. State material
  failures, checks not run, and limits of the evidence without implying a pass.
- **Context and follow-ups:** enough explanation to understand the change on
  its own, with links for depth. Mention deferred work or limitations when they
  affect the review; skip empty sections and unrelated exclusions.

Keep explanatory context even when a reviewer could reconstruct it from the
diff or linked docs. Remove repetition, file inventories, work-session history,
and abandoned approaches that do not explain a current tradeoff.

## Title guidance

Written LAST, after the description and the verify pass — a title written at
branch creation describes the plan, not the result.

- Aim for ≤ 70 characters and imperative mood, respecting the user's format
  and the repo's required prefix style.
- Name the main concrete problem or resulting behavior in familiar words.
  Keep internal abstractions out of the headline unless they are the subject
  the intended audience needs to recognize.
- Read the title on its own: could a teammate understand what changed without
  knowing the codebase?

### Example

Before: `fix(agent): preserve sandbox failures during workspace staging`

After: `fix: stop failed review setup from being marked complete`

Opening: "Before a review starts, Joymore copies the documents into a temporary
workspace. A technical problem with that workspace could be mistaken for a
missing file, allowing preparation to be marked complete with documents left
out. This fix makes preparation fail when the workspace still cannot accept
the files after retrying."

## Verify pass

Re-read the final diff and verification evidence, then check:

1. The title and opening explain the main problem and result in plain language.
2. Change claims match the final diff. Test claims match actual logs or results;
   adding a test does not prove it passed. No stale claims from earlier plans.
3. Technical detail earns its place by helping the reviewer assess the change.
4. The description stands on its own, without repetition or a retelling of the
   implementation process. Necessary context survives the brevity pass.
5. Material changes outside the branch's main purpose are mentioned briefly.
6. The user's chosen format and required repo template are preserved.

## Ship

- Push the branch (`git push -u origin HEAD` if it has no upstream yet), then
  `gh pr create --base {base}` — or `gh pr edit` when a PR already exists —
  with the final title and body.
- End the body with the repo's attribution footer if it uses one.
- Report the PR URL, the final title, and which verify-pass rules forced edits.

## Review feedback triage

When review comments land on an open PR, run this loop without waiting for
per-comment instructions.

Treat requests such as "triage the PR feedback" as authorization to execute
this entire loop, including in-scope fixes, thread replies and resolutions,
committing, and pushing. Stop after classification only when the user explicitly
asks for read-only triage or a feedback summary.

**Acknowledge every comment on its own thread.** Acting on feedback without a
thread reply leaves the reviewer unable to see what happened and why; silent
action is never an option.

1. Fetch every unresolved inline comment and review body:
   `gh api repos/{owner}/{repo}/pulls/{N}/comments --paginate` and
   `gh pr view {N} --json reviews`, then read the PR's GraphQL `reviewThreads`
   for each thread's resolution state and ID.
2. Triage each comment into exactly one bucket:
   - **Address** — the finding is real and belongs in this PR. Verify the
     suggestion against the final diff and runtime semantics; implement the
     right shape rather than blindly applying a suggested patch. Run the
     affected tests and the repo's checks proportionate to the change. Reply
     with the commit SHA and, when the fix differs from the suggestion, one
     sentence saying why. Resolve the thread.
   - **Defer** — the concern is real but out of scope. Reply with the scope
     reasoning and record the deferred work durably (follow-ups doc or a
     tracked issue), then resolve the thread.
   - **Dismiss** — the concern doesn't apply, conflicts with a recorded
     decision, or is unjustified gold-plating. Reply with the concrete reason;
     add no follow-up. Resolve the thread.
3. Put replies on the inline comment's own thread with
   `gh api repos/{owner}/{repo}/pulls/{N}/comments/{id}/replies -f body=…`,
   never as detached top-level PR comments.
4. Resolve replied-to threads with GraphQL `resolveReviewThread` using the IDs
   from `reviewThreads`. Leave a thread open only when genuinely waiting on the
   reviewer to answer.
5. Push once after all fixes and doc updates are committed. Report each
   comment's bucket, what changed, the commit SHA, and the reasoning.

## Babysit a PR

"Babysit the PR" means actively repeat review requests, triage, fixes, replies,
and verification until the current revision has sufficient positive evidence
from Cursor Bugbot, Copilot, and Greptile, plus passing required CI. It is not
a one-time review or a promise to monitor after ending the turn.

Read [references/babysitting.md](references/babysitting.md) for reviewer triggers,
affordable sub-agent delegation, completion criteria, and exception handling.
The parent agent owns decisions and thread resolutions. Target Greptile 5/5;
do not manufacture a clean result by repeatedly dismissing valid findings.
Babysitting does not authorize merging unless the user also asks to merge.
