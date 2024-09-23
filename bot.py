import requests
import time
import sys
import os
from colorama import init, Fore, Style
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
url_task_progress = 'https://elb.seeddao.org/api/v1/tasks/progresses'

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
        worm_data = response.json()['data']
        next_refresh = worm_data['next_refresh']
        is_caught = worm_data['is_caught']
        
        next_refresh_dt = datetime.datetime.fromisoformat(next_refresh[:-1] + '+00:00')
        now_utc = datetime.datetime.now(pytz.utc)

        time_diff_seconds = (next_refresh_dt - now_utc).total_seconds()
        hours = int(time_diff_seconds // 3600)
        minutes = int((time_diff_seconds % 3600) // 60)

        print(f"{Fore.GREEN+Style.BRIGHT}[ Worms ]: Next in {hours} jam {minutes} menit - Status: {'Caught' if is_caught else 'Available'}")
        return worm_data
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Gagal mendapatkan data worm.")
        return None

def catch_worm():
    worm_data = check_worm()
    if worm_data and not worm_data['is_caught']:
        response = requests.post(f'{url_worms}/catch', headers=headers)
        if response.status_code == 200:
            print(f"{Fore.GREEN+Style.BRIGHT}[ Worms ]: Berhasil menangkap worm")
        else:
            print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Gagal menangkap worm, status code: {response.status_code}")
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Worm tidak tersedia atau sudah tertangkap.")

def get_profile():
    response = requests.get(url_get_profile, headers=headers)
    if response.status_code == 200:
        profile_data = response.json()['data']
        name = profile_data['name']
        print(f"{Fore.CYAN+Style.BRIGHT}============== [ Akun | {name} ] ==============")
        for upgrade in profile_data['upgrades']:
            print(f"{Fore.BLUE+Style.BRIGHT}[ {upgrade['upgrade_type'].capitalize()} Level ]: {upgrade['upgrade_level'] + 1}")
    else:
        print("Gagal mendapatkan data profil.")

def check_balance():
    response = requests.get(url_balance, headers=headers)
    if response.status_code == 200:
        balance_data = response.json()['data']
        print(f"{Fore.YELLOW+Style.BRIGHT}[ Balance ]: {balance_data / 1000000000}")
        return True
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Balance ]: Gagal, status code: {response.status_code}")
        return False

def upgrade_item(url, confirm_message):
    confirm = input(confirm_message)
    if confirm.lower() == 'y':
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            print(f"{Fore.GREEN+Style.BRIGHT}[ Upgrade ]: Berhasil")
        else:
            print(f"{Fore.RED+Style.BRIGHT}[ Upgrade ]: Gagal, balance tidak cukup")
    else:
        print(f"{Fore.YELLOW+Style.BRIGHT}[ Upgrade ]: Dibatalkan")

def cekin_daily():
    response = requests.post(url_checkin, headers=headers)
    if response.status_code == 200:
        print(f"{Fore.GREEN+Style.BRIGHT}[ Check-in ]: Berhasil")
    else:
        data = response.json()
        if data.get('message') == 'already claimed for today':
            print(f"{Fore.RED+Style.BRIGHT}[ Check-in ]: Sudah dilakukan hari ini")
        else:
            print(f"{Fore.RED+Style.BRIGHT}[ Check-in ]: Gagal")

def get_tasks():
    response = requests.get(url_task_progress, headers=headers)
    tasks = response.json()['data']
    for task in tasks:
        if task['task_user'] is None or not task['task_user']['completed']:
            complete_task(task['id'], task['name'])

def complete_task(task_id, task_name):
    response = requests.post(f'https://elb.seeddao.org/api/v1/tasks/{task_id}', headers=headers)
    if response.status_code == 200:
        print(f"{Fore.GREEN+Style.BRIGHT}[ Tasks ]: Tugas {task_name} selesai.")
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Tasks ]: Gagal menyelesaikan tugas {task_name}, status code: {response.status_code}")

def main():
    print_welcome_message()
    tokens = load_credentials()

    while True:
        upgrade_item(url_upgrade_storage, "Auto upgrade storage? (y/n): ")
        upgrade_item(url_upgrade_mining, "Auto upgrade mining? (y/n): ")
        upgrade_item(url_upgrade_holy, "Auto upgrade holy? (y/n): ")

        for token in tokens:
            headers['telegram-data'] = token
            get_profile()

            if check_balance():
                response = requests.post(url_claim, headers=headers)
                if response.status_code == 200:
                    print(f"{Fore.GREEN+Style.BRIGHT}[ Claim ]: Claim berhasil")
                else:
                    print(f"{Fore.RED+Style.BRIGHT}[ Claim ]: Gagal, status code: {response.status_code}")

                cekin_daily()
                catch_worm()
                if input("Auto clear tasks? (y/n): ").lower() == 'y':
                    get_tasks()

        for i in range(30, 0, -1):
            sys.stdout.write(f"\r{Fore.CYAN+Style.BRIGHT}============ Selesai, tunggu {i} detik.. ============")
            sys.stdout.flush()
            time.sleep(1)
        print()
        clear_console()

if __name__ == "__main__":
    main()   
