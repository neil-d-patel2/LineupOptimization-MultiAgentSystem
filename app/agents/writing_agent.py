from langchain_anthropic import ChatAnthropic

from app.models import findings_block

PROMPT = """Write a Markdown article for lineupoptimization.com analyzing this lineup.

{summary}

Editorial verdict: {rationale}

Supporting context:
{findings}

Rules:
- Every number must come from the optimizer output above. Never invent or adjust statistics.
- Every claim about injuries, rest, or roster moves must cite the supporting context.
- Lead with the most interesting difference between the lineups, explain what the
  optimizer prefers and why the manager may have chosen otherwise.
- Conversational but grounded; no hedging filler.
- Output only the article Markdown, starting with an H1 title."""

def run(state):
    writer = ChatAnthropic(model='claude-sonnet-5', max_tokens=4096)
    article = writer.invoke(PROMPT.format(summary=state['result'].summary(),
                                          rationale=state['verdict'].rationale,
                                          findings=findings_block(state['context'])))
    return {'article': article.text}
