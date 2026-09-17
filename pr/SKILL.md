---
name: pr
description: Write and publish clear pull requests, triage review feedback, and babysit a PR through bot reviews and CI. Use when opening or updating a PR, responding to review comments, or asked to get a PR reviewed, babysit it, or ship it when green. Merge only with explicit user authorization for that PR.
---

# PR title & description

Write for a nontechnical teammate by default. They should understand the
problem and resulting behavior without knowing the implementation or reading
the conversation. Ground change claims in the final diff and validation claims
in actual results. Respect the user's chosen format and required repo template.

## Match the requested work

- A request for wording or a read-only review stays read-only. Opening or
  updating a PR alone does not request babysitting.
- "Get it reviewed," "babysit it," and "ship/merge when green" request the
  active review-and-CI loop below. Continue through findings and checks instead
  of stopping after opening the PR or requesting a review.
- Merge only with explicit authorization for this PR. An earlier instruction
  such as "merge when green" or "ship this PR when green" remains valid while
  the scope is unchanged; do not ask again once its conditions are met.
  Opening, reviewing, or babysitting a PR does not by itself authorize merging it.

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
   - Repository instructions, including required checks and merge conventions
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

Translate implementation terms into the concrete thing the reader recognizes.
Explain necessary mechanics after the problem and result; naming the code is
not an explanation.

For a product change, make the opening a plain-language before/after. Do not
pack it with detector names, numeric versions, or internal limits just because
they appear in the diff. Put material implementation details in a separate
sentence or note and explain why they matter. The evidence grounds the claims;
it is not a checklist of facts the description must repeat.

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

Before: `fix: exclude review handoffs from automation evidence`

After: `fix: stop automatic review messages from prompting suggestions`

Opening: "Joymore's automatic messages after a compliance review were being
mistaken for customer requests and producing misleading automation suggestions.
This change excludes those automatic messages while keeping genuine customer
requests eligible."

## Verify pass

Re-read the final diff and verification evidence, then check:

1. A teammate unfamiliar with the code can explain the problem and result from
   the title and opening alone. Replace unexplained internal terms before
   publishing.
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
- When review or conditional shipping was requested, continue into the
  babysitting loop; publication is not the end of that task.

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
     affected tests and the repo's required checks. Prepare a reply with the
     fix commit and, when the fix differs from the suggestion, one sentence why.
   - **Defer** — the concern is real but out of scope. Reply with the scope
     reasoning and record the deferred work durably (follow-ups doc or a
     tracked issue).
   - **Dismiss** — the concern doesn't apply, conflicts with a recorded
     decision, or is unjustified gold-plating. Reply with the concrete reason;
     add no follow-up.
3. If fixes or doc changes are needed, commit and push one coherent batch after
   validation. Never resolve an addressed finding while its fix exists only locally.
4. Put replies on the inline comment's own thread with
   `gh api repos/{owner}/{repo}/pulls/{N}/comments/{id}/replies -f body=…`,
   never as detached top-level PR comments.
5. Resolve replied-to threads with GraphQL `resolveReviewThread` using the IDs
   from `reviewThreads`. Leave a thread open only when genuinely waiting on the
   reviewer to answer.
6. Report each comment's bucket, what changed, the commit SHA, and the reasoning.

## Babysit a PR

"Babysit the PR" means actively request the configured reviews, triage, fix,
reply, and verify until each bot has its required positive verdict for this PR,
all actionable findings are handled, the parent has reviewed the final diff,
and required CI passes on the current head. A new commit does not erase an
earned positive bot verdict. It is not a one-time review or a promise to
monitor after ending the turn. Stop manually requesting a bot once it gives a
positive review for this PR; later commits do not change that status.

Read [references/babysitting.md](references/babysitting.md) for reviewer triggers,
affordable sub-agent delegation, completion criteria, and exception handling.
The parent agent owns decisions and thread resolutions. Target Greptile 5/5;
do not manufacture a clean result by repeatedly dismissing valid findings.
Babysitting does not authorize merging unless the user also asks to merge.
When that authorization is already present, complete the merge after the
review and CI conditions are met; follow the reference's merge procedure.
