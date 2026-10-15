# StudyMate — Complete UI/UX Specification

Goal: judges should understand the product in 10 seconds, verify
grounding in 3 clicks, and see personalization change live. The UI must
feel like one coherent product, not four tools stapled together.

Stack: Next.js (App Router) + TypeScript + Tailwind + shadcn/ui +
Recharts + React Flow + react-pdf + lucide-react + framer-motion.

## 1. Design principles
1. **Evidence is always one click away.** Citations are first-class UI,
   never footnote text.
2. **Show your reasoning for personalization.** Every recommendation and
   mastery number has a "Why?".
3. **Calm and focused.** Study tool, not a dashboard of noise. Generous
   whitespace, one primary action per view.
4. **State honesty.** Unsupported answers, low-confidence figures and
   unverified items are visibly marked — never hidden.
5. **Fast feedback.** Every action responds within 100 ms visually
   (optimistic UI, skeletons, streaming text).
6. **Accessible by default.** Keyboard operable, contrast ≥ 4.5:1,
   colour is never the only signal.

## 2. Design system
### 2.1 Colour tokens (CSS variables, light + dark)
```
--bg:          #F7F8FB   (dark #0E1117)
--surface:     #FFFFFF   (dark #151A23)
--surface-2:   #F0F2F7   (dark #1C2230)
--border:      #E3E6EE   (dark #272E3D)
--text:        #151A23   (dark #E8EBF2)
--text-muted:  #5B6475   (dark #9AA3B5)
--primary:     #4F46E5   indigo (dark #7C74FF)
--primary-fg:  #FFFFFF
--accent:      #0EA5A4   teal   (evidence / citations)
--success:     #16A34A   --warning: #D97706   --danger: #DC2626
--info:        #2563EB
```
Mastery scale (5 bands; each with label + icon, not colour only):
`0–20% Not started/Weak (red)`, `20–40% Shaky (orange)`,
`40–60% Developing (amber)`, `60–80% Good (lime)`,
`80–100% Mastered (green)`. Inferred (not directly tested) values use
a hatched/dashed style.

Citation chips use `--accent` tint with a small modality icon:
📄→ `FileText`, slides → `Presentation`, video → `PlayCircle`,
figure → `Image`.

### 2.2 Typography
Inter (UI) + JetBrains Mono (code/equations). Scale: 12 / 14 / 16 /
18 / 24 / 32. Body 16 in chat, 14 in dense tables. Line-height 1.55.
Math rendered with KaTeX.

### 2.3 Spacing, shape, elevation
4-pt grid; radius 12 (cards), 8 (inputs/buttons), full (chips).
Elevation: 1px border + subtle shadow only on overlays. Max content
width 1200 px; chat column 760 px.

### 2.4 Components to build (shared library `frontend/components/`)
`AppShell, SidebarNav, TopBar, CourseSwitcher, StudentSwitcher,
ThemeToggle, CommandPalette (⌘/Ctrl-K), Card, StatCard, Badge,
MasteryBadge, MasteryBar, Heatmap, ProgressRing, Stepper, JobProgress,
FileDropzone, SourceCard, CitationChip, CitationList, EvidencePanel,
SourceViewerDrawer (PDF | Slide | Video | Figure tabs),
VideoPlayerWithTranscript, PdfViewer (page jump + bbox highlight),
SlideViewer, FigureViewer, ChatMessage, ChatComposer, StyleSelector,
ModeToggle, SupportBanner, OutsideKnowledgeBlock, QuestionCard,
OptionList, ConfidenceSelector, Timer, FeedbackPanel,
MisconceptionCard, RecommendationCard, WhyDrawer, ConceptGraph,
ConceptSidePanel, EmptyState, ErrorState, Skeletons, Toast, ConfirmDialog,
MetricCard, EvalTable, FailureList, ChartCard`.

### 2.5 Motion
150–250 ms ease-out. Mastery bars animate from old → new value after a
quiz (this is the "personalization is happening" moment). Respect
`prefers-reduced-motion`.

