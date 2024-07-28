lista = []
memory = 65536

form = 9
tipo = 'x'





with open("teste.hex", "w") as arquivo:
    for x in lista:
        arquivo.write(f'0{tipo}{x}\n')

print(f'\n\033[3;32mSuccess!\033[m\n')