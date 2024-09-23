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
url_worms = 'https://elb.seeddao.org/api/v1/worms'
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
    response = requests.get(url_worms, headers=headers)
    if response.status_code == 200:
        worm_data = response.json()['data']
        next_refresh = worm_data.get('next_refresh')
        is_caught = worm_data.get('is_caught')

        if next_refresh:
            next_refresh_dt = datetime.datetime.fromisoformat(next_refresh[:-1] + '+00:00')
            now_utc = datetime.datetime.now(pytz.utc)
            time_diff_seconds = (next_refresh_dt - now_utc).total_seconds()
            hours = int(time_diff_seconds // 3600)
            minutes = int((time_diff_seconds % 3600) // 60)
            print(f"{Fore.GREEN+Style.BRIGHT}[ Worms ]: Next in {hours} jam {minutes} menit - Status: {'Caught' if is_caught else 'Available'}")
        else:
            print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Data 'next_refresh' tidak tersedia.")
        
        return worm_data
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Gagal mendapatkan data worm.")
        return None

def catch_worm():
    worm_data = check_worm()
    if worm_data and not worm_data.get('is_caught'):
        response = requests.post('https://elb.seeddao.org/api/v1/worms/catch', headers=headers)
        if response.status_code == 200:
            print(f"{Fore.GREEN+Style.BRIGHT}[ Worms ]: Berhasil menangkap")
        elif response.status_code == 400:
            print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Sudah terangkap")
        elif response.status_code == 404:
            print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Worm tidak ditemukan")
        else:
            print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Gagal menangkap worm, status code:", response.status_code)
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Worm tidak tersedia atau sudah tertangkap.")

def get_profile():
    response = requests.get(url_get_profile, headers=headers)
    if response.status_code == 200:
        profile_data = response.json()
        name = profile_data['data']['name']
        print(f"{Fore.CYAN+Style.BRIGHT}============== [ Akun | {name} ] ==============")
        upgrades = {upgrade['upgrade_type']: upgrade['upgrade_level'] for upgrade in profile_data['data']['upgrades']}
        for upgrade_type, level in upgrades.items():
            print(f"{Fore.BLUE+Style.BRIGHT}[ {upgrade_type.capitalize()} Level ]: {level + 1}")
    else:
        print("Gagal mendapatkan data, status code:", response.status_code)

def check_balance():
    response = requests.get(url_balance, headers=headers)
    if response.status_code == 200:
        balance_data = response.json()
        print(f"{Fore.YELLOW+Style.BRIGHT}[ Balance ]: {balance_data['data'] / 1000000000}")
        return True
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Balance ]: Gagal | {response.status_code}")
        return False

def cekin_daily():
    response = requests.post(url_checkin, headers=headers)
    if response.status_code == 200:
        data = response.json()
        day = data.get('data', {}).get('no', '')
        print(f"{Fore.GREEN+Style.BRIGHT}[ Check-in ]: Check-in berhasil | Day {day}")
    else:
        data = response.json()
        if data.get('message') == 'already claimed for today':
            print(f"{Fore.RED+Style.BRIGHT}[ Check-in ]: Sudah dilakukan hari ini")
        else:
            print(f"{Fore.RED+Style.BRIGHT}[ Check-in ]: Gagal | {data}")

def upgrade(storage_confirm, mining_confirm, holy_confirm):
    upgrades = {
        'storage': (url_upgrade_storage, storage_confirm),
        'mining': (url_upgrade_mining, mining_confirm),
        'holy': (url_upgrade_holy, holy_confirm)
    }
    results = []
    for upgrade_type, (url, confirm) in upgrades.items():
        if confirm.lower() == 'y':
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                results.append(f'[ Upgrade {upgrade_type} ]: Berhasil')
            else:
                results.append(f'[ Upgrade {upgrade_type} ]: Balance tidak tercukupi')
    return results

def get_tasks():
    response = requests.get('https://elb.seeddao.org/api/v1/tasks/progresses', headers=headers)
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
    storage_confirm = input("Auto upgrade storage? (y/n): ")
    mining_confirm = input("Auto upgrade mining? (y/n): ")
    holy_confirm = input("Auto upgrade holy? (y/n): ")
    task_confirm = input("Auto Clear Task? (y/n): ")

    while True:
        for index, token in enumerate(tokens):
            headers['telegram-data'] = token
            get_profile()
            hasil_upgrade = upgrade(storage_confirm, mining_confirm, holy_confirm)

            for result in hasil_upgrade:
                print(result)
                time.sleep(1)

            if check_balance():
                response = requests.post(url_claim, headers=headers)
                if response.status_code == 200:
                    print(f"{Fore.GREEN+Style.BRIGHT}[ Claim ]: Claim berhasil")
                elif response.status_code == 400:
                    print(f"{Fore.RED+Style.BRIGHT}[ Claim ]: Belum waktunya claim")
                cekin_daily()
                catch_worm()
                if task_confirm.lower() == 'y':
                    get_tasks()
                    
                for i in range(30 * 60, 0, -1):  # 30 menit dalam detik
                        sys.stdout.write(f"\r{Fore.CYAN+Style.BRIGHT}============ Selesai, tunggu {i // 60} menit {i % 60} detik.. ============")
                        sys.stdout.flush()
                        time.sleep(1)
                        print()  # Cetak baris baru setelah hitungan mundur selesai
                        clear_console()

if __name__ == "__main__":
    main()
