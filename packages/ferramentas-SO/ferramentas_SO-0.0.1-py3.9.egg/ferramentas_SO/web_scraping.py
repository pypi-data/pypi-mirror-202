'''
traz uma pagina de um site inteiro em HTML. 
'''
#from bs4 import BeautifulSoup
import bs4
import requests

site = requests.get("https://www.climatempo.com.br/").content
soup = bs4.BeautifulSoup(site, 'html.parser')
print(soup.prettify())
print(soup.a)
