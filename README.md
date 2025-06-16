# Wallet Checker Tool

This is a simple Python tool for checking Ethereum seed phrases and private keys for balances.  
It will output the results to the `results/` folder, highlighting any accounts ("hits") with a positive balance.

---

## Features

- Checks Ethereum addresses generated from seed phrases (BIP39 mnemonics, first account).
- Checks Ethereum addresses from private keys.
- Saves all results and "hits" (wallets with a positive ETH balance) to the `results/` folder.
- Organizes your input files in a `phrases/` folder for safety and clarity.

---

## Usage

### 1. Install Requirements

```bash
pip install web3 mnemonic requests
```

### 2. Run the Script

```bash
python wallet_checker.py
```

- On the first run, it will create:
  - `phrases/seeds.txt` — add one seed phrase per line.
  - `phrases/private_keys.txt` — add one private key per line.

### 3. Add Your Data

- Edit the above files and add your seed phrases and/or private keys (one per line, no quotes).

### 4. Run the Script Again

- The script will check each seed/private key for ETH balance:
  - Results are saved to `results/all_results.txt`
  - Hits (addresses with balance > 0) are saved to `results/hits.txt`

---

## Output

- **results/hits.txt** — All seeds/keys with a positive ETH balance.
- **results/all_results.txt** — All checked seeds/keys and their balance status.

---

## File Structure

```
wallet_checker.py
phrases/
  seeds.txt
  private_keys.txt
results/
  hits.txt
  all_results.txt
```

---

## Notes

- Only the first derived Ethereum address from a seed phrase is checked.
- This tool does not check other coins by default—let us know if you want multi-coin support.
- For best safety, do not use this tool with any private keys or seeds you actually use—**for research and recovery only**.

---

## Disclaimer

This tool is for educational and research purposes only.  
**Never use real, active wallet seeds or private keys with this script.**
