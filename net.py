import json
import socket
import time

import network

import config

UNREACHABLE = -1
TRANSPORT_ERROR = -2

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

_wifi_next_try = 0
_ip = ""


def wifi_ip():
    return _ip


def wifi_step():
    global _wifi_next_try, _ip

    if wlan.isconnected():
        _ip = wlan.ifconfig()[0]
        return True

    _ip = ""
    now = time.time()
    if now >= _wifi_next_try:
        _wifi_next_try = now + config.WIFI["retry_every"]
        print("[wifi] подключение к", config.WIFI["ssid"], "...")
        try:
            wlan.connect(config.WIFI["ssid"], config.WIFI["password"])
        except OSError as e:
            print("[wifi] ошибка:", e)
    return False


def wifi_wait():
    global _wifi_next_try
    deadline = time.time() + config.WIFI["timeout"]
    while time.time() < deadline:
        if wifi_step():
            return True
        time.sleep_ms(200)
    print("[wifi] не удалось подключиться, работаем OFFLINE")
    _wifi_next_try = time.time() + config.WIFI["retry_every"]
    return False


def _base_host_port():
    url = config.SERVER["base_url"]
    url = url.split("://", 1)[-1].split("/", 1)[0]
    host, _, port = url.partition(":")
    return host, int(port) if port else 80


def _connect(host, port):
    for attempt in (1, 2):
        sock = socket.socket()
        try:
            sock.settimeout(config.SERVER["timeout"])
            sock.connect((host, port))
            return sock
        except OSError as e:
            sock.close()
            print("[http] нет соединения (попытка %d):" % attempt, e)
            if attempt == 1:
                time.sleep(config.SERVER["retry_delay"])
    return None


def http_request(method, path, body=None):
    host, port = _base_host_port()

    sock = _connect(host, port)
    if sock is None:
        return UNREACHABLE, None

    try:
        payload = body.encode() if body else b""
        head = "%s %s HTTP/1.1\r\nHost: %s:%d\r\nConnection: close\r\n" \
               "User-Agent: web-pult-bridge/1.0\r\n" % (method, path, host, port)
        if payload:
            head += "Content-Type: application/json\r\n" \
                    "Content-Length: %d\r\n" % len(payload)
        head += "\r\n"
        sock.send(head.encode() + payload)

        buf = b""
        while True:
            chunk = sock.recv(1024)
            if not chunk:
                break
            buf += chunk
    except OSError as e:
        print("[http] таймаут/сбой:", e)
        return TRANSPORT_ERROR, None
    finally:
        sock.close()

    header, _, raw = buf.partition(b"\r\n\r\n")
    try:
        status = int(header.split(b" ", 2)[1])
    except (IndexError, ValueError):
        print("[http] битый ответ:", header[:60])
        return TRANSPORT_ERROR, None

    data = None
    if raw:
        try:
            data = json.loads(raw)
        except (ValueError, TypeError):
            pass
    return status, data
