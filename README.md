# LineupOptimization-MultiAgentSystem

Agent system for lineupoptimization.com

MLB lineup analysis in two pipelines:

- **Offline:** a deterministic optimizer computes optimal lineups from announced
  lineups and player statistics, persisting results to PostgreSQL.
- **Online:** agents retrieve stored results, gather context (injuries, rest days,
  platoons), judge whether the difference is worth discussing, and write the analysis.

The LLM explains optimization results; it never produces them.

## Development setup

Requires Python 3.14+.

```bash
git clone <repo-url>
cd LineupOptimization-MultiAgentSystem

# Create your local virtual environment (not committed — everyone makes their own)
python3 -m venv .venv
source .venv/bin/activate

# Install shared dependencies
pip install -r requirements.txt

# Set up local secrets
cp .env.example .env   # then fill in real values

# PostgreSQL (macOS / Homebrew)
brew install postgresql@17
brew services start postgresql@17
createdb lineupopt
psql -d lineupopt -f schema.sql
```

If `createdb`/`psql` aren't on your PATH, they live in
`/opt/homebrew/opt/postgresql@17/bin`.

Re-activate with `source .venv/bin/activate` at the start of each session.
When you add a dependency, add it to `requirements.txt` and commit so the
team stays in sync.
