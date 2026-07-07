from langchain_anthropic import ChatAnthropic

from app.models import Verdict, findings_block

PROMPT = """You are judging whether a lineup optimization result is worth publishing an
analysis about. You do not propose lineups or estimate run production — the numbers below
come from a deterministic optimizer and are ground truth.

{summary}

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
    judge = ChatAnthropic(model='claude-sonnet-5').with_structured_output(Verdict)
    verdict = judge.invoke(PROMPT.format(summary=state['result'].summary(),
                                         findings=findings_block(state['context'])))
    return {'verdict': verdict}
