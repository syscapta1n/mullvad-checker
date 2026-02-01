smert@smert:~/Pictures$ cat checker.py 
import subprocess
import re
import time
from datetime import datetime

INPUT_FILE = "list.txt"
VALID_FILE = "valid.txt"
TIMEOUT_LIMIT = 10
DELAY = 2 

def calculate_days_left(date_str):
    """Считает разницу между датой истечения и сегодняшним днем"""
    try:
        expiry_date = datetime.strptime(date_str.strip(), "%Y-%m-%d")
        today = datetime.now()
        delta = expiry_date - today
        return delta.days
    except Exception:
        return None

def run_mullvad_cmd(args):
    """Запускает команду Mullvad с ограничением по времени"""
    try:
        proc = subprocess.run(
            ['mullvad'] + args,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_LIMIT
        )
        return proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return "TIMEOUT", ""
    except Exception as e:
        return f"ERROR: {e}", ""

def check_mullvad():
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            accounts = list(set(re.findall(r'(?<!\d)\d{16}(?!\d)', content)))
    except FileNotFoundError:
        print(f"[-] Файл {INPUT_FILE} не найден!")
        return

    print(f"[*] Загружено уникальных ID: {len(accounts)}")
    print("[*] Начинаю проверку...\n")

    for acc in accounts:
        print(f"--> ID: {acc} |", end=" ", flush=True)

        out, err = run_mullvad_cmd(['account', 'login', acc])
        
        if out == "TIMEOUT":
            print("\033[93mПРОПУЩЕНО (Тайм-аут 10с)\033[0m")
            continue

        status_out, _ = run_mullvad_cmd(['account', 'get'])
        
        if "Expiration:" in status_out:
            date_match = re.search(r'Expiration: (\d{4}-\d{2}-\d{2})', status_out)
            
            if date_match:
                date_str = date_match.group(1)
                days_left = calculate_days_left(date_str)
                
                if days_left is not None and days_left > 0:
                    result = f"VALID | Осталось дней: {days_left} (до {date_str})"
                    print(f"\033[92m{result}\033[0m")
                    
                    # Сохраняем результат
                    with open(VALID_FILE, 'a', encoding='utf-8') as f:
                        f.write(f"{acc} | {days_left} days | {date_str}\n")
                else:
                    print(f"\033[91mEXPIRED (Истекло {date_str})\033[0m")
            else:
                print("\033[93mACTIVE (Дата не определена)\033[0m")
        else:
            print("\033[91mINVALID\033[0m")

        run_mullvad_cmd(['account', 'logout'])
        
        time.sleep(DELAY)

    print(f"\n[!] Проверка завершена. Результаты: {VALID_FILE}")

if __name__ == "__main__":
    check_mullvad()
