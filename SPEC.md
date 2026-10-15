# StudyMate — Technical Specification

Hackathon: Multimodal AI Hackathon 2026, Track D.
Rubric weights: Grounding 20 · Personalization 20 · Assessment 15 ·
UX + Demo 15 · Evaluation 15 · Implementation 15.

## 1. Product in one paragraph
StudyMate turns a student's lecture videos, textbooks and slides into a
source-linked knowledge graph. A grounded tutor explains concepts with
clickable citations to the exact page, slide or video second. An
adaptive assessment engine generates verified questions, diagnoses
misconceptions, and feeds a Bayesian learner model that decides what
the student should study next. A built-in evaluation lab proves that
grounding and personalization actually work.

**Central idea — the Evidence-to-Mastery Loop.** Every interaction
links: Evidence (exact source) → Concept (what is being learned) →
Mastery (how the estimate changes) → Next action (what to do next, with
a visible reason). Build everything so this loop is visible in the UI.

## 2. Scope
### MUST (milestones M0–M9)
Multimodal ingestion (PDF, PPTX, video) · concept graph with
prerequisites · hybrid retrieval · grounded tutor with clickable
citations and refusal handling · verified adaptive assessments
(MCQ, short answer, numerical) · learner model (BKT + spaced review) ·
cold-start diagnostic + intake · student dashboard · assessment report
with misconceptions · evaluation lab (RAGAS/DeepEval + custom metrics +
simulated students) · demo corpus and demo mode.

### SHOULD (M10–M11, only after MUST is green)
Course flow map interactions · flashcards from weak concepts ·
study schedule with forgetting curve · English↔Hinglish explanations
(Roman script).

### LATER (do not start unless everything above is done)
Voice tutoring (STT/TTS) · generated revision slide decks · audio
briefs.

### SKIP (never build)
Auth, payments, teacher/admin portals, social features, mobile apps,
LMS integrations.

## 3. Tech stack (fixed)
| Layer | Choice | Notes |
|---|---|---|
| Frontend | Next.js 14 (App Router) + TypeScript + Tailwind CSS + shadcn/ui | Only UI libs allowed below |
| Charts | Recharts | mastery trends, eval charts |
| Graph | @xyflow/react (React Flow) + dagre layout | course flow map |
| PDF viewer | react-pdf (pdf.js) | open at page, highlight bbox |
| Video | native HTML5 `<video>` + custom controls | seek to timestamp |
| State/data | TanStack Query + Zustand | |
| Icons/motion | lucide-react, framer-motion (sparingly) | |
| Markdown | react-markdown + remark-math + rehype-katex | equations |
| Backend | Python 3.11 + FastAPI + Pydantic v2 | |
| DB | SQLite via SQLModel/SQLAlchemy | single file `data/app.db` |
| Vector | ChromaDB persistent (local) | collection per course |
| Keyword | `rank_bm25` over stored units | fused with vectors via RRF |
| PDF parse | PyMuPDF (fitz) | text blocks with bboxes + page renders |
| PPTX parse | python-pptx + LibreOffice headless to render slide PNGs (fallback: render shapes via Pillow) | |
| Video | ffmpeg + faster-whisper (CPU, `small` model) | timestamps; fallback: LLM audio transcription |
| Frames | ffmpeg scene detection → keyframes | dedupe near-identical frames with imagehash |
| LLM/VLM | Provider abstraction in `backend/app/llm/` | default Gemini via env; swappable |
| Embeddings | provider abstraction; default Gemini embedding model or `sentence-transformers` local fallback | |
| Eval | RAGAS and/or DeepEval + custom metrics | judge model configurable |
| Tests | pytest, Playwright (smoke only) | |
| Task runner | FastAPI BackgroundTasks + `jobs` table with progress | no Celery |

Model names, API keys, and mode flags live in `.env`:
```
LLM_PROVIDER=gemini
LLM_MODEL_FAST=...        # tagging, extraction, bulk
LLM_MODEL_STRONG=...      # tutor answers, question generation
LLM_MODEL_VERIFIER=...    # DIFFERENT model/family from STRONG if possible
EMBED_MODEL=...
GEMINI_API_KEY=...
LLM_MODE=cache            # cache | live | offline
WHISPER_MODEL=small
```
`LLM_MODE=cache`: look up prompt-hash in `data/llm_cache/`; call API on
miss and store. `offline`: cache only, error on miss (used by tests).

