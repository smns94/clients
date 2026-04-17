import core
import os
import sys
import shutil

# --- [ UI COLORS ] ---
C_CYAN, C_GREEN, C_YELLOW, C_WHITE, C_RED, C_RESET, C_BOLD = '\033[96m', '\033[92m', '\033[93m', '\033[97m', '\033[91m', '\033[0m', '\033[1m'
LICENSE_FILE = os.path.join(os.path.expanduser("~"), ".turbo_license")

def get_terminal_width():
    # Termux screen အကျယ်ကို ယူပါမည်
    return shutil.get_terminal_size().columns

def display_smns_banner(did, key="N/A", expiry="N/A", status="PENDING"):
    os.system('clear')
    w = get_terminal_width()
    
    # TRB ကို SMNS သို့ ပြောင်းလဲခြင်း
    smns_did = str(did).replace("TRB-", "SMNS-")
    if not smns_did.startswith("SMNS-"):
        smns_did = f"SMNS-{smns_did}"

    logo = [
        " ██████╗███╗   ███╗███╗   ██╗███████╗",
        "██╔════╝████╗ ████║████╗  ██║██╔════╝",
        "╚█████╗ ██╔████╔██║██╔██╗ ██║███████╗",
        " ╚═══██╗██║╚██╔╝██║██║╚██╗██║╚════██║",
        "██████╔╝██║ ╚═╝ ██║██║ ╚████║███████║",
        "╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝"
    ]

    # အပေါ်ဘောင် မျဉ်းကြောင်း
    print(f"{C_CYAN}┌{'─'*(w-2)}┐{C_RESET}")
    for line in logo:
        print(f"{C_CYAN}│{C_GREEN}{C_BOLD}{line.center(w-2)}{C_CYAN}│{C_RESET}")
    
    print(f"{C_CYAN}│{C_YELLOW}{C_BOLD}{'SMNS TECHNOLOGY TOOLKIT'.center(w-2)}{C_CYAN}│{C_RESET}")
    print(f"{C_CYAN}├{'─'*(w-2)}┤{C_RESET}")

    # Info Display Section
    # စာလုံးအရှည်ကို (w-17) အသေထားပြီး တွက်ချက်ခြင်းဖြင့် ဘောင်ညီစေပါသည်
    info_width = w - 17
    
    status_color = C_GREEN if "VERIFIED" in str(status) else C_RED
    
    print(f"{C_CYAN}│ {C_YELLOW}DEVICE ID : {C_WHITE}{str(smns_did).ljust(info_width)}{C_CYAN} │")
    print(f"{C_CYAN}│ {C_YELLOW}KEY       : {C_WHITE}{str(key).ljust(info_width)}{C_CYAN} │")
    print(f"{C_CYAN}│ {C_YELLOW}EXPIRE    : {C_WHITE}{str(expiry).ljust(info_width)}{C_CYAN} │")
    print(f"{C_CYAN}│ {C_YELLOW}STATUS    : {status_color}{str(status).ljust(info_width)}{C_CYAN} │")

    # အောက်ဘောင် မျဉ်းကြောင်း
    print(f"{C_CYAN}└{'─'*(w-2)}┘{C_RESET}")

if __name__ == "__main__":
    try:
        # Device ID ကို core မှ ယူပါမည်
        did = core.get_device_id()
        
        authorized, expiry, status, current_key = False, "N/A", "PENDING", "N/A"
        
        # License File စစ်ဆေးခြင်း
        if os.path.exists(LICENSE_FILE):
            with open(LICENSE_FILE, "r") as f:
                current_key = f.read().strip()
            
            # core logic မှ validate လုပ်ပါမည်
            is_valid, msg, exp = core.validate_key(did, current_key)
            if is_valid:
                authorized, status, expiry = True, msg, exp

        display_smns_banner(did, current_key, expiry, status)
        
        if not authorized:
            print(f"\n{C_CYAN}[?] Activation Key: {C_RESET}")
            key_in = input(f"\033[92mroot@smns:~# \033[0m").strip().upper()
            v, m, e = core.validate_key(did, key_in)
            if v:
                with open(LICENSE_FILE, "w") as f: f.write(key_in)
                display_smns_banner(did, key_in, e, m)
                authorized = True
            else:
                print(f"\n{C_RED}[X] Invalid Activation Key!{C_RESET}")
                sys.exit(1)

        if authorized:
            # Main process စတင်ခြင်း
            core.start_process()

    except KeyboardInterrupt:
        print(f"\n{C_RED}[!] Stopped.{C_RESET}")
