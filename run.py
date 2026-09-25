
import hashlib
import os
import platform
import subprocess
import sys
import time
import webbrowser
from datetime import datetime
from urllib.parse import quote
import requests

# ANSI Color & Style Codes
R = "\033[1;31m"        # Red
G = "\033[1;32m"        # Green
Y = "\033[1;33m"        # Yellow
B = "\033[1;34m"        # Blue
C = "\033[1;36m"        # Cyan
W = "\033[1;37m"        # White
M = "\033[1;35m"        # Magenta
RESET = "\033[0m"       # Reset
BOLD = "\033[1m"        # Bold
ITALIC = "\033[3m"      # Italic

SERVER_URL = "https://admin-panel-af2x.onrender.com"
PHONE_NUMBER = "923209835904"
DEFAULT_MSG = "i Need New Key"
WHATSAPP_URL = f"https://wa.me/{PHONE_NUMBER}?text={quote(DEFAULT_MSG)}"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def get_real_device_name():
    try:
        if os.path.exists("/system/bin/getprop"):
            brand = subprocess.getoutput("getprop ro.product.brand").strip().title()
            model = subprocess.getoutput("getprop ro.product.model").strip()
            if model and model != "" and "not found" not in model.lower():
                return f"{brand} {model}".strip()

        if os.name == "posix":
            if os.path.exists("/etc/os-release"):
                with open("/etc/os-release") as f:
                    for line in f:
                        if line.startswith("PRETTY_NAME="):
                            return line.split("=")[1].replace('"', '').strip()

        if os.name == "nt":
            comp_name = os.getenv("COMPUTERNAME", "")
            if comp_name and comp_name.lower() != "localhost":
                return f"Windows PC ({comp_name})"

        node = platform.node()
        if node and node.lower() not in ["localhost", "127.0.0.1", "android"]:
            return node
    except Exception:
        pass
    
    return "Android Smartphone" if "ANDROID_ROOT" in os.environ else f"{platform.system()} Device"

def get_device_hwid():
    raw_info = f"{platform.node()}-{platform.machine()}-{os.getenv('USER', '')}-{os.getenv('HOME', '')}"
    return hashlib.sha256(raw_info.encode()).hexdigest()[:16].upper()

def get_current_local_time():
    now = datetime.now().astimezone()
    return now.strftime("%Y-%m-%d %I:%M:%S %p (%Z)")

def open_whatsapp():
    try:
        if "ANDROID_ROOT" in os.environ or os.path.exists("/system/bin/getprop"):
            cmd = f"termux-open-url '{WHATSAPP_URL}' > /dev/null 2>&1 || am start -a android.intent.action.VIEW -d '{WHATSAPP_URL}' > /dev/null 2>&1"
            os.system(cmd)
        else:
            webbrowser.open(WHATSAPP_URL)
    except Exception:
        pass

def print_colorful_banner():
    banner = [
        f"{R}███████╗███████╗███╗   ██╗    ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗ ",
        f"{Y}██╔════╝██╔════╝████╗  ██║    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗",
        f"{G}███████╗█████╗  ██╔██╗ ██║    ███████║███████║██║     █████╔╝ █████╗  ██████╔╝",
        f"{C}╚════██║██╔══╝  ██║╚██╗██║    ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗",
        f"{B}███████║███████╗██║ ╚████║    ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║",
        f"{M}╚══════╝╚══════╝╚═╝  ╚═══╝    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝"
    ]
    for line in banner:
        print(f"{line}{RESET}")

def text_slider_effect(label, value_colored, width=14):
    for i in range(width + 1):
        bar = "━" * i + "►" + " " * (width - i)
        slider_display = f"{G}[{bar}]{RESET}"
        sys.stdout.write(f"\r{C}║ {slider_display} {Y}{label:<12}{RESET} : {G}Connecting...{RESET}")
        sys.stdout.flush()
        time.sleep(0.03)

    final_slider = f"{G}[━━━━━ READY ━━━━━]{RESET}"
    sys.stdout.write(f"\r{C}║ {final_slider} {Y}{label:<12}{RESET} : {value_colored}\n")
    sys.stdout.flush()
    time.sleep(0.08)

def render_ui():
    clear_screen()
    print_colorful_banner()

    print(f"\n{C}╔═══════════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{C}║{BOLD}{W}                           SECURE HARDWARE ACCESS SYSTEM                                   {C}║{RESET}")
    print(f"{C}║{Y}                            DEVELOPER : {G}{BOLD}@SEN_HACKER                                         {C}║{RESET}")
    print(f"{C}╠═══════════════════════════════════════════════════════════════════════════════════════════╣{RESET}")

    device_name = get_real_device_name()
    hwid = get_device_hwid()
    local_time = get_current_local_time()

    items = [
        ("DEVICE NAME", f"{BOLD}{ITALIC}{W}{device_name}{RESET}"),
        ("DEVICE HWID", f"{BOLD}{G}{hwid}{RESET}"),
        ("GATEWAY    ", f"{BOLD}{ITALIC}{C}ONLINE (SSL ENCRYPTED){RESET}"),
        ("LOCAL TIME ", f"{BOLD}{ITALIC}{W}{local_time}{RESET}")
    ]

    for label, val in items:
        text_slider_effect(label, val)

    print(f"{C}╚═══════════════════════════════════════════════════════════════════════════════════════════╝{RESET}\n")
    return hwid, device_name