## 3. Information architecture & navigation
Left sidebar (collapsible, icons + labels; bottom nav on mobile):
1. **Home** (dashboard)
2. **Tutor**
3. **Practice** (assessments)
4. **Course Map**
5. **Library** (Knowledge Studio)
6. **Review** (revision queue + flashcards)
7. **Plan** (study schedule) — optional
8. **Evaluation Lab**
9. **Settings** (profile, model status, language, theme, demo mode)

Top bar: course switcher · student switcher (with avatar/name) ·
global search/command palette · processing-jobs indicator · theme
toggle.

URL map: `/`, `/tutor`, `/tutor/[threadId]`, `/practice`,
`/practice/new`, `/practice/[id]`, `/practice/[id]/report`, `/map`,
`/library`, `/library/[sourceId]`, `/review`, `/plan`, `/eval`,
`/settings`, `/onboarding`.

First launch with no student → redirect to `/onboarding`.

## 4. Screens

### 4.1 Onboarding (new student, cold start)
Goal: collect priors in under 60 seconds, feel conversational.
1. Welcome card: product promise in one line, "Start" button, "Use demo
   student" secondary.
2. Intake (stepper, 4 short steps, one question per step with big
   tappable choices): goal (exam / revise / learn from scratch) ·
   exam date (optional date picker) · background level (1–5 with plain
   descriptions) · preferred explanation style + language
   (English/Hinglish).
3. "Quick diagnostic" explainer: "10 questions, ~8 min, no pressure.
   This sets your starting map." Buttons: Start diagnostic / Skip for
   now (shows a banner "Your map is a rough estimate").
4. Diagnostic runs in the quiz player (§4.5). Progress shows
   "Question 4 of ~12".
5. Result: animated reveal of the mastery heatmap + 3 recommended next
   actions.

### 4.2 Home / Dashboard
Layout (desktop 12-col grid):
- **Hero row:** greeting + course name; "Continue" primary button that
  maps to the top recommendation; exam countdown chip if set.
- **Next best actions** (3 `RecommendationCard`s): icon, title ("Review
  Round Robin"), one-line reason, estimated minutes, action button,
  "Why?" link opening `WhyDrawer`.
- **Course mastery heatmap:** topics as rows/columns of concept tiles
  coloured by mastery band, with legend. Hover → concept name, %,
  attempts, last practiced. Click → `ConceptSidePanel` (explain,
  practice, sources). Inferred values hatched.
- **Progress over time:** line chart of average mastery per session +
  small multiples for weakest 3 topics.
- **Revision queue:** concepts due today (forgetting-curve based) with
  "Start 5-minute review".
- **Recent activity:** last quizzes (score, date, link to report).
- **Stat cards:** overall mastery, concepts mastered, streak, questions
  answered.
Empty state (no data): illustration + "Take the 8-minute diagnostic to
build your map."

### 4.3 Library (Knowledge Studio)
- **Upload zone** (drag-and-drop, multiple, accepts PDF/PPTX/MP4/MKV/
  WEBM/MP3; shows size/type validation errors inline).
- **Source list** (cards): thumbnail, title, type icon, size/duration,
  status badge (Queued / Processing / Ready / Needs attention),
  counts (pages/slides/minutes, units, figures, concepts).
- **Live processing view:** per-source `JobProgress` with named stages
  (Extracting → Transcribing → Understanding figures → Building
  concepts → Indexing), percentage, elapsed time, and a log line.
  Continues in background; global indicator in the top bar.
- **Processing report** (after ready): extraction counts, detected
  topics preview, warnings list ("3 low-confidence figures — review"),
  buttons: "Explore sources", "Open course map".
- **Source detail `/library/[id]`:** viewer on the left (PDF/slide
  carousel/video), right panel with tabs: *Units* (list with
  locators, concept tags), *Figures* (grid with VLM descriptions and
  confidence), *Concepts* (tags found in this source). Selecting a unit
  scrolls/jumps the viewer to its location with highlight.
- **Quality control:** a figure's description is editable (inline
  "Correct this") — edits are stored and re-indexed.

### 4.4 Tutor (grounded chat)
Three-pane layout (collapses responsively):
- **Left (240 px):** thread list, "New chat", scope picker (All course /
  chosen topics / chosen sources).
