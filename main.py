import gc
import time

import config
import net
import profiles
import ui

_ENV_MAP = {
    "WIFI_SSID": ("WIFI", "ssid"),
    "WIFI_PASSWORD": ("WIFI", "password"),
    "BASE_URL": ("SERVER", "base_url"),
}

app = {
    "profile": profiles.ALL[0],
    "online": False,
    "ip": "",
    "err": "",
    "err_until": 0,
    "dirty": True,
}


def load_env():
    try:
        with open(".env") as file:
            lines = file.readlines()
    except OSError:
        print("[env] .env не найден — используются значения из config.py")
        return

    loaded = 0
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition("=")
        key = key.strip()
        if not sep or key not in _ENV_MAP:
            continue
        target, field = _ENV_MAP[key]
        getattr(config, target)[field] = value.strip().strip("\"'")
        loaded += 1
    print("[env] переменных из .env:", loaded)


def flash_error(msg):
    app["err"] = msg
    app["err_until"] = time.time() + 2
    app["dirty"] = True


def run_action(action):
    if action not in config.ACTIONS:
        print("[cmd] неизвестное действие:", action)
        return
    if not app["online"]:
        print("[cmd] OFFLINE, пропущено:", action)
        return

    method, path, body = config.ACTIONS[action]
    print("[cmd]", method, path)
    status, data = net.http_request(method, path, body)

    if status == net.UNREACHABLE:
        flash_error("ERR CON")
    elif status == net.TRANSPORT_ERROR:
        flash_error("ERR TO")
    elif status >= 400:
        flash_error("ERR %d" % status)
    elif app["profile"].apply(data):
        app["dirty"] = True


def switch_profile():
    app["profile"] = profiles.next_after(app["profile"])
    app["dirty"] = True
    print("[ui] профиль:", app["profile"].NAME)
    run_action(app["profile"].STATUS_ACTION)


def handle_key(key):
    if key == "\t":
        switch_profile()
        return

    action = config.KEYS.get(app["profile"].NAME, {}).get(key.lower())
    if action:
        run_action(action)
    else:
        print("[key] нет действия для", repr(key))


def sync_wifi():
    online = net.wifi_step()
    if online != app["online"]:
        app["online"] = online
        app["ip"] = net.wifi_ip() if online else ""
        app["dirty"] = True
        print("[wifi]", "подключено:" if online else "связь потеряна",
              app["ip"])


def main():
    print("=== Web Pult Bridge ===")
    load_env()

    app["online"] = net.wifi_wait()
    app["ip"] = net.wifi_ip() if app["online"] else ""
    ui.draw(app)

    last_poll = 0
    while True:
        sync_wifi()

        for key in ui.read_keys():
            handle_key(key)

        if config.STATUS_POLL and app["online"]:
            now = time.time()
            if now - last_poll >= config.STATUS_POLL:
                last_poll = now
                run_action(app["profile"].STATUS_ACTION)

        if app["err"] and time.time() >= app["err_until"]:
            app["err"] = ""
            app["dirty"] = True

        if app["dirty"]:
            ui.draw(app)
            app["dirty"] = False

        gc.collect()
        time.sleep_ms(30)


if __name__ == "__main__":
    main()
