from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.agents import context_agent, database_agent, reasoning_agent, writing_agent
from app.models import ContextFinding, OptimizationResult, Verdict

class State(TypedDict, total=False):
    game_id: str
    team: str
    result: OptimizationResult
    context: list[ContextFinding]
    verdict: Verdict
    article: str

def _publish_or_end(state: State) -> str:
    return 'writing' if state['verdict'].should_publish else END

_g = StateGraph(State)
_g.add_node('database', database_agent.run)
_g.add_node('context', context_agent.run)
_g.add_node('reasoning', reasoning_agent.run)
_g.add_node('writing', writing_agent.run)
_g.add_edge(START, 'database')
_g.add_edge('database', 'context')
_g.add_edge('context', 'reasoning')
_g.add_conditional_edges('reasoning', _publish_or_end)
_g.add_edge('writing', END)
graph = _g.compile()

def analyze(game_id: str, team: str) -> State:
    """Run the online pipeline; returns final state, with 'article' set if publishable."""
    return graph.invoke({'game_id': game_id, 'team': team})
