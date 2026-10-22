NAME = "LIGHTS"
STATUS_ACTION = "lights.status"
HINT = "1-3=scene SPACE=pp S=st TAB"

state = {"on": False, "scene": "-", "brightness": 0}


def apply(data):
    if not isinstance(data, dict):
        return False
    changed = False
    if "on" in data:
        state["on"] = bool(data["on"])
        changed = True
    if "scene" in data:
        state["scene"] = str(data["scene"]) or "-"
        changed = True
    if "brightness" in data:
        state["brightness"] = int(data["brightness"])
        changed = True
    return changed


def rows():
    return [
        {"label": "POWER:", "value": "ON" if state["on"] else "OFF",
         "style": "ok" if state["on"] else "accent"},
        {"label": "SCENE:", "value": state["scene"], "lines": 1},
        {"label": "BRIGHT:", "value": "%d%%" % state["brightness"]},
    ]
