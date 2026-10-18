NAME = "ROULETTE"
STATUS_ACTION = "roulette.status"
HINT = "R=spin S=status TAB"

state = {"result": "-"}


def apply(data):
    if isinstance(data, dict) and "result" in data:
        state["result"] = str(data["result"]) or "-"
        return True
    return False


def rows():
    return [
        {"label": "RESULT:", "value": state["result"], "lines": 4},
    ]