## 4. Repository layout
```
backend/app/
  main.py                    FastAPI app, CORS, routers
  config.py                  settings from .env
  db.py  models.py  schemas.py
  llm/client.py              provider abstraction + disk cache + retries
  llm/prompts/*.md           prompt templates (versioned files)
  ingest/
    pipeline.py              orchestrates a job, writes progress
    pdf.py  pptx.py  video.py  figures.py
    chunker.py               content-unit creation
  knowledge/
    concepts.py              extraction, dedupe, tagging
    graph.py                 prerequisite edges, DAG validation
    index.py                 chroma + bm25 build/update
  retrieval/
    hybrid.py                dense + bm25 + RRF + rerank
    rerank.py                LLM or cross-encoder reranker
  tutor/
    answer.py                grounded answer pipeline
    verify.py                citation + claim checks
    refusal.py               support scoring and decline logic
    hinglish.py
  assess/
    generate.py  verify.py  dedupe.py  select.py  grade.py  report.py
    sandbox.py               safe numeric verification (subprocess)
  learner/
    bkt.py  mastery.py  scheduler.py  recommend.py  intake.py
  eval/ (thin API wrappers; real runners live in /eval)
  routers/                   courses, sources, units, concepts, tutor,
                             assessments, learner, eval, jobs, demo
backend/tests/
frontend/                    Next.js app (see UI_UX.md for screens)
eval/
  testsets/qa_testset.jsonl  offmaterial.jsonl  questions_gold.jsonl
  students/profiles.yaml
  run_rag_eval.py  run_citation_eval.py  run_assessment_eval.py
  run_student_sim.py  run_all.py
  results/                   JSON + CSV outputs, committed
data/demo/raw/               demo files (see §13)
data/demo/processed/         committed ingestion output
scripts/verify.sh seed.sh export.sh
Makefile  .env.example  README.md
```

`Makefile` targets: `setup`, `dev` (backend+frontend), `seed` (load
processed demo data into DB/vector store without calling APIs),
`verify`, `test`, `eval`, `export`.

## 5. Data model (SQLite)
```
courses(id, title, description, created_at)
sources(id, course_id, kind[pdf|pptx|video], title, filename, path,
        pages_or_slides, duration_sec, status, license_note)
units(id, course_id, source_id, kind[text|figure|table|transcript|
      slide|equation], text, page, slide, t_start, t_end,
      bbox_json, image_path, caption, parent_heading, order_idx,
      token_count)
concepts(id, course_id, name, description, parent_id, level[topic|
         subtopic|concept], importance)
unit_concepts(unit_id, concept_id, relevance)
prereq_edges(id, course_id, from_concept_id, to_concept_id,
             confidence, rationale)      -- from = prerequisite
questions(id, course_id, type[mcq|short|numeric], concept_id, topic_id,
          difficulty[1..5], stem, options_json, answer_key, solution,
          source_unit_ids_json, misconception_tags_json,
          verification_status[verified|rejected|pending],
          verification_log_json, embedding_id, created_at)
assessments(id, student_id, course_id, mode[diagnostic|practice|mock|
            remediation], scope_json, status, created_at, submitted_at)
assessment_items(id, assessment_id, question_id, position, response,
                 is_correct, score, time_ms, confidence, feedback_json)
students(id, name, intake_json, created_at, exam_date)
mastery(student_id, concept_id, p_known, attempts, correct, last_at,
        next_review_at, stability_days, recent_errors_json)
learning_events(id, student_id, kind[quiz|chat|review|diagnostic],
                concept_id, evidence_weight, payload_json, created_at)
chat_threads(id, student_id, course_id, mode[strict|assisted], title)
chat_messages(id, thread_id, role, content_json, citations_json,
              support_status, created_at)
jobs(id, kind, status, progress, message, error, created_at,
     finished_at, payload_json)
eval_runs(id, kind, started_at, finished_at, config_json,
          metrics_json, artifacts_path)
```

