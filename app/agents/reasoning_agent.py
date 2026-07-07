from langchain_anthropic import ChatAnthropic

from app.models import Verdict

PROMPT = """You are judging whether a lineup optimization result is worth publishing an
analysis about. You do not propose lineups or estimate run production — the numbers below
come from a deterministic optimizer and are ground truth.

Game {game_id}, {team}, {game_date} (optimizer {optimizer_version}):
- Announced lineup: {announced}
- Optimized lineup: {optimized}
- Expected runs announced: {announced_runs:.3f}
- Expected runs optimized: {optimized_runs:.3f}
- Expected improvement: {improvement:.3f} runs/game

Context gathered from public sources:
{findings}

Decide:
- materially_different: is the improvement meaningful (roughly 0.1 runs/game or more)
  and do the lineups differ in ways readers would care about?
- explained_by_context: do injuries, rest days, scratches, or roster moves account for
  the differences? A constrained manager is not making a mistake.
- should_publish: true only if the difference is material AND there is an interesting,
  evidence-backed story — either an unexplained suboptimal choice or a notable constraint.
- rationale: two or three sentences a writer can build the article around."""

def run(state):
    result, context = state['result'], state['context']
    findings = '\n'.join(f'- [{f.category}] {f.detail} ({f.source})' for f in context) or '- none found'
    judge = ChatAnthropic(model='claude-sonnet-5').with_structured_output(Verdict)
    verdict = judge.invoke(PROMPT.format(
        game_id=result.game_id, team=result.team, game_date=result.game_date,
        optimizer_version=result.optimizer_version,
        announced=result.announced_lineup, optimized=result.optimized_lineup,
        announced_runs=result.announced_expected_runs,
        optimized_runs=result.optimized_expected_runs,
        improvement=result.improvement, findings=findings))
    return {'verdict': verdict}
