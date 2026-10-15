# HANDOFF — continuing on a different Antigravity account

The project is designed so a brand-new account with zero chat history
can continue exactly where the last one stopped. Everything needed is
in the repository.

## A. What carries over (and what does not)
Carries over (because it is files in the repo):
code · `docs/*` · `docs/PROGRESS.md` · `data/demo/processed/` ·
`data/llm_cache/` (cached LLM answers, so no repeated credit use) ·
`eval/results/` · git history.

Does NOT carry over:
chat history · API keys (`.env`) · `node_modules` · `.venv` ·
`data/app.db` (rebuilt by `make seed`) · large raw videos if you
excluded them.

## B. Before your credits run out (do this routinely)
1. Ask the agent: "Wrap up this session per AGENTS.md §1."
   It will make the app runnable, update PROGRESS.md, and commit.
2. Push to a private GitHub repo (best, safest):
   ```
   git remote add origin <your-private-repo-url>   # first time only
   git push -u origin main
   ```
3. Also make a zip backup (works even without GitHub):
   ```
   bash scripts/export.sh      # creates ../studymate-backup-<date>.zip
   ```
   The script should include: everything except `node_modules`,
   `.venv`, `.next`, `__pycache__`, `.env`, and `data/app.db`.
   It must INCLUDE `data/llm_cache/` and `data/demo/processed/`.
4. Save your `.env` values somewhere private (password manager). Never
   put them in the repo.

## C. Resuming on a new account
1. Open Antigravity with the new account and open the project:
   - From GitHub: clone the repo, or
   - From zip: unzip and open the folder.
2. Create `.env` from `.env.example` and paste your keys.
3. Run:
   ```
   make setup      # installs backend + frontend deps
   make seed       # restores DB + vector store from data/demo/processed (no API calls)
   make verify     # prints what works right now
   ```
4. Paste the **Resume prompt** (below) into the Antigravity agent.
5. Let it read PROGRESS.md and continue from NEXT ACTION.

### Resume prompt (copy-paste, always works)
```
You are continuing an existing project called StudyMate in this
workspace. Do not start from scratch and do not re-plan.
1. Read AGENTS.md fully and follow it as binding rules.
2. Read docs/PROGRESS.md fully. Find "NEXT ACTION" and the milestone
   checklist.
3. Run `make verify` and compare its output with PROGRESS.md. If they
   disagree, trust `make verify`, fix PROGRESS.md, and tell me.
4. Read only the sections of docs/SPEC.md and docs/UI_UX.md needed for
   the NEXT ACTION.
5. In 3 lines, tell me: what is done, what you will do now, any
   blockers. Then continue building. Commit after each finished task
   and update docs/PROGRESS.md as you go.
Save credits: edit files in place, reuse the LLM cache, no big
rewrites, no new libraries beyond SPEC §3.
```

### Resume prompt for first-ever session (brand-new empty workspace)
```
Create the StudyMate project in this empty workspace using the files
AGENTS.md and docs/*.md that I have placed here. Read AGENTS.md, then
docs/PROGRESS.md, then start M0 exactly as NEXT ACTION says. Commit
after each task. Update docs/PROGRESS.md before you stop.
```

### Emergency prompt (credits almost gone)
```
Credits are nearly finished. Stop new work. Make sure the app still
runs, update docs/PROGRESS.md (Current state, NEXT ACTION, Known
issues, session log), commit everything, and tell me "Safe to export".
```

## D. Recommended working rhythm (saves credits and risk)
- One milestone per session. Ask for ONE task at a time from the
  checklist, not "build everything".
- After each task: run the app, click through the feature, then commit.
- Do expensive live-LLM work (ingesting the demo corpus, final eval run,
  recording the demo) in ONE focused session, then commit the outputs
  so no later account needs to repeat it.
- Keep the cache: never delete `data/llm_cache/`.
- If a session produced a broken state, run `git status`, then
  `git stash` or `git checkout .` and redo the last small step.

## E. Suggested prompts per milestone (give one at a time)
- M0: "Implement M0 from docs/SPEC.md §17 and the NEXT ACTION in PROGRESS.md."
- M1: "Implement M1: PDF and PPTX ingestion with locators, the viewer
  endpoints, and the Library upload UI with live job progress, per
  SPEC §6–7 and UI_UX §4.3."
- M2: "Implement M2: video transcription with timestamps, keyframes,
  figure understanding, and the video viewer with seek."
- M3: "Implement M3: concept extraction, consolidation, prerequisite DAG
  with cycle removal, unit tagging, and the Concepts view."
- M4: "Implement M4: hybrid retrieval, grounded answer JSON,
  citation validation, claim check, refusal flow, and the Tutor screen
  with EvidencePanel and SourceViewerDrawer per UI_UX §4.4."
- M5: "Implement M5: BKT learner model, students, onboarding intake,
  diagnostic, Home dashboard heatmap and WhyDrawer."
- M6: "Implement M6: question generation with the full verification
  pipeline, dedupe, selection, quiz player and feedback."
- M7: "Implement M7: assessment report, misconception cards,
  recommendation engine with reasons, remediation quiz."
- M8: "Implement M8: eval test set tooling, RAG metrics, deterministic
  citation/refusal metrics, simulated students, and the Evaluation Lab
  screen."
- M9: "Do the M9 polish pass using UI_UX §9, §10 and §8; enable demo
  mode; write README and architecture diagram; make the demo script in
  UI_UX §11 run cleanly."

## F. Hackathon submission checklist
- [ ] Working prototype runs with `make setup && make seed && make dev`
- [ ] README: architecture diagram, grounding method, learner-model
      approach, evaluation summary, limitations
- [ ] `eval/results/latest.json` produced by a real run, committed
- [ ] Demo video 3–10 min uploaded to YouTube (script: UI_UX §11)
- [ ] Repo link and video link ready; secrets not committed
- [ ] Fallback: recorded screen capture of the full flow in case the
      live demo fails
