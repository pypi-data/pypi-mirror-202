import os

ip = input("Digite o um IP ou Host: ")
os.system(f"ping -n 6 {ip}")
