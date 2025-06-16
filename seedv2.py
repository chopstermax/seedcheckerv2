import os
import time
from web3 import Web3, Account
from mnemonic import Mnemonic
import requests

# --- Configuration ---
PHRASES_DIR = "phrases"
RESULTS_DIR = "results"
SEEDS_FILE = os.path.join(PHRASES_DIR, "seeds.txt")
KEYS_FILE = os.path.join(PHRASES_DIR, "private_keys.txt")
HITS_FILE = os.path.join(RESULTS_DIR, "hits.txt")
ALL_RESULTS_FILE = os.path.join(RESULTS_DIR, "all_results.txt")
ETH_RPC = "https://rpc.ankr.com/eth"

def ensure_folders():
    if not os.path.exists(PHRASES_DIR):
        os.makedirs(PHRASES_DIR)
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
    if not os.path.exists(SEEDS_FILE):
        with open(SEEDS_FILE, "w") as f:
            f.write("# Put one seed phrase per line\n")
        print(f"Created {SEEDS_FILE} - please add your seed phrases and rerun the script.")
    if not os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, "w") as f:
            f.write("# Put one private key per line\n")
        print(f"Created {KEYS_FILE} - please add your private keys and rerun the script.")
    if (not os.path.exists(SEEDS_FILE)) or (not os.path.exists(KEYS_FILE)):
        exit(0)

def get_eth_address_from_seed(seed_phrase):
    try:
        acct = Account.from_mnemonic(seed_phrase)
        return acct.address
    except Exception:
        return None

def get_eth_address_from_key(private_key):
    try:
        acct = Account.from_key(private_key)
        return acct.address
    except Exception:
        return None

def get_eth_balance(address):
    try:
        w3 = Web3(Web3.HTTPProvider(ETH_RPC))
        bal_wei = w3.eth.get_balance(address)
        return Web3.from_wei(bal_wei, "ether")
    except Exception:
        return -1

def check_seed(seed):
    seed = seed.strip()
    if not seed or seed.startswith("#"):
        return None
    addr = get_eth_address_from_seed(seed)
    if not addr:
        return f"[INVALID] SEED: {seed}"
    balance = get_eth_balance(addr)
    if balance is None or balance < 0:
        return f"[ERROR] SEED: {seed} | {addr} | Unable to get balance"
    if balance > 0:
        return f"[HIT] SEED: {seed} | {addr} | Balance: {balance} ETH"
    else:
        return f"[EMPTY] SEED: {seed} | {addr} | Balance: {balance} ETH"

def check_key(key):
    key = key.strip()
    if not key or key.startswith("#"):
        return None
    addr = get_eth_address_from_key(key)
    if not addr:
        return f"[INVALID] KEY: {key}"
    balance = get_eth_balance(addr)
    if balance is None or balance < 0:
        return f"[ERROR] KEY: {key} | {addr} | Unable to get balance"
    if balance > 0:
        return f"[HIT] KEY: {key} | {addr} | Balance: {balance} ETH"
    else:
        return f"[EMPTY] KEY: {key} | {addr} | Balance: {balance} ETH"

def main():
    ensure_folders()
    with open(SEEDS_FILE, "r") as f:
        seeds = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    with open(KEYS_FILE, "r") as f:
        keys = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not seeds and not keys:
        print(f"No seed phrases or private keys found in {PHRASES_DIR}.")
        return

    hits = []
    all_results = []

    print(f"Checking {len(seeds)} seed phrases...")
    for seed in seeds:
        try:
            result = check_seed(seed)
            if result:
                all_results.append(result)
                if result.startswith("[HIT]"):
                    hits.append(result)
                print(result)
            time.sleep(1)
        except Exception as e:
            err = f"[ERROR] SEED: {seed} | Exception: {e}"
            all_results.append(err)
            print(err)

    print(f"Checking {len(keys)} private keys...")
    for key in keys:
        try:
            result = check_key(key)
            if result:
                all_results.append(result)
                if result.startswith("[HIT]"):
                    hits.append(result)
                print(result)
            time.sleep(1)
        except Exception as e:
            err = f"[ERROR] KEY: {key} | Exception: {e}"
            all_results.append(err)
            print(err)

    with open(ALL_RESULTS_FILE, "w") as f:
        f.write("\n".join(all_results))
    with open(HITS_FILE, "w") as f:
        f.write("\n".join(hits))

    print(f"Done. Results in '{RESULTS_DIR}' folder.")
    if hits:
        print(f"Found {len(hits)} hits! See {HITS_FILE}.")

if __name__ == "__main__":
    main()