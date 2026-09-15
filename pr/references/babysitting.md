# PR babysitting

## Scope and ownership

Treat a request to **babysit a PR** as authorization to request the configured
review bots, monitor their reviews and CI, delegate in-scope fixes, test,
commit, push, reply to feedback, and resolve handled threads. Continue the
loop until the completion criteria below are met. Merging remains a separate
action requiring user authorization.

The parent is the decider. Validate each finding against the actual code and
product requirements before assigning a fix. A bot's severity or suggested
patch is evidence to investigate, not an instruction to obey. Follow the main
skill's Address / Defer / Dismiss rules. Do not add speculative infrastructure
or change intended product behavior just to raise a review score.

## Start and request reviews

1. Record the PR URL, base, current head SHA, required checks, and reviewer
   identities. Read all review bodies, inline threads, summary comments, and
   failed check logs. Paginate; resolved or outdated findings may still explain
   a current review verdict.
2. The usual reviewers are **Cursor Bugbot, Copilot, and Greptile**. "Cursor
   Bug" and "Cursor Bugbot" normally name the same integration; confirm the
   repository's actual accounts rather than tagging a fourth invented bot.
3. Use completed reviews of the current head as the initial round. Request any
   missing reviews. After pushing fixes, request a fresh review from each bot
   that does not automatically start one. Avoid duplicate requests while a
   matching review is running.

Known trigger mechanisms (verify against the installed integration if these
stop working):

| Reviewer | Request |
| --- | --- |
| Cursor Bugbot | A standalone PR comment `cursor review` or `bugbot run`. Do not use a generic Cursor coding-agent request. |
| Copilot | Request `copilot-pull-request-reviewer[bot]` through GitHub's review-request API or reviewer picker. An `@copilot` comment can start coding work instead of code review. |
| Greptile | Use the integration's working mention or its **Re-trigger Greptile** control. Joymore has used `@greptile review`; current public docs also describe `@greptileai review this`. Confirm an actual review starts. |

Sources: [Cursor triggers](https://prod.cursor.com/docs/bugbot),
[Copilot review requests](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/copilot-code-review),
[Greptile triggers](https://www.greptile.com/docs/code-review/first-pr-review).

Use structured API inputs or a body file for comments. Do not post a draft
reply to the wrong thread or confuse a successful request with a completed
review.

## Fix and reassess

- Delegate accepted fixes to an affordable, capable sub-agent. Prefer the
  lowest-cost available coding model suited to the task; escalate only when
  complexity or a failed attempt warrants it. Give each agent the exact
  finding, affected files, required behavior, and focused validation. Parallel
  agents need non-overlapping ownership. Respect repository worktree rules.
- The parent inspects the resulting diff and test evidence. Agents may argue
  that a finding is invalid; the parent decides. Shared files, migrations,
  generated artifacts, commits, pushes, and external replies remain centrally
  coordinated unless explicitly assigned.
- Run relevant regression tests and repository-required checks. Investigate
  failing CI even when a bot calls the PR clean. A skipped deployment does not
  prove the application built or deployed successfully.
- Push a coherent batch. Reply on each original finding with the disposition,
  concrete reason, and fix commit when applicable. Resolve addressed threads
  after the fix is pushed and verified. Dismiss false positives with a clear
  explanation, then resolve the thread. Record deferred work durably; leave a
  thread open when a real issue or unanswered question still blocks progress.
- Re-request reviews as needed and repeat. A new commit makes older approval
  evidence insufficient for the changed code. Verify which head each review
  actually covers.

## Completion evidence

The normal target is all of the following on the final head:

- Required CI passes, with no unresolved actionable findings.
- **Greptile: 5/5 confidence**, with no remaining issues that contradict it.
- **Cursor Bugbot: a completed clean review**, such as no bugs found. A neutral
  check is sufficient only when its review output and findings support that
  interpretation.
- **Copilot: a completed review with no changes needed**, or its equivalent
  positive assessment. Copilot may submit `COMMENTED` rather than a formal
  `APPROVED` review; read the content.

Silence, an old review, an accepted trigger, or manually resolving every
thread is not positive review evidence.

A lower Greptile score is an exception, not a shortcut. If a fresh review still
scores 4/5 or 3/5 solely because of specific findings the parent can demonstrate
are false positives or intentionally deferred, document each disposition,
explain why another iteration would not improve correctness, and report the
lower score explicitly. Do not repeatedly dismiss valid concerns to end the
loop, weaken review settings, or describe the result as 5/5.

## Waiting, blockers, and handoff

While reviews run, continue independent useful work and check for new feedback
at a reasonable cadence. Use short interruptible waits and keep the user
informed; do not spam triggers or busy-poll. Persist the head SHA, per-reviewer
status, thread dispositions, outstanding work, and next step in a local
checkpoint so context compaction does not restart the cycle.

If a reviewer is unavailable, a quota or permission prevents a review, or the
same unchanged result recurs after a justified retry, investigate the blocker
and avoid endless requests with no new evidence. Finish independent work, then
report the exact missing evidence and what must change. Never call that a clean
review or claim monitoring will continue after the turn ends.

On completion, report the PR link, final head, CI result, each reviewer's
verdict/score, and any exceptions. Merge only when separately authorized.
