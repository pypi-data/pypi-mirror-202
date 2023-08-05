import socket

def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e:
        print("FALHA NA CONEXAO")
        print(f"ERRO {e}")
        sys.exit()
    
    print("Socket criado com sucesso")
    host = 'localhost'
    porta = 5433
    menssagem = 'Cliente logado!!'
    try:
        print(f"Cliente: {menssagem}")
        s.sendto(menssagem.encode(), (host, porta))
        dados, servidor = s.recvfrom(4096)
        dados = dados.decode()
        print(f"cliente: {dados} ")
    finally:
        print(f"cliente: fechado a conexão")
        s.close()

if __name__ == "__main__":
    main()