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
    print(Fore.GREEN + Style.BRIGHT + "https://t.me/mitomchanel")
    print(Fore.GREEN + Style.BRIGHT + "@mitomchanel")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

url_claim = 'https://elb.seeddao.org/api/v1/seed/claim'
url_balance = 'https://elb.seeddao.org/api/v1/profile/balance'
url_checkin = 'https://elb.seeddao.org/api/v1/login-bonuses'
url_upgrade_storage = 'https://elb.seeddao.org/api/v1/seed/storage-size/upgrade'
url_upgrade_mining = 'https://elb.seeddao.org/api/v1/seed/mining-speed/upgrade'
url_upgrade_holy = 'https://elb.seeddao.org/api/v1/upgrades/holy-water'
url_get_profile = 'https://elb.seeddao.org/api/v1/profile'
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
        print("File tokens.txt tidak ditemukan.")
        return []
    except Exception as e:
        print("Terjadi kesalahan saat memuat token:", str(e))
        return []

def get_profile():
    response = requests.get(url_get_profile, headers=headers)
    if response.status_code == 200:
        profile_data = response.json()
        name = profile_data['data']['name']
        print(f"{Fore.CYAN + Style.BRIGHT}============== [ Akun | {name} ] ==============")
        upgrades = {}
        for upgrade in profile_data['data']['upgrades']:
            upgrade_type = upgrade['upgrade_type']
            upgrade_level = upgrade['upgrade_level']
            upgrades[upgrade_type] = max(upgrades.get(upgrade_type, 0), upgrade_level)
        for upgrade_type, level in upgrades.items():
            print(f"{Fore.BLUE + Style.BRIGHT}[ {upgrade_type.capitalize()} Level ]: {level + 1}")
        return True
    else:
        print("Gagal mendapatkan data, status code:", response.status_code)
        return False

def check_balance():
    response = requests.get(url_balance, headers=headers)
    if response.status_code == 200:
        balance_data = response.json()
        print(f"{Fore.YELLOW + Style.BRIGHT}[ Balance ]: {balance_data['data'] / 1000000000}")
        return True
    else:
        print(f"{Fore.RED + Style.BRIGHT}[ Balance ]: Gagal |{response.status_code}")
        return False

def upgrade_item(item):
    url_map = {
        'storage': url_upgrade_storage,
        'mining': url_upgrade_mining,
        'holy': url_upgrade_holy
    }
    response = requests.post(url_map[item], headers=headers)
    print(f"Response untuk upgrade {item}: {response.status_code}, {response.text}")
    if response.status_code == 200:
        print(f"[ Upgrade {item} ]: Berhasil")
    else:
        print(f"[ Upgrade {item} ]: Gagal, balance tidak cukup atau kesalahan lain.")

def main():
    print_welcome_message()
    tokens = load_credentials()
    
    confirm_storage = input("Auto upgrade storage? (y/n): ")
    confirm_mining = input("Auto upgrade mining? (y/n): ")
    confirm_holy = input("Auto upgrade holy? (y/n): ")

    while True:
        for index, token in enumerate(tokens):
            headers['telegram-data'] = token
            print(f"Memproses untuk token ke {index + 1}")
            if get_profile():
                if confirm_storage.lower() == 'y':
                    upgrade_item('storage')
                    time.sleep(1)

                if confirm_mining.lower() == 'y':
                    upgrade_item('mining')
                    time.sleep(1)

                if confirm_holy.lower() == 'y':
                    upgrade_item('holy')
                    time.sleep(1)

                if check_balance():
                    response = requests.post(url_claim, headers=headers)
                    print(f"Response untuk claim: {response.status_code}, {response.text}")

                time.sleep(20)  # Tunggu 20 detik sebelum memproses token berikutnya
                clear_console()

if __name__ == "__main__":
    main()
