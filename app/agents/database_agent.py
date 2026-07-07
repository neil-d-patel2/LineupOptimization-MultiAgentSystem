from app import db

def run(state):
    result = db.fetch_result(state['game_id'], state['team'])
    if result is None:
        raise LookupError(f"no optimization stored for game {state['game_id']}, team {state['team']}")
    return {'result': result}
