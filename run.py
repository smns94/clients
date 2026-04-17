import core  # core.so ဖိုင်ရှိရန် လိုအပ်သည်
import os
import sys
import time
import hashlib
import shutil

# --- [ UI COLORS ] ---
C_RED, C_CYAN, C_GREEN, C_YELLOW, C_RESET, C_BOLD = '\033[91m', '\033[96m', '\033[92m', '\033[93m', '\033[0m', '\033[1m'
SECRET_SALT = "ohmygod@123"
LICENSE_FILE = os.path.join(os.path.expanduser("~"), ".turbo_license")

def get_terminal_width():
    """Screen ရဲ့ width ကို ယူပြီး Center ချိန်ရန်"""
    return shutil.get_terminal_size().columns

def print_center(text, color=C_RESET):
    """စာသားများကို အလယ်တည့်တည့်သို့ ပို့ပေးရန်"""
    width = get_terminal_width()
    for line in text.split('\n'):
        print(f"{color}{line.center(width)}{C_RESET}")

def display_smns_banner():
    """စတိုင်ကျသော SMNS Banner ကို Center ချိန်၍ ပြသရန်"""
    os.system('clear')
    width = get_terminal_width()
    
    # SMNS ASCII Art
    smns_logo = """
 ██████╗███╗   ███╗███╗   ██╗███████╗
██╔════╝████╗ ████║████╗  ██║██╔════╝
╚█████╗ ██╔████╔██║██╔██╗ ██║███████╗
 ╚═══██╗██║╚██╔╝██║██║╚██╗██║╚════██║
██████╔╝██║ ╚═╝ ██║██║ ╚████║███████║
╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝"""

    border = "═" * (width - 10)
    print(f"{C_CYAN}╔{border}╗{C_RESET}")
    print_center(smns_logo, C_GREEN + C_BOLD)
    print_center("SMNS TECHNOLOGY TOOLKIT", C_YELLOW + C_BOLD)
    print(f"{C_CYAN}╚{border}╝{C_RESET}")

if __name__ == "__main__":
    try:
        # Device ID နှင့် Time Manipulation စစ်ဆေးခြင်း
        did = core.get_device_id()
        
        if not core.check_time_manipulation():
            os.system('clear')
            print_center("FATAL ERROR: System time manipulation detected!", C_RED)
            sys.exit(1)

        authorized, expiry, status = False, None, "PENDING"
        
        # License File စစ်ဆေးခြင်း
        if os.path.exists(LICENSE_FILE):
            with open(LICENSE_FILE, "r") as f:
                saved_key = f.read().strip()
            
            is_valid, msg, expiry = core.validate_key(did, saved_key)
            if is_valid:
                authorized, status = True, msg
            elif core.verify_legacy_user(saved_key):
                # Legacy Migration Logic
                lt_exp = "212601010000"
                raw_new = f"{did}{lt_exp}{SECRET_SALT}"
                new_k = f"{hashlib.sha256(raw_new.encode()).hexdigest()[:12].upper()}{lt_exp}"
                
                with open(LICENSE_FILE, "w") as f:
                    f.write(new_k)
                
                authorized, status = True, "VERIFIED_LIFETIME"
                display_smns_banner()
                print_center("LEGACY USER DETECTED! NEW LIFETIME KEY GENERATED:", C_CYAN)
                print_center(new_k, C_GREEN + C_BOLD)
                time.sleep(5)

        display_smns_banner()
        
        # Activation Key တောင်းခံခြင်း
        if not authorized:
            print_center(f"Device ID: {did}", C_CYAN)
            print(f"\n{C_CYAN}[?] Activation Key: {C_RESET}")
            key = input(f"\033[92mroot@smns:~# \033[0m").strip().upper()
            
            v, m, e = core.validate_key(did, key)
            if v:
                with open(LICENSE_FILE, "w") as f: f.write(key)
                display_smns_banner()
                authorized = True
            elif core.verify_legacy_user(key):
                lt_exp = "212601010000"
                raw_new = f"{did}{lt_exp}{SECRET_SALT}"
                new_k = f"{hashlib.sha256(raw_new.encode()).hexdigest()[:12].upper()}{lt_exp}"
                with open(LICENSE_FILE, "w") as f: f.write(new_k)
                display_smns_banner()
                print_center("NEW LIFETIME KEY GENERATED (SAVE THIS):", C_CYAN)
                print_center(new_k, C_GREEN + C_BOLD)
                time.sleep(5)
                authorized = True
            else:
                print_center("Invalid Activation Key!", C_RED)
                sys.exit(1)

        if authorized:
            # အောင်မြင်ပါက ပင်မ လုပ်ဆောင်ချက်ကို စတင်ရန်
            print_center(f"STATUS: {status}", C_GREEN)
            core.start_process()

    except KeyboardInterrupt:
        print(f"\n{C_RED}[!] STOPPED BY USER.{C_RESET}")
