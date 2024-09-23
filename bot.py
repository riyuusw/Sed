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
        print("File tokens.txt tidak ditemukan.")
        return []
    except Exception as e:
        print("Terjadi kesalahan saat memuat token:", str(e))
        return []

def check_worm():
    try:
        response = requests.get('https://elb.seeddao.org/api/v1/worms', headers=headers)
        if response.status_code == 200:
            worm_data = response.json().get('data', {})

            next_refresh = worm_data.get('next_refresh')
            is_caught = worm_data.get('is_caught')

            if next_refresh is None or is_caught is None:
                print(f"{Fore.RED}[Error]: 'next_refresh' atau 'is_caught' tidak ditemukan.")
                return None

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
    except Exception as e:
        print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Terjadi kesalahan - {str(e)}")
        return None

def catch_worm():
    worm_data = check_worm()
    if worm_data and not worm_data['is_caught']:
        response = requests.post('https://elb.seeddao.org/api/v1/worms/catch', headers=headers)
        if response.status_code == 200:
            print(f"{Fore.GREEN+Style.BRIGHT}[ Worms ]: Berhasil menangkap worm")
        elif response.status_code == 400:
            print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Worm sudah tertangkap")
        elif response.status_code == 404:
            print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Worm tidak ditemukan")
        else:
            print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Gagal menangkap worm, status code:", response.status_code)
    else:
        print(f"{Fore.RED+Style.BRIGHT}[ Worms ]: Worm tidak tersedia atau sudah tertangkap.")

def main():
    print_welcome_message()
    tokens = load_credentials()

    confirm_storage = input("Auto upgrade storage? (y/n): ")
    confirm_mining = input("Auto upgrade mining? (y/n): ")
    confirm_holy = input("Auto upgrade holy? (y/n): ")
    confirm_task = input("Auto Clear Task? (y/n): ")

    while True:
        for index, token in enumerate(tokens):
            headers['telegram-data'] = token
            print(f"Memproses token {index+1}...")

            # Upgrade otomatis berdasarkan konfirmasi awal
            if confirm_storage.lower() == 'y':
                print(upgrade_storage(confirm_storage))
            if confirm_mining.lower() == 'y':
                print(upgrade_mining(confirm_mining))
            if confirm_holy.lower() == 'y':
                print(upgrade_holy(confirm_holy))

            # Cek balance
            if check_balance():
                # Lakukan claim dan daily check-in
                cekin_daily()
                catch_worm()
                if confirm_task.lower() == 'y':
                    get_tasks()

        # Timer sebelum loop berikutnya
        for i in range(30, 0, -1):
            sys.stdout.write(f"\r{Fore.CYAN+Style.BRIGHT}============ Selesai, tunggu {i} detik.. ============")
            sys.stdout.flush()
            time.sleep(1)
        clear_console()

if __name__ == "__main__":
    main()
