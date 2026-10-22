# Значения Wi-Fi и SERVER.base_url по умолчанию.
# Секреты переопределяются в файле .env (см. .env.example).

WIFI = {
    "ssid": "YOUR_SSID",
    "password": "YOUR_PASSWORD",
    "timeout": 15,       # сек
    "retry_every": 10,    # сек между попытками переподключения
}

SERVER = {
    "base_url": "http://192.168.1.100:8000",
    "timeout": 5,         # сек, таймаут HTTP-запроса
    "retry_delay": 2,     # сек, пауза перед ОДНОЙ повторной попыткой
}

KEYS = {
    "ROULETTE": {
        "r": "roulette.spin",
        "s": "roulette.status",
    },
    "RADIO": {
        "1": "radio.station.1",
        "2": "radio.station.2",
        "3": "radio.station.3",
        " ": "radio.toggle",
        "n": "radio.next",
    },
    "LIGHTS": {
        "1": "lights.scene.1",
        "2": "lights.scene.2",
        "3": "lights.scene.3",
        " ": "lights.toggle",
        "s": "lights.status",
    },
}

# действие -> (метод, путь, тело запроса JSON-строкой или None)
ACTIONS = {
    "roulette.spin":    ("POST", "/api/roulette/spin",   None),
    "roulette.status":  ("GET",  "/api/roulette/status", None),
    "radio.station.1":  ("POST", "/api/radio/station",   '{"id": 1}'),
    "radio.station.2":  ("POST", "/api/radio/station",   '{"id": 2}'),
    "radio.station.3":  ("POST", "/api/radio/station",   '{"id": 3}'),
    "radio.toggle":     ("POST", "/api/radio/toggle",    None),
    "radio.next":       ("POST", "/api/radio/next",      None),
    "radio.status":     ("GET",  "/api/radio/status",    None),
    "lights.scene.1":   ("POST", "/api/lights/scene",    '{"id": 1}'),
    "lights.scene.2":   ("POST", "/api/lights/scene",    '{"id": 2}'),
    "lights.scene.3":   ("POST", "/api/lights/scene",    '{"id": 3}'),
    "lights.toggle":    ("POST", "/api/lights/toggle",   None),
    "lights.status":    ("GET",  "/api/lights/status",   None),
}

# период фонового опроса статуса активного профиля в секундах, 0 = выкл.
STATUS_POLL = 5

KEYBOARD = {
    "uart": 2,
    "rx": 15,
    "tx": 13,
    "baud": 115200,
    "cooldown": 300,     # мс: защита от автоповтора при зажатой клавише
}

DISPLAY = {
    "sck": 36,
    "mosi": 35,
    "dc": 34,
    "cs": 33,
    "rst": 37,
    "bl": 38,
    "width": 240,
    "height": 135,
    "rotation": 90,      # 0 / 90 / 180 / 270, если картинка перевёрнута
    "spi_baud": 40000000,
}
