
import pathlib
import time
import webbrowser as web
from platform import system

import lackey
from lackey import *
from pyautogui import click, hotkey, press, size, typewrite

WIDTH, HEIGHT = size()

_ALWAYS_SAFE = frozenset(b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                         b'abcdefghijklmnopqrstuvwxyz'
                         b'0123456789'
                         b'_.-~')
_ALWAYS_SAFE_BYTES = bytes(_ALWAYS_SAFE)

btn_send = "../Files/src/send_msg.JPG"

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
        hotkey("ctrl", "w")
    elif system().lower() == "darwin":
        hotkey("command", "w")
    else:
        raise Warning(f"{system().lower()} not supported!")
    press("enter")

def enviar_mensaje_instantaneamente(
    phone_no: str,
    message: str,
    wait_time: int = 8,
    tab_close: bool = False,
    close_time: int = 3,
        ) -> None:
    if not check_number(number=phone_no):
        raise print("Country Code Missing in Phone Number!")
    web.open(f"https://web.whatsapp.com/send?phone={phone_no}&text={quote(message)}")
    print(f"https://web.whatsapp.com/send?phone={phone_no}&text={quote(message)}")
    time.sleep(wait_time)
    if lackey.exists(btn_send):
      lackey.click(btn_send)
    time.sleep(1)
    if tab_close:
        close_tab(wait_time=close_time)

def check_navegador(tab_close: bool = False,close_time: int = 3,):
    web.open(f"https://web.whatsapp.com/")
    time.sleep(8)
    if tab_close:
        close_tab(wait_time=close_time)

def enviar_imagen(
    receiver: str,
    img_path: str,
    caption: str = "",
    wait_time: int = 15,
    tab_close: bool = False,
    close_time: int = 3,
) -> None:
    """Send Image to a WhatsApp Contact or Group at a Certain Time"""

    if (not receiver.isalnum()) and (not check_number(number=receiver)):
        raise print("Country Code Missing in Phone Number!")

    current_time = time.localtime()
    send_image(
        path=img_path, caption=caption, receiver=receiver, wait_time=wait_time
    )
    log_image(_time=current_time, path=img_path, receiver=receiver, caption=caption)
    if tab_close:
        close_tab(wait_time=close_time)


def log_image(_time: time.struct_time, path: str, receiver: str, caption: str) -> None:
    """Logs the Image Information after it is Sent"""

    if not os.path.exists("PyWhatKit_DB.txt"):
        file = open("PyWhatKit_DB.txt", "w+")
        file.close()

    caption = format_message(caption)

    with open("PyWhatKit_DB.txt", "a", encoding="utf-8") as file:
        if check_number(number=receiver):
            file.write(
                f"Date: {_time.tm_mday}/{_time.tm_mon}/{_time.tm_year}\nTime: {_time.tm_hour}:{_time.tm_min}\n"
                f"Phone Number: {receiver}\nImage: {path}\nCaption: {caption}"
            )

        else:
            file.write(
                f"Date: {_time.tm_mday}/{_time.tm_mon}/{_time.tm_year}\nTime: {_time.tm_hour}:{_time.tm_min}\n"
                f"Group ID: {receiver}\nImage: {path}\nCaption: {caption}"
            )
        file.write("\n--------------------\n")
        file.close()


def format_message(message: str) -> str:
    """Formats the Message to remove redundant Spaces and Newline chars"""
    msg_l = message.split(" ")
    new = []
    for x in msg_l:
        if "\n" in x:
            x = x.replace("\n", "")
            new.append(x) if not len(x) == 0 else None

        elif len(x) != 0:
            new.append(x)

    return " ".join(new)


def send_image(path: str, caption: str, receiver: str, wait_time: int) -> None:
    """Sends the Image to a Contact or a Group based on the Receiver"""

    _web(message=caption, receiver=receiver)

    time.sleep(7)
    click(WIDTH / 2, HEIGHT / 2)
    time.sleep(wait_time - 7)
    copy_image(path=path)
    if not check_number(number=receiver):
        for char in caption:
            if char == "\n":
                hotkey("shift", "enter")
            else:
                typewrite(char)
    else:
        typewrite(" ")
    if system().lower() == "darwin":
        hotkey("command", "v")
    else:
        hotkey("ctrl", "v")
    time.sleep(1)
    press("enter")

def _web(receiver: str, message: str) -> None:
    """Opens WhatsApp Web based on the Receiver"""
    if check_number(number=receiver):
        web.open(
            "https://web.whatsapp.com/send?phone="
            + receiver
            + "&text="
            + quote(message)
        )
    else:
        web.open("https://web.whatsapp.com/accept?code=" + receiver)


def copy_image(path: str) -> None:
    """Copy the Image to Clipboard based on the Platform"""

    if system().lower() == "linux":
        if pathlib.Path(path).suffix in (".PNG", ".png"):
            os.system(f"copyq copy image/png - < {path}")
        elif pathlib.Path(path).suffix in (".jpg", ".JPG", ".jpeg", ".JPEG"):
            os.system(f"copyq copy image/jpeg - < {path}")
        else:
            raise Exception(
                f"File Format {pathlib.Path(path).suffix} is not Supported!"
            )
    elif system().lower() == "windows":
        from io import BytesIO

        import win32clipboard
        from PIL import Image

        image = Image.open(path)
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
    elif system().lower() == "darwin":
        if pathlib.Path(path).suffix in (".jpg", ".jpeg", ".JPG", ".JPEG"):
            os.system(
                f"osascript -e 'set the clipboard to (read (POSIX file \"{path}\") as JPEG picture)'"
            )
        else:
            raise Exception(
                f"File Format {pathlib.Path(path).suffix} is not Supported!"
            )
    else:
        raise Exception(f"Unsupported System: {system().lower()}")