## 6. Content-unit contract (the heart of grounding)
Every unit stored by ingestion MUST have a **locator**:
- PDF: `{source_id, page, bbox?, section}`
- Slide: `{source_id, slide, shape_ref?}` plus rendered PNG of the slide
- Video: `{source_id, t_start, t_end}` (seconds, integer), optional
  `frame_path` for the nearest keyframe
- Figure: `{source_id, page|slide|t, image_path (crop), caption,
  labels[], vlm_description}`

Citation id format used everywhere: `u_<unit_id>`. Citation resolves to
an API `GET /units/{id}` returning locator + text + preview, and the
frontend opens the viewer at that locator.

### Chunking rules
- PDF: split by heading/paragraph; 150–350 tokens; never split
  equations/tables/figure+caption. Keep the heading path in
  `parent_heading`.
- Slides: one unit per slide (text + notes) PLUS one `figure` unit per
  image/diagram on it.
- Video: transcript segments merged to 20–45 s windows with ~5 s
  overlap, never crossing a detected scene change by more than 3 s.
  Attach text from OCR/VLM of the nearest keyframe as a `figure` unit
  when slides/board content is visible.
- Figures: crop the image, ask the VLM for: what it depicts, labels,
  relationships, and any numbers. Store the description as searchable
  text AND keep the original image. Mark `confidence` low when the
  VLM is unsure; show this in the Knowledge Studio warnings.

## 7. Ingestion pipeline (job with live progress)
Stages (each updates `jobs.progress` and a human-readable message):
1. validate + store file
2. extract (PDF pages / slide render / audio + frames)
3. transcribe video (faster-whisper; keep segment timestamps)
4. figure understanding (VLM, batch, cached)
5. chunk into units
6. concept extraction (batch units → candidate concepts)
7. concept consolidation (embedding clustering + LLM merge → hierarchy
   Topic > Subtopic > Concept; target 8–15 topics, 40–120 concepts for
   the demo course)
8. prerequisite inference (LLM proposes edges with rationale; code
   validates it is a DAG — drop the lowest-confidence edge in any cycle)
9. unit→concept tagging (top 1–3 concepts per unit with relevance)
10. index build (Chroma embeddings + BM25)
11. report: counts, warnings (OCR failures, low-confidence figures,
    unreadable pages), time taken

Idempotent: re-running a stage must not duplicate rows. Stage outputs
for the demo corpus are exported to `data/demo/processed/` and
re-importable via `make seed`.

## 8. Retrieval
`retrieve(query, course_id, scope?, k=8)`:
1. Dense search (top 30) + BM25 (top 30) → Reciprocal Rank Fusion.
2. Optional scope filter (selected topics/sources).
3. Rerank top 20 → top k (LLM-based rerank with a short prompt, or a
   cross-encoder if installed). Cache aggressively.
4. Return units with scores and locators. Figures retrieved via their
   VLM description.
5. Add neighbours: for a transcript unit also return the keyframe
   figure unit within its window if present.

Log retrieved ids, scores, and latency in every tutor message for
evaluation and debugging.

## 9. Grounded tutor
### 9.1 Pipeline
1. Classify intent: `explain | question | summarize | compare |
   practice_request | off_topic | small_talk`.
