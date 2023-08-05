import re
import json
from urllib.request import urlopen

url = 'https://ipinfo.io/json'
resposta = urlopen(url)
dados = json.load(resposta)
ip = dados['ip']
org = dados['org']
cid = dados['city']
pas = dados['country']
regiao = dados['region']

print('Daos do IP externo:')
print(f"IP: {ip} \nregiao: {regiao} \npais: {pas} \ncidade: {cid} \norg: {org}")

