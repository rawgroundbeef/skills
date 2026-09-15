# PR

Write plain-language pull request copy, publish the branch, and close the loop
on review feedback.

The default reader is a nontechnical teammate. Titles name the concrete problem
or behavior, and descriptions explain the trigger, consequence, and result.
Change claims stay grounded in the final diff; testing summaries use actual
results. The skill preserves the user's format and required repo template,
with technical detail where it helps a reviewer assess the change.

## What it handles

- Plain-language PR titles written after the diff is final.
- Concise descriptions with useful context, testing evidence, and material limitations.
- Branch push plus PR creation or update.
- Review-comment triage into **Address**, **Defer**, or **Dismiss**.
- A reply and resolution on every original review thread.
- PR babysitting: affordable sub-agent fixes and repeated Cursor Bugbot,
  Copilot, and Greptile reviews until the current revision has positive review
  evidence and passing CI, normally including Greptile 5/5.

## Try it

```text
Use $pr to write and open the pull request from the final diff.
```

```text
Use $pr to triage the feedback on this pull request.
```

```text
Babysit PR #453 until the reviewers are satisfied.
```

Babysitting leaves the merge to the user unless merging is also authorized.

The executable workflow lives in [SKILL.md](./SKILL.md).
