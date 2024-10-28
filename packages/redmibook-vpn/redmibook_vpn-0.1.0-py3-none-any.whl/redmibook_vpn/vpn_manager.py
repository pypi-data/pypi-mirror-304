import subprocess
def check_vpn_status(vpn_name):
    try:
        # Проверяем активные подключения
        result = subprocess.run(['nmcli', 'con', 'show', '--active'], capture_output=True, text=True, check=True)
        active_connections = result.stdout
        active_connections = [x.split() for x in active_connections.split('\n')][1:]
        active_connections = [x for x in active_connections if x and (x[2] == 'vpn')]
        
        # Проверяем, подключен ли VPN по имени
        return vpn_name in [i[0] for i in active_connections]
    
    except subprocess.CalledProcessError as e:
        print("Ошибка при проверке состояния VPN:", e.stderr)

def connect_vpn(vpn_name):
    # Подключаемся к VPN через nmcli
    try:
        result = subprocess.run(['nmcli', 'con', 'up', vpn_name], check=True, capture_output=True, text=True)
        print("VPN подключен:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Ошибка подключения к VPN:", e.stderr)

def disconnect_vpn(vpn_name):
    # Отключаемся от VPN через nmcli
    try:
        result = subprocess.run(['nmcli', 'con', 'down', vpn_name], check=True, capture_output=True, text=True)
        print("VPN отключен:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Ошибка отключения от VPN:", e.stderr)