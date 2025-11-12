Phase 0 — Scope, Risks, and Groundwork

Goal: lock target languages, IDE, and “happy-path” flows.

Decisions

Primary language: Python first (pdb), then JS/TS (Node Inspector), then Java (jdb).

UX surface: VS Code extension (primary), minimal Electron shell later if needed.

STT: Whisper (local or API). TTS: optional (pyttsx3/Azure).

LLM: OpenAI (models you prefer). Use small local model for offline fallback (optional).

Deliverables

Product spec (top 10 voice intents, see Phase 2).

Risk register (privacy, code-mod safety, hallucinations, latency).

Repo scaffold: backend/, vscode-extension/, shared/.

Acceptance

You can explain the end-to-end flow on paper and point to a skeleton repo.

Phase 1 — MVP CLI (No IDE)

Goal: prove the core loop with a CLI over a local folder.

Build

Speech capture → Whisper → text.

Intent inference → LLM turns text into a structured command.

Filesystem actions: grep-like search, AST parse (Python via ast), run pytest or python -m pdb script.py.

Return text (stdout) with suggested fix as a patch.

Minimal Intents

find_errors, explain_code, find_symbol, run_tests, propose_fix, apply_fix.

Deliverables

backend/main.py with /stt, /intent, /actions/* (can be CLI functions now).

Whisper wrapper, basic LLM prompt, patch creation (unified diff).

Acceptance

Say “Find where counter changes” → CLI prints occurrences.

Say “Explain function foo” → returns summary.

Say “Fix indentation in file X” → outputs a diff.

Phase 2 — Intent Schema & Router

Goal: make the NLU reliable and auditable.

Schema (JSON)

{
  "intent": "find_symbol",
  "confidence": 0.82,
  "entities": {
    "symbol": "userData",
    "file": null,
    "language": "python",
    "scope": "writes"  // reads|writes|declarations|all
  },
  "follow_up_allowed": true
}


Router

Deterministic mapping: intent -> handler.

Guardrails: require confirmation for destructive intents (apply_fix).

Prompt Outline (system)

Provide repo summary + file list (top-K from index).

Define valid intents + JSON format.

Refuse outside scope.

Acceptance

20 sample utterances map to correct intent ≥90% of time (manual eval).

Phase 3 — Symbol Indexing & Code Intelligence (v1)

Goal: fast, accurate answers without scanning the whole repo.

Implement

File inventory: glob include/exclude (.gitignore aware).

Static index: identifiers, defs, refs, imports (Python via ast).

X-ref search: regex + token windows.

Embeddings index (optional) for “explain this function” retrieval.

APIs

GET /symbols?name=foo

POST /search body { "query":"assignment to counter", "lang":"python" }

Acceptance

find_symbol(userData) returns all writes in <1s for mid-size repo.

Phase 4 — VS Code Extension (Core UX)

Goal: real developer experience.

Features

Push-to-talk button + keyboard shortcut.

Transcript panel (editable).

Inline highlights and diagnostics (Decorations).

Diff view for suggested patches with Accept / Reject / Edit.

Extension Pack

Webview panel (React).

IPC to backend (vscode.ExtensionContext.globalState for config).

Commands: echodebug.talk, echodebug.applyFix, echodebug.explainSelection.

Acceptance

You can say “highlight where userData is modified” and see inline highlights + a side panel summary.

Patch proposal opens in VS Code diff.

Phase 5 — Debugging Adapters (Runtime)

Goal: execute and interpret runtime errors.

Python

Launch with pdb hooks or pytest --maxfail=1 -q.

Parse stack trace → map frames to file:line → annotate in editor.

LLM template: “Given this stack trace + snippet, identify most likely root cause and propose minimal patch.”

JS/TS (Phase 5.2)

Node Inspector Protocol (inspector), capture exceptions, stack, scopes.

API

POST /run body { "cmd":"pytest -q", "env":{}, "timeout":20 }

POST /explain-trace body { "trace":"...", "snippets":[...] }

Acceptance

Given a failing test, assistant narrates root cause and opens the failing line with an explanation.

Phase 6 — Safe Code-Mod Engine

Goal: apply changes safely and reversibly.

Strategy

Use AST edits (preferred) → regenerate code (Black/Prettier).

If diff-based, enforce patch guards: context lines must match.

Always create a backup or Git worktree/branch: echodebug/fix/<slug>.

API

POST /propose-fix → { diff, rationale, risk_level }

POST /apply-fix → applies diff, returns new diagnostics.

Acceptance

Applying a fix never corrupts syntax; formatting preserved; one-command revert is available.

Phase 7 — Conversational Memory & Context

Goal: multi-turn flows that feel coherent.

Implement

Short-term memory: last N intents + artifacts (symbols, files touched).

Thread store per workspace (JSON or SQLite).

“Because you asked earlier to optimize, I also inlined X.”

Acceptance

Ask: “why did you change that?” → coherent explanation referencing prior step.

Phase 8 — Latency, Caching, and Offline Mode

Goal: <1s for simple tasks, <3s for complex (best-effort).

Implement

Cache STT results per audio hash.

Cache LLM responses for repeated prompts (fingerprint by code hash + query).

Optional local STT/LLM toggles.

Acceptance

Repeating the same query is noticeably faster; cold vs warm benchmarks recorded.

Phase 9 — Security & Privacy Hardening

Goal: protect source code and secrets.

Controls

Redaction of .env, keys, tokens before sending to LLM.

Allow “never upload code” mode: local-only heuristics + model.

Sandboxed execution for /run (working dir jail, resource limits).

Telemetry strictly opt-in; no code content in analytics.

Acceptance

Security checklist passes; redaction unit tests cover common secret patterns.

Phase 10 — QA Harness & Evaluation

Goal: measurable quality, not vibes.

Test Kits

Golden repos with seeded bugs: syntax, off-by-one, null deref, import error.

Task scripts: voice → text → intent → handler → result → metric.

Metrics: task success, edit correctness, time-to-fix, regressions.

Acceptance

Baseline success rate established; PRs must not regress threshold.

Phase 11 — Packaging & Distribution

Goal: frictionless install.

Outputs

VS Code extension (.vsix) + Marketplace manifest.

Backend packaged as uvicorn app (FastAPI), single-command runner.

Optional Docker compose (backend, whisper, vector-db).

Acceptance

Fresh machine install guide works end-to-end with zero manual tweaks.

Phase 12 — Polished UX & TTS (Optional)

Goal: delightful touches.

Add

Wake word (“Echo, debug this file”) toggle.

Status toasts with quick actions (Undo, View Diff, Explain).

TTS summary for hands-free mode.

Acceptance

Demo can be run eyes-off: ask, fix, hear summary.

Phase 13 — Docs, Demos, and Samples

Goal: make it portfolio-ready.

Produce

README (done), quickstart GIFs, 2-min demo video script:

Voice “find where counter increments”

Highlight + explanation

“Fix off-by-one”

Patch shown → Accept → tests pass → TTS summary

Acceptance

Someone new can clone and reproduce the demo without help.

Core Interfaces (Copy-Ready)
FastAPI Endpoints (sketch)
# backend/main.py
@app.post("/stt")           # wav/flac -> { "text": "..." }
@app.post("/intent")        # { text, context } -> IntentJSON
@app.post("/search")        # { query, lang, scope } -> [{file, line, preview}]
@app.post("/symbols")       # { name, lang } -> [{file, line, kind}]
@app.post("/run")           # { cmd, env, timeout } -> { exit, stdout, stderr }
@app.post("/explain-trace") # { trace, snippets } -> { summary, suspects }
@app.post("/propose-fix")   # { file, span?, goal } -> { diff, rationale }
@app.post("/apply-fix")     # { diff } -> { ok, files_changed }

Intent List (v1)

find_errors, explain_code, find_symbol, navigate_to, run_tests,
explain_trace, propose_fix, apply_fix, format_file, rename_symbol.

Extension Commands

echodebug.talk, echodebug.stopListening,
echodebug.explainSelection, echodebug.applyFix, echodebug.openSettings.

Sample LLM Prompt (Intent Classification)
System: You are an NLU router for a voice debugger. Output ONLY JSON per schema.
User: "highlight everywhere userData is changed and then explain the last change"
Assistant (JSON):
{
  "intent": "find_symbol",
  "entities": { "symbol": "userData", "scope": "writes" },
  "follow_up_allowed": true
}

Risk → Mitigation

Hallucinated fixes → AST validation + unit tests post-patch.

Breaking changes → Always use a branch; require confirmation.

Latency → Caching, chunked context, local STT.

Privacy → Redaction + local-only mode.

Backlog Ideas (post-MVP)

Multi-file refactors via language servers.

“Explain diff” and “Why test failed” narratives.

Agents that propose tests before fixes.

Session export (markdown transcript with code refs)
