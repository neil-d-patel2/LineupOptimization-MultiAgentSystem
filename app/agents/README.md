# Agents

The online pipeline, run as a LangGraph graph (see `app/graph.py`):

```
database → context → reasoning → (publish?) → writing
```

Each agent is a node function that takes the pipeline state and returns the
keys it adds. State keys: `game_id`, `team` (inputs), then `result`,
`context`, `verdict`, `article` added in order.

## Database Agent — `database_agent.py`

Retrieves the stored optimization result for a game/team from PostgreSQL.
Pure retrieval: no LLM, no inference. Fails loudly if no result exists —
the offline optimizer must have run first.

- In: `game_id`, `team`
- Out: `result` (`OptimizationResult`: both lineups, expected runs for each,
  improvement, optimizer version)

## Context Agent — `context_agent.py`

Gathers outside evidence that could explain why the announced lineup differs
from the optimizer's: injuries, rest days, late scratches, probable pitcher /
platoon considerations, roster moves, manager comments. Uses Claude with the
web search tool — the model decides what to search for and loops until it has
what it needs. Collects evidence only; it does not judge the lineup.

- In: `result`
- Out: `context` (list of `ContextFinding`: category, detail, source)

## Reasoning Agent — `reasoning_agent.py`

Combines the optimization result with the contextual evidence and decides
whether there is a story worth publishing: Is the difference material? Is it
explained by injuries or availability rather than managerial choice? One
structured-output LLM call; no searching, no writing.

- In: `result`, `context`
- Out: `verdict` (`Verdict`: materially_different, explained_by_context,
  should_publish, rationale)

If `should_publish` is false the graph ends here — "nothing worth writing
about today" is a normal outcome.

## Writing Agent — `writing_agent.py`

Turns the result, evidence, and verdict into a publication-ready Markdown
article. Presentation only: every number comes from the optimizer output and
every claim from the gathered context. It never invents statistics.

- In: `result`, `context`, `verdict`
- Out: `article` (Markdown)
