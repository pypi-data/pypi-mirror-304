from .vpn_manager import connect_vpn, disconnect_vpn, check_vpn_status
import argparse
import evdev
from datetime import datetime, timedelta

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--vpn_name', type=str)
    args = parser.parse_args()

    vpn_name = args.vpn_name
    last_update = datetime.now()
    for event in evdev.InputDevice('/dev/input/event2').read_loop():
        if event.value == 114 and event.code == 4 and event.type == 4: 
            if datetime.now() - last_update < timedelta(seconds=1):
                continue
            status = check_vpn_status(vpn_name=vpn_name)
            if status:
                disconnect_vpn(vpn_name=vpn_name)
            else:
                connect_vpn(vpn_name=vpn_name)
            last_update = datetime.now()

if __name__ == "__main__":
    main()