2. If practice_request → hand off to Assessment (UI shows "Start a
   quiz on X" action).
3. Retrieve evidence (§8). Compute `support_score` = f(top rerank
   scores, coverage judged by a short LLM "can these passages answer
   the question? yes/partial/no" call).
4. Branch:
   - `supported` → generate the answer.
   - `partial` → answer only the supported part; state exactly what is
     missing.
   - `unsupported` → say the material doesn't cover it; list the
     nearest covered topics as clickable chips; offer "Show outside
     knowledge (labelled)". Never silently answer.
5. Generate answer as **structured JSON**:
```json
{
  "status": "supported|partial|unsupported",
  "segments": [
    {"text": "...", "citations": ["u_123","u_130"]}
  ],
  "outside_knowledge": null,
  "followups": ["..."],
  "concepts": ["concept_id", "..."]
}
```
6. **Validation (code, not LLM):** every cited id exists, belongs to the
   course, and was in the retrieved set. Strip or regenerate otherwise.
7. **Claim check (LLM, cheap):** for each segment, is it entailed by its
   cited units? Unsupported segments are removed or flagged "weakly
   supported". Record result for evaluation.
8. Render: prose with inline numbered citation chips `[1]`; side panel
   shows the exact excerpt for each citation with an "Open source"
   action.

### 9.2 Modes
- **Strict** (default): only course material. Unsupported → decline.
- **Assisted**: may add outside knowledge, ALWAYS in a separate
  visually distinct block titled "Outside your course material" with no
  citation chips and a warning icon.

### 9.3 Explanation styles (user-selectable)
Simple · Standard · Deep dive · Worked example · Analogy ·
Hinglish (Roman script; technical terms stay English; same citations).

### 9.4 Learner-aware behavior
- Read mastery for the concepts in the answer. Low mastery → simpler
  language, add prerequisite refresher link; high mastery → concise.
- After an explanation, optionally ask ONE quick comprehension check
  (a micro-question). Its graded result updates mastery with weight 0.6.
- Plain chat questions do NOT raise mastery. They are logged as weak
  evidence (weight 0.1) and may lower confidence if the student asks
  about a prerequisite basic.

### 9.5 Refusal rules
Refuse/flag when: no retrieved unit passes the support threshold; the
question is outside the course; the student asks for answers to an
active graded assessment (offer hints instead).

## 10. Assessment engine
### 10.1 Generation request
```
POST /assessments {student_id, course_id, mode, scope:{topic_ids?,
 concept_ids?, source_ids?}, n_questions, types[], difficulty:
 "adaptive"|1..5, timed?}
```
### 10.2 Question selection (adaptive)
For each slot choose a concept by score:
```
score(c) = w1*(1 - p_known[c])            # weak concepts first
         + w2*uncertainty(c)              # few attempts → explore
         + w3*review_due(c)               # forgetting curve
         + w4*prereq_gap(c)               # weak prerequisite → fix first
         - w5*recently_asked(c)
```
defaults `w = (0.40, 0.20, 0.20, 0.15, 0.25)`. Target difficulty
`d = clamp(round(1 + 4*p_known[c] + 0.5), 1, 5)`, aiming for ~70%
expected success. Prefer an existing verified unused question from the
bank; generate new ones only when none fits (saves credits).

### 10.3 Generation + verification pipeline (per question)
1. Retrieve 2–4 units for the concept in scope.
2. Generate JSON: stem, options (MCQ with 3 plausible distractors each
   mapped to a `misconception_tag`), answer_key, solution steps,
   difficulty, source unit ids.
3. **Schema validation** (pydantic). Reject on failure.
4. **Source validation:** answer must be supported by the cited units
   (entailment check).
5. **Independent solve:** the VERIFIER model answers the question blind
   (without the key). Mismatch → reject. For MCQ also check exactly one
   option is correct.
6. **Numeric verification:** for numerical questions, the generator
   must also output a Python function; run it in `sandbox.py`
   (subprocess, 3 s timeout, no network, restricted builtins) and
   compare to the key with tolerance.
7. **Ambiguity check:** verifier lists any alternative defensible
   answers; reject if any.
8. **Dedupe:** embed the stem; reject if cosine similarity ≥ 0.88 to any
   previously shown question for this student OR to another question in
   the same assessment; also reject exact-normalized duplicates.
9. Store with `verification_status` and the full `verification_log`.

Reject rate and reasons are an evaluation metric — log them.

### 10.4 Grading
- MCQ: exact.
- Numeric: tolerance (default 1%) + unit check.
- Short answer: LLM grader with rubric (key points from the solution),
  returns `score 0..1`, matched/missed key points, and misconception
  guess. Treat ≥0.7 as correct for mastery updates; use fractional
  evidence weight otherwise.
- Always collect optional **confidence** (Guess / Think so / Sure).
  Confident-and-wrong is flagged as a likely misconception.

### 10.5 Feedback per answer
Correct/incorrect · why · the cited excerpt (clickable) · if wrong:
"Likely misconception" (hypothesis wording, never certainty) · a
targeted follow-up question on the same concept with a different
surface form.

### 10.6 Post-assessment report
Score summary · per-topic mastery before→after · weak concepts ranked ·
misconception cards (observed error vs hypothesised cause, evidence
count) · time analysis · recommended next steps (each with reason) ·
"Start remediation quiz" and "Review these concepts" actions.

### 10.7 Modes
Diagnostic (cold start, 10–15 Q, spans topics, adaptive branching) ·
Practice (scope chosen, instant feedback) · Mock exam (timed, no
feedback until submit, mixed types) · Remediation (auto from weak
concepts and misconceptions).

## 11. Learner model
### 11.1 BKT per concept
State `p = P(known)`. Parameters (defaults, per concept overridable):
`p_init = 0.30, p_learn = 0.15, p_guess = 0.25 (MCQ) / 0.10 (short,
numeric), p_slip = 0.10`.

Update with evidence weight `w` (quiz=1.0, comprehension check=0.6,
chat=0.1, review card=0.8):
```
if correct:  post = p*(1-slip) / (p*(1-slip) + (1-p)*guess)
else:        post = p*slip     / (p*slip     + (1-p)*(1-guess))
post_w = p + w*(post - p)          # damp by evidence weight
p_new  = post_w + (1 - post_w)*learn*w
```
Clamp to [0.02, 0.98]. Store attempts, correct, recent errors.

### 11.2 Prerequisite propagation
On a wrong answer for concept C, for each prerequisite P of C:
`p[P] -= 0.05 * confidence_edge * (1 - p[P])` only if P has ≤2
attempts (uncertain). On a correct answer: `p[P] += 0.03 * (1-p[P])`.
Never push below 0.05 / above 0.95 via propagation. Show these as
"inferred" (dashed) in the UI, distinct from directly observed.

### 11.3 Cold start
`POST /students` → intake chat (goal, exam date, background level 1–5,
weekly hours, preferred explanation style, language preference). Intake
sets `p_init` priors by level (e.g. beginner 0.15, intermediate 0.30,
advanced 0.50). Then a **diagnostic quiz** (10–15 Q): choose concepts
covering each topic once, starting at medium difficulty, branching
up/down by correctness. After it, mastery is initialised from
posteriors.

### 11.4 Forgetting & spaced review
Stability `S` (days) = `1 + 6*p_known*(1 + 0.3*correct_streak)`.
Retention `R(t) = exp(-t/S)`. A concept is **due** when `R < 0.7`.
`next_review_at = last_at + S * ln(1/0.7)` days. Review cards and
review quizzes feed the scheduler.

### 11.5 Recommendation engine (`recommend.py`)
Returns the ordered "Next best actions" with machine-readable reasons:
`{action: review|learn|practice|challenge|remediate, concept_id,
reason_code, reason_text, evidence: [event ids]}`. The UI shows
`reason_text` verbatim, e.g. "Recommended because your last 3 answers
on *Round Robin* were wrong and *Time Quantum* (its prerequisite) is at
24%."

Rules (priority order): 1) misconception remediation with ≥2 evidence
→ 2) weak prerequisite of a weak concept → 3) due reviews → 4) weakest
in-scope concept → 5) challenge on a mastered concept (p>0.85).

