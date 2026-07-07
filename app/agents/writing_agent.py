from langchain_anthropic import ChatAnthropic

PROMPT = """Write a Markdown article for lineupoptimization.com analyzing this lineup.

Game {game_id}, {team}, {game_date} (optimizer {optimizer_version}):
- Announced lineup: {announced}
- Optimized lineup: {optimized}
- Expected runs announced: {announced_runs:.3f}
- Expected runs optimized: {optimized_runs:.3f}
- Expected improvement: {improvement:.3f} runs/game

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
    result, verdict = state['result'], state['verdict']
    findings = '\n'.join(f'- [{f.category}] {f.detail} ({f.source})' for f in state['context']) or '- none'
    writer = ChatAnthropic(model='claude-sonnet-5', max_tokens=4096)
    article = writer.invoke(PROMPT.format(
        game_id=result.game_id, team=result.team, game_date=result.game_date,
        optimizer_version=result.optimizer_version,
        announced=result.announced_lineup, optimized=result.optimized_lineup,
        announced_runs=result.announced_expected_runs,
        optimized_runs=result.optimized_expected_runs,
        improvement=result.improvement,
        rationale=verdict.rationale, findings=findings))
    return {'article': article.text}
