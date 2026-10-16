внутренний интерфейс со статическим IP

```yaml
network:
  version: 2
  ethernets:
    enp0s3:
      dhcp4: true
    enp0s8:
      addresses:
        - 10.10.10.1/24
      dhcp4: false
```

```bash
sudo sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward=1" | sudo tee /etc/sysctl.d/99-ipforward.conf
sudo sysctl --system

sudo iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE
sudo iptables -A FORWARD -i enp0s8 -o enp0s3 -j ACCEPT
sudo iptables -A FORWARD -i enp0s3 -o enp0s8 -m state --state RELATED,ESTABLISHED -j ACCEPT

sudo apt install -y iptables-persistent
sudo netfilter-persistent save
```
сеть в первой ВМ
```yaml
network:
  version: 2
  ethernets:
    enp0s3:
      addresses:
        - 10.10.10.10/24
      routes:
        - to: default
          via: 10.10.10.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 1.1.1.1
      dhcp4: false
```
<img width="1727" height="548" alt="image" src="https://github.com/user-attachments/assets/808d0b08-5514-46e5-98d7-4716f26bc89f" />
<img width="1007" height="404" alt="image" src="https://github.com/user-attachments/assets/4e7d3b91-2c4b-437f-a38a-81443af76246" />