### 11.6 Explainability
Every mastery number links to a "Why this number?" drawer listing the
attempts that moved it (question, result, delta).

## 12. Optional features (after M9)
- **Flow map:** React Flow graph of topics→concepts, node colour =
  mastery, dashed edge = prerequisite, click → side panel with
  explanation, practice and sources.
- **Flashcards:** auto-generate from weak concepts with cited back
  side; SM-2-like scheduling feeding the learner model.
- **Study schedule:** inputs exam date + weekly hours; allocate minutes
  per concept proportional to `(1-p)*importance` plus due reviews;
  output a calendar of daily sessions; recompute after each quiz.
- **Hinglish:** a post-generation transformation preserving citations
  and technical terms; Roman script only.

## 13. Demo corpus
Pick ONE small course and keep it traceable. Recommended: **Operating
Systems — CPU scheduling and memory management** (familiar domain, good
diagrams, numerical problems for scheduling).
- 1 textbook/notes PDF (30–60 pages) with a permissive/redistributable
  licence (e.g. MIT OCW materials CC BY-NC-SA, or self-written notes).
- 1 slide deck PPTX (20–40 slides, with diagrams: Gantt charts, page
  tables) — create from the notes if needed.
- 2–3 lecture videos, 8–15 minutes each (NPTEL / OCW, licence noted in
  `sources.license_note`; trim with ffmpeg if long).
