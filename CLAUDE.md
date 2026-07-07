# Project Memory

## Overview

MLB batting-lineup analysis system for lineupoptimization.com. Two pipelines:

- **Offline:** deterministic lineup optimizer runs once per game when official
  lineups are announced; results (announced lineup, optimized lineup, expected
  runs for both, improvement, optimizer version, timestamp) persist to PostgreSQL.
- **Online:** Database Agent (retrieval) → Context Agent (injuries, rest days,
  platoons, manager comments) → Reasoning Agent (is the difference meaningful and
  explainable?) → Writing Agent (Markdown article).

Core principle: the LLM explains optimizer output; it never proposes lineups or
estimates run production itself.

## Architecture

Full design document lives in the repo owner's notes; key decisions:

- Optimization is expensive and runs offline once per game; the online path is
  DB lookup + reasoning only.
- Every published analysis references a stored optimization result and optimizer
  version for reproducibility.
- Context gathering is separated from interpretation so injuries/constraints are
  not misread as managerial mistakes.

## Development Commands

- Setup: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
- Secrets: copy `.env.example` to `.env` (gitignored) and fill in values.
  `ANTHROPIC_API_KEY` is read by langchain-anthropic; `DATABASE_URL` by `app/db.py`.
- Dependencies are shared via `requirements.txt`, not the venv itself — the
  `.venv/` directory is gitignored and machine-specific.
- Postgres (macOS/Homebrew): `brew install postgresql@17 && brew services start postgresql@17`,
  then `createdb lineupopt && psql -d lineupopt -f schema.sql`
  (binaries in `/opt/homebrew/opt/postgresql@17/bin` if not on PATH).
- Local `DATABASE_URL`: `postgresql://localhost:5432/lineupopt`.

## Build Process

(none yet)

## Deployment Process

(none yet)

## Coding Standards

- Python 3.14.
- Agent orchestration uses LangGraph (`langgraph` + `langchain-anthropic`);
  the online pipeline is modeled as a LangGraph graph. The Context Agent is the
  component with real tool-use loops (web lookups for injuries, scratches, etc.).

## Known Issues

(none yet)

## Lessons Learned

- Homebrew `postgresql@17` (brew 6.0.6, macOS arm64) can install with a broken
  post-install: the server expects `/opt/homebrew/lib/postgresql@17` but brew
  links `/opt/homebrew/lib/postgresql`, so `initdb` never runs and the service
  crash-loops. Fix: `ln -s /opt/homebrew/Cellar/postgresql@17/<ver>/lib/postgresql
  /opt/homebrew/lib/postgresql@17`, run `initdb /opt/homebrew/var/postgresql@17`,
  then `brew services restart postgresql@17`.
- `.env` uses `ANTHROPIC_API_KEY` (not `LLM_API_KEY`) — it's the name
  langchain-anthropic reads from the environment.

## Decisions

- 2026-07-06: venv-per-developer with committed `requirements.txt`, rather than
  attempting to share a venv (venvs contain machine-specific paths/binaries).
- 2026-07-06: LangGraph chosen as the agent framework — the Context Agent needs
  online lookup loops (injuries, outside factors affecting lineups), and the
  owner wants the pipeline built as agents rather than plain functions.

## Notes

Suggested build order: MLB data ingestion → optimizer → Postgres persistence →
online pipeline (DB/context/reasoning/writing).
