import urllib3
from datetime import datetime, timezone
from pathlib import Path
import csv
import logging as log
log.basicConfig(format='%(levelname)s:%(message)s', level=log.INFO)

ACCT = "<<some_koinos_account>>" #Target Koinos account
API_KEY = "<<coingecko_key>>" #Not required. Only if you want price. From your CoinGecko account. You can get a free API key.
LOG_OUTPUT = True #If want to see output in console
APPEND_CSV = True  #If want to write to a CSV file

KOIN_API = "https://rest.koinos.tools/api"
COINGECKO_API = "https://api.coingecko.com/api/v3"
KOIN = "15DJN4a8SgrbGhhGksSBASiSYjGnMU8dGL"
VHP = "18tWNU7E4yuQzz7hMVpceb9ixmaWLVyQsr"
ACCOUNT_URL = f"account/{ACCT}"
BALANCE = f"{ACCOUNT_URL}/balance"
MANA_BALANCE = f"{ACCOUNT_URL}/mana"
KOIN_BALANCE = f"{BALANCE}/{KOIN}"
VHP_BALANCE = f"{BALANCE}/{VHP}"
HISTORY_CSV = f"{Path.cwd()}/acct_history.csv"

def get_balances():
    koin = get_koin_data(KOIN_BALANCE)
    vhp = get_koin_data(VHP_BALANCE)
    total_koin_vhp = float(koin) + float(vhp)
    mana = get_koin_data(MANA_BALANCE)
    price = get_coingecko_price()
    now = datetime.now(timezone.utc)
    today = f"{now.month}/{now.day}/{now.year}"
    if LOG_OUTPUT:
        log.info(f"{today = }")
        log.info(f"{total_koin_vhp = }")
        log.info(f"{koin = }")
        log.info(f"{vhp = }")
        log.info(f"{mana = }")
        log.info(f"{price = }")
    if APPEND_CSV:
        file_exists = Path(HISTORY_CSV).exists()
        with open(HISTORY_CSV, "a") as csv_file:
            writer = csv.writer(csv_file)
            if not file_exists:
                writer.writerow(["date","total_koin_vhp","koin","vhp","mana","price"])
            writer.writerow([today,total_koin_vhp,koin,vhp,mana,price])


def get_koin_data(action):
    try:
        resp = urllib3.request("GET", f"{KOIN_API}/{action}")
        return resp.json()['value']
    except Exception as e:
        log.exception(e)


def get_coingecko_price():
    try:
        resp = urllib3.request("GET", f"{COINGECKO_API}/simple/price?ids=koinos&" + \
                f"vs_currencies=usd&x_cg_api_key={API_KEY}")
        return resp.json()['koinos']['usd']
    except Exception as e:
        log.exception(e)


get_balances()
