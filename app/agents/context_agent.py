from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel

from app.models import ContextFinding

class Findings(BaseModel):
    findings: list[ContextFinding]

RESEARCH_PROMPT = """Search the web for context on the {team} lineup for their game on {game_date}.
Look for: injuries, scheduled rest days, late scratches, the probable opposing starting pitcher
and platoon considerations, recent roster transactions, and manager comments about the lineup.

Announced lineup: {announced}
Optimizer's preferred lineup: {optimized}

Pay special attention to players whose batting slot differs between the two lineups.
Report only what you find, citing the source of each item. Do not evaluate whether the
lineup is good or bad."""

def run(state):
    result = state['result']
    researcher = ChatAnthropic(model='claude-sonnet-5', max_tokens=4096).bind_tools(
        [{'type': 'web_search_20250305', 'name': 'web_search', 'max_uses': 5}])
    research = researcher.invoke(RESEARCH_PROMPT.format(
        team=result.team, game_date=result.game_date,
        announced=result.announced_lineup, optimized=result.optimized_lineup))

    extractor = ChatAnthropic(model='claude-sonnet-5').with_structured_output(Findings)
    extracted = extractor.invoke(
        'Extract each lineup-relevant fact from this research as a finding with '
        'category (injury, rest_day, scratch, platoon, transaction, manager_comment), '
        f'detail, and source:\n\n{research.text}')
    return {'context': extracted.findings}
