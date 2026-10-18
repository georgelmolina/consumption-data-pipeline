---
name: portfolio-audit
description: 'Use when reviewing, cleaning, or documenting code for a public portfolio or interview. Triggers on: "review my project for portfolio", "is this portfolio-ready", "prepare for GitHub", "clean up my code for review", "check my notebook structure", "rename variables for clarity", or any request to improve documentation, comments, naming, or readability for a professional audience. Always audit first and wait for explicit confirmation before making any change — this is a learning workflow, not an automated fixer.'
argument-hint: 'Target file or folder to polish (e.g. notebooks/merge.ipynb)'
---

# Portfolio audit

## Purpose

Prepare a data engineering or data analysis project for public portfolio publication.
The audience is recruiters and technical profiles reviewing a junior-to-mid level portfolio.
The work must demonstrate that the author understood what they built — clean, readable, and self-explanatory.

## Core Behavioral Rule — ALWAYS FOLLOW.

**Never proceed autonomously. This is a learning-driven workflow.**

Before making any change — no matter how small:

1. **Confirm scope** — which files or folders are in scope? Full review or one category only?
2. **Audit** all files in scope and list findings grouped by category.
3. **Present** the full audit. Do not make any change yet.
4. **Ask** which category to start with and wait for confirmation.
5. **For each finding:** explain the issue, the proposed fix, and *why it matters* for a portfolio.
6. **Wait for explicit approval** before applying any change.
7. After each change, ask whether to continue to the next finding or stop.

> The goal is not to deliver a polished file — it is to build the user's understanding of what makes code portfolio-ready, one decision at a time.

---

## Audit Categories

### Category 1 — Naming

**Notebooks:**
- Numbered with execution order prefix (`01_`, `02_`, etc.).
- Name reflects the step or purpose (e.g. `02_merge_products_consumption.ipynb`).
- No spaces in filenames — use underscores.

**Variables and DataFrames:**
- `snake_case`, descriptive — name reflects content, not version (`sales_df`, not `df2`).
- No abbreviations that require a comment to decode.
- Path variables prefixed with `path_` (e.g. `path_raw_data`).

**Functions:**
- Verb + noun pattern (`load_data`, `assign_category`, `build_mapping`).
- No single-letter names except standard loop indices (`i`, `j`).

---

### Category 2 — Comments and Docstrings

**Notebook cells:**
- Every code cell has a one-line comment stating what it does and why.
- Markdown section headers introduce each major step with 1–2 sentences of context for a reader who has never seen the project.

**Python functions (.py files):**
- Every function has a short docstring: what it does, what it takes, what it returns.
- Inline comments only for non-obvious logic — not for restating the code.

**config.yaml:**
- Each key has an inline comment explaining its purpose.

---

### Category 3 — Notebook Structure

Each notebook must be self-contained and follow this cell order:

```
[Markdown] — Title, purpose, inputs and outputs of this notebook
[Code]     — Imports
[Code]     — Config / path loading
[Code]     — Data load + basic sanity check
[Code]     — Transformation steps (one logical step per cell)
[Markdown] — Section headers between major steps
[Code]     — Export / save
```

Flag:
- Missing title cell.
- Imports not at the top.
- Variables assumed from a previous session (not defined in this notebook).
- Cells with no comment.
- Missing section headers between major steps.
- Notebook does not run clean top to bottom.

---

### Category 4 — Code Clarity

Flag only what a reader would genuinely find confusing:
- Hardcoded file paths (should be loaded from `config.yaml`).
- Magic numbers or strings with no named variable.
- `print()` used instead of `display()` for DataFrames in notebooks.
- Missing `index=False` on `.to_csv()` / `.to_excel()` exports.

Do not flag advanced refactoring patterns (abstracting functions, utils structure) — that is out of scope for a junior portfolio.

---

### Category 5 — README

A portfolio-ready project must have a `README.md` covering:
- Project title and one-paragraph description.
- Business context: what problem does the data solve?
- Data sources (anonymised if needed).
- Ordered list of notebooks with one-line descriptions.
- Setup: environment name, install command, how to run.

Flag any of the above that are missing or incomplete.

---

## Final Check

After all categories are done:
- Confirm no broken imports or cell errors introduced by renaming.
- Present a summary of all changes made.
- Ask if anything else needs attention before publishing.

---

## Tone

- Present findings as a senior peer review, not a list of errors.
- Explain the professional reason behind each suggestion.
- When a choice is debatable, present both options and the trade-off.
- If the user disagrees, accept it and move on.

---

## What This Skill Does Not Do

- Does not refactor business logic or change how transformations work.
- Does not optimise performance.
- Does not evaluate analytical correctness.
- Does not add functionality that was not already present.
4. **For each item:** explain the issue, explain the fix, explain *why it matters for a portfolio*, then ask for approval
5. **Apply** the change only after explicit confirmation
6. **Ask** whether to continue to the next item or stop

---

## What NOT to change
- Do not refactor working logic unless explicitly asked
- Do not add features or new analysis
- Do not alter data pipeline behavior
- Do not batch multiple changes in one step — one finding at a time