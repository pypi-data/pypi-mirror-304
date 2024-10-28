### Установка 
```bash
pip3 install redmibook_vpn
```
### Создание сервиса

```bash
cd /etc/systemd/system
```
создаем redmivpn.service
```bash
[Unit]
Description=vpn button
[Service]
User=root
WorkingDirectory=/
ExecStart=python3 -m redmibook_vpn --vpn_name <NAME>
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```
инициализируем

```bash
sudo systemctl daemon-reload
```
```bash
sudo systemctl start redmivpn.service
```
```bash
sudo systemctl enable redmivpn.service
```