# PROGRESS — live tracker (UPDATE AFTER EVERY TASK)

> Any Antigravity session on any account must read this file first and
> update it before ending. This file is the project's memory.

## Current state (rewrite this block every session)
- Last updated: 2026-10-10
- Last account/session: (n/a)
- Working branch/commit: (main)
- App runs with `make dev`: NO (nothing built yet)
- `make verify` result: (not run)
- Active milestone: **M1 PDF + PPTX ingestion**

## NEXT ACTION (be precise; one concrete task)
Create the repo skeleton exactly as in `AGENTS.md` §5 and `docs/SPEC.md`
§4, then implement M0: Makefile, `.env.example`, FastAPI `/health`,
Next.js app shell with sidebar/topbar/theme, SQLite models, LLM client
with disk cache, `scripts/verify.sh`. Commit as `M0: scaffold`.

## Milestone checklist
Mark `[x]` only when the acceptance test in SPEC §17 passes.

- [x] **M0 Scaffold** (repo, Makefile, env, health, app shell, LLM cache, verify)
  - [ ] repo structure + git init + .gitignore (.env, data/app.db, node_modules, .venv, data/llm_cache is COMMITTED)
  - [ ] Makefile targets: setup, dev, seed, verify, test, eval, export
  - [ ] backend: config, db, models, /health, LLM client + cache
  - [ ] frontend: AppShell, nav, theme (light/dark), course/student switcher stubs
  - [ ] scripts/verify.sh prints a subsystem status table
- [ ] **M1 PDF + PPTX ingestion** (units, locators, page/slide PNGs, viewer, upload UI, job progress)
- [ ] **M2 Video + figures** (transcription, keyframes, VLM figure understanding, video player + seek)
- [ ] **M3 Concept graph** (extraction, consolidation, prerequisite DAG, tagging)
- [ ] **M4 Retrieval + grounded tutor** (hybrid retrieval, citations, validation, refusal, chat UI + evidence panel)
- [ ] **M5 Learner model** (BKT, students, intake, diagnostic, dashboard heatmap, Why drawer)
- [ ] **M6 Assessment engine** (generation, verification, dedupe, quiz player, grading, feedback)
- [ ] **M7 Report + recommendations + remediation**
- [ ] **M8 Evaluation lab** (test set, RAG eval, simulated students, UI)
- [ ] **M9 Polish + demo mode + README + architecture diagram**
- [ ] M10 Course map polish + flashcards (optional)
- [ ] M11 Study schedule + Hinglish (optional)

## Screens status
| Screen | Built | Empty/Loading/Error states | Responsive | Dark mode | A11y pass |
|---|---|---|---|---|---|
| Onboarding | ☐ | ☐ | ☐ | ☐ | ☐ |
| Home / Dashboard | ☐ | ☐ | ☐ | ☐ | ☐ |
| Library | ☐ | ☐ | ☐ | ☐ | ☐ |
| Source detail | ☐ | ☐ | ☐ | ☐ | ☐ |
| Tutor | ☐ | ☐ | ☐ | ☐ | ☐ |
| Source Viewer Drawer | ☐ | ☐ | ☐ | ☐ | ☐ |
| Practice builder | ☐ | ☐ | ☐ | ☐ | ☐ |
| Quiz player | ☐ | ☐ | ☐ | ☐ | ☐ |
| Assessment report | ☐ | ☐ | ☐ | ☐ | ☐ |
| Course map | ☐ | ☐ | ☐ | ☐ | ☐ |
| Evaluation lab | ☐ | ☐ | ☐ | ☐ | ☐ |
| Settings | ☐ | ☐ | ☐ | ☐ | ☐ |

## Demo corpus status
- [ ] Sources chosen and licences recorded in `data/demo/SOURCES.md`
- [ ] Raw files placed in `data/demo/raw/` (or `scripts/fetch_demo.sh` works)
- [ ] Ingestion run in `LLM_MODE=live`; output exported to `data/demo/processed/`
- [ ] `make seed` restores everything without any API calls

## Evaluation status
- [ ] `eval/testsets/qa_testset.jsonl` (target ~75 items, human-checked)
- [ ] RAG metrics run (RAGAS/DeepEval) → `eval/results/latest.json`
- [ ] Citation/refusal deterministic metrics
- [ ] Assessment audit (≥40 questions)
- [ ] Simulated students (≥5 profiles × ≥6 sessions, adaptive vs static)

## Known issues / blockers
(none yet — add: date, description, workaround, whether it blocks)

## Open decisions
(none — decisions made go to `docs/DECISIONS.md`)

## Session log (newest first; one entry per session)
Template:
```
### YYYY-MM-DD HH:MM — account label (e.g. "acct-2")
- Done: ...
- Broke / reverted: ...
- Verified by: (make verify / test names)
- Credits: roughly how much was used / remaining signal
- Next: ...
```
(no sessions yet)
