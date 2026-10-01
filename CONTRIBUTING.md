# Contributing

Keep changes focused on reusable Rhino/GH Python workflows. Put project-specific geometry contracts, private paths and individual delivery policies in the consuming project.

## Report an issue

Include the Rhino build, operating system, Python component type, relevant source/specs, reproduction steps, expected and actual behavior, and current runtime messages or `Debug` output. A small `.gh` example is useful when it can be shared. Remove private paths and data before posting.

For port issues, say whether the component was fresh, already connected, or restored from disk. Include the old and new port declarations and whether any affected port contains persistent data.

## Propose a change

- Explain the concrete behavior changed and why.
- Keep `SKILL.md` concise; put conditional detail in the corresponding reference.
- Keep reference code and agent instructions in English; update both README languages when their user-facing behavior changes.
- Preserve stable loader paths, compatible parameter objects and current-run diagnostics.
- Document any third-party code you adapt and preserve its required notices.

Run the relevant existing checks from the repository root:

```sh
python scripts/check_loader.py
python scripts/check_starter.py
python scripts/check_examples.py
```

For documentation-only changes, check links and consistency. For behavior changes, add a focused regression case when warranted. Port/runtime changes also need real GH validation: a fresh instance, a connected instance, repeated solves and save/reopen. State which checks ran and which remain unavailable. Passing substitute tests must not be reported as live Rhino validation.

Before proposing changes to an installed skill, work in a recoverable source checkout. Do not include caches, generated local loaders, personal configuration or runtime output in a contribution.
