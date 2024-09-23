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

# URL endpoint
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

def check_worm():
    response = requests.get('https://elb.seeddao.org/api/v1/worms', headers=headers)
    if response.status_code == 200:
        worm_data = response.json()['data']
        next_refresh = worm_data.get('next_refresh')
        is_caught = worm_data['is_caught']

        if next_refresh:
            next_refresh_dt = datetime.datetime.fromisoformat(next_refresh[:-1] + '+00:00')
            now_utc = datetime.datetime.now(pytz.utc)
            time_diff_seconds = (next_refresh_dt - now_utc).total_seconds()
            hours = int(time_diff_seconds // 3600)
            minutes = int((time_diff_seconds % 3600) // 60)
            print(f"{Fore.GREEN + Style.BRIGHT}[ Worms ]: Next in {hours} jam {minutes} menit - Status: {'Caught' if is_caught else 'Available'}")
        else:
            print(f"{Fore.RED + Style.BRIGHT}[ Worms ]: Data next_refresh tidak tersedia.")
        
        return worm_data
    else:
        print(f"{Fore.RED + Style.BRIGHT}[ Worms ]: Gagal mendapatkan data worm.")
        return None

def catch_worm():
    worm_data = check_worm()
    if worm_data and not worm_data['is_caught']:
        response = requests.post('https://elb.seeddao.org/api/v1/worms/catch', headers=headers)
        if response.status_code == 200:
            print(f"{Fore.GREEN + Style.BRIGHT}[ Worms ]: Berhasil menangkap")
        elif response.status_code == 400:
            print(f"{Fore.RED + Style.BRIGHT}[ Worms ]: Sudah tertangkap")
        elif response.status_code == 404:
            print(f"{Fore.RED + Style.BRIGHT}[ Worms ]: Worm tidak ditemukan")
        else:
            print(f"{Fore.RED + Style.BRIGHT}[ Worms ]: Gagal menangkap worm, status code:", response)
    else:
        print(f"{Fore.RED + Style.BRIGHT}[ Worms ]: Worm tidak tersedia atau sudah tertangkap.")

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
            if upgrade_type in upgrades:
                if upgrade_level > upgrades[upgrade_type]:
                    upgrades[upgrade_type] = upgrade_level
            else:
                upgrades[upgrade_type] = upgrade_level
        for upgrade_type, level in upgrades.items():
            print(f"{Fore.BLUE + Style.BRIGHT}[ {upgrade_type.capitalize()} Level ]: {level + 1}")
    else:
        print("Gagal mendapatkan data, status code:", response.status_code)
        return None

def check_balance():
    response = requests.get(url_balance, headers=headers)
    if response.status_code == 200:
        balance_data = response.json()
        print(f"{Fore.YELLOW + Style.BRIGHT}[ Balance ]: {balance_data['data'] / 1000000000}")
        return True
    else:
        print(f"{Fore.RED + Style.BRIGHT}[ Balance ]: Gagal |{response.status_code}")
        return False

def cekin_daily():
    response = requests.post(url_checkin, headers=headers)
    if response.status_code == 200:
        data = response.json()
        day = data.get('data', {}).get('no', '')
        print(f"{Fore.GREEN + Style.BRIGHT}[ Check-in ]: Check-in berhasil | Day {day}")
    else:
        data = response.json()
        if data.get('message') == 'already claimed for today':
            print(f"{Fore.RED + Style.BRIGHT}[ Check-in ]: Sudah dilakukan hari ini")
        else:
            print(f"{Fore.RED + Style.BRIGHT}[ Check-in ]: Gagal | {data}")

def upgrade_item(item):
    url_map = {
        'storage': url_upgrade_storage,
        'mining': url_upgrade_mining,
        'holy': url_upgrade_holy
    }
    confirm = input(f"Apakah Anda ingin melakukan upgrade {item}? (y/n): ")
    if confirm.lower() == 'y':
        response = requests.post(url_map[item], headers=headers)
        if response.status_code == 200:
            print(f"[ Upgrade {item} ]: Berhasil")
        else:
            print(f"[ Upgrade {item} ]: Gagal, balance tidak cukup.")

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
                        print(f"{Fore.GREEN + Style.BRIGHT}[ Claim ]: Claim berhasil")
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}[ Claim ]: Gagal, status code: {response.status_code}")

                    cekin_daily()
                    
                worm_data = check_worm()
                if worm_data:
                    next_refresh = worm_data.get('next_refresh')
                    if next_refresh:
                        next_refresh_dt = datetime.datetime.fromisoformat(next_refresh[:-1] + '+00:00')
                        now_utc = datetime.datetime.now(pytz.utc)
                        time_diff_seconds = (next_refresh_dt - now_utc).total_seconds()
                        wait_time = max(0, int(time_diff_seconds))
                        print(f"{Fore.CYAN + Style.BRIGHT}Menunggu hingga worm tersedia dalam {wait_time} detik.")
                    else:
                        wait_time = 20  # Fallback jika tidak ada next_refresh
                else:
                    wait_time = 20  # Default wait time jika gagal mendapatkan data worm

                for i in range(wait_time, 0, -1):
                    sys.stdout.write(f"\r{Fore.CYAN + Style.BRIGHT}============ Selesai, tunggu {i} detik.. ============")
                    sys.stdout.flush()
                    time.sleep(1)
                print()
                clear_console()

if __name__ == "__main__":
    main()
                    
