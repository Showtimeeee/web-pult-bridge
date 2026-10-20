import time

from machine import Pin, SPI, UART

import config

COL_BG = 0x0000
COL_FG = 0xFFFF
COL_DIM = 0x8410
COL_ACCENT = 0xF800
COL_OK = 0x07E0

_STYLES = {"fg": COL_FG, "dim": COL_DIM, "accent": COL_ACCENT, "ok": COL_OK}
_CHARS_PER_LINE = 30

_kbd = UART(config.KEYBOARD["uart"], baudrate=config.KEYBOARD["baud"],
            rx=Pin(config.KEYBOARD["rx"]), tx=Pin(config.KEYBOARD["tx"]))

_last_press = {}


def read_keys():
    # спецклавиши Cardputer приходят многобайтовыми последовательностями,
    # здесь нужны только Tab (0x09) и печатные ASCII-символы
    keys = []
    if not _kbd.any():
        return keys
    now = time.ticks_ms()
    for byte in _kbd.read() or b"":
        if byte == 0x09:
            key = "\t"
        elif 32 <= byte < 127:
            key = chr(byte)
        else:
            continue
        last = _last_press.get(key)
        if last is not None and \
                time.ticks_diff(now, last) < config.KEYBOARD["cooldown"]:
            continue
        _last_press[key] = now
        keys.append(key)
    return keys


def _init_lcd():
    cfg = config.DISPLAY
    try:
        import st7789
        spi = SPI(1, baudrate=cfg["spi_baud"],
                  sck=Pin(cfg["sck"]), mosi=Pin(cfg["mosi"]))
        lcd = st7789.ST7789(
            height=cfg["height"], width=cfg["width"], spi=spi,
            cs=Pin(cfg["cs"]), dc=Pin(cfg["dc"]), rst=Pin(cfg["rst"]),
            rotation=cfg["rotation"],
        )
        if "bl" in cfg:
            try:
                Pin(cfg["bl"], Pin.OUT).value(1)
            except Exception as e:
                print("[lcd] подсветка:", e)
        print("[lcd] инициализирован 240x135")
        return lcd
    except Exception as e:
        print("[lcd] экран недоступен, консольный режим:", e)
        return None


lcd = _init_lcd()


def _wrap(text, limit=_CHARS_PER_LINE - 1):
    lines, current = [], ""
    for word in str(text).split():
        while len(word) > limit:
            if current:
                lines.append(current)
                current = ""
            lines.append(word[:limit])
            word = word[limit:]
        candidate = (current + " " + word).strip()
        if len(candidate) <= limit:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or ["-"]


def draw(app):
    if lcd is None:
        return

    profile = app["profile"]

    lcd.fill(COL_BG)
    lcd.text("WEB PULT", 2, 2, COL_DIM)
    lcd.text(profile.NAME, 240 - len(profile.NAME) * 8, 2, COL_OK)
    lcd.fill_rect(0, 13, 240, 1, COL_DIM)

    y = 24
    for row in profile.rows():
        lcd.text(row["label"], 2, y, COL_DIM)
        y += 10
        for line in _wrap(row["value"])[:row.get("lines", 1)]:
            lcd.text(line, 2, y, _STYLES.get(row.get("style", "fg"), COL_FG))
            y += 10
        y += 2

    if y < 108:
        lcd.text(profile.HINT, 2, 110, COL_DIM)

    if app["online"]:
        lcd.text("ON " + app["ip"], 2, 124, COL_FG)
    else:
        lcd.text("OFFLINE", 2, 124, COL_ACCENT)
    if app["err"]:
        lcd.text(app["err"], 240 - len(app["err"]) * 8, 124, COL_ACCENT)

    try:
        lcd.show()
    except AttributeError:
        pass
