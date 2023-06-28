import os
import requests
from bitcoin import *
from eth_utils import encode_hex, keccak
from colorama import Fore, Style

# Create a directory to store the wallets
directory = 'bitcoin_wallets'
os.makedirs(directory, exist_ok=True)

# Generate wallets infinitely
wallet_counter = 0

while True:
    # Generate a new Bitcoin private key
    private_key = random_key()

    # Derive the corresponding Bitcoin address from the private key
    public_key = privtopub(private_key)
    bitcoin_address = pubtoaddr(public_key)

    # Derive the corresponding ETH address from the private key
    private_key_bytes = bytes.fromhex(private_key)
    eth_address_bytes = keccak(private_key_bytes[1:])[-20:]
    eth_address = encode_hex(eth_address_bytes)


    # Derive the corresponding BCH address from the private key
    bch_address = privtoaddr(private_key, magicbyte=0)  # BCH address has magic byte 0

    # Rest of the code...


    # Derive the corresponding BCH address from the private key
    bch_address = privtoaddr(private_key, magicbyte=0)  # BCH address has magic byte 0

    # Get the balance of the Bitcoin address
    response_bitcoin = requests.get(f'https://blockchain.info/q/addressbalance/{bitcoin_address}')
    balance_bitcoin = int(response_bitcoin.text) if response_bitcoin.status_code == 200 else 0

    # Get the balance of the ETH address
    url_eth = f'https://api.etherscan.io/api?module=account&action=balance&address={eth_address}&tag=latest'
    response_eth = requests.get(url_eth)
    response_eth_data = response_eth.json()
    balance_eth = (
        int(response_eth_data['result']) / 1e18
        if 'result' in response_eth_data and response_eth_data['result'].isdigit()
        else 0
    )

    # Get the balance of the BCH address
    url_bch = f'https://api.blockchair.com/bitcoin-cash/dashboards/address/{bch_address}'
    response_bch = requests.get(url_bch)
    balance_bch = response_bch.json()['data'][bch_address]['address']['balance'] if response_bch.status_code == 200 else 0

    # Check if any of the balances are non-zero
    if balance_bitcoin > 0 or balance_eth > 0 or balance_bch > 0:
        # Create a filename for the wallet and store the private key, addresses, and balances in a text file
        filename = f'{directory}/wallet_{bitcoin_address}.txt'
        with open(filename, 'w') as file:
            file.write(f'Private Key: {private_key}\n')
            file.write(f'Bitcoin Address: {bitcoin_address}\n')
            file.write(f'ETH Address: {eth_address}\n')
            file.write(f'BCH Address: {bch_address}\n')
            file.write(f'Balance (Bitcoin): {balance_bitcoin} satoshis\n')
            file.write(f'Balance (ETH): {balance_eth} ETH\n')
            file.write(f'Balance (BCH): {balance_bch} BCH\n')
        wallet_counter += 1

    # Define color codes based on the balance
    balance_color = Fore.GREEN if balance_bitcoin > 0 or balance_eth > 0 or balance_bch > 0 else Fore.RED

    print(f'Total wallets saved: {wallet_counter}')
    print(f'{balance_color}Wallet generated')
    print(f'Bitcoin Address: {bitcoin_address}')
    print(f'ETH Address: {eth_address}')
    print(f'BCH Address: {bch_address}')
    print(f'Balance (Bitcoin): {balance_bitcoin} satoshis')
    print(f'Balance (ETH): {balance_eth} ETH')
    print(f'Balance (BCH): {balance_bch} BCH\n')
    print(Style.RESET_ALL)
