'''
Wordlist são arquivos contendo uma palavra por linha. São utilizados em ataques 
de força bruta como quebra de autenticação de senhas e logins. 
'''
import itertools

string = input('palavra a ser permutada: ')
result = itertools.permutations(string, len(string))
for i in result:
    print(''.join(i))
