import random, string

tamanho = int(input("Informe o tamanho de senhas"))

chars = string.ascii_letters + string.digits + '!@#$%&*_-+=/?'
rnd = random.SystemRandom()
print(''.join(rnd.choice(chars) for i in range(tamanho)))
