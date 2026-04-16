import hashlib
import sys

# run.py ထဲက SECRET_SALT အတိုင်း ဖြစ်ရပါမယ်
SECRET_SALT = "ohmygod@123"

def make_key():
    print(f"--- AI BPPS KEY GENERATOR ---")
    did = input("Enter User Device ID: ").strip()
    # format: YYYYMMDDHHMM (ဥပမာ- 202612312359)
    expiry = input("Enter Expiry Date (YYYYMMDDHHMM): ").strip()
    
    # Logic: SHA256(ID + EXPIRY + SALT)
    raw = f"{did}{expiry}{SECRET_SALT}"
    auth_hash = hashlib.sha256(raw.encode()).hexdigest()
    
    # Key Format: Hash ရှေ့ ၁၂ လုံး + Expiry Date
    final_key = f"{auth_hash[:12].upper()}{expiry}"
    
    print(f"\n[✓] Generated Key for {did}:")
    print(f"--> {final_key}\n")

if __name__ == "__main__":
    make_key()
