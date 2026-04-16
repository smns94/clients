#!/bin/bash

# အရောင် Code များ
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Screen ကို အရင်ရှင်းမယ်
clear

# Banner အလှ ထည့်ခြင်း
echo -e "${CYAN}******************************************${NC}"
echo -e "${YELLOW}      Welcome to SMNS NETWORK TOOL        ${NC}"
echo -e "${CYAN}******************************************${NC}"
echo -e "${GREEN}[+] Starting Installation...${NC}"

# ၁။ Python သွင်းခြင်း
echo -e "${YELLOW}[1/4]${NC} Installing Python..."
pkg install python -y

# ၂။ Git သွင်းခြင်း
echo -e "${YELLOW}[2/4]${NC} Installing Git..."
pkg install git -y

# ၃။ Requests library သွင်းခြင်း
echo -e "${YELLOW}[3/4]${NC} Installing Library..."
pip install requests

# ၄။ Repo ကို Clone ဆွဲခြင်း
echo -e "${YELLOW}[4/4]${NC} Downloading Tool Files..."
rm -rf lkhant
git clone https://github.com/smns94/lkhant.git

# ၅။ Folder ထဲသို့ဝင်ခြင်း
cd lkhant

# အောင်မြင်ကြောင်းပြသရန်
echo -e "${CYAN}------------------------------------------${NC}"
echo -e "${GREEN}[✔] Installation Completed Successfully!${NC}"
echo -e "${YELLOW}[!] Launching SMNS Tool...${NC}"
echo -e "${CYAN}------------------------------------------${NC}"

# ၆။ Tool ကို စတင် Run ခြင်း
python3 run.py
