NAME = "RADIO"
STATUS_ACTION = "radio.status"
HINT = "1-3=st SPACE=pp N=next TAB"

state = {"station": "-", "track": "-", "playing": False}


def apply(data):
    if not isinstance(data, dict):
        return False
    changed = False
    if "station" in data:
        state["station"] = str(data["station"]) or "-"
        changed = True
    if "track" in data:
        state["track"] = str(data["track"]) or "-"
        changed = True
    if "playing" in data:
        state["playing"] = bool(data["playing"])
        changed = True
    return changed


def rows():
    return [
        {"label": "STATION:", "value": state["station"], "lines": 1},
        {"label": "TRACK:", "value": state["track"], "lines": 2},
        {"label": "PLAYING:",
         "value": "ON" if state["playing"] else "OFF",
         "style": "ok" if state["playing"] else "accent"},
    ]