Record the licence/source URL of each file in
`data/demo/SOURCES.md`. Do not commit copyrighted files whose licence
forbids redistribution; instead provide a `scripts/fetch_demo.sh`.

## 14. API contract (REST, JSON)
```
POST   /courses                       GET /courses  GET /courses/{id}
POST   /courses/{id}/sources          (multipart upload) → job
GET    /courses/{id}/sources          GET /sources/{id}
GET    /sources/{id}/file             (streams original, range support)
GET    /sources/{id}/page/{n}.png     GET /sources/{id}/slide/{n}.png
GET    /jobs/{id}                     GET /jobs?course_id=
GET    /courses/{id}/concepts         GET /courses/{id}/graph
GET    /units/{id}                    GET /units?source_id=&page=
POST   /tutor/chat                    (stream SSE) {thread_id?, message,
                                       mode, style, scope?, student_id}
GET    /tutor/threads?student_id=     GET /tutor/threads/{id}
POST   /students                      GET /students  GET /students/{id}
POST   /students/{id}/intake
GET    /students/{id}/mastery         GET /students/{id}/mastery/{cid}/why
GET    /students/{id}/recommendations GET /students/{id}/schedule
POST   /assessments                   GET /assessments/{id}
POST   /assessments/{id}/answer       POST /assessments/{id}/submit
GET    /assessments/{id}/report
GET    /questions/{id}                (for review)
POST   /eval/run  (kind)              GET /eval/runs  GET /eval/runs/{id}
GET    /health                        POST /demo/reset  POST /demo/load
```
Errors: `{error:{code,message,detail?}}`, HTTP status accurate.
Streaming chat uses SSE events: `retrieval`, `token`, `citation`,
`status`, `done`.

## 15. Evaluation lab (build under `/eval`, surfaced in UI)
### 15.1 Test sets (team-built, committed)
`qa_testset.jsonl`, ~75 items:
```
{"id":"q001","category":"direct|multi|diagram|video|unsupported",
 "question":"...","reference_answer":"...",
 "gold_sources":[{"source":"os_notes.pdf","page":12},
                 {"source":"lec2.mp4","t_start":310,"t_end":360}],
 "should_refuse":false}
```
Distribution: 20 direct, 15 multi-source, 15 diagram, 15 video, 10
unsupported. Include hard ones. Questions are written/checked by a
human (the team), not purely LLM-generated.

### 15.2 Metrics
- RAGAS or DeepEval: faithfulness, answer relevancy, context precision,
  context recall. Document the judge model and note LLM-judge caveats.
- Custom, deterministic: **citation location accuracy** (cited locator
  overlaps a gold locator: same page / slide / |t − t_gold| within the
  window), **retrieval hit@k / MRR** on gold sources, **refusal
  precision/recall** (unsupported questions refused; answerable ones not
  refused), **citation validity rate** (cited ids exist and were
  retrieved).
- Assessment: answer-key validity (human-audited sample of ≥40
  questions), source-validity rate, topic-tag accuracy (audited
  sample), verification reject rate, semantic duplicate rate,
  distractor quality note.
- Ablations (small table): dense-only vs hybrid vs hybrid+rerank;
  with vs without claim-check.

### 15.3 Simulated students
`eval/students/profiles.yaml` defines ≥5 profiles with hidden true
mastery per concept, response model (IRT-style
`P(correct)=guess+(1-guess-slip)*sigmoid(a*(θ_c - b_q))`), learning
rate when exposed to cited explanations, and forgetting rate:
beginner · misconception-prone (specific systematic wrong
answers) · strong · forgetful · missing-prerequisites.
Run ≥6 sessions each. Compare **Adaptive (ours)** vs **Static**
(random questions, no recommendations) vs optional **Random-adaptive**.
Report per profile and aggregate: mastery gain (true), held-out
post-test score gain, estimated-vs-true mastery error (MAE), repeat
question rate, coverage of weak topics, number of sessions to reach
target. Store per-session traces. State simulator limitations plainly.

