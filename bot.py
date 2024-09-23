import requests
import time
from colorama import init, Fore, Style
import os
import datetime
import pytz

init(autoreset=True)

def debug_print(msg):
    print(f"[DEBUG] {msg}")

def print_welcome_message():
    print(r"""
          
█▀▀ █░█ ▄▀█ █░░ █ █▄▄ █ █▀▀
█▄█ █▀█ █▀█ █▄▄ █ █▄█ █ ██▄
          """)
    print(Fore.GREEN + Style.BRIGHT + "Seed BOT")
    print(Fore.GREEN + Style.BRIGHT + "Update Link: https://t.me/mitomchanel")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# URL endpoints
url_claim = 'https://elb.seeddao.org/api/v1/seed/claim'
url_balance = 'https://elb.seeddao.org/api/v1/profile/balance'
url_upgrade_storage = 'https://elb.seeddao.org/api/v1/seed/storage-size/upgrade'
url_upgrade_mining = 'https://elb.seeddao.org/api/v1/seed/mining-speed/upgrade'
url_upgrade_holy = 'https://elb.seeddao.org/api/v1/upgrades/holy-water'
url_get_profile = 'https://elb.seeddao.org/api/v1/profile'
url_check_worm = 'https://elb.seeddao.org/api/v1/worms'

headers = {
    'accept': 'application/json, text/plain, */*',
    'content-length': '0',
    'dnt': '1',
    'origin': 'https://cf.seeddao.org',
    'referer': 'https://cf.seeddao.org/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

def load_credentials():
    try:
        with open('query.txt', 'r') as file:
            tokens = file.read().strip().split('\n')
        debug_print(f"Loaded tokens: {tokens}")
        return tokens
    except FileNotFoundError:
        print("File tokens.txt tidak ditemukan.")
        return []
    except Exception as e:
        print("Terjadi kesalahan saat memuat token:", str(e))
        return []

def get_profile():
    response = requests.get(url_get_profile, headers=headers)
    debug_print(f"Get Profile Response: {response.status_code} - {response.text}")
    if response.status_code == 200:
        profile_data = response.json()
        name = profile_data['data']['name']
        debug_print(f"Profile retrieved: {name}")
        return profile_data
    else:
        print("Gagal mendapatkan data profil, status code:", response.status_code)
        return None

def check_balance():
    response = requests.get(url_balance, headers=headers)
    debug_print(f"Check Balance Response: {response.status_code} - {response.text}")
    if response.status_code == 200:
        balance_data = response.json()
        balance = balance_data['data'] / 1000000000
        debug_print(f"Balance retrieved: {balance}")
        return balance
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Balance ]: Gagal | {response.status_code}")
        return 0

def claim():
    response = requests.post(url_claim, headers=headers)
    debug_print(f"Claim Response: {response.status_code} - {response.text}")
    if response.status_code == 200:
        print(f"{Fore.GREEN+Style.BRIGHT}[ Claim ]: Claim berhasil")
    elif response.status_code == 400:
        print(f"{Fore.RED+Style.BRIGHT}[ Claim ]: Belum waktunya claim")
    else:
        print("Terjadi kesalahan saat klaim, status code:", response.status_code)

def check_worm():
    response = requests.get(url_check_worm, headers=headers)
    debug_print(f"Check Worm Response: {response.status_code} - {response.text}")
    if response.status_code == 200:
        worm_data = response.json().get('data', {})
        next_refresh = worm_data.get('next_refresh', 'Data next_refresh tidak tersedia.')
        is_caught = worm_data.get('is_caught', False)
        debug_print(f"Worm data: {worm_data}")

        if 'next_refresh' in worm_data:
            next_refresh_dt = datetime.datetime.fromisoformat(worm_data['next_refresh'][:-1] + '+00:00')
            now_utc = datetime.datetime.now(pytz.utc)
            time_diff_seconds = (next_refresh_dt - now_utc).total_seconds()
            hours = int(time_diff_seconds // 3600)
            minutes = int((time_diff_seconds % 3600) // 60)
            print(f"{Fore.GREEN+Style.BRIGHT}[ Worms ]: Next in {hours} jam {minutes} menit - Status: {'Caught' if is_caught else 'Available'}")
        else:
            print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: {next_refresh}")
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Gagal mendapatkan data worm, status code: {response.status_code}")

def main():
    print_welcome_message()
    tokens = load_credentials()

    confirm_storage = input("Auto upgrade storage? (y/n): ")
    confirm_mining = input("Auto upgrade mining? (y/n): ")
    confirm_holy = input("Auto upgrade holy? (y/n): ")

    while True:
        for index, token in enumerate(tokens):
            headers['telegram-data'] = token
            debug_print(f"Processing token {index + 1} with token: {token}")

            profile = get_profile()
            if profile:
                balance = check_balance()
                if balance > 0:
                    claim()
                else:
                    print(Fore.RED + Style.BRIGHT + "[ Klaim ]: Balance tidak cukup.")

                check_worm()

            time.sleep(20)  # Adjust the waiting time as needed
            clear_console()

if __name__ == "__main__":
    main()
    
