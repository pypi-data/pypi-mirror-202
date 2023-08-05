import ctypes

atributo_ocultar = 0x02
returno = ctypes.windll.kernel32.SetFileAttributesW('ocultar.txt')
if returno:
    print('Arquivo oi ocultado')
else:
    print('Arquivo nao foi ocultado')
    