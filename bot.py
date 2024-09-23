import requests
import time
from colorama import init, Fore, Style
import sys
import os
import datetime
import pytz

init(autoreset=True)

def print_welcome_message():
    print(r"""
          
█▀▀ █░█ ▄▀█ █░░ █ █▄▄ █ █▀▀
█▄█ █▀█ █▀█ █▄▄ █ █▄█ █ ██▄
          """)
    print(Fore.GREEN + Style.BRIGHT + "Seed BOT")
    print(Fore.GREEN + Style.BRIGHT + "Update Link: https://t.me/mitomchanel")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# URL endpoint
url_claim = 'https://elb.seeddao.org/api/v1/seed/claim'
url_balance = 'https://elb.seeddao.org/api/v1/profile/balance'
url_checkin = 'https://elb.seeddao.org/api/v1/login-bonuses'
url_upgrade_storage = 'https://elb.seeddao.org/api/v1/seed/storage-size/upgrade'
url_upgrade_mining = 'https://elb.seeddao.org/api/v1/seed/mining-speed/upgrade'
url_upgrade_holy = 'https://elb.seeddao.org/api/v1/upgrades/holy-water'
url_get_profile = 'https://elb.seeddao.org/api/v1/profile'
url_check_worms = 'https://elb.seeddao.org/api/v1/worms'

# Headers yang diperlukan untuk request
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
    'content-length': '0',
    'dnt': '1',
    'origin': 'https://cf.seeddao.org',
    'priority': 'u=1, i',
    'referer': 'https://cf.seeddao.org/',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'telegram-data': 'tokens',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

def load_credentials():
    try:
        with open('query.txt', 'r') as file:
            tokens = file.read().strip().split('\n')
        return tokens
    except FileNotFoundError:
        print("File query.txt tidak ditemukan.")
        return []
    except Exception as e:
        print("Terjadi kesalahan saat memuat token:", str(e))
        return []

def check_balance():
    response = requests.get(url_balance, headers=headers)
    if response.status_code == 200:
        balance_data = response.json()
        balance = balance_data['data'] / 1000000000
        print(f"{Fore.YELLOW + Style.BRIGHT}[ Balance ]: {balance}")
        return balance
    else:
        print(f"{Fore.RED + Style.BRIGHT}[ Balance ]: Gagal |{response.status_code}")
        return 0  # Kembalikan 0 jika gagal

def get_profile():
    response = requests.get(url_get_profile, headers=headers)
    if response.status_code == 200:
        profile_data = response.json()
        name = profile_data['data']['name']
        print(f"{Fore.CYAN+Style.BRIGHT}============== [ Akun | {name} ] ==============")

        upgrades = {}
        for upgrade in profile_data['data']['upgrades']:
            upgrade_type = upgrade['upgrade_type']
            upgrade_level = upgrade['upgrade_level']
            if upgrade_type in upgrades:
                if upgrade_level > upgrades[upgrade_type]:
                    upgrades[upgrade_type] = upgrade_level
            else:
                upgrades[upgrade_type] = upgrade_level

        for upgrade_type, level in upgrades.items():
            print(f"{Fore.BLUE+Style.BRIGHT}[ {upgrade_type.capitalize()} Level ]: {level + 1}")
    else:
        print("Gagal mendapatkan data, status code:", response.status_code)
        return None

def claim():
    response = requests.post(url_claim, headers=headers)
    print(f"Response untuk claim: {response.status_code}, {response.text}")
    if response.status_code == 200:
        print(f"{Fore.GREEN + Style.BRIGHT}[ Klaim ]: Klaim berhasil")
    else:
        print(Fore.RED + Style.BRIGHT + f"[ Klaim ]: Gagal | {response.json()}")

def check_worm():
    response = requests.get(url_check_worms, headers=headers)
    if response.status_code == 200:
        worm_data = response.json()['data']
        next_refresh = worm_data.get('next_refresh')
        if next_refresh:
            is_caught = worm_data['is_caught']
            next_refresh_dt = datetime.datetime.fromisoformat(next_refresh[:-1] + '+00:00')
            now_utc = datetime.datetime.now(pytz.utc)
            time_diff_seconds = (next_refresh_dt - now_utc).total_seconds()
            hours = int(time_diff_seconds // 3600)
            minutes = int((time_diff_seconds % 3600) // 60)

            print(f"{Fore.GREEN + Style.BRIGHT}[ Worms ]: Next in {hours} jam {minutes} menit - Status: {'Caught' if is_caught else 'Available'}")
        else:
            print(f"{Fore.RED + Style.BRIGHT}[ Worms ]: Data next_refresh tidak tersedia.")
    else:
        print(f"{Fore.RED + Style.BRIGHT}[ Worms ]: Gagal mendapatkan data worm.")

def main():
    print_welcome_message()
    tokens = load_credentials()

    confirm_storage = input("Auto upgrade storage? (y/n): ")
    confirm_mining = input("Auto upgrade mining? (y/n): ")
    confirm_holy = input("Auto upgrade holy? (y/n): ")

    while True:
        for index, token in enumerate(tokens):
            headers['telegram-data'] = token
            info = get_profile()
            if info:
                print(f"Memproses untuk token ke {index + 1}")

                if check_balance() > 0:
                    claim()
                else:
                    print(Fore.RED + Style.BRIGHT + "[ Klaim ]: Balance tidak cukup.")

                check_worm()

            time.sleep(20)  # Menunggu 20 detik sebelum memproses token berikutnya
            clear_console()

if __name__ == "__main__":
    main()
                