### 15.4 Reporting
`make eval` runs everything, writes `eval/results/<timestamp>/`
(JSON, CSV, charts as PNG) and `latest.json`. The Evaluation Lab screen
reads `latest.json` and lists failed cases with expandable detail. No
number is ever hard-coded in the UI.

## 16. Quality bars
- Backend: type hints, pydantic schemas on all endpoints, ≥ one pytest
  per module for the logic that matters (bkt, scheduler, dedupe,
  citation validation, sandbox, selection).
- Frontend: strict TypeScript, no `any` in shared types, API types
  generated or mirrored from backend schemas in `frontend/lib/types.ts`.
- Lint/format: ruff + black (backend), eslint + prettier (frontend).
- Logging: structured logs; every LLM call logs model, tokens, cache
  hit/miss.
- Security hygiene: file type/size validation on upload, no path
  traversal, sandboxed code execution for numerical checks.
- README: setup in ≤5 commands, architecture diagram (Mermaid),
  grounding method, learner-model description, eval results summary,
  limitations. These double as the Project Documentation deliverable.

## 17. Milestones (execute in order; each has acceptance tests)
**M0 Scaffold** — repo, Makefile, env, FastAPI health, Next.js shell
with layout/nav/theme, SQLite models, LLM client with cache, verify
script. *Accept:* `make dev` shows empty app shell; `make verify` green.

**M1 Ingestion: PDF + PPTX** — upload, extraction, units with locators,
page/slide PNGs, source viewer endpoints, Knowledge Studio upload UI
with live job progress. *Accept:* upload sample PDF+PPTX; every unit
opens at the right page/slide in the viewer.

**M2 Ingestion: video + figures** — transcription with timestamps,
keyframes, figure understanding, video player with seek. *Accept:*
transcript unit opens video at the right second; figure units show crop
+ description.

**M3 Concept graph** — extraction, consolidation, prerequisites DAG,
tagging, Concepts tab + basic graph view. *Accept:* ≥8 topics,
≥40 concepts, no cycles, every unit tagged.

**M4 Retrieval + grounded tutor** — hybrid retrieval, answer JSON,
citation validation, claim check, refusal, streaming chat UI with
citation chips and source panel. *Accept:* 10 manual questions answer
with working citations; 3 off-material questions are declined.

**M5 Learner model + intake + diagnostic** — BKT, mastery store,
students, intake chat, diagnostic flow, dashboard heatmap with
"why this number". *Accept:* new student → intake → diagnostic →
mastery map populated.

**M6 Assessment engine** — generation + full verification pipeline,
question bank, selection, quiz player UI, grading, feedback.
*Accept:* 20 questions generated; reject log visible; no duplicates in
3 consecutive quizzes.

**M7 Report + recommendations + remediation** — report screen,
misconception cards, recommendation engine with reasons, remediation
quiz. *Accept:* wrong answers produce targeted follow-ups; mastery
changes visibly on dashboard.

**M8 Evaluation lab** — test set, runners, simulated students, results
UI. *Accept:* `make eval` produces real numbers; screen displays them.

**M9 Polish + demo mode** — empty/loading/error states, responsive
checks, accessibility pass, demo-mode switcher, seeded demo students,
README, architecture diagram, record-ready flow. *Accept:* the full
demo script in `docs/UI_UX.md` §11 runs in under 6 minutes without
errors.

**M10 Flow map + flashcards** · **M11 Schedule + Hinglish** (optional).

## 18. Known risks and mitigations
| Risk | Mitigation |
|---|---|
| Credits expire mid-build | Commit often, PROGRESS.md, cached LLM calls, committed processed demo data |
| Slow video ingestion | Short videos, `small` whisper, precomputed outputs |
| VLM misreads diagrams | Keep original image visible, confidence flag, warnings list |
| LLM judge noise | Pair with deterministic metrics, report honestly |
| Duplicate / wrong questions | Verification pipeline + dedupe + audited sample |
| Scope creep | Follow MUST/SHOULD/LATER/SKIP strictly |
| Live demo failure | `LLM_MODE=cache` with warmed cache + recorded fallback video |
