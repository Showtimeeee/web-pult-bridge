# Web Pult Bridge

MicroPython-приложение для **M5Stack Cardputer ADV**: превращает устройство в
физический пульт для веб-рулетки и веб-радио. Cardputer подключается к Wi-Fi и по
нажатию клавиш шлёт HTTP-запросы на твой веб-сервер, показывая состояние на экране.

Клавиши: **Tab** — смена профиля.
`ROULETTE`: **R** — крутить, **S** — статус.
`RADIO`: **1/2/3** — станция, **Space** — пауза/игра, **N** — следующий трек.

## Запуск

1. Прошей устройство community-сборкой MicroPython (нужен модуль `st7789`;
   без него приложение работает в консольном режиме).

2. Заполни секреты:

   ```bash
   cp .env.example .env
   ```

   В `.env` — `WIFI_SSID`, `WIFI_PASSWORD`, `BASE_URL` (адрес твоего веб-сервера).
   Остальное (клавиши, эндпоинты, пины, таймауты) — в `config.py`.

3. Загрузи файлы на устройство (папку `profiles` тоже) и запусти:

   ```bash
   mpremote connect auto cp config.py .env net.py ui.py main.py :
   mpremote connect auto cp -r profiles :
   mpremote connect auto run main.py
   ```

   либо через Thonny: перетащи все файлы и папку `profiles` в корень устройства
   и запусти `main.py`.

Сервер должен отдавать JSON по эндпоинтам из `config.ACTIONS`
(`POST /api/roulette/spin`, `GET /api/roulette/status`, `POST /api/radio/station`,
`POST /api/radio/toggle`, `POST /api/radio/next`, `GET /api/radio/status`).
