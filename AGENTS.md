# AGENTS.md — READ THIS FIRST, EVERY SESSION

Project: **StudyMate** — source-grounded, adaptive AI study companion
(Multimodal AI Hackathon 2026, Track D: Personalized Tutoring & Adaptive Learning)

You are building this project with limited credits and possibly across
several different accounts. The repository is the ONLY memory that
survives. Treat these rules as binding.

## 0. Session start routine (always, in this order)
1. Read `docs/PROGRESS.md` completely. It says what is done, what is
   in progress, and the exact NEXT ACTION.
2. Read `docs/SPEC.md` sections relevant to the NEXT ACTION only
   (do not re-read everything; it wastes credits).
3. If the NEXT ACTION touches any screen, read `docs/UI_UX.md`.
4. Run `make verify` (or `bash scripts/verify.sh`). It prints which
   subsystems currently work. Trust it over any written claim.
5. Tell the user in 3 lines: what is done, what you will do now, what
   could block you. Then start.

## 1. Session end routine (also when you suspect credits are low)
1. Make the code run again (no half-edited broken state). If a change
   is too big to finish, revert it with `git stash` or `git checkout`
   and note it in PROGRESS.md.
2. Update `docs/PROGRESS.md`: tick finished items, update "Current
   state", write the precise "NEXT ACTION", append a session log entry.
3. `git add -A && git commit -m "<milestone>: <what changed>"`.
4. Tell the user: "Safe to export now" and give the one-line resume
   prompt from `docs/HANDOFF.md`.

Commit after EVERY finished task, not just at session end. Credits can
run out without warning.

## 2. Credit-saving rules
- Work in **vertical slices** (backend endpoint + UI + test for one
  feature) rather than building all backends first.
- Never rewrite a whole file for a small change. Edit in place.
- Do not regenerate boilerplate that already exists. Search first.
- Do not run long installs/builds repeatedly; reuse the existing venv
  and `node_modules`.
- All LLM calls go through `backend/app/llm/client.py` which has a
  disk cache (`LLM_MODE=cache` default in dev). Identical prompts are
  never paid for twice. Use `LLM_MODE=live` only for ingestion of the
  demo corpus, final evaluation runs, and the demo recording.
- Precompute and COMMIT the demo corpus ingestion output
  (`data/demo/processed/`) so a fresh account never needs to re-ingest.
- Prefer small/fast models for bulk work (tagging, extraction); use the
  stronger model only for tutoring answers, question generation and
  verification. Model names live in `.env` — never hard-code them.
- Do not ask the user questions you can answer from the docs. Make a
  reasonable decision, write it to `docs/DECISIONS.md` (one line), and
  continue.

## 3. Non-negotiable product rules
1. Every explanation or answer shown to a student carries citations to
   stored content units, and every citation opens the exact page / slide
   / video timestamp. A citation that cannot open is a bug.
2. If the course material does not support an answer, the app says so
   and separates any outside knowledge in a clearly labelled block.
3. Every quiz question has: topic, concept, source location,
   difficulty, verified answer key, explanation with citation.
   Unverified questions are never shown to students.
4. Mastery is updated only through the learner model code
   (`backend/app/learner/`), never by ad-hoc code in endpoints.
5. All numbers shown in the Evaluation dashboard come from real runs
   saved in `eval/results/`. Never hard-code or invent metrics.
6. The app must work end-to-end on the committed demo corpus with no
   manual steps beyond `make dev`.

## 4. What to AVOID (hard list)
- No auth providers, payments, social features, notifications, mobile
  apps, multi-tenant admin. Use a single local "student profile"
  switcher (multiple profiles allowed, no passwords).
- No Postgres, Redis, Docker-compose orchestration, Kubernetes,
  message queues. Use SQLite + local vector store + a simple
  background-task runner. Docker is optional and last.
- No fine-tuning or training of models.
- No new UI libraries beyond those listed in `docs/SPEC.md` §3.
- No placeholder text such as "Lorem ipsum", "TODO", fake charts, or
  fake data in any shipped screen. Every screen shows real state or a
  designed empty state.
- No silent failures: every async action has loading, success, and
  error states (see `docs/UI_UX.md` §9).
- No features from the "Later/Skip" list until milestones M0–M9 are
  ticked in PROGRESS.md.
- Do not change the folder structure, API contract or data model
  without recording the change in `docs/DECISIONS.md` and updating
  `docs/SPEC.md`.
- Do not commit secrets. `.env` is git-ignored; `.env.example` is
  committed.
- Do not claim something works unless `make verify` or a test proves it.

## 5. Where things live
```
AGENTS.md                 this file
docs/SPEC.md              full technical specification
docs/UI_UX.md             complete UI/UX specification
docs/PROGRESS.md          live tracker — UPDATE CONSTANTLY
docs/DECISIONS.md         one-line decisions log
docs/HANDOFF.md           how to move to another account
backend/                  FastAPI app (see SPEC §4)
frontend/                 Next.js app (see UI_UX)
eval/                     test sets, runners, results
data/demo/                demo corpus (raw + processed)
scripts/                  verify.sh, seed.sh, export.sh
```
