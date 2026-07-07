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

def build():
    g = StateGraph(State)
    g.add_node('database', database_agent.run)
    g.add_node('context', context_agent.run)
    g.add_node('reasoning', reasoning_agent.run)
    g.add_node('writing', writing_agent.run)
    g.add_edge(START, 'database')
    g.add_edge('database', 'context')
    g.add_edge('context', 'reasoning')
    g.add_conditional_edges('reasoning', _publish_or_end)
    g.add_edge('writing', END)
    return g.compile()

def analyze(game_id: str, team: str) -> State:
    """Run the online pipeline; returns final state, with 'article' set if publishable."""
    return build().invoke({'game_id': game_id, 'team': team})
