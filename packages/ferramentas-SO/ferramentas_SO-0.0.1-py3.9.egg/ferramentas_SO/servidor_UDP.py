import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Socket criado com sucesso")
host = 'localhost'
porta = 5433

s.bind((host, porta))
menssagem = 'Servidor: Ola Cliente logado!!'

while 1:
    dados, end = s.recvfrom(4096)
if dados:
    print("Servidor enviando menssagem...")
    s.sendto(dados + (menssagem.encode()), end)
    