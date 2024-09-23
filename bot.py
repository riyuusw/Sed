import requests
import time
from colorama import init, Fore, Style
import sys
import os
import datetime
import pytz

init(autoreset=True)

# URL endpoint
url_claim = 'https://elb.seeddao.org/api/v1/seed/claim'
url_balance = 'https://elb.seeddao.org/api/v1/profile/balance'
url_checkin = 'https://elb.seeddao.org/api/v1/login-bonuses'
url_upgrade_storage = 'https://elb.seeddao.org/api/v1/seed/storage-size/upgrade'
url_upgrade_mining = 'https://elb.seeddao.org/api/v1/seed/mining-speed/upgrade'
url_upgrade_holy = 'https://elb.seeddao.org/api/v1/upgrades/holy-water'
url_get_profile = 'https://elb.seeddao.org/api/v1/profile'
url_worms = 'https://elb.seeddao.org/api/v1/worms'

# Headers yang diperlukan untuk request
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
    'dnt': '1',
    'origin': 'https://cf.seeddao.org',
    'referer': 'https://cf.seeddao.org/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

def print_welcome_message():
    print(r"""
          
█▀▀ █░█ ▄▀█ █░░ █ █▄▄ █ █▀▀
█▄█ █▀█ █▀█ █▄▄ █ █▄█ █ ██▄
          """)
    print(Fore.GREEN + Style.BRIGHT + "Seed BOT")
    print(Fore.GREEN + Style.BRIGHT + "Update Link: https://t.me/mitomchanel")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

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

def check_worm():
    response = requests.get(url_worms, headers=headers)
    if response.status_code == 200:
        worm_data = response.json().get('data', {})
        next_refresh = worm_data.get('next_refresh')
        is_caught = worm_data.get('is_caught', False)

        if next_refresh:
            next_refresh_dt = datetime.datetime.fromisoformat(next_refresh[:-1] + '+00:00')
            now_utc = datetime.datetime.now(pytz.utc)
            time_diff_seconds = (next_refresh_dt - now_utc).total_seconds()
            hours = int(time_diff_seconds // 3600)
            minutes = int((time_diff_seconds % 3600) // 60)
            print(f"{Fore.GREEN+Style.BRIGHT}[ Worms ]: Next in {hours} jam {minutes} menit - Status: {'Caught' if is_caught else 'Available'}")
        else:
            print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Data next_refresh tidak tersedia.")
        return worm_data
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Gagal mendapatkan data worm, status code: {response.status_code}")
        return None

def catch_worm():
    worm_data = check_worm()
    if worm_data and not worm_data.get('is_caught', False):
        response = requests.post('https://elb.seeddao.org/api/v1/worms/catch', headers=headers)
        if response.status_code == 200:
            print(f"{Fore.GREEN+Style.BRIGHT}[ Worms ]: Berhasil menangkap")
        else:
            print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Gagal menangkap worm, status code:", response.status_code)
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Worm tidak tersedia atau sudah tertangkap.")

def upgrade_item(item_type):
    upgrade_urls = {
        'storage': url_upgrade_storage,
        'mining': url_upgrade_mining,
        'holy': url_upgrade_holy
    }
    
    if item_type not in upgrade_urls:
        print(f"{Fore.RED+Style.BRIGHT}[ Upgrade ]: Jenis upgrade tidak dikenal.")
        return
    
    response = requests.post(upgrade_urls[item_type], headers=headers)
    if response.status_code == 200:
        print(f"{Fore.GREEN+Style.BRIGHT}[ Upgrade ]: Berhasil melakukan upgrade {item_type}.")
    elif response.status_code == 400:
        print(f"{Fore.RED+Style.BRIGHT}[ Upgrade ]: Gagal, balance tidak cukup untuk upgrade {item_type}.")
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Upgrade ]: Gagal melakukan upgrade {item_type}, status code: {response.status_code}")

def get_profile():
    response = requests.get(url_get_profile, headers=headers)
    if response.status_code == 200:
        profile_data = response.json().get('data', {})
        name = profile_data.get('name', 'Tidak diketahui')
        print(f"{Fore.CYAN+Style.BRIGHT}============== [ Akun | {name} ] ==============")

        upgrades = {}
        for upgrade in profile_data.get('upgrades', []):
            upgrade_type = upgrade.get('upgrade_type')
            upgrade_level = upgrade.get('upgrade_level')
            upgrades[upgrade_type] = max(upgrades.get(upgrade_type, 0), upgrade_level)

        for upgrade_type, level in upgrades.items():
            print(f"{Fore.BLUE+Style.BRIGHT}[ {upgrade_type.capitalize()} Level ]: {level + 1}")
        return True
    else:
        print("Gagal mendapatkan data, status code:", response.status_code)
        return False

def check_balance():
    response = requests.get(url_balance, headers=headers)
    if response.status_code == 200:
        balance_data = response.json().get('data', 0)
        print(f"{Fore.YELLOW+Style.BRIGHT}[ Balance ]: {balance_data / 1000000000}")
        return True
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Balance ]: Gagal | {response.status_code}")
        return False

def cekin_daily():
    response = requests.post(url_checkin, headers=headers)
    if response.status_code == 200:
        data = response.json().get('data', {})
        day = data.get('no', '')
        print(f"{Fore.GREEN+Style.BRIGHT}[ Check-in ]: Check-in berhasil | Day {day}")
    else:
        data = response.json()
        message = data.get('message', 'Gagal melakukan check-in.')
        print(f"{Fore.RED+Style.BRIGHT}[ Check-in ]: {message}")

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
                    if response.status_code == 200:
                        print(f"{Fore.GREEN+Style.BRIGHT}[ Claim ]: Claim berhasil")
                    else:
                        print(f"{Fore.RED+Style.BRIGHT}[ Claim ]: Gagal, status code: {response.status_code}")

                    cekin_daily()
                    catch_worm()

        for i in range(30, 0, -1):
            sys.stdout.write(f"\r{Fore.CYAN+Style.BRIGHT}============ Selesai, tunggu {i} detik.. ============")
            sys.stdout.flush()
            time.sleep(1)
        print()
        clear_console()

if __name__ == "__main__":
    main()
    
