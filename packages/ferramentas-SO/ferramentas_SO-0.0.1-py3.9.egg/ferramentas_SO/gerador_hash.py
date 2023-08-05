import hashlib

palav = input("Escreva: ")
menu = int(input('''
                1 - MD5
                2 - SH1
                3 - SHA256
                4 - SHA512
                Digite a opcao de hash:
'''))
if menu == 1:
    hash1 = hashlib.md5(palav.encode('utf-8'))
    print(hash1.hexdigest())
elif menu == 2:
    hash1 = hashlib.sha1(palav.encode('utf-8'))
    print(hash1.hexdigest())
elif menu == 3:
    hash1 = hashlib.sha256(palav.encode('utf-8'))
    print(hash1.hexdigest())
elif menu == 4:
    hash1 = hashlib.sha512(palav.encode('utf-8'))
    print(hash1.hexdigest())
else:
    print("opcao incorreta")
    