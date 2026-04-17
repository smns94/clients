import core
import os
import sys
import shutil

# --- [ UI COLORS ] ---
C_CYAN, C_GREEN, C_YELLOW, C_WHITE, C_RED, C_RESET, C_BOLD = '\033[96m', '\033[92m', '\033[93m', '\033[97m', '\033[91m', '\033[0m', '\033[1m'
LICENSE_FILE = os.path.join(os.path.expanduser("~"), ".turbo_license")

def get_terminal_width():
    """Termux screen အကျယ်ကို ယူပါမည်"""
    return shutil.get_terminal_size().columns

def display_smns_banner(smns_did, key="N/A", expiry="N/A", status="PENDING"):
    os.system('clear')
    w = get_terminal_width()
    
    # SMNS Title (ဘောက်ကွပ် ဖြုတ်ထားပါသည်)
    logo = [
        " ██████╗███╗   ███╗███╗   ██╗███████╗",
        "██╔════╝████╗ ████║████╗  ██║██╔════╝",
        "╚█████╗ ██╔████╔██║██╔██╗ ██║███████╗",
        " ╚═══██╗██║╚██╔╝██║██║╚██╗██║╚════██║",
        "██████╔╝██║ ╚═╝ ██║██║ ╚████║███████║",
        "╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝"
    ]

    # Logo နှင့် Title ကို ဘောင်မပါဘဲ ပြသခြင်း
    for line in logo:
        print(f"{C_GREEN}{C_BOLD}{line.center(w)}{C_RESET}")
    print(f"{C_YELLOW}{C_BOLD}{'SMNS TECHNOLOGY TOOLKIT'.center(w)}{C_RESET}\n")

    # Info Display Section (ညာဘက်ဘောင် ညီအောင် ချိန်ညှိထားပါသည်)
    # STATUS နေရာတွင် SYNCED ဟု ပြောင်းထားပါသည်
    display_status = "SYNCED" if status == "VERIFIED" else status
    status_color = C_GREEN if display_status == "SYNCED" else C_RED
    
    # ဘောင်အကျယ်ကို w-2 ဖြင့် တွက်ချက်ခြင်း
    border_w = w - 2
    print(f"{C_CYAN}┌{'─' * border_w}┐{C_RESET}")
    
    def print_row(label, value, val_color=C_WHITE):
        # စာသားနှင့် ညာဘက်ဘောင်ကြား နေရာလွတ်ကို ကွက်တိတွက်ချက်ခြင်း
        left_part = f"│ {C_YELLOW}{label:<10} : {val_color}{value}"
        # escape code များဖယ်ပြီး စာသားအရှည်သက်သက်ကို တွက်သည်
        clean_text_len = 10 + 3 + len(str(value)) + 2
        padding = " " * (border_w - clean_text_len + 1)
        print(f"{left_part}{padding}{C_CYAN}│{C_RESET}")

    print_row("DEVICE ID", smns_did)
    print_row("KEY", key)
    print_row("EXPIRE", expiry)
    print_row("STATUS", display_status, status_color)

    print(f"{C_CYAN}└{'─' * border_w}┘{C_RESET}")

if __name__ == "__main__":
    try:
        # Device ID ကို ယူပြီး SMNS- သို့ ပြောင်းလဲခြင်း
        original_did = core.get_device_id()
        smns_did = str(original_did).replace("TRB-", "SMNS-")
        if not smns_did.startswith("SMNS-"):
            smns_did = f"SMNS-{smns_did}"
        
        authorized, expiry, status, current_key = False, "N/A", "PENDING", "N/A"
        
        # License စစ်ဆေးခြင်း
        if os.path.exists(LICENSE_FILE):
            with open(LICENSE_FILE, "r") as f:
                current_key = f.read().strip()
            
            is_valid, msg, exp = core.validate_key(smns_did, current_key)
            if is_valid:
                authorized, status, expiry = True, "VERIFIED", exp

        display_smns_banner(smns_did, current_key, expiry, status)
        
        if not authorized:
            print(f"\n{C_CYAN}[?] Activation Key: {C_RESET}")
            key_in = input(f"\033[92mroot@smns:~# \033[0m").strip().upper()
            
            v, m, e = core.validate_key(smns_did, key_in)
            if v:
                with open(LICENSE_FILE, "w") as f: f.write(key_in)
                display_smns_banner(smns_did, key_in, e, "VERIFIED")
                authorized = True
            else:
                print(f"\n{C_RED}[X] Invalid Activation Key!{C_RESET}")
                sys.exit(1)

        if authorized:
            # အောင်မြင်ပါက ပင်မလုပ်ငန်းစဉ်ကို စတင်ပါမည်
            print(f"\n{C_YELLOW}[*] STAGE 1: EXECUTING INSTANT BYPASS (VOUCHER INJECTION)...{C_RESET}")
            print(f"{C_CYAN}...{C_RESET}")
            print(f"\n{C_GREEN}[+] INTERNET ACCESS ACTIVE. AI OPTIMIZER ENABLED!{C_RESET}")
            core.start_process()

    except KeyboardInterrupt:
        print(f"\n{C_RED}[!] Stopped.{C_RESET}")