- **Center (chat):**
  - Header: thread title, **Mode toggle** (Strict ⇄ Assisted) with
    tooltip explaining each, **Explain-style selector** (Simple /
    Standard / Deep / Worked example / Analogy / Hinglish).
  - Messages: student bubble right; tutor message left in a card.
    Tutor message structure: *SupportBanner* (green "Fully supported by
    your material", amber "Partly covered — missing: …", red "Not
    covered in your material") → answer text with inline numbered
    `CitationChip`s → optional `OutsideKnowledgeBlock` (dashed border,
    warning icon, "Outside your course material — not verified against
    your sources") → follow-up chips → action row (👍/👎, copy,
    "Quiz me on this", "Simplify", "Explain in Hinglish").
  - **Streaming:** tokens appear progressively; a "Searching your
    material…" step list (Retrieving → Checking support → Writing)
    shows before text.
  - **Composer:** multiline, attach-scope chip, send; suggestions row
    on empty chat ("Explain Round Robin simply", "Compare FCFS and
    SJF", "Quiz me on paging").
- **Right (360 px) EvidencePanel:** lists the evidence for the focused
  message: each item = modality icon + source title + locator
  ("Slide 12", "p. 41", "12:36–13:10") + the exact excerpt with the
  supporting phrase highlighted + image thumbnail for figures + **Open
  source** button. Hovering a citation chip highlights the matching
  evidence item and vice-versa.
- **Opening a citation** (chip or button) slides in the
  `SourceViewerDrawer` over the right pane: PDF at the page with the
  bbox highlighted; slide image; video seeking to `t_start` with
  transcript scrolled to the line; figure viewer with zoom. Drawer has
  prev/next evidence arrows and "Open in Library".
- **Learner-aware touches:** a small chip under tutor messages: "Your
  mastery here: 38% (Shaky)" and, when low, "Review prerequisite:
  *Process States*" link. After some explanations a **comprehension
  check** appears inline ("Quick check — 30 seconds") with 1 question;
  results animate mastery.
- **Unsupported flow:** red banner, text "I can't find this in your
  uploaded material." + chips of nearest covered topics + button "Show
  outside knowledge (labelled)". Never auto-answer.
- Keyboard: Enter send, Shift+Enter newline, ⌘/Ctrl-K palette,
  `1–9` focus evidence item n.

### 4.5 Practice — builder, player, feedback
**Builder `/practice/new`:** a single card:
1. Mode tabs: Diagnostic · Practice · Mock exam · Remediation.
2. Scope: tree picker of topics/concepts (checkbox, with mastery
   badges), or "Pick for me (weakest first)".
3. Settings: number of questions slider (5–30), types (MCQ / Short /
   Numerical), difficulty (Adaptive default / fixed 1–5), timer toggle.
4. Summary line: "12 questions · adaptive · ~15 min · covers 4
   topics". Primary: "Generate". 
5. Generation progress: stepper (Selecting concepts → Writing questions
   → Verifying answers → Checking for repeats) with a live count
   "9/12 verified, 1 rejected & regenerated". This makes verification
   visible.

**Player `/practice/[id]`:**
- Top: progress bar + "Q 4/12", timer (mock), exit (confirm).
- Question card: topic breadcrumb chip, difficulty dots, stem (markdown
  + KaTeX + image if figure-based), answer area by type (OptionList with
  A–D keyboard shortcuts / textarea with word counter / numeric input
  with unit hint).
- **ConfidenceSelector** (Guess / Think so / Sure) before submitting
  (can be disabled in settings).
- Practice mode: after "Check", a `FeedbackPanel` slides under:
  ✔/✖ headline, short explanation, **cited excerpt** chip(s) opening the
  source drawer, "Likely misconception: …" (if wrong; hedged wording),
  mastery delta micro-animation ("Round Robin 32% → 41%"), buttons:
  Next / "Explain more" (opens Tutor with context) / "Flag question".
- Mock mode: no feedback until submit; question navigator grid with
  answered/flagged states.
- Hints (practice only): up to 2, each reduces evidence weight.
- Keyboard: 1–4 or A–D select, Enter submit/next, F flag, H hint.

**Report `/practice/[id]/report`:**
- Header: score ring, time, comparison with previous attempt.
- **Mastery changes:** before→after bars per topic (animated).
- **Weak concepts** ranked list with reasons and "Practice now".
- **Misconception cards** (`MisconceptionCard`): "Observed: chose
  'burst time' as waiting time (3 times)" · "Hypothesis: confusing
  burst time with waiting time" · evidence count · cited explanation ·
  "Fix this" → remediation quiz.
- **Question review** table: filter by wrong/flagged, expand for
  solution + citation + tags (topic, difficulty, source).
- **Next steps** (RecommendationCards) and "Start remediation quiz".
- Export: "Download report (PDF)" optional.

### 4.6 Course Map
React Flow canvas, dagre left→right layout. Nodes: concepts (rounded
rect, mastery colour + band icon + %), topic groups as containers.
Edges: solid = prerequisite (arrow); dashed = related. Controls:
zoom/fit, search concept, filter by topic, toggle "Show weak only",
"Highlight learning path to <concept>". Click node → right
`ConceptSidePanel`: description, mastery + "Why?", prerequisites
(with their mastery), top 3 sources (chips), buttons: "Explain in
Tutor", "Practice this", "Add to review". Minimap and legend
included. Mobile: list view fallback.

### 4.7 Review (revision + flashcards) — optional
Queue of due concepts, "Start review" runs a short mixed set (flashcards
and 1-click questions). Flashcard UI: front prompt, flip, rate (Again /
Hard / Good / Easy) feeding the scheduler; back shows cited answer.

### 4.8 Plan (study schedule) — optional
Inputs: exam date, hours/week. Output: week calendar with sessions
labelled by concept and type (learn/practice/review) and minutes;
"Why this order?" drawer; reschedule button after each quiz.

### 4.9 Evaluation Lab
Purpose: honest proof. Tabs:
1. **Overview:** MetricCards for faithfulness, answer relevancy,
   context precision, context recall, citation location accuracy,
   refusal precision/recall, question duplicate rate; each shows value,
   n, and a tooltip with its definition. Header shows run date, git
   commit, judge model, corpus size.
2. **Retrieval & grounding:** bar charts by category (direct, multi,
   diagram, video, unsupported); ablation table (dense vs hybrid vs
   +rerank, ±claim check).
3. **Assessment quality:** verification funnel (generated → verified →
   rejected by reason), key-validity audit result, duplicate rate.
4. **Personalization:** line charts of simulated-student mastery over
   sessions — Adaptive vs Static baseline per profile; table of mastery
   gain, held-out score gain, repetition rate, estimate error (MAE).
5. **Failures:** list of failed test cases with question, expected vs
   actual sources, answer, and judge notes; filter by category.
6. **Run history & "Run evaluation" button** (shows job progress).
7. **Limitations** card: simulator and judge caveats written plainly.
Empty state: "No evaluation run yet — Run evaluation."

### 4.10 Settings
Profile (name, goal, exam date, language, default style), Appearance
(theme, density), Models (read-only status: provider, models, cache
mode, API reachable ✔/✖), Data (Reset demo, Export data), Demo mode
switch.

## 5. Global UX patterns
- **Source Viewer Drawer** is global; any citation chip anywhere (chat,
  feedback, report, map) opens it the same way.
- **WhyDrawer** is global; opens for any recommendation or mastery
  number: lists contributing events with deltas and the rule that fired.
- **Command palette (⌘/Ctrl-K):** jump to screens, concepts, sources;
  actions "New chat", "Start quiz on …".
- **Toasts** for background completion ("Lecture 2 is ready").
- **Persistent job indicator** in the top bar with popover list.
- **Breadcrumbs** inside Library and Practice.
- **Undo** for destructive-but-reversible actions (delete source →
  5-second undo toast).
- Confirm dialogs only for irreversible actions (reset data, abandon
  active mock exam).

## 6. Content & microcopy rules
- Tone: supportive, concise, never condescending. Use "you".
- Wrong answers: "Not quite — here's what happened", never "Wrong!".
- Hypotheses: "Likely misconception" / "This may be…", never "You
  don't understand…".
- Unsupported: "I can't find this in your uploaded material." + next
  steps.
- No jargon on student-facing screens ("mastery" is OK; "BKT" only in
  Why drawers/docs).
- All numbers formatted consistently (percent integers, minutes,
  `mm:ss` timestamps).

## 7. Responsive behaviour
- ≥1280: full 3-pane layouts.
- 768–1279: sidebar collapses to icons; evidence panel becomes a drawer.
- <768: bottom tab bar (Home, Tutor, Practice, Map, More); tutor
  evidence opens as bottom sheet; Course Map shows list view; PDF
  viewer is full screen.
Test every screen at 390, 768, 1440 widths.

## 8. Accessibility checklist
Semantic landmarks · visible focus rings · keyboard path for every
action (including the graph via list fallback) · aria-live for
streaming text and quiz feedback · alt text for figures (VLM
description) · captions/transcript for video · colour-independent
mastery (labels + icons + hatch) · reduced motion · min tap target 44px
· form errors announced.

## 9. UI states (required for every async view)
| State | Treatment |
|---|---|
| Loading | Skeletons matching final layout, never spinners alone |
| Empty | Illustration (simple SVG) + one-sentence explanation + primary CTA |
| Error | Plain-language message, retry button, "Copy details" for logs |
| Partial | Banner explaining what is missing (e.g. figure confidence low) |
| Offline/API down | Top banner "Can't reach the server — retrying" |
| Long job | Progress with named stages, ETA text, continue-in-background |
| Success | Toast + inline confirmation, no modal unless needed |

## 10. Visual polish checklist (do in M9)
Consistent card padding · aligned baselines · real thumbnails for every
source · app icon and favicon · page titles · consistent chart colours ·
no layout shift on load · tested dark mode on every screen · no raw
JSON or IDs visible to users · all buttons have hover/active/disabled
states · long titles truncate with tooltip.

## 11. Demo script the UI must support (≈5:30)
1. 0:00 Home shows empty state → click "Use demo student"? No: start
   from **Onboarding** (new student) to show cold start.
2. 0:25 **Library:** drop PDF + PPTX + video (pre-processed copy is
   already available; show live progress on one small file), open the
   processing report.
3. 1:05 **Tutor:** ask a diagram question → streamed answer with
   citations → click a video citation → drawer seeks to the timestamp.
4. 1:50 Ask an off-material question → red "not covered" banner;
   show Strict vs Assisted block.
5. 2:15 **Diagnostic quiz** → feedback with cited excerpt on a wrong
   answer → misconception hint → mastery delta animation.
6. 3:05 **Dashboard** heatmap updated + "Next best actions" with Why
   drawer.
7. 3:40 Take a remediation question on the same concept in a new
   surface form.
8. 4:00 **Course Map** with weak path highlighted.
9. 4:20 **Evaluation Lab:** metrics, ablation, simulated-student chart
   (adaptive vs static), failures list.
10. 5:00 Architecture slide and closing statement.
The `Demo mode` setting preloads: 3 sources (ready), concept graph,
2 students (new, and "Aarav" with 4 sessions of history), and cached
LLM responses so the flow is fast and deterministic.

## 12. Frontend implementation notes
- Use server components only for static shells; data screens are client
  components with TanStack Query (stale time 30 s; invalidate on
  mutation).
- Chat uses an SSE hook (`useChatStream`) handling `retrieval`, `token`,
  `citation`, `status`, `done` events with abort support.
- Global Zustand store: current course, current student, theme, drawer
  state (source viewer, why drawer).
- API client in `frontend/lib/api.ts` with typed functions; all
  endpoint shapes mirrored in `frontend/lib/types.ts`.
- Citations rendering: parse segments' citation arrays — never regex
  user text. Numbering is per message in order of first appearance.
- PDF highlight: draw bbox overlay scaled to the rendered page size.
- Video: `video.currentTime = t_start` on `loadedmetadata`; highlight
  the active transcript line while playing; keep the drawer open
  while navigating the page.
- Accessibility lint: `eslint-plugin-jsx-a11y`.
- Add `data-testid` on key elements; Playwright smoke test covers:
  onboarding → ask question → open citation → take 3-question quiz →
  see dashboard update.