def verify():
    hwid, device_name = render_ui()

    # --- STEP 1: GMAIL VERIFICATION ---
    try:
        email = input(f"{W}[{C}?{W}] Enter Your Gmail Address {G}>> {W}").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print(f"\n\n{R}[X] Operation cancelled.{RESET}")
        sys.exit(0)

    if not email or "@" not in email:
        print(f"\n{R}[X] ERROR: Valid Gmail zaroori hai!{RESET}")
        time.sleep(1.5)
        sys.exit(1)

    print(f"\n{C}[*] OTP code aapke Gmail par bhej rahe hain...{RESET}")
    try:
        otp_res = requests.post(
            f"{SERVER_URL}/api/send_otp",
            headers={"Content-Type": "application/json"},
            json={"email": email},
            timeout=25
        )
        otp_data = otp_res.json()
        if not otp_data.get("status"):
            print(f"\n{R}[X] Email Error: {otp_data.get('message')}{RESET}")
            sys.exit(1)
        print(f"{G}[✓] 6-digit OTP aapke Gmail par bhej diya gaya hai (Check Inbox/Spam)!{RESET}")
    except Exception as e:
        print(f"\n{R}[X] Server Offline ya Connection Timeout: {str(e)}{RESET}")
        sys.exit(1)

    # --- STEP 2: ENTER OTP ---
    try:
        otp_input = input(f"\n{W}[{C}?{W}] Enter 6-Digit OTP {G}>> {W}").strip()
    except (KeyboardInterrupt, EOFError):
        print(f"\n\n{R}[X] Operation cancelled.{RESET}")
        sys.exit(0)

    print(f"\n{C}[*] Verifying OTP & registering device...{RESET}")
    try:
        verify_otp_res = requests.post(
            f"{SERVER_URL}/api/verify_otp",
            headers={"Content-Type": "application/json"},
            json={
                "email": email,
                "otp": otp_input,
                "hwid": hwid,
                "model": device_name
            },
            timeout=25
        )
        v_data = verify_otp_res.json()
        if not v_data.get("status"):
            print(f"\n{R}[X] Verification Failed: {v_data.get('message')}{RESET}")
            sys.exit(1)
        print(f"{G}[✓] {v_data.get('message')}{RESET}")
        print(f"{Y}[i] Aapka HWID aur Gmail Google Sheet me sync ho chuka hai.{RESET}\n")
    except Exception as e:
        print(f"\n{R}[X] Error: {str(e)}{RESET}")
        sys.exit(1)

    # --- STEP 3: LICENSE KEY VERIFICATION ---
    try:
        license_key = input(f"{W}[{C}?{W}] Enter Your License Key {G}>> {W}").strip()
    except (KeyboardInterrupt, EOFError):
        print(f"\n\n{R}[X] Operation cancelled.{RESET}")
        sys.exit(0)

    if not license_key:
        print(f"\n{R}[X] ERROR: License Key khali nahi ho sakti!{RESET}")
        time.sleep(1.2)
        print(f"{Y}[*] WhatsApp open kiya ja raha hai...{RESET}")
        open_whatsapp()
        sys.exit(1)

    print(f"\n{C}[*] Server key verify kar raha hai... Please wait.{RESET}")
    try:
        res = requests.post(
            f"{SERVER_URL}/api/verify",
            headers={"Content-Type": "application/json"},
            json={
                "key": license_key,
                "hwid": hwid,
                "model": device_name  # <- Yeh line add karein
            },
            timeout=60
        )

        try:
            data = res.json()
        except Exception:
            print(f"\n{R}[X] Server Error (HTTP {res.status_code}): Invalid server response.{RESET}")
            sys.exit(1)

        if res.status_code == 200 and (data.get("status") is True or data.get("status") == "success"):
            expiry = data.get("expiry", "LIFETIME VIP")
            
            print(f"\n{G}╔═══════════════════════════════════════════════════════════════════════╗{RESET}")
            print(f"{G}║  {W}{BOLD}✓ ACCESS GRANTED{RESET}                                                     {G}║{RESET}")
            print(f"{G}║  {Y}Your Key Valid For :{RESET} {W}{BOLD}{expiry:<44}{RESET} {G}║{RESET}")
            print(f"{G}╚═══════════════════════════════════════════════════════════════════════╝{RESET}")
            
            print(f"\n{G}[*] Redirecting to tool in 2 seconds...{RESET}")
            time.sleep(2)
            clear_screen()
            return True
        else:
            reason = data.get("message", "License Key Expired or Invalid!")
            print(f"\n{R}[X] ACCESS DENIED: {reason}{RESET}")
            print(f"{Y}[*] Admin WhatsApp open kiya ja raha hai...{RESET}")
            time.sleep(1.5)
            open_whatsapp()
            sys.exit(1)

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        print(f"\n{R}[X] Auth Server offline hai ya response nahi mil raha.{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{R}[X] Error: {str(e)}{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    if verify():
        print(f"{G}[+] SUCCESS! Tool initialized successfully.{RESET}\n")
        print(f"{C}[*] Welcome @SEN_HACKER User! Running main script...{RESET}\n")
        # Aapka aage ka main payload / menu code yahan se run hoga

#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-
# ============================================================
# SEN_HACKERxTEAM MOD TOOL v4.6 - TERMUX OPTIMIZED - FULL
# ============================================================

import itertools as it
import math
import struct
import shutil
import os
import sys
import uuid
import hashlib
import platform
import subprocess
import requests
import base64
import zlib
import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import PurePath, Path
from typing import List, Dict, Tuple, Optional, Any, Union
import time
from rich.console import Console, Group
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.rule import Rule
from rich import box
from rich import print as rprint
from rich.markup import escape
import gmalg
from datetime import datetime
from collections import Counter
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Cipher.AES import MODE_CBC
from Crypto.Hash import SHA1
try:
    from zstandard import ZstdDecompressor, ZstdCompressionDict, DICT_TYPE_AUTO, ZstdCompressor
except ImportError:
    print("zstandard not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "zstandard"])
    from zstandard import ZstdDecompressor, ZstdCompressionDict, DICT_TYPE_AUTO, ZstdCompressor
from colorama import init, Fore, Style, Back
init(autoreset=True)

# ========== OBB TOOL IMPORTS ==========
import zipfile
import fnmatch
import sys

# Python 3.14 compatibility check
console = Console()

if sys.version_info >= (3, 14):
    console.print("[yellow]⚠ Python 3.14 detected - some packages may need manual install[/yellow]")
    
# itertools.batched fallback (automatic)
try:
    from itertools import batched
except ImportError:
    import itertools as _itertools
    def batched(iterable, n):
        if n < 1:
            raise ValueError('n must be at least one')
        it = iter(iterable)
        while True:
            batch = tuple(_itertools.islice(it, n))
            if not batch:
                break
            yield batch

# ========== TERMUX PATHS ==========
BASE_DIR = Path("/storage/emulated/0/Download/SEN_PAK_TOOL")
#AUTH_CONFIG_FILE = BASE_DIR / "config.json"
#HWID_FILE = BASE_DIR / ".hwid"

# ========== BANNER COLORS ==========
MAGENTA = "\033[1;35m"
CYAN    = "\033[1;36m"
YELLOW  = "\033[1;33m"
GREEN   = "\033[1;32m"
RED     = "\033[1;31m"
WHITE   = "\033[1;37m"
BLUE    = "\033[1;34m"
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
BG_YELLOW = "\033[43m"
BG_MAGENTA = "\033[45m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_CYAN = "\033[46m"

# ========== ONLINE LOGIN SYSTEM CONSTANTS ==========
#GAME_NAME = "PUBG"
#_auth_data = None

# ========== ENHANCED BANNER FUNCTIONS ==========

def get_terminal_size():
    """Safely get terminal size for Termux"""
    try:
        return shutil.get_terminal_size()
    except:
        return os.terminal_size((62, 24))

def print_enhanced_banner():
    """Print modern SEN_HACKER banner using rich (rounded panel, gradient title, status grid)"""
    os.system('clear' if os.name == 'posix' else 'cls')

    try:
        terminal_width = get_terminal_size().columns
    except:
        terminal_width = 62

    now = datetime.now()
    date_str = now.strftime("%d-%m-%Y")
    time_str = now.strftime("%H:%M:%S")

    panel_width = max(46, min(terminal_width - 2, 64))

    # ===== GRADIENT TITLE =====
    title = Text(justify="center")
    gradient = ["#00E5FF", "#22D3EE", "#4FC3FF", "#7CB2FF", "#A599FF", "#C98CFF"]
    for ch, color in zip("SEN_HACKER", gradient):
        title.append(ch, style=f"bold {color}")
    title.append("  MOD TOOL", style="bold white")

    subtitle = Text("v4.6  •  PREMIUM  •  BGMI / PUBG MOBILE", style="dim italic", justify="center")

    # ===== STATUS GRID =====
    grid = Table.grid(expand=True, padding=(0, 2))
    grid.add_column(justify="center", ratio=1)
    grid.add_column(justify="center", ratio=1)
    grid.add_row("[bold #00FF88]●[/bold #00FF88] [white]ACTIVE[/white]", f"[cyan]📦 VERSION[/cyan] [yellow]4.6[/yellow]")
    grid.add_row(f"[cyan]📅[/cyan] [white]{date_str}[/white]", f"[cyan]⏰[/cyan] [white]{time_str}[/white]")

    badges = Text(justify="center")
    badges.append("  🔐 SECURE  ", style="bold white on #0F9D58")
    badges.append("  ")
    badges.append("  🔑 LICENSED  ", style="bold #1a1a1a on #F4B400")
    badges.append("  ")
    badges.append("  📱 READY  ", style="bold white on #7B5CFF")

    body = Group(
        Align.center(title),
        Align.center(subtitle),
        Rule(style="#5B4A9E"),
        Align.center(grid),
        "",
        Align.center(badges),
    )

    console.print(
        Panel(
            body,
            title="[bold #22D3EE]⚡ SEN_HACKER ⚡[/bold #22D3EE]",
            title_align="center",
            border_style="#7B5CFF",
            box=box.ROUNDED,
            width=panel_width,
            padding=(1, 2),
        ),
        justify="center",
    )

def print_banner():
    """Legacy banner function"""
    print_enhanced_banner()

# ========== ONLINE LOGIN SYSTEM ==========

def flush_stdin():
    """Flush any lingering input from stdin"""
    try:
        import termios
        termios.tcflush(sys.stdin.fileno(), termios.TCIFLUSH)
    except:
        pass
    try:
        import select
        if select.select([sys.stdin], [], [], 0.1)[0]:
            sys.stdin.read()
    except:
        pass

def safe_input(prompt: str = "") -> str:
    """Safe input function that properly handles stdin"""
    try:
        return input(prompt)
    except (EOFError, RuntimeError, KeyboardInterrupt):
        try:
            if sys.platform != "win32":
                with open("/dev/tty", "r") as tty:
                    sys.stderr.write(prompt)
                    sys.stderr.flush()
                    result = tty.readline().rstrip("\n")
                    try:
                        import termios
                        termios.tcflush(sys.stdin.fileno(), termios.TCIFLUSH)
                    except:
                        pass
                    return result
            else:
                with open("CON", "r") as con:
                    sys.stderr.write(prompt)
                    sys.stderr.flush()
                    result = con.readline().rstrip("\r\n")
                    return result
        except Exception:
            return ""

# ========== INSTALL DEPENDENCIES ==========
def install_dependencies():
    """Install required Python packages for Termux with smart skip"""
    
    # Python version check
    python_ver = sys.version_info
    console.print(f"[dim]🐍 Python {python_ver.major}.{python_ver.minor}.{python_ver.micro} detected[/dim]")
    
    # All required packages with import names
    deps = {
        'rich': 'rich',
        'pycryptodome': 'Crypto',
        'zstandard': 'zstandard',
        'gmalg': 'gmalg',
        'requests': 'requests',
        'colorama': 'colorama',
        'cffi': 'cffi',
        'six': 'six',
    }
    
    missing = []
    installed = []
    
    console.print("[cyan]📦 Checking dependencies...[/cyan]")
    
    for package_name, import_name in deps.items():
        try:
            __import__(import_name)
            installed.append(package_name)
            console.print(f"  [green]✅ {package_name}[/green] [dim](already installed)[/dim]")
        except ImportError:
            missing.append(package_name)
            console.print(f"  [yellow]⚠ {package_name}[/yellow] [dim](missing)[/dim]")
    
    if not missing:
        console.print("[bold green]✅ All dependencies ready![/bold green]")
        time.sleep(1)
        return
    
    console.print(f"\n[yellow]📥 Installing {len(missing)} missing package(s)...[/yellow]")
    
    # Install missing packages
    for package_name in missing:
        console.print(f"[cyan]⏳ Installing {package_name}...[/cyan]")
        try:
            # Try normal install first
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            console.print(f"  [green]✅ {package_name} installed[/green]")
        except:
            # Retry with --no-deps for problematic packages
            try:
                console.print(f"  [yellow]Retrying {package_name} with --no-deps...[/yellow]")
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package_name, "--no-deps"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                console.print(f"  [green]✅ {package_name} installed (no-deps)[/green]")
            except:
                console.print(f"  [red]❌ Failed to install {package_name}[/red]")
                
                # Special handling for critical packages
                if package_name == 'pycryptodome':
                    console.print("[yellow]  ↳ Try manual: pkg install python-cryptography[/yellow]")
                elif package_name == 'gmalg':
                    console.print("[yellow]  ↳ Try manual: pip install gmalg --no-deps[/yellow]")
                elif package_name == 'zstandard':
                    console.print("[yellow]  ↳ Try manual: pkg install libzstd && pip install zstandard[/yellow]")
    
    # Final verification
    console.print("\n[cyan]🔍 Verifying installations...[/cyan]")
    failed = []
    for package_name in missing:
        import_name = deps.get(package_name, package_name)
        try:
            __import__(import_name)
            console.print(f"  [green]✅ {package_name}[/green]")
        except ImportError:
            failed.append(package_name)
            console.print(f"  [red]❌ {package_name}[/red]")
    
    if failed:
        console.print(f"\n[bold red]⚠ {len(failed)} package(s) failed to install![/bold red]")
        console.print("[yellow]Some features may not work. Continue anyway?[/yellow]")
        
        # Auto-continue after 3 seconds
        console.print("[dim]Continuing in 3 seconds...[/dim]")
        time.sleep(3)
    else:
        console.print("[bold green]✅ All dependencies ready![/bold green]")
    
    time.sleep(1)

# ========== CONSTANTS ==========
ZUC_KEY = bytes.fromhex('01010101010101010101010101010101')
ZUC_IV = bytes.fromhex('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')

RSA_MOD_1 = bytes.fromhex(
    'CBE8B9F2504050EF9831B719E9A6249A6D238505ADE909BDE78C180DED6072A0C3347B8AF4780E1F212D952D82D4BF7F233C1ECA499E1F9D9A85B4FAD759F54BABC1666C5DE411EA9E4B2374425DD6C6F54333BBC8F2610FE6063E4D0D6C21A671A8F7C3740555E5DC06D4E1691C456DB4116C0C012BF7B206E8311AAAEC689952BF804EF638F09D5822B4117B114208F14DEB459E80CB770E5B0D7978E21F5E6CED4999D3583108221A7AB28B960277ADB5690A332784019D9C195BE4EA9EA0A09459010F236465DE0D59C3EF7324E954E1118D93EE19F299760C2CDB963CE87973EA5ECC9BBE81C27D4C7C8572AC07E9BCEAC9BD72AB7A56A3C0AD736ABCE4')
RSA_MOD_2 = bytes.fromhex(
    '7F58E8A39A4DA4E87357DDD650EAA16D3B5CE95B213D1030A662566444796A78A84AE9AC3DBFFDE7F41094896696835DAF13B89E6EC2B84963B1B1BAF7151DA245C3FBFAE2A6AE18B2684D03F9229DE2C91440F2A3A3BCDE1E5680C16722A88039C73560D5D43F4B6562C2EEA5B1D926D86B51108A2643C70FB74D6442CE3A08339B8FD8F660AE88129B7AB8C46F2FA58124485CCCB1E987B05A6DA65A01858ED3F89905449AE42BB07290FCB9994BF22E26610BCABB9804783A3B9587917F3D97316EDDA15C5E13F79066407B55A93B291B68A4AC42A98D6E35FED84B14A792D154E62028DDAD20FC301951E5924BE9AD62FB719DD94CC30CAB871BEC4377A8')

SIMPLE1_DECRYPT_KEY = 0x79
SIMPLE2_DECRYPT_KEY = bytes.fromhex('E55B4ED1')
SIMPLE2_BLOCK_SIZE = 16

SM4_SECRET_4 = 'eb691efea914241317a8'
SM4_SECRET_2 = 'Q0hVTKey$as*1ZFlQCiA'
SM4_SECRET_NEW = [
    "xG2qW5lP7lV2iN5fN5pG", "xT1cJ6dL5wC0kK1rB4dK", "qC4jS5bZ6fL5xE6nD4zA",
    "gD4jQ2aL3bS3lC3xT0iW", "xU1yQ8wE9zY3gZ3bT5aE", "uQ3cO2dX7xY4xU7gH7iS",
    "gW1fR0jK6wQ4oN0oK1kZ", "aJ4pV7iZ7pU4wP2aC2cZ", "cX6jT3cM2oT3vK0kJ1qN",
    "iT2vS0cS6yT6cZ1sE1lO", "hM1pH9iY8wM9hT4lN5uJ", "kG6bC8jK0fL0dE4sH4mL",
    "dB6lB3vE0eZ8wM8rI0aC", "tP7sP7nI9rA2vQ4cV5yQ", "aT0cL1yN4pT3sZ7eM2vY",
    "uV6fU8fC9zN3mP5dH8mN", "rT6aQ6oZ1yM0gO5tO1aN", "jU5bH7lQ0fM9hK2kI0oF",
    "iQ0eM0mJ7uT0kV6kL5zY"
]

EM_SIMPLE1 = 1
EM_SIMPLE2 = 16 
EM_SM4_2 = 2
EM_SM4_4 = 4
EM_SM4_NEW_BASE = 31
EM_SM4_NEW_MASK = ~EM_SM4_NEW_BASE
EM_UNKNOWN_17 = 17

CM_NONE = 0
CM_ZLIB = 1
CM_ZSTD = 6
CM_ZSTD_DICT = 8
CM_MASK = 15

# ========== SM4 IMPLEMENTATION ==========
class SM4:
    """SM4 Algorithm Implementation."""
    
    _S_BOX = bytes([
        0x34, 0x66, 0x25, 0x74, 0x89, 0x78, 0xE4, 0xA9, 0x5A, 0x41, 0xBC, 0x7A, 0xD6, 0x16, 0x21, 0x23,
        0x4D, 0x61, 0xDA, 0x94, 0x9B, 0xDF, 0x13, 0x3C, 0x69, 0x3A, 0x31, 0x0A, 0x5F, 0xD7, 0x99, 0x95,
        0xF1, 0xAE, 0x72, 0x3D, 0x07, 0x60, 0x24, 0xB6, 0x98, 0xEE, 0xC4, 0xA2, 0x2D, 0x88, 0xDD, 0x8D,
        0x04, 0xEA, 0xBB, 0x11, 0xCA, 0x3E, 0x5D, 0xA1, 0xF6, 0x3F, 0xB0, 0x97, 0x80, 0x47, 0x2B, 0xA6,
        0xE6, 0xF7, 0xD9, 0xB1, 0x59, 0xC0, 0x7C, 0xBE, 0x54, 0x28, 0xB7, 0x7E, 0x4F, 0xF8, 0x43, 0x6E,
        0xA0, 0x50, 0x0E, 0xF5, 0x90, 0xB8, 0xFB, 0xA3, 0x7B, 0x62, 0x19, 0x46, 0x03, 0x2A, 0xB9, 0x8F,
        0x9F, 0x77, 0xB4, 0x5B, 0x83, 0x87, 0x08, 0xEB, 0xE2, 0x1E, 0x42, 0xF0, 0x0F, 0xE8, 0x71, 0x6A,
        0x75, 0xAD, 0x55, 0x1F, 0xB5, 0xAB, 0x33, 0xFA, 0x7F, 0x15, 0xBD, 0x85, 0xD8, 0x06, 0x68, 0xB3,
        0x52, 0x30, 0x48, 0x0B, 0x00, 0xED, 0xEF, 0xB2, 0x57, 0x8E, 0xE7, 0x6C, 0xD5, 0xE5, 0x2E, 0x53,
        0x82, 0x05, 0xF9, 0x81, 0xF4, 0x56, 0xBF, 0x8C, 0x4B, 0xE3, 0xDB, 0x4A, 0x91, 0x4C, 0x2C, 0xD3,
        0x40, 0x29, 0x4E, 0x20, 0x14, 0x36, 0x79, 0x09, 0x6F, 0xD1, 0x37, 0xE0, 0x39, 0x0C, 0x8A, 0x92,
        0x38, 0x12, 0x35, 0x6D, 0xE1, 0xFD, 0x93, 0x9A, 0x17, 0xD4, 0xC9, 0x9C, 0x6B, 0x84, 0x26, 0x9D,
        0xAF, 0x76, 0xC1, 0x9E, 0xD0, 0x96, 0xC5, 0xCB, 0xE9, 0x73, 0x49, 0xD2, 0xCD, 0x64, 0xC3, 0xC7,
        0x01, 0x7D, 0xF3, 0xAC, 0xFC, 0xDE, 0xA4, 0x44, 0x32, 0x1B, 0xC2, 0xBA, 0x1C, 0x02, 0xC6, 0x27,
        0x45, 0x8B, 0xF2, 0x18, 0xA7, 0x10, 0x51, 0x1D, 0xC8, 0xCF, 0x63, 0xFF, 0x2F, 0x0D, 0x58, 0xCE,
        0x65, 0xA5, 0xDC, 0x1A, 0x3B, 0x86, 0xFE, 0x22, 0x5C, 0xA8, 0x5E, 0x67, 0xAA, 0xEC, 0x70, 0xCC
    ])

    _FK = [
        0x46970E9C, 0x4BC0685E, 0x59056186, 0xBCA2491E
    ]

    _CK = [
        0x000EB92B, 0x3A0AE783, 0x9E3B5C67, 0xADDBDABF, 0x7B7484CB, 0x49156C63, 0xC79AB5E7, 0x79EC9CFF,
        0x1725BEAB, 0x2FB89CA3, 0x24808AD7, 0xDDD28B1F, 0x4740DA4B, 0xBBC3EA73, 0x247B30E7, 0x91BE385F,
        0x0401248B, 0x45FCD3A3, 0x530B4CE7, 0xC68DD35F, 0xE3D16C2B, 0x4F698C13, 0x6B92C747, 0x769EFB1F,
        0x4C73BE9B, 0xC942B193, 0xAD80D827, 0x372FB33F, 0x13CB6AAB, 0x2BDC0AA3, 0x17A4A247, 0xD5E96CAF
    ]

    @staticmethod
    def ROL32(x, n):
        return ((x << n) & 0xFFFFFFFF) | (x >> (32 - n))

    @staticmethod
    def _BS(X):
        return ((SM4._S_BOX[(X >> 24) & 0xff] << 24) |
                (SM4._S_BOX[(X >> 16) & 0xff] << 16) |
                (SM4._S_BOX[(X >> 8) & 0xff] << 8) |
                (SM4._S_BOX[X & 0xff]))

    @staticmethod
    def _T0(X):
        X = SM4._BS(X)
        return X ^ SM4.ROL32(X, 2) ^ SM4.ROL32(X, 10) ^ SM4.ROL32(X, 18) ^ SM4.ROL32(X, 24)

    @staticmethod
    def _T1(X):
        X = SM4._BS(X)
        return X ^ SM4.ROL32(X, 13) ^ SM4.ROL32(X, 23)

    @staticmethod
    def _key_expand(key: bytes, rkey: list):
        K0 = int.from_bytes(key[0:4], "big") ^ SM4._FK[0]
        K1 = int.from_bytes(key[4:8], "big") ^ SM4._FK[1]
        K2 = int.from_bytes(key[8:12], "big") ^ SM4._FK[2]
        K3 = int.from_bytes(key[12:16], "big") ^ SM4._FK[3]

        for i in range(0, 32, 4):
            K0 = K0 ^ SM4._T1(K1 ^ K2 ^ K3 ^ SM4._CK[i])
            rkey[i] = K0
            K1 = K1 ^ SM4._T1(K2 ^ K3 ^ K0 ^ SM4._CK[i + 1])
            rkey[i + 1] = K1
            K2 = K2 ^ SM4._T1(K3 ^ K0 ^ K1 ^ SM4._CK[i + 2])
            rkey[i + 2] = K2
            K3 = K3 ^ SM4._T1(K0 ^ K1 ^ K2 ^ SM4._CK[i + 3])
            rkey[i + 3] = K3

    @classmethod
    def key_length(cls):
        return 16

    @classmethod
    def block_length(cls):
        return 16

    def __init__(self, key: bytes):
        if len(key) != self.key_length():
            raise ValueError(f"Key must be {self.key_length()} bytes")

        self._key = key
        self._rkey = [0] * 32
        SM4._key_expand(self._key, self._rkey)
        self._block_buffer = bytearray()

    def encrypt(self, block: bytes) -> bytes:
        if len(block) != self.block_length():
            raise ValueError(f"Block must be {self.block_length()} bytes")

        RK = self._rkey
        X0 = int.from_bytes(block[0:4], "big")
        X1 = int.from_bytes(block[4:8], "big")
        X2 = int.from_bytes(block[8:12], "big")
        X3 = int.from_bytes(block[12:16], "big")

        for i in range(0, 32, 4):
            X0 = X0 ^ SM4._T0(X1 ^ X2 ^ X3 ^ RK[i])
            X1 = X1 ^ SM4._T0(X2 ^ X3 ^ X0 ^ RK[i + 1])
            X2 = X2 ^ SM4._T0(X3 ^ X0 ^ X1 ^ RK[i + 2])
            X3 = X3 ^ SM4._T0(X0 ^ X1 ^ X2 ^ RK[i + 3])

        BUFFER = self._block_buffer
        BUFFER.clear()
        BUFFER.extend(X3.to_bytes(4, "big"))
        BUFFER.extend(X2.to_bytes(4, "big"))
        BUFFER.extend(X1.to_bytes(4, "big"))
        BUFFER.extend(X0.to_bytes(4, "big"))
        return bytes(BUFFER)

    def decrypt(self, block: bytes) -> bytes:
        if len(block) != self.block_length():
            raise ValueError(f"Block must be {self.block_length()} bytes")

        RK = self._rkey
        X0 = int.from_bytes(block[0:4], "big")
        X1 = int.from_bytes(block[4:8], "big")
        X2 = int.from_bytes(block[8:12], "big")
        X3 = int.from_bytes(block[12:16], "big")

        for i in range(0, 32, 4):
            X0 = X0 ^ SM4._T0(X1 ^ X2 ^ X3 ^ RK[31 - i])
            X1 = X1 ^ SM4._T0(X2 ^ X3 ^ X0 ^ RK[30 - i])
            X2 = X2 ^ SM4._T0(X3 ^ X0 ^ X1 ^ RK[29 - i])
            X3 = X3 ^ SM4._T0(X0 ^ X1 ^ X2 ^ RK[28 - i])

        BUFFER = self._block_buffer
        BUFFER.clear()
        BUFFER.extend(X3.to_bytes(4, "big"))
        BUFFER.extend(X2.to_bytes(4, "big"))
        BUFFER.extend(X1.to_bytes(4, "big"))
        BUFFER.extend(X0.to_bytes(4, "big"))
        return bytes(BUFFER)

# ========== UTILITY CLASSES ==========
class Misc:
    @staticmethod
    def pad_to_n(data: bytes, n: int) -> bytes:
        assert n > 0
        padding = n - (len(data) % n)
        if padding == n:
            return data
        return data + b'\x00' * padding

    @staticmethod
    def align_up(x: int, n: int) -> int:
        return ((x + n - 1) // n) * n

class Reader:
    def __init__(self, buffer, cursor=0):
        self._buffer = buffer
        self._cursor = cursor

    def u1(self, move_cursor=True) -> int:
        return self.unpack('B', move_cursor=move_cursor)[0]

    def u4(self, move_cursor=True) -> int:
        return self.unpack('<I', move_cursor=move_cursor)[0]

    def u8(self, move_cursor=True) -> int:
        return self.unpack('<Q', move_cursor=move_cursor)[0]

    def i1(self, move_cursor=True) -> int:
        return self.unpack('b', move_cursor=move_cursor)[0]

    def i4(self, move_cursor=True) -> int:
        return self.unpack('<i', move_cursor=move_cursor)[0]

    def i8(self, move_cursor=True) -> int:
        return self.unpack('<q', move_cursor=move_cursor)[0]

    def s(self, n: int, move_cursor=True) -> bytes:
        return self.unpack(f'{n}s', move_cursor=move_cursor)[0]

    def unpack(self, f: Union[str, bytes], offset=0, move_cursor=True):
        x = struct.unpack_from(f, self._buffer, self._cursor + offset)
        if move_cursor:
            self._cursor += struct.calcsize(f)
        return x

    def string(self, move_cursor=True) -> str:
        length = self.i4(move_cursor=move_cursor)
        if length == 0:
            return str()
        assert length > 0
        offset = 0 if move_cursor else 4
        return self.unpack(f'{length}s', offset=offset, move_cursor=move_cursor)[0].rstrip(b'\x00').decode()

# ========== PAK CLASSES ==========
class PakInfo:
    def __init__(self, buffer, keystream: List[int]):
        def decrypt_index_encrypted(x: int) -> int:
            MASK_8 = 0xFF
            return (x ^ keystream[3]) & MASK_8

        def decrypt_magic(x: int) -> int:
            return x ^ keystream[2]

        def decrypt_index_hash(x: bytes) -> bytes:
            key = struct.pack('<5I', *keystream[4:][:5])
            assert len(x) == len(key)
            return bytes(a ^ b for a, b in zip(x, key))

        def decrypt_index_size(x: int) -> int:
            return x ^ ((keystream[10] << 32) | keystream[11])

        def decrypt_index_offset(x: int) -> int:
            return x ^ ((keystream[0] << 32) | keystream[1])

        reader = Reader(buffer[-PakInfo._mem_size(-1):])
        self.index_encrypted: bool = decrypt_index_encrypted(reader.u1()) == 1
        self.magic: int = decrypt_magic(reader.u4())
        self.version: int = reader.u4()
        self.index_hash: bytes = decrypt_index_hash(reader.s(20)) if self.version >= 6 else bytes()
        self.index_size: int = decrypt_index_size(reader.u8())
        self.index_offset: int = decrypt_index_offset(reader.u8())
        if self.version <= 3:
            self.index_encrypted = False

    @staticmethod
    def _mem_size(_: int) -> int:
        return 1 + 4 + 4 + 20 + 8 + 8

class TencentPakInfo(PakInfo):
    def __init__(self, buffer, keystream: List[int]):
        def decrypt_unk(x: bytes) -> bytes:
            key = struct.pack('<8I', *keystream[7:][:8])
            assert len(x) == len(key)
            return bytes(a ^ b for a, b in zip(x, key))

        def decrypt_stem_hash(x: int) -> int:
            return x ^ keystream[8]

        def decrypt_unk_hash(x: int) -> int:
            return x ^ keystream[9]

        super().__init__(buffer, keystream)
        reader = Reader(buffer[-TencentPakInfo._mem_size(self.version):])
        self.unk1: bytes = decrypt_unk(reader.s(32)) if self.version >= 7 else bytes()
        self.packed_key: bytes = reader.s(256) if self.version >= 8 else bytes()
        self.packed_iv: bytes = reader.s(256) if self.version >= 8 else bytes()
        self.packed_index_hash: bytes = reader.s(256) if self.version >= 8 else bytes()
        self.stem_hash: int = decrypt_stem_hash(reader.u4()) if self.version >= 9 else 0
        self.unk2: int = decrypt_unk_hash(reader.u4()) if self.version >= 9 else 0
        self.content_org_hash: bytes = reader.s(20) if self.version >= 12 else bytes()

    @staticmethod
    def _mem_size(version: int) -> int:
        size_for_7 = 32 if version >= 7 else 0
        size_for_8 = 256 * 3 if version >= 8 else 0
        size_for_9 = 4 * 2 if version >= 9 else 0
        size_for_12 = 20 if version >= 12 else 0
        return PakInfo._mem_size(version) + size_for_7 + size_for_8 + size_for_9 + size_for_12

class PakCompressedBlock:
    def __init__(self, reader: Reader):
        self.start: int = reader.u8()
        self.end: int = reader.u8()

@dataclass
class TencentPakEntry:
    def __init__(self, reader: Reader, version: int):
        self.content_hash: bytes = reader.s(20)
        if version <= 1:
            _ = reader.u8()
        self.offset: int = reader.u8()
        self.uncompressed_size: int = reader.u8()
        self.compression_method: int = reader.u4() & CM_MASK
        self.size: int = reader.u8()
        self.unk1: int = reader.u1() if version >= 5 else 0
        self.unk2: bytes = reader.s(20) if version >= 5 else bytes()
        self.compressed_blocks: List[PakCompressedBlock] = [PakCompressedBlock(reader) for _ in range(
            reader.u4())] if self.compression_method != 0 and version >= 3 else []
        self.compression_block_size: int = reader.u4() if version >= 4 else 0
        self.encrypted: bool = reader.u1() == 1 if version >= 4 else False
        self.encryption_method: int = reader.u4() if version >= 12 else 0
        self.index_new_sep: int = reader.u4() if version >= 12 else 0

    def _mem_size(self, version: int) -> int:
        size_for_123 = 20 + 8 + 8 + 4 + 8 + (8 if version == 1 else 0)
        size_for_4 = 4 + 1 if version >= 4 else 0
        size_for_compressed_blocks = 4 + len(self.compressed_blocks) * 16 if self.compressed_blocks else 0
        size_for_5 = 1 + 20 if version >= 5 else 0
        size_for_12 = 4 if version >= 12 else 0
        return size_for_123 + size_for_4 + size_for_5 + size_for_12 + size_for_compressed_blocks

class PakCrypto:
    class _LCG:
        def __init__(self, seed: int):
            self.state = seed

        def next(self) -> int:
            MASK_32 = 0xFFFFFFFF
            MSB_1 = 1 << 31

            def wrap(x: int) -> int:
                x &= MASK_32
                if not x & MSB_1:
                    return x
                else:
                    return ((x + MSB_1) & MASK_32) - MSB_1

            x1 = wrap(0x41C64E6D * self.state)
            self.state = wrap(x1 + 12345)
            x2 = wrap(x1 + 0x13038) if self.state < 0 else self.state
            return ((x2 >> 16) & MASK_32) % 0x7FFF

    @staticmethod
    def zuc_keystream() -> List[int]:
        zuc = gmalg.ZUC(ZUC_KEY, ZUC_IV)
        return [struct.unpack('>I', zuc.generate())[0] for _ in range(16)]

    @staticmethod
    def _xorxor(buffer, x) -> bytes:
        return bytes(buffer[i] ^ x[i % len(x)] for i in range(len(buffer)))

    @staticmethod
    def _hashhash(buffer, n: int) -> bytes:
        result = bytes()
        for i in range(math.ceil(n / SHA1.digest_size)):
            result += SHA1.new(buffer).digest()
        if len(result) >= n:
            result = result[:n]
        else:
            result += b'\x00' * (n - len(result))
        return result

    @staticmethod
    def _meowmeow(buffer) -> bytes:
        def unpad(x):
            skip = 1 + next((i for i in range(len(x)) if x[i] != 0))
            return x[skip:]

        if len(buffer) < 43:
            return bytes()

        x1 = buffer[1:][:SHA1.digest_size]
        x2 = buffer[SHA1.digest_size + 1:]
        x1 = PakCrypto._xorxor(x1, PakCrypto._hashhash(x2, len(x1)))
        x2 = PakCrypto._xorxor(x2, PakCrypto._hashhash(x1, len(x2)))

        part1, m = (x2[:SHA1.digest_size], x2[SHA1.digest_size:])
        if part1 != SHA1.new(b'\x00' * SHA1.digest_size).digest():
            return bytes()

        return unpad(m)

    @staticmethod
    def rsa_extract(signature: bytes, modulus: bytes) -> bytes:
        c = int.from_bytes(signature, 'little')
        n = int.from_bytes(modulus, 'little')
        e = 0x10001
        m = pow(c, e, n).to_bytes(256, 'little').rstrip(b'\x00')
        return PakCrypto._meowmeow(Misc.pad_to_n(m, 4))

    @staticmethod
    def _decrypt_simple1(ciphertext) -> bytes:
        return bytes(x ^ SIMPLE1_DECRYPT_KEY for x in ciphertext)

    @staticmethod
    def _decrypt_simple2(ciphertext) -> bytes:
        class RollingKey:
            def __init__(self, initial_value: int):
                self._value = initial_value

            def update(self, x: int) -> int:
                self._value ^= x
                return self._value

        assert len(ciphertext) % SIMPLE2_BLOCK_SIZE == 0
        initial_key, = struct.unpack('<I', SIMPLE2_DECRYPT_KEY)
        rolling_key = RollingKey(initial_key)
        plaintext = (
            struct.pack('<I', rolling_key.update(x)) for x in struct.unpack(f'<{len(ciphertext) // 4}I', ciphertext)
        )
        return bytes(it.chain.from_iterable(plaintext))

    @staticmethod
    @lru_cache(maxsize=1)
    def _derive_sm4_key(file_path: PurePath, encryption_method: int) -> bytes:
        part1 = file_path.stem.lower()
        if encryption_method == EM_SM4_2:
            secret = SM4_SECRET_2
        elif encryption_method == EM_SM4_4:
            secret = SM4_SECRET_4
        elif encryption_method == EM_UNKNOWN_17:
            index = (encryption_method - EM_SM4_NEW_BASE) % len(SM4_SECRET_NEW)
            secret = SM4_SECRET_NEW[index]
        else:
            index = (encryption_method - EM_SM4_NEW_BASE) % len(SM4_SECRET_NEW)
            secret = f'{SM4_SECRET_NEW[index]}{encryption_method}'
        return SHA1.new(str(part1 + secret).encode()).digest()[:SM4.key_length()]

    @staticmethod
    @lru_cache(maxsize=1)
    def _sm4_context_for_key(key: bytes) -> SM4:
        return SM4(key)

    @staticmethod
    def _decrypt_sm4(ciphertext, file_path: PurePath, encryption_method: int) -> bytes:
        assert len(ciphertext) % SM4.block_length() == 0
        key = PakCrypto._derive_sm4_key(file_path, encryption_method)
        sm4 = PakCrypto._sm4_context_for_key(key)
        return bytes(
            it.chain.from_iterable(
                sm4.decrypt(x) for x in it.batched(ciphertext, SM4.block_length())
            )
        )

    @staticmethod
    def decrypt_index(ciphertext, pak_info: TencentPakInfo) -> bytes:
        if pak_info.version > 7:
            key = PakCrypto.rsa_extract(pak_info.packed_key, RSA_MOD_1)
            iv = PakCrypto.rsa_extract(pak_info.packed_iv, RSA_MOD_1)
            assert len(key) == 32 and len(iv) == 32
            aes = AES.new(key, MODE_CBC, iv[:16])
            return unpad(aes.decrypt(ciphertext), AES.block_size)
        else:
            return bytes(PakCrypto._decrypt_simple1(ciphertext))

    @staticmethod
    def _is_simple1_method(encryption_method: int) -> bool:
        return encryption_method == EM_SIMPLE1

    @staticmethod
    def _is_simple2_method(encryption_method: int) -> bool:
        return encryption_method == EM_SIMPLE2 or encryption_method == 17

    @staticmethod
    def _is_sm4_method(encryption_method: int) -> bool:
        return (encryption_method == EM_SM4_2
                or encryption_method == EM_SM4_4
                or encryption_method == EM_UNKNOWN_17
                or encryption_method & EM_SM4_NEW_MASK != 0)

    @staticmethod
    def align_encrypted_content_size(n: int, encryption_method: int) -> int:
        if PakCrypto._is_simple2_method(encryption_method):
            return Misc.align_up(n, SIMPLE2_BLOCK_SIZE)
        elif PakCrypto._is_sm4_method(encryption_method):
            return Misc.align_up(n, SM4.block_length())
        else:
            return n

    @staticmethod
    def decrypt_block(ciphertext, file: PurePath, encryption_method: int) -> bytes:
        if PakCrypto._is_simple1_method(encryption_method):
            return PakCrypto._decrypt_simple1(ciphertext)
        elif PakCrypto._is_simple2_method(encryption_method):
            return PakCrypto._decrypt_simple2(ciphertext)
        elif PakCrypto._is_sm4_method(encryption_method):
            return PakCrypto._decrypt_sm4(ciphertext, file, encryption_method)
        else:
            raise ValueError(f"Unknown encryption method: {encryption_method}")

    @staticmethod
    @lru_cache(maxsize=33)
    def generate_block_indices(n: int, encryption_method: int) -> List[int]:
        if not PakCrypto._is_sm4_method(encryption_method):
            return list(range(n))
        permutation = []
        lcg = PakCrypto._LCG(n)
        while len(permutation) != n:
            x = lcg.next() % n
            if x not in permutation:
                permutation.append(x)
        inverse = [0] * len(permutation)
        for i, x in enumerate(permutation):
            inverse[x] = i
        return inverse

class PakCompression:
    @staticmethod
    @lru_cache(maxsize=33)
    def _zstd_decompressor(dict: ZstdCompressionDict) -> ZstdDecompressor:
        return ZstdDecompressor(dict)

    @staticmethod
    def zstd_dictionary(dict_data) -> ZstdCompressionDict:
        return ZstdCompressionDict(dict_data, DICT_TYPE_AUTO)

    @staticmethod
    def decompress_block(block, dict: Optional[ZstdCompressionDict], compression_method: int) -> bytes:
        if compression_method == CM_ZLIB:
            try:
                return zlib.decompress(block)
            except zlib.error:
                return block
        elif compression_method == CM_ZSTD or compression_method == CM_ZSTD_DICT:
            if compression_method != CM_ZSTD_DICT:
                dict = None
            return PakCompression._zstd_decompressor(dict).decompress(block)
        else:
            raise ValueError(f"Unknown compression method: {compression_method}")

class TencentPakFile:
    def __init__(self, file_path: PurePath, is_od=True):
        self._file_path = file_path
        with open(file_path, 'rb') as file:
            self._file_content = memoryview(file.read())
        self._is_od = is_od
        self._mount_point = PurePath()
        self._is_zstd_with_dict = 'zsdic' in str(self._file_path)
        self._zstd_dict = None
        self._files: List[TencentPakEntry] = []
        self._index: Dict[PurePath, Dict[str, TencentPakEntry]] = {}
        self._pak_info = TencentPakInfo(self._file_content, PakCrypto.zuc_keystream())
        self._verify_stem_hash()
        self._tencent_load_index()

    def _verify_stem_hash(self) -> None:
        if not self._is_od and self._pak_info.version >= 9:
            assert self._pak_info.stem_hash == zlib.crc32(self._file_path.stem.encode('utf-32le'))

    def _tencent_load_index(self) -> None:
        index_data = self._file_content[self._pak_info.index_offset:][:self._pak_info.index_size]
        if self._pak_info.index_encrypted:
            index_data = PakCrypto.decrypt_index(index_data, self._pak_info)
        else:
            index_data = index_data
        self._verify_index_hash(index_data)
        self._load_index(index_data)

    def _verify_index_hash(self, index_data) -> None:
        expected_hash = self._pak_info.index_hash
        if not self._is_od and self._pak_info.version >= 8:
            assert expected_hash == PakCrypto.rsa_extract(self._pak_info.packed_index_hash, RSA_MOD_2)
        assert expected_hash == SHA1.new(index_data).digest()

    @staticmethod
    def _construct_mount_point(mount_point: str) -> PurePath:
        result = PurePath()
        for part in PurePath(mount_point).parts:
            if part != '..':
                result /= part
        return result

    def _peek_content(self, offset: int, size: int, encryption_method: int) -> memoryview:
        size = PakCrypto.align_encrypted_content_size(size, encryption_method)
        return self._file_content[offset:][:size]

    def _peek_block_content(self, block: PakCompressedBlock, encryption_method: int) -> memoryview:
        size = PakCrypto.align_encrypted_content_size(block.end - block.start, encryption_method)
        return self._file_content[block.start:][:size]

    def _construct_zstd_dict(self, dict_entry: TencentPakEntry) -> None:
        assert not self._zstd_dict
        assert not dict_entry.encrypted
        assert dict_entry.compression_method == CM_NONE
        reader = Reader(self._peek_content(dict_entry.offset, dict_entry.size, 0))
        dict_size = reader.u8()
        _ = reader.u4()
        assert dict_size == reader.u4()
        dict_data = reader.s(dict_size)
        self._zstd_dict = PakCompression.zstd_dictionary(dict_data)

    def _load_index(self, index_data) -> None:
        if self._pak_info.version <= 10:
            raise ValueError(f"Unsupported version: {self._pak_info.version}")
        reader = Reader(index_data)
        self._mount_point = self._construct_mount_point(reader.string())
        self._files = [TencentPakEntry(reader, self._pak_info.version) for _ in range(reader.u4())]
        for _ in range(reader.u8()):
            dir_path = PurePath(reader.string())
            e = {reader.string(): self._files[~reader.i4()] for _ in range(reader.u8())}
            if self._is_zstd_with_dict and dir_path.name == 'zstddic':
                assert len(e) == 1
                self._construct_zstd_dict(e[[*e.keys()][0]])
                continue
            self._index.update({PurePath(dir_path): e})

    def detect_dominant_style(self) -> dict:
        comp_counter = Counter()
        enc_counter = Counter()
        blk_counter = Counter()
        enc_flag_counter = Counter()
        total = len(self._files)
        if total == 0:
            return {'comp_method': CM_ZSTD, 'enc_method': 0, 'encrypted': False, 'block_size': 0x10000}
        for entry in self._files:
            comp_counter[entry.compression_method] += 1
            if entry.encrypted:
                enc_counter[entry.encryption_method] += 1
                enc_flag_counter['encrypted'] += 1
            else:
                enc_flag_counter['plain'] += 1
            if entry.compression_block_size:
                blk_counter[entry.compression_block_size] += 1
        non_none = [(m,c) for m,c in comp_counter.items() if m != CM_NONE]
        comp_method = max(non_none, key=lambda x: x[1])[0] if non_none else CM_NONE
        encrypted = enc_flag_counter.get('encrypted', 0) > enc_flag_counter.get('plain', 0)
        enc_method = enc_counter.most_common(1)[0][0] if encrypted and enc_counter else 0
        block_size = blk_counter.most_common(1)[0][0] if blk_counter else 0x10000
        return {'comp_method': comp_method, 'enc_method': enc_method, 'encrypted': encrypted, 'block_size': block_size}

    def list_existing_paths(self) -> List[str]:
        out = []
        for dir_path, files in self._index.items():
            for fname in files.keys():
                out.append(str(dir_path / fname).replace('\\', '/').lstrip('/'))
        return out

    def _make_signature_marker(self, current_offset: int) -> dict:
        empty_hash = SHA1.new(b'').digest()
        return {
            'content_hash': empty_hash,
            'offset': current_offset,
            'uncompressed_size': 0,
            'size': 0,
            'comp_method': CM_NONE,
            'enc_method': 0,
            'encrypted': False,
            'block_size_val': 0,
            'compressed_blocks': [],
            'unk1': 0,
            'unk2': b'\x00' * 20,
            'index_new_sep': 0,
            '_dir_path': PurePath('SEN_HACKER'),
            '_file_name': 'PATCHED.txt',
        }

    @staticmethod
    def _extract_entry_plain(pak_buffer: memoryview, entry: TencentPakEntry,
                             file_path_for_crypto: PurePath, zstd_dict) -> bytes:
        """Extract a single entry's plaintext (decrypted + decompressed) bytes."""
        if entry.compression_method == CM_NONE:
            sz = PakCrypto.align_encrypted_content_size(entry.size, entry.encryption_method)
            data = bytes(pak_buffer[entry.offset:][:sz])
            if entry.encrypted:
                data = PakCrypto.decrypt_block(data, file_path_for_crypto, entry.encryption_method)
            return data

        parts = []
        for real_idx in PakCrypto.generate_block_indices(len(entry.compressed_blocks), entry.encryption_method):
            block = entry.compressed_blocks[real_idx]
            bsz = PakCrypto.align_encrypted_content_size(block.end - block.start, entry.encryption_method)
            blk = bytes(pak_buffer[block.start:][:bsz])
            if entry.encrypted:
                blk = PakCrypto.decrypt_block(blk, file_path_for_crypto, entry.encryption_method)
            dec = PakCompression.decompress_block(blk, zstd_dict, entry.compression_method)
            parts.append(dec)
        return b''.join(parts)

    def inject_files(self, inject_plan: list, output_pak: Path, add_signature_marker: bool = True) -> None:
        """Inject new files into this PAK, producing a new PAK at output_pak."""
        if not inject_plan:
            raise ValueError('inject_plan is empty — nothing to inject')

        console.print(Panel(
            f'[bold magenta]💉 CUSTOM INJECT[/bold magenta]\n'
            f'[white]Source PAK:[/] [yellow]{self._file_path.name}[/yellow]\n'
            f'[white]Output    :[/] [cyan]{output_pak.name}[/cyan]\n'
            f'[white]Injecting :[/] [green]{len(inject_plan)} new file(s)[/green]',
            title='INJECT MODE', border_style='magenta', padding=(0, 2)
        ))

        console.print('\n[bold magenta]━━ STEP 1/5 : LOADING INJECT FILES ━━[/bold magenta]')
        work_items = []
        for i, item in enumerate(inject_plan):
            if item.get('plain_bytes') is not None:
                plain = item['plain_bytes']
            elif item.get('src_path') is not None:
                try:
                    plain = Path(item['src_path']).read_bytes()
                except Exception as e:
                    console.print(f'   [red]✗ Cannot read {item["src_path"]}: {e} — skipping[/red]')
                    continue
            else:
                console.print(f'   [red]✗ Inject item {i} has no src_path or plain_bytes — skipping[/red]')
                continue

            internal = item['internal_path'].replace('\\', '/').lstrip('/')
            if not internal:
                console.print(f'   [red]✗ Empty internal_path for item {i} — skipping[/red]')
                continue

            parts = internal.rsplit('/', 1)
            if len(parts) == 2:
                dir_str, file_name = parts[0], parts[1]
            else:
                dir_str, file_name = '', parts[0]

            work_items.append({
                'dir_str':       dir_str,
                'file_name':     file_name,
                'internal_path': internal,
                'plain':         plain,
                'comp_method':   item['comp_method'],
                'enc_method':    item['enc_method'],
                'encrypted':     bool(item['encrypted']),
                'block_size':    item['block_size'],
                'comp_level':    item.get('comp_level', 19),
            })
            console.print(f'   [blue]✨[/] {internal} [dim]({len(plain):,} bytes)[/dim]')

        if not work_items:
            raise RuntimeError('No valid inject items after loading')
        console.print(f'[green]✔ Loaded {len(work_items)} file(s)[/green]')

        console.print('\n[bold magenta]━━ STEP 2/5 : ENCODING INJECT FILES ━━[/bold magenta]')
        keystream = PakCrypto.zuc_keystream()
        version = self._pak_info.version
        header_size = TencentPakInfo._mem_size(version)
        PAK_MAGIC = self._pak_info.magic

        orig_index_offset = self._pak_info.index_offset
        current_new_offset = orig_index_offset
        new_data_region = bytearray()
        new_injected_entries = []
        preferred_level = 19

        # Helper function for encryption
        def _encrypt_plaintext(plaintext, pak_relative_path, encryption_method):
            if PakCrypto._is_simple1_method(encryption_method):
                return bytes(b ^ SIMPLE1_DECRYPT_KEY for b in plaintext)
            elif PakCrypto._is_simple2_method(encryption_method):
                pad = (-len(plaintext)) % SIMPLE2_BLOCK_SIZE
                plaintext += b"\x00" * pad
                key, = struct.unpack("<I", SIMPLE2_DECRYPT_KEY)
                rolling = key
                out = []
                for x, in struct.iter_unpack("<I", plaintext):
                    c = rolling ^ x
                    out.append(c)
                    rolling ^= c
                return struct.pack(f"<{len(out)}I", *out)
            elif PakCrypto._is_sm4_method(encryption_method):
                key = PakCrypto._derive_sm4_key(pak_relative_path, encryption_method)
                sm4 = PakCrypto._sm4_context_for_key(key)
                pad_len = (-len(plaintext)) % 16
                if pad_len > 0:
                    plaintext = plaintext + b'\x00' * pad_len
                out = bytearray()
                for i in range(0, len(plaintext), 16):
                    block = plaintext[i:i+16]
                    if len(block) < 16:
                        block = block.ljust(16, b'\x00')
                    out.extend(sm4.encrypt(block))
                return bytes(out)
            return plaintext

        for item in work_items:
            plain = item['plain']
            comp_method = item['comp_method']
            enc_method = item['enc_method']
            encrypted = item['encrypted']
            block_size_val = item['block_size']
            file_path_for_crypto = PurePath(item['file_name'])

            if len(plain) == 0:
                new_injected_entries.append({
                    'content_hash': SHA1.new(b'').digest(),
                    'offset': current_new_offset,
                    'uncompressed_size': 0, 'size': 0,
                    'comp_method': CM_NONE, 'enc_method': 0, 'encrypted': False,
                    'block_size_val': 0, 'compressed_blocks': [],
                    'unk1': 0, 'unk2': b'\x00' * 20, 'index_new_sep': 0,
                    '_dir_path': PurePath(item['dir_str']) if item['dir_str'] else PurePath(),
                    '_file_name': item['file_name'],
                })
                continue

            if comp_method == CM_NONE:
                if encrypted:
                    aligned_size = PakCrypto.align_encrypted_content_size(len(plain), enc_method)
                    padded = plain + b'\x00' * (aligned_size - len(plain))
                    stored_data = _encrypt_plaintext(padded, file_path_for_crypto, enc_method)
                else:
                    stored_data = plain
                new_size = len(stored_data)
                new_compressed_blocks = []
            else:
                chunks = [plain[i:i+block_size_val] for i in range(0, len(plain), block_size_val)]
                if not chunks: chunks = [b'']
                compressed_chunks = []
                for chunk in chunks:
                    comp = None
                    if comp_method in (CM_ZSTD, CM_ZSTD_DICT):
                        zstd_dict = self._zstd_dict if comp_method == CM_ZSTD_DICT else None
                        for lvl in range(22, 0, -1):
                            try:
                                c = ZstdCompressor(level=lvl, dict_data=zstd_dict, threads=1)
                                comp = c.compress(chunk)
                                break
                            except: continue
                    elif comp_method == CM_ZLIB:
                        comp = zlib.compress(chunk, level=9)
                    if comp is None: comp = chunk
                    compressed_chunks.append(comp)

                encrypted_chunks = []
                for comp_data in compressed_chunks:
                    if encrypted:
                        comp_data = _encrypt_plaintext(comp_data, file_path_for_crypto, enc_method)
                    encrypted_chunks.append(comp_data)

                n_blocks = len(encrypted_chunks)
                indices = PakCrypto.generate_block_indices(n_blocks, enc_method)
                physical_blocks = [None] * n_blocks
                for j, chunk_data in enumerate(encrypted_chunks):
                    physical_blocks[indices[j]] = chunk_data

                physical_offsets = []
                block_cursor = current_new_offset
                for phys_block in physical_blocks:
                    physical_offsets.append((block_cursor, block_cursor + len(phys_block)))
                    block_cursor += len(phys_block)
                new_compressed_blocks = physical_offsets
                stored_data = b''.join(physical_blocks)
                new_size = len(stored_data)
                if encrypted:
                    aligned_total = PakCrypto.align_encrypted_content_size(new_size, enc_method)
                    if aligned_total > new_size:
                        stored_data = stored_data + b'\x00' * (aligned_total - new_size)
                        new_size = aligned_total

            new_content_hash = SHA1.new(stored_data).digest()
            new_data_region.extend(stored_data)

            new_injected_entries.append({
                'content_hash': new_content_hash,
                'offset': current_new_offset,
                'uncompressed_size': len(plain),
                'size': new_size,
                'comp_method': comp_method,
                'enc_method': enc_method if encrypted else 0,
                'encrypted': encrypted,
                'block_size_val': block_size_val,
                'compressed_blocks': new_compressed_blocks,
                'unk1': 0, 'unk2': b'\x00' * 20, 'index_new_sep': 0,
                '_dir_path': PurePath(item['dir_str']) if item['dir_str'] else PurePath(),
                '_file_name': item['file_name'],
            })
            current_new_offset += new_size

        console.print(f'[green]✔ Encoded {len(new_injected_entries)} file(s)[/green]')

        # Build final entries
        new_entries = []
        entry_to_path = {}
        for dir_path, files in self._index.items():
            for fname, entry in files.items():
                entry_to_path[id(entry)] = (dir_path, fname)
        for i, entry in enumerate(self._files):
            dir_path, fname = entry_to_path.get(id(entry), (PurePath(), f'unknown_{i}'))
            new_entries.append({
                'content_hash': entry.content_hash,
                'offset': entry.offset,
                'uncompressed_size': entry.uncompressed_size,
                'size': entry.size,
                'comp_method': entry.compression_method,
                'enc_method': entry.encryption_method if entry.encrypted else 0,
                'encrypted': entry.encrypted,
                'block_size_val': entry.compression_block_size,
                'compressed_blocks': [(b.start, b.end) for b in entry.compressed_blocks],
                'unk1': entry.unk1, 'unk2': entry.unk2,
                'index_new_sep': entry.index_new_sep,
            })
        new_entries.extend(new_injected_entries)

        if add_signature_marker:
            marker_already_present = False
            for dp, files_dict in self._index.items():
                if dp.name == 'HR_DHAMA' and 'PATCHED.txt' in files_dict:
                    marker_already_present = True
                    break
            if not marker_already_present:
                new_entries.append(self._make_signature_marker(current_new_offset))

        # Build Index
        index_data = bytearray()
        raw_orig_index = self._file_content[self._pak_info.index_offset:][:self._pak_info.index_size]
        orig_index_decoded = PakCrypto.decrypt_index(bytes(raw_orig_index), self._pak_info)
        orig_reader = Reader(orig_index_decoded)
        orig_mount_len = orig_reader.i4()
        orig_mount_bytes = bytes(orig_reader.s(orig_mount_len))
        index_data.extend(struct.pack('<I', orig_mount_len))
        index_data.extend(orig_mount_bytes)
        index_data.extend(struct.pack('<I', len(new_entries)))

        for item in new_entries:
            index_data.extend(item['content_hash'])
            if version <= 1: index_data.extend(struct.pack('<Q', 0))
            index_data.extend(struct.pack('<Q', item['offset']))
            index_data.extend(struct.pack('<Q', item['uncompressed_size']))
            index_data.extend(struct.pack('<I', item['comp_method'] & CM_MASK))
            index_data.extend(struct.pack('<Q', item['size']))
            if version >= 5:
                index_data.extend(struct.pack('<B', item['unk1']))
                index_data.extend(item['unk2'] if item['unk2'] else b'\x00' * 20)
            if item['comp_method'] != CM_NONE and version >= 3:
                index_data.extend(struct.pack('<I', len(item['compressed_blocks'])))
                for (start, end) in item['compressed_blocks']:
                    index_data.extend(struct.pack('<Q', start))
                    index_data.extend(struct.pack('<Q', end))
            if version >= 4:
                index_data.extend(struct.pack('<I', item['block_size_val']))
                index_data.extend(struct.pack('<B', 1 if item['encrypted'] else 0))
            if version >= 12:
                index_data.extend(struct.pack('<I', item['enc_method']))
                index_data.extend(struct.pack('<I', item['index_new_sep']))

        file_to_dirname = {}
        for dir_path, files_dict in self._index.items():
            dir_str = dir_path.as_posix()
            for fname, entry in files_dict.items():
                for i, fe in enumerate(self._files):
                    if id(fe) == id(entry):
                        file_to_dirname[i] = (dir_str, fname)
                        break
        for i, item in enumerate(new_entries):
            if i not in file_to_dirname:
                if '_dir_path' in item:
                    file_to_dirname[i] = (item['_dir_path'].as_posix(), item['_file_name'])
                else:
                    file_to_dirname[i] = ('', f'file_{i}')

        all_dirs = []
        dir_to_files = {}
        for dir_path in self._index.keys():
            ds = dir_path.as_posix()
            all_dirs.append(ds)
            dir_to_files[ds] = []
        for i, item in enumerate(new_entries):
            ds, fn = file_to_dirname[i]
            if ds not in dir_to_files:
                dir_to_files[ds] = []
                all_dirs.append(ds)
            dir_to_files[ds].append((fn, i))

        index_data.extend(struct.pack('<Q', len(all_dirs)))
        for dir_str in all_dirs:
            files_list = dir_to_files[dir_str]
            if not dir_str or dir_str == '.':
                index_data.extend(struct.pack('<I', 0))
            else:
                if not dir_str.endswith('/'): dir_str_with_slash = dir_str + '/'
                else: dir_str_with_slash = dir_str
                dir_bytes = dir_str_with_slash.encode('utf-8') + b'\x00'
                index_data.extend(struct.pack('<I', len(dir_bytes)))
                index_data.extend(dir_bytes)
            index_data.extend(struct.pack('<Q', len(files_list)))
            for file_name, fi in files_list:
                name_bytes = file_name.encode('utf-8') + b'\x00'
                index_data.extend(struct.pack('<I', len(name_bytes)))
                index_data.extend(name_bytes)
                index_data.extend(struct.pack('<i', -fi - 1))
        index_data.extend(b'\x1d\x00\x00\x00\x2e\x2e')

        index_hash = SHA1.new(bytes(index_data)).digest()

        if version > 7 and self._pak_info.index_encrypted:
            key = PakCrypto.rsa_extract(self._pak_info.packed_key, RSA_MOD_1)
            iv = PakCrypto.rsa_extract(self._pak_info.packed_iv, RSA_MOD_1)
            assert len(key) == 32 and len(iv) == 32
            padded = pad(bytes(index_data), AES.block_size)
            aes = AES.new(key, MODE_CBC, iv[:16])
            encrypted_index = aes.encrypt(padded)
        elif self._pak_info.index_encrypted:
            encrypted_index = bytes(b ^ SIMPLE1_DECRYPT_KEY for b in bytes(index_data))
        else:
            encrypted_index = bytes(index_data)

        index_size = len(encrypted_index)
        new_index_offset = orig_index_offset + len(new_data_region)

        encrypted_magic = PAK_MAGIC ^ keystream[2]
        key_stream_hash = struct.pack('<5I', *keystream[4:][:5])
        encrypted_index_hash = bytes(a ^ b for a, b in zip(index_hash, key_stream_hash))
        encrypted_index_size = index_size ^ ((keystream[10] << 32) | keystream[11])
        encrypted_index_offset = new_index_offset ^ ((keystream[0] << 32) | keystream[1])
        encrypted_flag_byte = (1 if self._pak_info.index_encrypted else 0) ^ (keystream[3] & 0xFF)

        orig_data_region = bytearray(self._file_content[0:orig_index_offset])
        output_pak.parent.mkdir(parents=True, exist_ok=True)
        with open(output_pak, 'wb') as f:
            f.write(bytes(orig_data_region))
            f.write(bytes(new_data_region))
            f.write(encrypted_index)
            if version >= 7:
                key_unk1 = struct.pack('<8I', *keystream[7:][:8])
                unk1_plain = self._pak_info.unk1 if self._pak_info.unk1 else b'\x00' * 32
                encrypted_unk1 = bytes(a ^ b for a, b in zip(unk1_plain, key_unk1))
                f.write(encrypted_unk1)
            if version >= 8:
                f.write(self._pak_info.packed_key if self._pak_info.packed_key else b'\x00' * 256)
                f.write(self._pak_info.packed_iv if self._pak_info.packed_iv else b'\x00' * 256)
                f.write(self._pak_info.packed_index_hash if self._pak_info.packed_index_hash else b'\x00' * 256)
            if version >= 9:
                f.write(struct.pack('<I', (self._pak_info.stem_hash or 0) ^ keystream[8]))
                f.write(struct.pack('<I', (self._pak_info.unk2 or 0) ^ keystream[9]))
            if version >= 12:
                f.write(self._pak_info.content_org_hash if self._pak_info.content_org_hash else b'\x00' * 20)
            f.write(struct.pack('<B', encrypted_flag_byte))
            f.write(struct.pack('<I', encrypted_magic))
            f.write(struct.pack('<I', version))
            if version >= 6:
                f.write(encrypted_index_hash)
            else:
                f.write(b'\x00' * 20)
            f.write(struct.pack('<Q', encrypted_index_size))
            f.write(struct.pack('<Q', encrypted_index_offset))

        console.print(Panel(
            f'[bold green]🎉 INJECT COMPLETE![/bold green]\n\n'
            f'[white]Output  :[/] [cyan]{output_pak.name}[/cyan]',
            title='✅ SUCCESS', border_style='green', padding=(1, 2)
        ))

    def _write_to_disk(self, file_path: PurePath, entry: TencentPakEntry) -> None:
        encryption_method = entry.encryption_method
        compression_method = entry.compression_method
        
        console.print(f"[#00CCFF]{file_path.name}[/#00CCFF] - Encryption: {encryption_method}, Compression: {compression_method}, Blocks: {len(entry.compressed_blocks)}")
        
        # ----- BYPASS FOR ENC 17 (DSxDEMON) -----
        if encryption_method == 17:
            with open(file_path, 'wb') as file:
                for blk in entry.compressed_blocks:
                    raw_data = self._file_content[blk.start:blk.end]
                    file.write(raw_data)
            return
        # --------------------------------------------
        
        with open(file_path, 'wb') as file:
            if compression_method == CM_NONE:
                data = self._peek_content(entry.offset, entry.size, encryption_method)
                if entry.encrypted:
                    data = PakCrypto.decrypt_block(data, file_path, encryption_method)
                file.write(data)
                return
            for x in PakCrypto.generate_block_indices(len(entry.compressed_blocks), encryption_method):
                data = self._peek_block_content(entry.compressed_blocks[x], encryption_method)
                if entry.encrypted:
                    data = PakCrypto.decrypt_block(data, file_path, encryption_method)
                data = PakCompression.decompress_block(data, self._zstd_dict, compression_method)
                file.write(data)

    def dump(self, out_path: PurePath) -> None:
        out_path /= self._mount_point
        for dir_path, dir in self._index.items():
            current_out_path = Path(out_path / dir_path)
            if not current_out_path.exists():
                current_out_path.mkdir(parents=True, exist_ok=True)
            for file_name, entry in dir.items():
                self._write_to_disk(current_out_path / file_name, entry)

        # Generate manifest
        manifest = {
            'tool': 'SEN_HACKER_4.6',
            'pak_file': str(self._file_path),
            'mount_point': str(self._mount_point),
            'extracted_at': datetime.now().isoformat(),
            'files': []
        }
        for dir_path, files in self._index.items():
            for fname, entry in files.items():
                manifest['files'].append({
                    'internal_path': str(dir_path / fname).replace('\\', '/'),
                    'uncompressed_size': entry.uncompressed_size,
                    'compression': entry.compression_method,
                    'encryption': entry.encryption_method,
                    'encrypted': entry.encrypted,
                })
        manifest_path = Path(out_path) / 'pak_manifest.json'
        try:
            with open(manifest_path, 'w') as mf:
                json.dump(manifest, mf, indent=2)
            console.print(f"[cyan]📋 Manifest saved: {manifest_path}[/cyan]")
        except Exception as e:
            console.print(f"[yellow]⚠ Could not save manifest: {e}[/yellow]")

# ========== REPACK FUNCTIONALITY ==========

def _build_pak_filename_map(pak_file):
    """Build safe filename → full pak path map"""
    name_map = {}

    for dir_path, files in pak_file._index.items():
        for name in files.keys():
            full = str(PurePath(dir_path) / name).replace("\\", "/")
            stem = Path(name).stem.lower()
            ext = Path(name).suffix.lower()

            key1 = name.lower()
            key2 = f"{stem}{ext}"
            key3 = stem

            for k in (key1, key2, key3):
                name_map.setdefault(k, []).append(full)

    return name_map

def dump_unpacking_log(pak_file, output_log_path: Path):
    """Dump detailed unpacking log"""
    with open(output_log_path, 'w', encoding='utf-8') as log_file:
        log_file.write("=" * 80 + "\n")
        log_file.write("PAK UNPACKING DEBUG LOG\n")
        log_file.write("=" * 80 + "\n\n")
        
        log_file.write(f"PAK File: {pak_file._file_path}\n")
        log_file.write(f"PAK Info Version: {pak_file._pak_info.version}\n")
        log_file.write(f"Mount Point: {pak_file._mount_point}\n")
        log_file.write(f"Is ZSTD with Dict: {pak_file._is_zstd_with_dict}\n")
        log_file.write(f"Has ZSTD Dict: {pak_file._zstd_dict is not None}\n")
        log_file.write("-" * 80 + "\n\n")
        
        file_count = 0
        compression_stats = {}
        encryption_stats = {}
        block_stats = {}
        
        for dir_path, files in pak_file._index.items():
            for file_name, entry in files.items():
                file_count += 1
                full_path = str(PurePath(dir_path) / file_name).replace("\\", "/")
                
                comp_method = entry.compression_method
                compression_stats[comp_method] = compression_stats.get(comp_method, 0) + 1
                
                enc_method = entry.encryption_method
                encryption_stats[enc_method] = encryption_stats.get(enc_method, 0) + 1
                
                block_count = len(entry.compressed_blocks)
                block_stats[block_count] = block_stats.get(block_count, 0) + 1
                
                log_file.write(f"\n[{file_count}] {full_path}\n")
                log_file.write(f"  {'─' * 60}\n")
                log_file.write(f"  Uncompressed Size: {entry.uncompressed_size:,} bytes\n")
                log_file.write(f"  Compressed Size:   {entry.size:,} bytes\n")
                
                comp_method_name = {
                    CM_NONE: "NONE",
                    CM_ZLIB: "ZLIB",
                    CM_ZSTD: "ZSTD",
                    CM_ZSTD_DICT: "ZSTD_DICT"
                }.get(comp_method, f"UNKNOWN({comp_method})")
                log_file.write(f"  Compression Method: {comp_method_name} ({comp_method})\n")
                
                enc_method_name = "NONE"
                if enc_method == EM_SIMPLE1:
                    enc_method_name = "SIMPLE1"
                elif enc_method in (EM_SIMPLE2, EM_UNKNOWN_17):
                    enc_method_name = "SIMPLE2"
                elif enc_method == EM_SM4_2:
                    enc_method_name = "SM4_2"
                elif enc_method == EM_SM4_4:
                    enc_method_name = "SM4_4"
                elif enc_method & EM_SM4_NEW_MASK != 0:
                    enc_method_name = f"SM4_NEW({enc_method})"
                else:
                    enc_method_name = f"UNKNOWN({enc_method})"
                log_file.write(f"  Encryption Method: {enc_method_name}\n")
                log_file.write(f"  Is Encrypted: {entry.encrypted}\n")
                log_file.write(f"  Compressed Blocks: {len(entry.compressed_blocks)}\n")
                log_file.write(f"  Compression Block Size: {entry.compression_block_size:,} bytes\n")
                
                if entry.compressed_blocks:
                    total_compressed = sum(blk.end - blk.start for blk in entry.compressed_blocks)
                    log_file.write(f"  Total Compressed Space: {total_compressed:,} bytes\n")
                    if entry.uncompressed_size > 0:
                        compression_ratio = total_compressed / entry.uncompressed_size
                        log_file.write(f"  Compression Ratio: {compression_ratio:.2%}\n")
                    
                    for i, blk in enumerate(entry.compressed_blocks[:10]):
                        block_size = blk.end - blk.start
                        log_file.write(f"    Block {i}: Offset={blk.start:,} Size={block_size:,} bytes\n")
                    if len(entry.compressed_blocks) > 10:
                        log_file.write(f"    ... and {len(entry.compressed_blocks) - 10} more blocks\n")
                    
                    block_sizes = [blk.end - blk.start for blk in entry.compressed_blocks]
                    if block_sizes:
                        log_file.write(f"  Min Block Size: {min(block_sizes):,} bytes\n")
                        log_file.write(f"  Max Block Size: {max(block_sizes):,} bytes\n")
                        log_file.write(f"  Avg Block Size: {sum(block_sizes) / len(block_sizes):,.0f} bytes\n")
                
                log_file.write(f"  {'─' * 60}\n")
        
        log_file.write("\n" + "=" * 80 + "\n")
        log_file.write("SUMMARY STATISTICS\n")
        log_file.write("=" * 80 + "\n\n")
        log_file.write(f"Total Files: {file_count}\n\n")
        
        log_file.write("Compression Methods:\n")
        for method, count in sorted(compression_stats.items()):
            method_name = {
                CM_NONE: "NONE",
                CM_ZLIB: "ZLIB",
                CM_ZSTD: "ZSTD",
                CM_ZSTD_DICT: "ZSTD_DICT"
            }.get(method, f"UNKNOWN({method})")
            log_file.write(f"  {method_name}: {count} files ({count/file_count*100:.1f}%)\n")
        
        log_file.write("\nEncryption Methods:\n")
        for method, count in sorted(encryption_stats.items()):
            if method == EM_SIMPLE1:
                method_name = "SIMPLE1"
            elif method == EM_SIMPLE2:
                method_name = "SIMPLE2"
            elif method == EM_SM4_2:
                method_name = "SM4_2"
            elif method == EM_SM4_4:
                method_name = "SM4_4"
            elif method & EM_SM4_NEW_MASK != 0:
                method_name = f"SM4_NEW({method})"
            else:
                method_name = f"UNKNOWN({method})"
            log_file.write(f"  {method_name}: {count} files ({count/file_count*100:.1f}%)\n")
        
        log_file.write("\nBlock Count Distribution:\n")
        for block_count, file_count_with_blocks in sorted(block_stats.items()):
            percentage = file_count_with_blocks / file_count * 100
            log_file.write(f"  {block_count:3d} blocks: {file_count_with_blocks:4d} files ({percentage:5.1f}%)\n")
        
        log_file.write("\n" + "=" * 80 + "\n")
        log_file.write("END OF LOG\n")
        log_file.write("=" * 80 + "\n")
    
    console.print(f"[bold #00FF88]✅ Debug log saved to: {output_log_path}[/bold #00FF88]")

def debug_entry_info(entry):
    """Debug function to print entry details"""
    console.print(f"[bold #FFFF00]ENTRY DEBUG INFO:[/bold #FFFF00]")
    console.print(f"  • Uncompressed size: {entry.uncompressed_size}")
    console.print(f"  • Compressed size: {entry.size}")
    console.print(f"  • Compression method: {entry.compression_method}")
    console.print(f"  • Encryption method: {entry.encryption_method}")
    console.print(f"  • Encrypted: {entry.encrypted}")
    console.print(f"  • Blocks: {len(entry.compressed_blocks)}")
    console.print(f"  • Block size: {entry.compression_block_size}")
    
    if entry.compressed_blocks:
        console.print(f"  • Block ranges:")
        for i, blk in enumerate(entry.compressed_blocks[:5]):
            console.print(f"    Block {i}: {blk.start} - {blk.end} (size: {blk.end - blk.start})")
        if len(entry.compressed_blocks) > 5:
            console.print(f"    ... and {len(entry.compressed_blocks) - 5} more blocks")

def _zstd_add_skippable_padding(data: bytes, pad_len: int) -> bytes:
    if pad_len <= 0:
        return data

    out = bytearray(data)
    while pad_len > 0:
        frame_len = min(max(pad_len - 8, 0), 1024 * 1024)
        out += b"\x50\x2A\x4D\x18"
        out += struct.pack("<I", frame_len)
        out += b"\x00" * frame_len
        pad_len -= (8 + frame_len)
    return bytes(out)

def _compress_to_target(
    plaintext: bytes,
    method: int,
    zstd_dict,
    target_size: int,
    encryption_method: int
) -> bytes:

    align = PakCrypto.align_encrypted_content_size

    if method in (CM_ZSTD, CM_ZSTD_DICT):
        for lvl in (22, 19, 16, 13, 10, 7, 4, 1):
            try:
                c = ZstdCompressor(
                    level=lvl,
                    dict_data=zstd_dict if method == CM_ZSTD_DICT else None,
                    threads=1
                )
                comp = c.compress(plaintext)
                a = align(len(comp), encryption_method)
                if a <= target_size:
                    if a < target_size:
                        comp = _zstd_add_skippable_padding(comp, target_size - a)
                    return comp
            except Exception:
                pass

        c = ZstdCompressor(
            dict_data=zstd_dict if method == CM_ZSTD_DICT else None,
            threads=1
        )
        return c.compress(plaintext)[:target_size]

def _encrypt_plaintext(
    plaintext: bytes,
    pak_relative_path: PurePath,
    encryption_method: int
) -> bytes:

    if PakCrypto._is_simple1_method(encryption_method):
        return bytes(b ^ SIMPLE1_DECRYPT_KEY for b in plaintext)

    if PakCrypto._is_simple2_method(encryption_method):
        pad = (-len(plaintext)) % SIMPLE2_BLOCK_SIZE
        plaintext += b"\x00" * pad

        key, = struct.unpack("<I", SIMPLE2_DECRYPT_KEY)
        rolling = key
        out = []

        for x, in struct.iter_unpack("<I", plaintext):
            c = rolling ^ x
            out.append(c)
            rolling ^= c

        return struct.pack(f"<{len(out)}I", *out)

    if PakCrypto._is_sm4_method(encryption_method):
        key = PakCrypto._derive_sm4_key(pak_relative_path, encryption_method)
        sm4 = PakCrypto._sm4_context_for_key(key)

        pad_len = (-len(plaintext)) % 16
        if pad_len > 0:
            plaintext = plaintext + b'\x00' * pad_len

        out = bytearray()
        for i in range(0, len(plaintext), 16):
            block = plaintext[i:i+16]
            if len(block) < 16:
                block = block.ljust(16, b'\x00')
            out.extend(sm4.encrypt(block))
        
        return bytes(out)

    return plaintext

def _repack_uncompressed(
    outfh,
    pak_file,
    entry,
    pak_relative_path: PurePath,
    new_data: bytes
):

    enc_method = entry.encryption_method
    target_size = entry.size

    enc_region = (
        PakCrypto.align_encrypted_content_size(target_size, enc_method)
        if entry.encrypted else target_size
    )

    plaintext = new_data[:enc_region]

    if entry.encrypted:
        a = PakCrypto.align_encrypted_content_size(len(plaintext), enc_method)
        plaintext += b"\x00" * (a - len(plaintext))
        cipher = _encrypt_plaintext(plaintext, pak_relative_path, enc_method)

        outfh.seek(entry.offset)
        outfh.write(cipher)

        with open(pak_file._file_path, "rb") as src:
            src.seek(entry.offset + len(cipher))
            outfh.write(src.read(enc_region - len(cipher)))
    else:
        outfh.seek(entry.offset)
        outfh.write(plaintext)

        with open(pak_file._file_path, "rb") as src:
            src.seek(entry.offset + len(plaintext))
            outfh.write(src.read(target_size - len(plaintext)))

def _repack_compressed(
    outfh,
    pak_file,
    entry,
    pak_relative_path,
    new_data,
    repack_dir
):
    blocks = entry.compressed_blocks
    enc_method = entry.encryption_method
    comp_method = entry.compression_method
    
    order = PakCrypto.generate_block_indices(len(blocks), enc_method)
    
    console.print(f"[#FFFF00]REPACK DEBUG:[/#FFFF00]")
    console.print(f"  Original uncompressed: {entry.uncompressed_size:,} bytes")
    console.print(f"  New data size: {len(new_data):,} bytes")
    console.print(f"  Blocks: {len(blocks)}")
    console.print(f"  Total compressed space: {sum(b.end-b.start for b in blocks):,} bytes")
    
    if len(new_data) != entry.uncompressed_size:
        console.print(f"[#FF0055]❌ CRITICAL: New data size mismatch![/#FF0055]")
        if len(new_data) < entry.uncompressed_size:
            new_data = new_data.ljust(entry.uncompressed_size, b'\x00')
        else:
            new_data = new_data[:entry.uncompressed_size]
    
    # ================= MULTI BLOCK =================
    if len(blocks) > 1:
        block_sizes = [blk.end - blk.start for blk in blocks]
        total_block_size = sum(block_sizes)
        
        if entry.compression_block_size > 0:
            chunk_size = entry.compression_block_size
        else:
            avg_block_size = sum(block_sizes) / len(block_sizes)
            avg_compression_ratio = total_block_size / entry.uncompressed_size
            chunk_size = int(avg_block_size / avg_compression_ratio) if avg_compression_ratio > 0 else 65536
        
        ptr = 0
        processed_blocks = 0
        skipped_blocks = 0
        
        for logical_i, phys_i in enumerate(order):
            blk = blocks[phys_i]
            target_size = blk.end - blk.start
            
            chunk_len = min(chunk_size, len(new_data) - ptr)
            if chunk_len <= 0:
                break
            
            chunk = new_data[ptr:ptr + chunk_len]
            ptr += chunk_len
            
            with open(pak_file._file_path, "rb") as src:
                src.seek(blk.start)
                original_compressed = src.read(target_size)
            
            compressed_ok = False
            new_compressed = None
            
            if comp_method == CM_ZSTD:
                zstd_dict = None
            elif comp_method == CM_ZSTD_DICT:
                zstd_dict = pak_file._zstd_dict
            else:
                zstd_dict = None
            
            if comp_method in (CM_ZSTD, CM_ZSTD_DICT):
                for level in [22, 19, 16, 13, 10, 7, 4, 1]:
                    try:
                        c = ZstdCompressor(level=level, dict_data=zstd_dict, threads=1)
                        new_compressed = c.compress(chunk)
                        if len(new_compressed) <= target_size:
                            compressed_ok = True
                            break
                    except:
                        continue
            
            elif comp_method == CM_ZLIB:
                try:
                    new_compressed = zlib.compress(chunk, zlib.Z_BEST_COMPRESSION)
                    if len(new_compressed) <= target_size:
                        compressed_ok = True
                except:
                    compressed_ok = False
            
            if not compressed_ok or new_compressed is None:
                outfh.seek(blk.start)
                outfh.write(original_compressed)
                skipped_blocks += 1
                continue
            
            if entry.encrypted:
                if PakCrypto._is_sm4_method(enc_method):
                    pad_len = (-len(new_compressed)) % 16
                    if pad_len > 0:
                        new_compressed += b'\x00' * pad_len
                new_compressed = _encrypt_plaintext(new_compressed, pak_relative_path, enc_method)
            
            if len(new_compressed) > target_size:
                outfh.seek(blk.start)
                outfh.write(original_compressed)
                skipped_blocks += 1
                continue
            
            outfh.seek(blk.start)
            outfh.write(new_compressed)
            if len(new_compressed) < target_size:
                outfh.write(b'\x00' * (target_size - len(new_compressed)))
            
            processed_blocks += 1
        
        if ptr < len(new_data):
            console.print("[#FF0055]❌ Data alignment error, stopping[/#FF0055]")
            return False
    
    # ================= SINGLE BLOCK =================
    else:
        blk = blocks[0]
        target_size = blk.end - blk.start
        
        with open(pak_file._file_path, "rb") as src:
            src.seek(blk.start)
            original_compressed = src.read(target_size)
        
        compressed_ok = False
        new_compressed = None
        
        if comp_method == CM_ZSTD:
            zstd_dict = None
        elif comp_method == CM_ZSTD_DICT:
            zstd_dict = pak_file._zstd_dict
        else:
            zstd_dict = None
        
        if comp_method in (CM_ZSTD, CM_ZSTD_DICT):
            for level in [22, 19, 16, 13, 10, 7, 4, 1]:
                try:
                    c = ZstdCompressor(level=level, dict_data=zstd_dict, threads=1)
                    new_compressed = c.compress(new_data)
                    if len(new_compressed) <= target_size:
                        compressed_ok = True
                        break
                except:
                    continue
        
        elif comp_method == CM_ZLIB:
            try:
                new_compressed = zlib.compress(new_data, zlib.Z_BEST_COMPRESSION)
                if len(new_compressed) <= target_size:
                    compressed_ok = True
            except:
                compressed_ok = False
        
        if not compressed_ok or new_compressed is None:
            console.print(f"[#FFAA00]⚠ Cannot compress, keeping original[/#FFAA00]")
            outfh.seek(blk.start)
            outfh.write(original_compressed)
            return True
        
        if entry.encrypted:
            if PakCrypto._is_sm4_method(enc_method):
                pad_len = (-len(new_compressed)) % 16
                if pad_len > 0:
                    new_compressed += b'\x00' * pad_len
            new_compressed = _encrypt_plaintext(new_compressed, pak_relative_path, enc_method)
        
        if len(new_compressed) > target_size:
            console.print(f"[#FFAA00]⚠ Compressed too big, keeping original[/#FFAA00]")
            outfh.seek(blk.start)
            outfh.write(original_compressed)
            return True
        
        outfh.seek(blk.start)
        outfh.write(new_compressed)
        if len(new_compressed) < target_size:
            outfh.write(b'\x00' * (target_size - len(new_compressed)))
    
    return True

def detect_repack_mode(pak_path: Path) -> str:
    name = pak_path.name.lower()

    if name == "mini_obb.pak":
        return "MINI_OBB"

    if "zsdic" in name:
        return "OBBZSDIC"

    if "game" in name or "patch" in name:
        return "GAMEPATCH"

    return "OBBZSDIC"

def smart_resolve_by_fingerprint(
    filename: str,
    repack_file: Path,
    candidates: list
):
    repack_size = repack_file.stat().st_size

    size_matches = [
        (path, entry)
        for path, entry in candidates
        if entry.uncompressed_size == repack_size
    ]

    if len(size_matches) == 1:
        return size_matches[0]

    if not size_matches:
        return None

    def fingerprint(e):
        return (
            e.uncompressed_size,
            e.compression_method,
            e.encryption_method,
            len(e.compressed_blocks),
            e.compression_block_size
        )

    base_fp = fingerprint(size_matches[0][1])

    final_matches = [
        (path, entry)
        for path, entry in size_matches
        if fingerprint(entry) == base_fp
    ]

    if len(final_matches) == 1:
        return final_matches[0]

    return None

def repack_pak_file_fileA_style(
    pak_file,
    edited_root: Path,
    output_path: Path
):
    shutil.copy2(pak_file._file_path, output_path)
    
    pak_name_map = {}
    for dir_path, files in pak_file._index.items():
        for name, entry in files.items():
            full_path = str(PurePath(dir_path) / name).replace("\\", "/")
            key = name.lower()
            pak_name_map.setdefault(key, []).append((full_path, entry))
    
    edited = {}
    skipped_files = []
    
    console.print(f"[#00CCFF]🔍 Matching files from {edited_root}...[/#00CCFF]")
    
    for p in edited_root.rglob("*"):
        if not p.is_file():
            continue
        
        fname_lower = p.name.lower()
        
        if fname_lower in pak_name_map:
            candidates = pak_name_map[fname_lower]
            
            if len(candidates) == 1:
                full_path, entry = candidates[0]
                edited[full_path] = (p, entry)
                console.print(f"[#00FF88]✓ Match: {p.name} → {full_path}[/#00FF88]")
            else:
                resolved = smart_resolve_by_fingerprint(
                    filename=p.name,
                    repack_file=p,
                    candidates=candidates
                )

                if resolved:
                    full_path, entry = resolved
                    edited[full_path] = (p, entry)
                    console.print(f"[#00FF88]✓ Smart-matched: {p.name} → {full_path}[/#00FF88]")
                else:
                    console.print(f"[#FFAA00]⚠ Multiple matches for {p.name}:[/#FFAA00]")
                    for cand_path, _ in candidates:
                        console.print(f"    - {cand_path}")
                    skipped_files.append(p.name)
        else:
            stem = p.stem.lower()
            ext = p.suffix.lower()
            
            potential_matches = []
            for dir_path, files in pak_file._index.items():
                for name, entry in files.items():
                    if (Path(name).stem.lower() == stem and 
                        Path(name).suffix.lower() == ext):
                        full_path = str(PurePath(dir_path) / name).replace("\\", "/")
                        potential_matches.append((full_path, entry))
            
            if len(potential_matches) == 1:
                full_path, entry = potential_matches[0]
                edited[full_path] = (p, entry)
                console.print(f"[#00FF88]✓ Stem+Ext Match: {p.name} → {full_path}[/#00FF88]")
            elif len(potential_matches) > 1:
                console.print(f"[#FF0055]✗ Multiple stem matches for {p.name}:[/#FF0055]")
                for cand_path, _ in potential_matches:
                    console.print(f"    - {cand_path}")
                skipped_files.append(p.name)
            else:
                console.print(f"[#FF0055]✗ No match found for {p.name}[/#FF0055]")
                skipped_files.append(p.name)
    
    console.print("\n[bold #00FFFF]📊 Matching Summary:[/bold #00FFFF]")
    console.print(f"[#00FF88]✓ Files matched: {len(edited)}[/#00FF88]")
    if skipped_files:
        console.print(f"[#FFAA00]⚠ Files skipped: {len(skipped_files)}[/#FFAA00]")
        for fname in skipped_files[:10]:
            console.print(f"    - {fname}")
        if len(skipped_files) > 10:
            console.print(f"    ... and {len(skipped_files) - 10} more")
    
    if not edited:
        console.print("[bold #FF0055]❌ No files to repack![/bold #FF0055]")
        return
    
    with open(output_path, "r+b") as outfh:
        for full_path, (p, entry) in edited.items():
            console.print(
                f"[#FFFF00][REPACK][/#FFFF00] {full_path} | "
                f"Compression: {entry.compression_method} | "
                f"Encryption: {entry.encryption_method} | "
                f"Blocks: {len(entry.compressed_blocks)}"
            )
            debug_entry_info(entry)
            new_data = p.read_bytes()
            pak_rel = PurePath(full_path)
            
            if entry.compression_method == CM_NONE:
                _repack_uncompressed(outfh, pak_file, entry, pak_rel, new_data)
            else:
                success = _repack_compressed(outfh, pak_file, entry, pak_rel, new_data, edited_root)
                if not success:
                    console.print(f"[#FF0055]❌ FAILED to repack {full_path}. File may be corrupted![/#FF0055]")
                
    console.print(f"[bold #00FF88]✅ Repack completed! {len(edited)} file(s) replaced.[/bold #00FF88]")

# ========== REPACK MODE WRAPPERS ==========
def repack_mini_obb(pak, repack_dir, output_pak):
    console.print("[bold #00FFFF]🧩 Repack Mode: MINI_OBB[/bold #00FFFF]")
    pak._is_zstd_with_dict = False
    pak._zstd_dict = None
    repack_pak_file_fileA_style(
        pak_file=pak,
        edited_root=repack_dir,
        output_path=output_pak
    )

def repack_obbzsdic(pak, repack_dir, output_pak):
    console.print("[bold #00FFFF]🧩 Repack Mode: OBBZSDIC[/bold #00FFFF]")
    repack_pak_file_fileA_style(
        pak_file=pak,
        edited_root=repack_dir,
        output_path=output_pak
    )

def repack_gamepatch(pak, repack_dir, output_pak):
    console.print("[bold #00FFFF]🧩 Repack Mode: GAMEPATCH[/bold #00FFFF]")
    pak._is_zstd_with_dict = False
    pak._zstd_dict = None
    repack_pak_file_fileA_style(
        pak_file=pak,
        edited_root=repack_dir,
        output_path=output_pak
    )

def handle_repack():
    console.print("\n[bold #00AAFF]📦 REPACK PAK[/bold #00AAFF]")
    console.print("[white]Repack Lua files into PAK[/white]")
    
    out_path = BASE_DIR
    edit_dir = BASE_DIR / "Edited"
    
    # CHECK: Does edit_dir have files?
    if not edit_dir.exists():
        edit_dir.mkdir(parents=True, exist_ok=True)
        console.print(f"[yellow]⚠ Created empty folder: {edit_dir}[/yellow]")
        console.print("[yellow]Please add your LUA files there first![/yellow]")
        flush_stdin()
        safe_input("\nPress Enter to continue...")
        return
    
    # Check for actual files
    files_in_edit = [f for f in edit_dir.rglob("*") if f.is_file() and f.name not in ['pak_manifest.json','.DS_Store']]
    if not files_in_edit:
        console.print("[bold red]❌ Edited folder is empty![/bold red]")
        console.print(f"[red]📁 Please put LUA files in: {edit_dir}[/red]")
        flush_stdin()
        safe_input("\nPress Enter to continue...")
        return
    
    console.print("[cyan]🔍 Searching for PAK files...[/cyan]")
    pak_files = []
    for file in BASE_DIR.iterdir():
        if file.name.lower().endswith('.pak'):
            pak_files.append(file)
    
    if not pak_files:
        console.print("[bold red]❌ No PAK file found in folder![/bold red]")
        console.print(f"[red]📁 Please put PAK file in: {BASE_DIR}[/red]")
        flush_stdin()
        safe_input("\nPress Enter to continue...")
        return
    
    # ... baaki code same rahega
    
    if len(pak_files) == 1:
        pak_path = pak_files[0]
        console.print(f"[green]✅ Found PAK: {pak_path.name}[/green]")
    else:
        console.print(f"[yellow]⚠️ Multiple PAK files found:[/yellow]")
        for i, pak in enumerate(pak_files, 1):
            console.print(f"  [{i}] {pak.name}")
        console.print("\n[bold yellow]Enter number to select:[/bold yellow]")
        try:
            choice_pak = int(safe_input("> ").strip())
            if 1 <= choice_pak <= len(pak_files):
                pak_path = pak_files[choice_pak - 1]
                console.print(f"[green]✅ Selected: {pak_path.name}[/green]")
            else:
                console.print("[bold red]❌ Invalid choice![/bold red]")
                flush_stdin()
                safe_input("\nPress Enter to continue...")
                return
        except:
            console.print("[bold red]❌ Invalid input![/bold red]")
            flush_stdin()
            safe_input("\nPress Enter to continue...")
            return
    
    if not edit_dir.exists():
        console.print("[bold red]❌ Edited folder not found![/bold red]")
        console.print(f"[red]📁 Please put files in: {edit_dir}[/red]")
        flush_stdin()
        safe_input("\nPress Enter to continue...")
        return
    
    console.print("\n[bold yellow]Enter Target Repacking Path in PAK:[/bold yellow]")
    console.print("[dim](Press Enter for default: Content/Lua/)[/dim]")
    console.print("[dim]Example: Content/Lua/GameLua/Mod/BRMod/Gameplay/Core/[/dim]")
    target_path = safe_input("> ").strip()
    flush_stdin()
    if not target_path:
        target_path = "Content/Lua/"
        console.print(f"[cyan]🎯 Using default: {target_path}[/cyan]")
    else:
        if not target_path.endswith('/'):
            target_path += '/'
        console.print(f"[cyan]🎯 Target path: {target_path}[/cyan]")
    
    BACKUP_FOLDER = BASE_DIR / "BACKUP"
    BACKUP_FOLDER.mkdir(exist_ok=True)
    backup_name = f"{pak_path.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pak"
    backup_path = BACKUP_FOLDER / backup_name
    shutil.copy2(pak_path, backup_path)
    console.print(f"[bold green]✅ Backup created: {backup_path}[/bold green]")
    
    try:
        console.print("[cyan]📦 Loading PAK file...[/cyan]")
        pak = TencentPakFile(PurePath(pak_path))
        output_name = f"{pak_path.stem}_MODIFIED.pak"
        output_pak = out_path / output_name
        console.print("[cyan]🔄 Repacking PAK...[/cyan]")
        
        inject_folder = edit_dir
        files = [f for f in inject_folder.rglob("*") if f.is_file() and f.name not in ['pak_manifest.json','.DS_Store']]
        
        if not files:
            console.print("[yellow]No files to inject from Edited folder.[/yellow]")
            flush_stdin()
            safe_input("\nPress Enter to continue...")
            return
        
        dominant = pak.detect_dominant_style()
        console.print(f"[cyan]Dominant style: comp={dominant['comp_method']}, enc={dominant['enc_method']}, encrypted={dominant['encrypted']}, block={dominant['block_size']}[/cyan]")
        
        inject_plan = []
        for f in files:
            rel = str(f.relative_to(inject_folder)).replace("\\", "/")
            full_path = target_path + rel if not rel.startswith(target_path) else rel
            inject_plan.append({
                'src_path': f,
                'internal_path': full_path,
                'comp_method': dominant['comp_method'],
                'enc_method': dominant['enc_method'],
                'encrypted': dominant['encrypted'],
                'block_size': dominant['block_size'],
            })
        
        console.print(f"[green]Plan: {len(inject_plan)} files.[/green]")
        
        pak.inject_files(inject_plan, Path(output_pak))
        console.print(f"[bold green]✅ Repack complete! Output: {output_pak}[/bold green]")
        console.print(f"[green]Processed {len(inject_plan)} files.[/green]")
        
    except Exception as e:
        console.print(f"[bold red]❌ Error: {e}[/bold red]")
        import traceback
        traceback.print_exc()
    
    flush_stdin()
    safe_input("\nPress Enter to continue...")

# ========== OBB TOOL FUNCTIONS ==========
def _obb_get_obb(input_dir: Path) -> Optional[Path]:
    files = [f for f in input_dir.iterdir() if f.suffix.lower() == ".obb"]
    if not files:
        console.print("[red]❌ No OBB found in input folder[/red]")
        return None
    if len(files) > 1:
        console.print("[red]❌ Keep only ONE OBB file in input folder[/red]")
        return None
    return files[0]

def _obb_fix_size(file: Path, target: int) -> None:
    size = file.stat().st_size
    if size > target:
        console.print("[red]❌ New OBB is larger than original[/red]")
        return
    with open(file, "ab") as f:
        f.write(b"\x00" * (target - size))

def _obb_select_paks(pak_dir: Path) -> List[str]:
    pak_files = [f.name for f in pak_dir.iterdir() if f.suffix.lower() == ".pak"]
    if not pak_files:
        console.print("[red]❌ No PAK files found in repack_pak folder[/red]")
        return []
    
    console.print("\n[cyan]📂 Available PAK files:[/cyan]")
    for i, f in enumerate(pak_files, 1):
        console.print(f"  [{i}] {f}")
    
    choice = safe_input("\nSelect (1,3-5 or name, Enter = ALL): ").strip()
    flush_stdin()
    
    if not choice:
        return pak_files
    
    selected = []
    tokens = choice.split(",")
    
    for tok in tokens:
        tok = tok.strip()
        
        if "-" in tok:
            try:
                a, b = map(int, tok.split("-"))
                for i in range(a, b+1):
                    if 1 <= i <= len(pak_files):
                        selected.append(pak_files[i-1])
            except:
                pass
        elif tok.isdigit():
            i = int(tok)
            if 1 <= i <= len(pak_files):
                selected.append(pak_files[i-1])
        else:
            matches = fnmatch.filter(pak_files, f"*{tok}*")
            selected.extend(matches)
    
    return list(dict.fromkeys(selected))

def _obb_unpack(input_dir: Path, unpack_dir: Path) -> None:
    obb = _obb_get_obb(input_dir)
    if not obb:
        flush_stdin()
        safe_input("\nPress Enter to continue...")
        return
    
    console.print("[cyan]📦 Extracting OBB...[/cyan]")
    try:
        with zipfile.ZipFile(obb, 'r') as z:
            z.extractall(unpack_dir)
        console.print(f"[green]✅ Extracted to: {unpack_dir}[/green]")
    except Exception as e:
        console.print(f"[red]❌ Error extracting: {e}[/red]")
    
    flush_stdin()
    safe_input("\nPress Enter to continue...")

def _obb_repack(input_dir: Path, unpack_dir: Path, repack_dir: Path, pak_dir: Path) -> None:
    obb = _obb_get_obb(input_dir)
    if not obb:
        flush_stdin()
        safe_input("\nPress Enter to continue...")
        return
    
    original_size = obb.stat().st_size
    
    if unpack_dir.exists():
        shutil.rmtree(unpack_dir)
    unpack_dir.mkdir(parents=True, exist_ok=True)
    
    console.print("[cyan]📦 Extracting original OBB...[/cyan]")
    try:
        with zipfile.ZipFile(obb, 'r') as z:
            z.extractall(unpack_dir)
    except Exception as e:
        console.print(f"[red]❌ Error extracting: {e}[/red]")
        flush_stdin()
        safe_input("\nPress Enter to continue...")
        return
    
    selected = _obb_select_paks(pak_dir)
    if not selected:
        flush_stdin()
        safe_input("\nPress Enter to continue...")
        return
    
    pak_path = unpack_dir / "ShadowTrackerExtra" / "Content" / "Paks"
    pak_path.mkdir(parents=True, exist_ok=True)
    
    console.print("\n[cyan]📥 Injecting PAK files...[/cyan]")
    for fname in selected:
        src = pak_dir / fname
        if src.exists():
            dst = pak_path / fname
            shutil.copy2(src, dst)
            console.print(f"  [green]✔ {fname}[/green]")
        else:
            console.print(f"  [red]✗ {fname} not found[/red]")
    
    new_name = obb.name
    new_path = repack_dir / new_name
    
    console.print("\n[cyan]📦 Repacking OBB...[/cyan]")
    try:
        with zipfile.ZipFile(new_path, 'w', compression=zipfile.ZIP_STORED) as z:
            for root, _, files in os.walk(unpack_dir):
                for f in files:
                    path = Path(root) / f
                    arc = str(path.relative_to(unpack_dir))
                    z.write(path, arc)
        
        console.print("[cyan]📏 Matching size...[/cyan]")
        _obb_fix_size(new_path, original_size)
        
        console.print(f"\n[bold green]✅ Done! Saved at: {new_path}[/bold green]")
    except Exception as e:
        console.print(f"[red]❌ Error repacking: {e}[/red]")
    
    flush_stdin()
    safe_input("\nPress Enter to continue...")

def obb_tool_menu():
    console.print(Panel(
        "[bold #FF8800]📦 OBB TOOL[/bold #FF8800]\n"
        "[white]Unpack and repack .obb files (Unity asset bundles)[/white]",
        title='OBB MODULE', border_style='orange1', padding=(0, 2)
    ))
    
    obb_root = BASE_DIR / "OBBZIP"
    obb_input = obb_root / "input"
    obb_unpack = obb_root / "unpacked_obb"
    obb_repack = obb_root / "repack_obb"
    obb_pak = obb_root / "repack_pak"
    
    for p in [obb_input, obb_unpack, obb_repack, obb_pak]:
        p.mkdir(parents=True, exist_ok=True)
    
    while True:
        console.print("\n" + "─" * 50, style="#666699")
        console.print("[bold #FF8800]📦 OBB TOOL MENU[/bold #FF8800]")
        console.print("[#00FF88]1. Unpack OBB - Extract files from .obb[/#00FF88]")
        console.print("[#00FFFF]2. Repack OBB - Inject PAK files into .obb[/#00FFFF]")
        console.print("[#FF0055]0. Back to Main Menu[/#FF0055]")
        console.print("─" * 50, style="#666699")
        
        choice = safe_input("Select (0-2): ").strip()
        flush_stdin()
        
        if choice == "1":
            _obb_unpack(obb_input, obb_unpack)
        elif choice == "2":
            _obb_repack(obb_input, obb_unpack, obb_repack, obb_pak)
        elif choice == "0":
            break
        else:
            console.print("[red]Invalid choice.[/red]")
            time.sleep(1)

# ========== UTILITY FUNCTIONS ==========
def detect_pak_files(base_path: Path) -> List[Path]:
    pak_files = list(BASE_DIR.glob("*.pak"))
    pak_files.extend(BASE_DIR.glob("*.obb"))
    return sorted(pak_files, key=lambda x: x.name)

def human_size(size: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

def clear_folders(base_path: Path) -> None:
    with Progress() as progress:
        task = progress.add_task("[#00CCFF]Cleaning folders...", total=1)
        count = 0
        for item in base_path.iterdir():
            if item.is_dir() and (item.name.startswith("Unpack_") or item.name.startswith("Repack_")):
                try:
                    shutil.rmtree(item)
                    console.print(f"[#00FF88]✓ Cleared: {item.name}[/#00FF88]")
                    count += 1
                except Exception as e:
                    console.print(f"[#FF0055]✗ Error clearing {item.name}: {escape(str(e))}[/#FF0055]")
        progress.update(task, completed=1)
        if count > 0:
            console.print(f"[#00FF88]✓ Successfully cleared {count} folder(s)[/#00FF88]")
        else:
            console.print("[#FFAA00]⚠ No folders to clear[/#FFAA00]")

# ========== AUTO TOOL FUNCTIONS ==========
def headshot_auto_make():
    FOLDER = BASE_DIR / "Auto_Mod_Pak"
    print("Wait HeadShot Making in Progress......")

    all_files = sorted(os.listdir(FOLDER))
    os.makedirs(FOLDER, exist_ok=True)

    i = 0
    while i < len(all_files):
        file_name = all_files[i]
        source_file = os.path.join(FOLDER, file_name)

        if not os.path.isfile(source_file):
            i += 1
            continue

        size = os.path.getsize(source_file)

        if size == 64 * 1024:
            with open(source_file, "rb") as f:
                data = f.read()

            if b"BigBody" in data and b"/Game/Arts/PhysicalMaterial/PhysicalMaterial_Flesh" in data:
                merge_files = [file_name]
                j = i + 1
                while j < len(all_files):
                    next_file = os.path.join(FOLDER, all_files[j])
                    if not os.path.isfile(next_file):
                        break
                    next_size = os.path.getsize(next_file)
                    merge_files.append(all_files[j])
                    j += 1
                    if next_size != 64 * 1024:
                        break

                merged_data = bytearray()
                sizes = []
                for fname in merge_files:
                    with open(os.path.join(FOLDER, fname), "rb") as f:
                        chunk = f.read()
                    sizes.append(len(chunk))
                    merged_data.extend(chunk)

                replacement_map = {
                    b"EAvatarDamagePosition::BigBody": b"EAvatarDamagePosition::BigHead",
                    b"EAvatarDamagePosition::BigFoot": b"EAvatarDamagePosition::BigHead",
                    b"EAvatarDamagePosition::BigHand": b"EAvatarDamagePosition::BigHead",
                    b"EAvatarDamagePosition::BigLimbs": b"EAvatarDamagePosition::BigHead",
                    b"spine_01": b"spine_03",
                    b"spine_02": b"spine_03"
                }

                modified = False
                for target, replacement in replacement_map.items():
                    start = 0
                    while True:
                        idx = merged_data.find(target, start)
                        if idx == -1:
                            break
                        modified = True
                        if len(replacement) < len(target):
                            padded = replacement + b'\x00' * (len(target) - len(replacement))
                        elif len(replacement) > len(target):
                            padded = replacement[:len(target)]
                        else:
                            padded = replacement
                        merged_data[idx:idx + len(target)] = padded
                        if target == b"EAvatarDamagePosition::BigLimbs":
                            pos_s = idx + len(target) - 1
                            merged_data[pos_s] = 0x00
                        start = idx + len(target)

                if modified:
                    offset = 0
                    for fname, fsize in zip(merge_files, sizes):
                        part = merged_data[offset:offset + fsize]
                        offset += fsize
                        if fname == file_name:
                            dest_file = os.path.join(FOLDER, fname)
                            with open(dest_file, "wb") as f:
                                f.write(part)
                            print(f"[✔] Patched & Saved: {fname}")
                else:
                    print(f"[–] No modification found, skipping all.")

                i = j
                continue

        i += 1

    print("Auto HeadShot Done.....")

def patch_bones_from_head():
    FOLDER = BASE_DIR / "Auto_Mod_Pak"
    bones = [
        "upperarm_l","lowerarm_l","hand_l","hand_r",
        "thigh_l","calf_l","thigh_r","calf_r",
        "foot_l","spine_03","foot_r","lowerarm_r",
        "upperarm_r","pelvis"
    ]

    head_file = None

    for f in FOLDER.rglob("*"):
        if f.is_file():
            try:
                data = f.read_bytes()
                if b"TemperatureLow_Phase0" in data:
                    head_file = f
                    print(f"✅ Found in FOLDER: {f.name}")
                    break
            except:
                continue

    if head_file is None:
        for f in FOLDER.rglob("*"):
            if f.is_file():
                try:
                    data = f.read_bytes()
                    if b"TemperatureLow_Phase0" in data:
                        target_file = FOLDER / f.name
                        shutil.copy(f, target_file)
                        head_file = target_file
                        print(f"✅ Found in FOLDER and copied to FOLDER: {f.name}")
                        break
                except:
                    continue

    if head_file is None:
        print("❌ No file with 'TemperatureLow_Phase0' found in either directory.")
        return

    data = head_file.read_bytes()
    pos = data.find(b"head")
    if pos == -1:
        print("❌ 'head' text not found.")
        return

    val_pos = pos + len(b"head") + 1
    if val_pos + 2 > len(data):
        print("❌ Not enough bytes after 'head'.")
        return

    value_bytes = data[val_pos:val_pos+2]
    print(f"🧠 Extracted 2 bytes after 'head': {value_bytes.hex().upper()}")

    patched = 0
    for f in FOLDER.rglob("*"):
        if not f.is_file():
            continue
        file_data = f.read_bytes()
        modified = False
        for bone in bones:
            b = bone.encode()
            idx = 0
            while True:
                pos = file_data.find(b, idx)
                if pos == -1:
                    break
                after = pos + len(b)
                if after < len(file_data) and file_data[after] == 0x00:
                    after += 1
                if after + 2 <= len(file_data):
                    ba = bytearray(file_data)
                    ba[after:after+2] = value_bytes
                    file_data = bytes(ba)
                    modified = True
                    patched += 1
                idx = pos + 1
        if modified:
            f.write_bytes(file_data)
            print(f"✏️ Patched {f.name}")

    print(f"\n✅ Done. Total patched: {patched}")

FLOAT_TARGET = 1300.0
TARGET_LE = struct.pack('<f', FLOAT_TARGET)
PATTERN_FULL = bytes.fromhex('ddffff')  

def float32_bytes(value):
    return struct.pack('<f', float(value))

def find_all(data: bytes, sub: bytes):
    i = data.find(sub)
    while i != -1:
        yield i
        i = data.find(sub, i + 1)

def IPadV():
    FOLDER = BASE_DIR / "Auto_Mod_Pak"
    files = list(FOLDER.glob("*"))
    if not files:
        print("No files found in Auto_Mod_Pak")
        return

    new_val = None
    while new_val is None:
        new_val_raw = input("What value do you want (300–400): ").strip()
        try:
            new_val = float(new_val_raw)
        except ValueError:
            print("Invalid input")

    new_bytes = float32_bytes(new_val)

    for p in files:
        data = bytearray(p.read_bytes())
        occurrences = list(find_all(data, TARGET_LE))
        if not occurrences:
            continue

        modified = False

        for cur_idx in occurrences:
            cut_start = cur_idx - 25
            cut_end = cur_idx + 4
            if cut_start < 0:
                continue

            cut_bytes = bytes(data[cut_start:cut_end])
            del data[cut_start:cut_end]

            pat_idx = data.find(PATTERN_FULL)
            if pat_idx == -1 or pat_idx < 33:
                continue
            insert_pos = pat_idx - 33
            data[insert_pos:insert_pos] = cut_bytes
            modified = True

            new_idx = data.find(TARGET_LE)
            if new_idx == -1:
                continue

            data[new_idx:new_idx + 4] = new_bytes

        if modified:
            out_path = FOLDER / p.name
            out_path.write_bytes(data)
            print(f"Done. Saved modified file to {out_path.name} — Go and Check")

TARGET_FLOAT = struct.pack("<f", 5.0)

def float_to_bytes(f):
    return struct.pack("<f", f)

def modify_file(path, new_val):
    FOLDER = BASE_DIR / "Auto_Mod_Pak"
    data = bytearray(path.read_bytes())
    matches = list(find_all(data, TARGET_FLOAT))
    if len(matches) == 24: 
        pos22 = matches[21]
        new_bytes = float_to_bytes(new_val)
        data[pos22:pos22+4] = new_bytes
        out_path = FOLDER / path.name
        out_path.write_bytes(data)
        print(f"Modified 6th 5.0 in {path.name} to {new_val}")
        return True
    return False

def IPadS():
    FOLDER = BASE_DIR / "Auto_Mod_Pak"
    files = list(FOLDER.glob("*"))
    if not files:
        print("No files found in Auto_Mod_Pak")
        return

    new_val = None
    while new_val is None:
        try:
            new_val = float(input("What value you want under (20): ").strip())
        except ValueError:
            print("Invalid input")

    modified = False
    for f in files:
        if modify_file(f, new_val):
            modified = True

    if not modified:
        print("No files with exactly {path.name} times {new_val} found.")

SEARCH_STRING = b"BodyDuability"  
HEX_TO_FIND = b"\xcd\xcc"        
OCCURRENCE = 17                   
OFFSET_BEHIND = 49               
NUM_BYTES = 2           

FLOAT_TO_FIND = -88.0
OFFSET_BEHIND_2 = 61
NUM_BYTES_2 = 2

def find_body_duability_file():
    FOLDER = BASE_DIR / "Auto_Mod_Pak"
    for file in FOLDER.iterdir():
        if file.is_file():
            with open(file, "rb") as f:
                content = f.read()
                if SEARCH_STRING in content:
                    return file
    return None

def extract_and_overwrite(file_path):
    FOLDER = BASE_DIR / "Auto_Mod_Pak"
    with open(file_path, "rb") as f:
        data = bytearray(f.read()) 

    step1_bytes = None
    indices = []
    start = 0
    while True:
        idx = data.find(HEX_TO_FIND, start)
        if idx == -1:
            break
        indices.append(idx)
        start = idx + 1

    if len(indices) < OCCURRENCE:
        print(f"❌ {OCCURRENCE} occurrences nahi mili.")
    else:
        target_idx = indices[OCCURRENCE - 1]
        hex_pos1 = target_idx - OFFSET_BEHIND
        if 0 <= hex_pos1 <= len(data) - NUM_BYTES:
            step1_bytes = data[hex_pos1:hex_pos1 + NUM_BYTES]

    float_bytes = struct.pack('<f', FLOAT_TO_FIND)
    indices2 = []
    start = 0
    while True:
        idx = data.find(float_bytes, start)
        if idx == -1:
            break
        indices2.append(idx)
        start = idx + 1

    step2_positions = []
    for i, idx in enumerate(indices2, 1):
        hex_pos2 = idx + 4 - OFFSET_BEHIND_2
        if 0 <= hex_pos2 <= len(data) - NUM_BYTES_2:
            extracted2 = data[hex_pos2:hex_pos2 + NUM_BYTES_2]
            step2_positions.append(hex_pos2)

    if step1_bytes and step2_positions:
        for pos in step2_positions:
            data[pos:pos + NUM_BYTES] = step1_bytes
        with open(file_path, "wb") as f:
            f.write(data)

    user_val = None
    while True:
        try:
            user_val = float(input("Please Write Your Value into (0/3): "))
            if 0 <= user_val <= 3:
                break
            else:
                print("❌ Value must be between 0 and 3.")
        except:
            print("❌ Invalid input. Try again.")

    user_bytes = struct.pack('<f', user_val)

    for idx in indices2:
        float_pos = idx
        data[float_pos:float_pos + 4] = user_bytes
        data[float_pos - 4:float_pos] = user_bytes
        data[float_pos - 8:float_pos - 4] = user_bytes

    with open(file_path, "wb") as f:
        f.write(data)
    print(f"✔ User value {user_val} pasted. Enjoy Your Character 🙂.")

def bigC():
    FOLDER = BASE_DIR / "Auto_Mod_Pak"
    file_path = find_body_duability_file()
    if not file_path:
        print("❌ No file with BodyDuability found in Auto_Mod_Pak!")
        return
    print(f"✔ File found: {file_path.name}")
    extract_and_overwrite(file_path)

# ========== SUB-MENUS FOR AUTO TOOL ==========
def headshot_uasset_menu():
    while True:
        print_enhanced_banner()
        print(Fore.CYAN + "\n--- Headshot (Uasset) - 4 Options ---" + Fore.RESET)
        print(Fore.GREEN + "1. Option A - Standard Headshot")
        print(Fore.GREEN + "2. Option B - Aggressive Headshot")
        print(Fore.GREEN + "3. Option C - Custom Headshot")
        print(Fore.GREEN + "4. Option D - Extreme Headshot")
        print(Fore.RED + "0. Back" + Fore.RESET)
        
        choice = safe_input(Fore.YELLOW + "Select (1-4, 0=Back): " + Fore.RESET).strip()
        flush_stdin()
        if choice == "1":
            headshot_auto_make()
            input("Press Enter to continue...")
        elif choice == "2":
            print("Option B - Aggressive Headshot (coming soon)")
            input("Press Enter to continue...")
        elif choice == "3":
            print("Option C - Custom Headshot (coming soon)")
            input("Press Enter to continue...")
        elif choice == "4":
            print("Option D - Extreme Headshot (coming soon)")
            input("Press Enter to continue...")
        elif choice == "0":
            break
        else:
            print(Fore.RED + "Invalid choice." + Fore.RESET)

def headshot_uexp_menu():
    while True:
        print_enhanced_banner()
        print(Fore.CYAN + "\n--- Headshot (Uexp) - 4 Options ---" + Fore.RESET)
        print(Fore.GREEN + "1. Option A - Standard Uexp Headshot")
        print(Fore.GREEN + "2. Option B - Advanced Uexp Headshot")
        print(Fore.GREEN + "3. Option C - Custom Uexp Headshot")
        print(Fore.GREEN + "4. Option D - Extreme Uexp Headshot")
        print(Fore.RED + "0. Back" + Fore.RESET)
        
        choice = safe_input(Fore.YELLOW + "Select (1-4, 0=Back): " + Fore.RESET).strip()
        flush_stdin()
        if choice == "1":
            patch_bones_from_head()
            input("Press Enter to continue...")
        elif choice == "2":
            print("Option B - Advanced Uexp Headshot (coming soon)")
            input("Press Enter to continue...")
        elif choice == "3":
            print("Option C - Custom Uexp Headshot (coming soon)")
            input("Press Enter to continue...")
        elif choice == "4":
            print("Option D - Extreme Uexp Headshot (coming soon)")
            input("Press Enter to continue...")
        elif choice == "0":
            break
        else:
            print(Fore.RED + "Invalid choice." + Fore.RESET)

def ipad_view_menu():
    while True:
        print_enhanced_banner()
        print(Fore.CYAN + "\n--- iPad View - 4 Options ---" + Fore.RESET)
        print(Fore.GREEN + "1. Option A - Standard iPad View")
        print(Fore.GREEN + "2. Option B - Wide iPad View")
        print(Fore.GREEN + "3. Option C - Custom iPad View")
        print(Fore.GREEN + "4. Option D - Extreme iPad View")
        print(Fore.RED + "0. Back" + Fore.RESET)
        
        choice = safe_input(Fore.YELLOW + "Select (1-4, 0=Back): " + Fore.RESET).strip()
        flush_stdin()
        if choice == "1":
            IPadV()
            input("Press Enter to continue...")
        elif choice == "2":
            print("Option B - Wide iPad View (coming soon)")
            input("Press Enter to continue...")
        elif choice == "3":
            print("Option C - Custom iPad View (coming soon)")
            input("Press Enter to continue...")
        elif choice == "4":
            print("Option D - Extreme iPad View (coming soon)")
            input("Press Enter to continue...")
        elif choice == "0":
            break
        else:
            print(Fore.RED + "Invalid choice." + Fore.RESET)

def ipad_scope_menu():
    while True:
        print_enhanced_banner()
        print(Fore.CYAN + "\n--- iPad Scope - 4 Options ---" + Fore.RESET)
        print(Fore.GREEN + "1. Option A - Standard Scope")
        print(Fore.GREEN + "2. Option B - Zoom Scope")
        print(Fore.GREEN + "3. Option C - Custom Scope")
        print(Fore.GREEN + "4. Option D - Extreme Scope")
        print(Fore.RED + "0. Back" + Fore.RESET)
        
        choice = safe_input(Fore.YELLOW + "Select (1-4, 0=Back): " + Fore.RESET).strip()
        flush_stdin()
        if choice == "1":
            IPadS()
            input("Press Enter to continue...")
        elif choice == "2":
            print("Option B - Zoom Scope (coming soon)")
            input("Press Enter to continue...")
        elif choice == "3":
            print("Option C - Custom Scope (coming soon)")
            input("Press Enter to continue...")
        elif choice == "4":
            print("Option D - Extreme Scope (coming soon)")
            input("Press Enter to continue...")
        elif choice == "0":
            break
        else:
            print(Fore.RED + "Invalid choice." + Fore.RESET)

# ========== AUTO TOOL MAIN MENU ==========
def MainMenu():
    while True:
        os.system("clear")
        print_enhanced_banner()
        print()
        print(Fore.CYAN + "Select Option.." + Style.RESET_ALL)
        
        menu_items = [
            ("7.", "Headshot (Uasset - method)"),
            ("8.", "Headshot (Uexp - method)"),
            ("9.", "Ipad View (Uexp - Method)"),
            ("10.", "Ipad View ( Scope ) (Uexp - Method)"),
            ("0.", "Exit"),
        ]
        
        color_sets = [
            (Fore.MAGENTA, Fore.YELLOW),
            (Fore.GREEN, Fore.MAGENTA),
            (Fore.BLUE, Fore.CYAN),
            (Fore.YELLOW, Fore.GREEN),
            (Fore.CYAN, Fore.BLUE),
        ]
        max_name = max(len(name) for _, name in menu_items)
        border_len = max_name + 8
        print(Fore.CYAN + "╔" + "═" * border_len + "╗" + Style.RESET_ALL)
        for idx, (num, name) in enumerate(menu_items):
            num_col, name_col = color_sets[idx % len(color_sets)]
            line = (
                Fore.CYAN + "║ " +
                num_col + Style.BRIGHT + f"{num}" +
                Fore.CYAN + "│" +
                name_col + f"{name.ljust(max_name)} " +
                Fore.CYAN + "║" + Style.RESET_ALL
            )
            print(line)
            if idx != len(menu_items) - 1:
                print(Fore.CYAN + "╟" + "─" * border_len + "╢" + Style.RESET_ALL)
        print(Fore.CYAN + "╚" + "═" * border_len + "╝" + Style.RESET_ALL)
        
        choice = safe_input(Fore.MAGENTA + "Select an option (7,8,9,10,0): " + Style.RESET_ALL).strip()
        flush_stdin()
        time.sleep(1)
        
        if choice == "7":
            headshot_uasset_menu()
        elif choice == "8":
            headshot_uexp_menu()
        elif choice == "9":
            ipad_view_menu()
        elif choice == "10":
            ipad_scope_menu()
        elif choice == "0":
            print(Fore.YELLOW + "Returning to Main Menu..." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)

# ========== MAIN PAK MENU ==========
def main_menu():
    """Main menu interface with enhanced Cyberpunk banner"""
    
    while True:
        print_enhanced_banner()
        console.print(Align.center("[dim]👤 SEN_HACKER  |  💰 UNLIMITED  |  ⏳ NO EXPIRY[/dim]"))

        pak_files = detect_pak_files(BASE_DIR)

        if not pak_files:
            console.print(Panel(
                "[bold #FF0055]⚠  No .pak/.obb files found in the storage/downloads/SEN_PAK_TOOL![/bold #FF0055]\n"
                "[#FFAA00]Place your .pak/.obb files in the same directory as this tool.[/#FFAA00]",
                border_style="#FF0055", box=box.ROUNDED, padding=(1, 2)
            ))
            flush_stdin()
            safe_input("\nPress Enter to continue...")
            continue

        files_table = Table(box=box.SIMPLE_HEAD, border_style="#4A4A6A", show_edge=False, pad_edge=False, expand=True)
        files_table.add_column("#", style="bold #7B5CFF", width=4, justify="right")
        files_table.add_column("File", style="#22D3EE")
        files_table.add_column("Size", style="#F4B400", justify="right")
        for i, pak_file in enumerate(pak_files, 1):
            file_size = pak_file.stat().st_size
            size_mb = file_size / (1024 * 1024)
            files_table.add_row(str(i), pak_file.name, f"{size_mb:.2f} MB")

        console.print(Panel(
            files_table,
            title=f"[bold #22D3EE]📁 {len(pak_files)} FILE(S) DETECTED[/bold #22D3EE]",
            title_align="left", border_style="#4A4A6A", box=box.ROUNDED, padding=(0, 1)
        ))

        options = Table.grid(padding=(0, 1))
        options.add_column(style="bold", width=3)
        options.add_column()
        options.add_row("[#00FF88]1[/#00FF88]", "[#00FF88]📂 UNPAK[/#00FF88] [dim](Obb & Gamepatch) — Extract .pak file[/dim]")
        options.add_row("[#22D3EE]2[/#22D3EE]", "[#22D3EE]🔧 REPAK[/#22D3EE] [dim](Obb & Gamepatch) — Rebuild .pak file[/dim]")
        options.add_row("[#00FF88]3[/#00FF88]", "[#00FF88]🤖 AUTO TOOL[/#00FF88] [dim]— Menu file[/dim]")
        options.add_row("[#FF8800]4[/#FF8800]", "[#FF8800]📦 OBB TOOL[/#FF8800] [dim]— Unzip/Rezip .obb (ANTIRESET OBB) files[/dim]")
        options.add_row("[#FF0055]5[/#FF0055]", "[#FF0055]💉 INJECT[/#FF0055] [dim]— Inject any LUA into a custom Pak[/dim]")
        options.add_row("[#F4B400]6[/#F4B400]", "[#F4B400]🗑️  CLEAR[/#F4B400] [dim]— Remove all Unpack/Repack folders[/dim]")
        options.add_row("[#FF4444]7[/#FF4444]", "[#FF4444]ℹ️  ABOUT[/#FF4444] [dim]— Tool information[/dim]")
        options.add_row("[white]0[/white]", "[white]🚪 EXIT[/white] [dim]— Close the tool[/dim]")

        console.print(Panel(
            options,
            title="[bold #7B5CFF]⚙  OPTIONS[/bold #7B5CFF]",
            title_align="left", border_style="#7B5CFF", box=box.ROUNDED, padding=(1, 2)
        ))

        choice = safe_input(f"Enter your choice (0-7): ").strip()
        flush_stdin()
        
        if choice == '1':
            if len(pak_files) == 1:
                selected_pak = pak_files[0]
            else:
                file_choice = safe_input(f"Select .pak file (1-{len(pak_files)}): ").strip()
                flush_stdin()
                try:
                    index = int(file_choice) - 1
                    if 0 <= index < len(pak_files):
                        selected_pak = pak_files[index]
                    else:
                        console.print("[bold #FF0055]❌ Invalid selection![/bold #FF0055]")
                        time.sleep(2)
                        continue
                except ValueError:
                    console.print("[bold #FF0055]❌ Invalid input! Please enter a number.[/bold #FF0055]")
                    time.sleep(2)
                    continue
            
            pak_name = selected_pak.stem
            unpack_path = BASE_DIR / f"Unpack_{pak_name}"
            repack_path = BASE_DIR / f"Repack_{pak_name}"
            
            with Progress() as progress:
                task = progress.add_task(f"[#00CCFF]Creating directories...", total=1)
                unpack_path.mkdir(exist_ok=True)
                repack_path.mkdir(exist_ok=True)
                progress.update(task, completed=1)
            
            try:
                console.print(f"[bold #00FFFF]🚀 Unpacking {selected_pak.name}...[/bold #00FFFF]")
                
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    console=console
                ) as progress:
                    task = progress.add_task(f"Processing {selected_pak.name}", total=100)
                    
                    pak = TencentPakFile(selected_pak)
                    progress.update(task, advance=30)
                    
                    pak.dump(unpack_path)
                    progress.update(task, advance=40)
                    
                    log_path = unpack_path / f"SEN_HACKER_Debug{pak_name}.log"
                    dump_unpacking_log(pak, log_path)
                    progress.update(task, advance=20)
                    
                    progress.update(task, completed=100)
                
                console.print("[bold #00FF88]✅ UNPACK COMPLETED![/bold #00FF88]")
                console.print(f"[#00CCFF]📁 Unpacked to: {unpack_path}[/#00CCFF]")
                console.print(f"[#00CCFF]🔧 Repack folder: {repack_path}[/#00CCFF]")
                console.print(f"[#00CCFF]📝 Debug log saved in unpack folder[/#00CCFF]")
                
                file_count = sum(len(files) for _, files in pak._index.items())
                console.print(f"[#FFFF00]📄 Total files extracted: {file_count}[/#FFFF00]")
                
            except Exception as e:
                console.print(f"[bold #FF0055]❌ Error unpacking:[/bold #FF0055] {escape(str(e))}")
                import traceback
                traceback.print_exc()
                
            flush_stdin()
            safe_input("\nPress Enter to continue...")
            
        elif choice == '2':
            if len(pak_files) == 1:
                selected_pak = pak_files[0]
            else:
                file_choice = safe_input(f"Select .pak file (1-{len(pak_files)}): ").strip()
                flush_stdin()
                try:
                    index = int(file_choice) - 1
                    if 0 <= index < len(pak_files):
                        selected_pak = pak_files[index]
                    else:
                        console.print("[bold #FF0055]❌ Invalid selection![/bold #FF0055]")
                        time.sleep(2)
                        continue
                except ValueError:
                    console.print("[bold #FF0055]❌ Invalid input! Please enter a number.[/bold #FF0055]")
                    time.sleep(2)
                    continue
                    
            pak_name = selected_pak.stem
            repack_dir = BASE_DIR / f"Repack_{pak_name}"
            
            if not repack_dir.exists():
                console.print(f"[bold #FF0055]❌ ERROR: {repack_dir} not found.[/bold #FF0055]")
                console.print("[#FFAA00]⚠  Please unpack the .pak file first using option 1.[/#FFAA00]")
                flush_stdin()
                safe_input("\nPress Enter to continue...")
                continue
                
            try:
                console.print(f"[bold #00FFFF]🚀 Repacking {selected_pak.name}...[/bold #00FFFF]")
                
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    console=console
                ) as progress:
                    task = progress.add_task(f"Repacking {selected_pak.name}", total=100)
                    
                    pak = TencentPakFile(selected_pak)
                    progress.update(task, advance=20)

                    output_pak = selected_pak.with_suffix(".repacked")

                    mode = detect_repack_mode(selected_pak)

                    if mode == "MINI_OBB":
                        repack_mini_obb(pak, repack_dir, output_pak)
                    elif mode == "GAMEPATCH": 
                        repack_gamepatch(pak, repack_dir, output_pak)
                    else:  
                        repack_obbzsdic(pak, repack_dir, output_pak)

                    progress.update(task, advance=50)
                    
                    # Close PAK object before file operations
                    del pak
                    import gc
                    gc.collect()
                    
                    if output_pak.exists():
                        if output_pak.stat().st_size != selected_pak.stat().st_size:
                            console.print(f"[#FFAA00]⚠ Size mismatch! Original: {selected_pak.stat().st_size}, New: {output_pak.stat().st_size}[/#FFAA00]")
                            console.print("[#FFAA00]Keeping both files - manual check needed[/#FFAA00]")
                        else:
                            backup_path = selected_pak.with_suffix(".pak.bak")
                            selected_pak.rename(backup_path)
                            output_pak.rename(selected_pak)
                            backup_path.unlink()
                            console.print("[bold #00FF88]✅ File replaced successfully![/bold #00FF88]")
                    else:
                        console.print("[bold #FF0055]❌ Output file not created![/bold #FF0055]")
                    
                    progress.update(task, completed=100)
                
                console.print("[bold #00FF88]✅ REPACK COMPLETED![/bold #00FF88]")
                
            except Exception as e:
                console.print(f"[bold #FF0055]❌ Repack failed:[/bold #FF0055] {e}")
                import traceback
                traceback.print_exc()
                
            flush_stdin()
            safe_input("\nPress Enter to continue...")
            
        elif choice == '3':
            MainMenu()
            flush_stdin()
            safe_input("\nPress Enter to continue...")
            
        elif choice == '4':
            obb_tool_menu()
            flush_stdin()
            safe_input("\nPress Enter to continue...")
            
        elif choice == '5':
            handle_repack()
            flush_stdin()
            safe_input("\nPress Enter to continue...")
            
        elif choice == '6':
            console.print("[bold #FFFF00]⚠  WARNING: This will delete all Unpack_* and Repack_* folders[/bold #FFFF00]")
            confirm = safe_input("Are you sure? (y/N): ").strip().lower()
            flush_stdin()
            
            if confirm == 'y':
                clear_folders(BASE_DIR)
            else:
                console.print("[#FFAA00]Operation cancelled.[/#FFAA00]")
            
            flush_stdin()
            safe_input("\nPress Enter to continue...")
            
        elif choice == '7':
            console.print(Panel(
                "[bold #22D3EE]📱 SEN_HACKER MOD TOOL v4.6[/bold #22D3EE]\n"
                "[white]No Login Required[/white]\n"
                "[dim]Modding toolkit for BGMI / PUBG Mobile PAK & OBB files[/dim]",
                title="ℹ️  ABOUT", title_align="left", border_style="#7B5CFF", box=box.ROUNDED, padding=(1, 2)
            ))
            flush_stdin()
            safe_input("\nPress Enter to continue...")
            continue
            
        elif choice == '0':
            console.print("[bold #FFFF00]\n👋 Allah Hafiz... Thanks for Using This Tool![/bold #FFFF00]")
            time.sleep(2)
            break
            
        else:
            console.print("[bold #FF0055]❌ Invalid choice! Please enter 0, 1, 2, 3, 4, 5, 6, or 7.[/bold #FF0055]")
            time.sleep(2)

# ========== FOLDER CREATION ==========
def create_required_folders():
    folders = [
        BASE_DIR / "Auto_Mod_Pak",
        BASE_DIR / "Edited",
        BASE_DIR / "OBBZIP" / "input",
        BASE_DIR / "OBBZIP" / "unpacked_obb",
        BASE_DIR / "OBBZIP" / "repack_obb",
        BASE_DIR / "OBBZIP" / "repack_pak",
        BASE_DIR / "BACKUP",
    ]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
        console.print(f"[#00FF88]✓ Created: {folder.relative_to(BASE_DIR)}[/#00FF88]")

# ========== MAIN ENTRY POINT ==========
if __name__ == "__main__":
    try:
        # Install dependencies first
        install_dependencies()
        
        # Create required folders
        create_required_folders()
        
        # Start main menu
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[bold #FFFF00]⚠ Interrupted by user. Exiting...[/bold #FFFF00]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold #FF0055]💥 UNEXPECTED ERROR:[/bold #FF0055] {escape(str(e))}")
        import traceback
        traceback.print_exc()
        flush_stdin()
        safe_input("\nPress Enter to exit...")
        sys.exit(1)
        
