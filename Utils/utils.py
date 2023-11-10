
import time
import webbrowser as web
from platform import system

import pyautogui

import os

os.environ['DISPLAY'] = ':0'

_ALWAYS_SAFE = frozenset(b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                         b'abcdefghijklmnopqrstuvwxyz'
                         b'0123456789'
                         b'_.-~')
_ALWAYS_SAFE_BYTES = bytes(_ALWAYS_SAFE)

def check_number(number: str) -> bool:
    return "+" in number or "_" in number

def quote(string, safe='/', encoding=None, errors=None):
    if isinstance(string, str):
        if not string:
            return string
        if encoding is None:
            encoding = 'utf-8'
        if errors is None:
            errors = 'strict'
        string = string.encode(encoding, errors)
    else:
        if encoding is not None:
            raise TypeError("quote() doesn't support 'encoding' for bytes")
        if errors is not None:
            raise TypeError("quote() doesn't support 'errors' for bytes")
    return quote_from_bytes(string, safe)

class _Quoter(dict):
    def __init__(self, safe):
        self.safe = _ALWAYS_SAFE.union(safe)
    def __repr__(self):
        return f"<Quoter {dict(self)!r}>"
    def __missing__(self, b):
        res = chr(b) if b in self.safe else '%{:02X}'.format(b)
        self[b] = res
        return res

def _byte_quoter_factory(safe):
    return _Quoter(safe).__getitem__

def quote_from_bytes(bs, safe='/'):
    if not isinstance(bs, (bytes, bytearray)):
        raise TypeError("quote_from_bytes() expected bytes")
    if not bs:
        return ''
    if isinstance(safe, str):
        safe = safe.encode('ascii', 'ignore')
    else:
        safe = bytes([c for c in safe if c < 128])
    if not bs.rstrip(_ALWAYS_SAFE_BYTES + safe):
        return bs.decode()
    quoter = _byte_quoter_factory(safe)
    return ''.join([quoter(char) for char in bs])

def close_tab(wait_time: int = 2) -> None:
    time.sleep(wait_time)
    if system().lower() in ("windows", "linux"):
        pyautogui.hotkey("ctrl", "w")
    elif system().lower() == "darwin":
        pyautogui.hotkey("command", "w")
    else:
        raise Warning(f"{system().lower()} not supported!")
    pyautogui.press("enter")

def enviar_mensaje_instantaneamente(
    phone_no: str,
    message: str,
    wait_time: int = 15,
    tab_close: bool = False,
    close_time: int = 3,
) -> None:
    if not check_number(number=phone_no):
        raise print("Country Code Missing in Phone Number!")
    web.open(f"https://web.whatsapp.com/send?phone={phone_no}&text={quote(message)}")
    time.sleep(8)
    pyautogui.press("enter")
    if tab_close:
        close_tab(wait_time=close_time)