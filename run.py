import core
import os
import sys
import shutil

# --- [ COLORS ] ---
C_CYAN, C_GREEN, C_YELLOW, C_WHITE, C_RESET, C_BOLD = '\033[96m', '\033[92m', '\033[93m', '\033[97m', '\033[0m', '\033[1m'
LICENSE_FILE = os.path.join(os.path.expanduser("~"), ".turbo_license")

def get_terminal_width():
    return shutil.get_terminal_size().columns

def display_smns_banner(did, key="N/A", expiry="N/A", status="PENDING"):
    os.system('clear')
    w = get_terminal_width()
    
    # TRB ကို SMNS အဖြစ် UI မှာ အတင်းပြောင်းခိုင်းခြင်း [အရေးကြီးသည်]
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

    print(f"{C_CYAN}┌{'─'*(w-2)}┐")
    for line in logo:
        print(f"│{C_GREEN}{C_BOLD}{line.center(w-2)}{C_CYAN}│")
    
    print(f"│{C_YELLOW}{C_BOLD}{'SMNS TECHNOLOGY TOOLKIT'.center(w-2)}{C_CYAN}│")
    print(f"├{'─'*(w-2)}┤")

    # Info Display Section
    info_list = [
        ("DEVICE ID", smns_did),
        ("KEY", key),
        ("EXPIRE", expiry),
        ("STATUS", status)
    ]

    for label, value in info_list:
        color = C_GREEN if "VERIFIED" in str(value) else C_WHITE
        # ဘယ်ညာ ညီအောင် space ဖြည့်ခြင်း logic
        line_content = f" {C_YELLOW}{label:<10} : {color}{value}"
        # escape code တွေကြောင့် len() မမှန်မှာစိုး၍ စာသားသက်သက်ကိုပဲ တွက်ပါသည်
        actual_len = len(label) + len(str(value)) + 4 
        padding = " " * (w - actual_len - 3)
        print(f"{C_CYAN}│{line_content}{padding}│")

    print(f"└{'─'*(w-2)}┘{C_RESET}")

if __name__ == "__main__":
    try:
        # core ထဲက TRB ID ကို ယူပါသည်
        did = core.get_device_id()
        # UI အတွက် SMNS အဖြစ် ပြောင်းပါသည်
        smns_id = str(did).replace("TRB-", "SMNS-")
        if not smns_id.startswith("SMNS-"): smns_id = f"SMNS-{smns_id}"

        authorized, expiry, status, current_key = False, "N/A", "PENDING", "N/A"
        
        # Key အဟောင်းဖျက်ချင်ရင် အောက်က line ကို တစ်ခါသုံးပြီး ပြန်ဖျက်ပါ
        # os.remove(LICENSE_FILE) 

        if os.path.exists(LICENSE_FILE):
            with open(LICENSE_FILE, "r") as f:
                current_key = f.read().strip()
            # အစ်ကို့ရဲ့ core.validate_key က TRB ပဲ လက်ခံတာဆိုရင် 'did' ကိုသုံးပါ
            # SMNS ပဲ လက်ခံတာဆိုရင် 'smns_id' ကိုသုံးပါ
            is_valid, msg, exp = core.validate_key(did, current_key)
            if is_valid:
                authorized, status, expiry = True, msg, exp

        display_smns_banner(smns_id, current_key, expiry, status)
        
        if not authorized:
            print(f"\n{C_CYAN}[?] Activation Key: {C_RESET}")
            key_in = input(f"\033[92mroot@smns:~# \033[0m").strip().upper()
            v, m, e = core.validate_key(did, key_in)
            if v:
                with open(LICENSE_FILE, "w") as f: f.write(key_in)
                display_smns_banner(smns_id, key_in, e, m)
                authorized = True
            else:
                print(f"\n\033[91m[X] Invalid Key for {smns_id}!\033[0m")
                sys.exit(1)

        if authorized:
            core.start_process()

    except KeyboardInterrupt:
        print("\n\033[91m[!] Stopped.\033[0m")
