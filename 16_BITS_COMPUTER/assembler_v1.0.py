''' Transferindo da EEPROM pra RAM:
0000: JMP (xxyy)
0001: xx = ff
0002: yy = e9
|
|               <- ESPAÇO LIVRE PARA O PROGRAMA (addr: 0003~ffe8)
|
ffe9: DCL (xxyy)
ffea: xx
ffeb: yy
ffec: JPZ (xxyy)
ffed: xx = ff
ffee: yy = f4
ffef: SFT
fff0: DCS
fff1: JM  (xxyy)
fff2: xx = ff
fff3: yy = ec
fff4: MVI A (zz)
fff5: zz = 00
fff6: STA (xxyy)
fff7: xx = 00
fff8: yy = 02
fff9: STA (xxyy)
fffa: xx = 00
fffb: yy = 01
fffc: STA (xxyy)
fffd: xx = 00
fffe: yy = 00
ffff: HLT
---- '''

### O transferidor utilzia 26 endereços da memória, logo livre para o programa será = total - 26

# Definindo endereços da memória:
memory = 65536
exe = []
livre = memory


if livre < 0:
    print(f'\033[31m\nMemória abaixo do mínimo esperado\n\033[m')
    raise MemoryError

# Definindo palavras da memória:
bits = 2
form = 'x'

# Iniciando slots da memória:
for addr in range(memory):
    exe.append(f'{0:0{bits}{form}}')

# Adicionando tranferência do APP da EEPROM para a RAM:
starter = (0x07, 0xff, 0xe9)
index = 0
for value in starter:
    exe[index] = f'{value:0{bits}{form}}'
    index += 1
    livre -= 1

finsher = (0x03, 0x00, 0x30, 0x02, 0xff, 0xf4, 0x04, 0x05, 0x07, 0xff, 0xec, 0x0b, 0x00, 0x0c, 0x00, 0x02, 0x0c, 0x00, 0x01, 0x0c, 0x00, 0x00, 0x06)
index = memory - 23
for value in finsher:
    exe[index] = f'{value:0{bits}{form}}'
    livre -= 1
    index += 1
'''
23 É o número de etapas do finalizador, logo o index sempre
irá apontar para começar 23 endereços antes do fim da memória
'''

assembly = '''
    !x,
    !y,
    !z,

    MVI_A #01,
    STA   $!y,
    MVI_A #00,
    STA   $!x,

    JPC   $002b,
        OUT   $!x,

        INR_A $!x,
        ADD_B $!y,
        STA   $!z,

        INR_A $!y,
        STA   $!x,

        INR_A $!z,
        STA   $!y,

        JM    $000d,

    JM   $0003,
'''


commands = {
    'NOP':   0X00,
    'ADD_B': 0x01,
    'JPZ':   0x02,
    'DCL':   0x03,
    'SFT':   0x04,
    'DCS':   0x05,
    'HLT':   0x06,
    'JM':    0x07,
    'JPC':   0x08,
    'OUT':   0x09,
    'INR_A': 0x0a,
    'MVI_A': 0x0b,
    'STA':   0x0c,
}


def compilar(code: str):
    app = []
    variables = []
    code = code.replace(' ', '')
    code = code.replace('\n', '')
    code = code.upper()
    lista = code.split(',')
    errors = 0

    # Lógica de compilação:
    for item in lista:
        addrs = item.find('$')
        byte = item.find('#')
        nop = item.find('@')
        var = item.find('!')

        # Verifica valores vazios
        if item != '':

            # Se opcode possui um endereço:
            if addrs > 0 :
                opcode = item.split('$')[0]
                operand = item.split('$')[1]
                has_var = item.find('!')

                if has_var > 0:
                    variable = item.split('!')[1]
                    if variable in variables:
                        app.append(f'{commands.get(opcode):0{bits}{form}}')
                        app.append(variable)
                        app.append(variable)
                    else:
                        print(f'\033[31mVariable "{variable}" is not defined\033[m')
                        errors += 1
                else:
                    if opcode in commands:
                        if len(operand) == 4:
                            app.append(f'{commands.get(opcode):0{bits}{form}}')
                            app.append(f'{int(operand[0:2], base=16):0{bits}{form}}')
                            app.append(f'{int(operand[2:4], base=16):0{bits}{form}}')
                            if opcode == 'JM' or opcode == 'JPZ' or opcode == 'JPC':
                                print(f'{int(len(app)):0{bits}{form}}: {opcode}')
                        else:
                            print(f'\033[31mArgError: {opcode} ${operand}, expect at least 4 bits addr\033[m')
                            errors += 1
                    else:
                        print(f'\033[31mUnknow command: {opcode}\033[m')
                        errors += 1
            # ----

            # Se opcode possui um byte:
            elif byte > 0 :
                opcode = item.split('#')[0]
                operand = item.split('#')[1]
                has_var = item.find('!')

                if has_var > 0:
                    variable = item.split('!')[1]
                    if variable in variables:
                        app.append(f'{commands.get(opcode):0{bits}{form}}')
                        app.append(variable)
                        app.append(variable)
                    else:
                        print(f'\033[31mVariable "{variable}" is not defined\033[m')
                        errors += 1
                else:
                    if len(operand) == 2:
                        if opcode in commands:
                            app.append(f'{commands.get(opcode):0{bits}{form}}')
                            app.append(operand)            
                        else:
                            print(f'\033[31mUnknow command: {opcode}\033[m')
                            errors += 1
                    else:
                        print(f'\033[31mArgError: {opcode} ${operand}, expect at least 2 bits value\033[m')
                        errors += 1
            # ----

            # Se opcode não possuir operando nenhum:
            elif nop > 0:
                opcode = item.split('@')[0]

                if opcode in commands:
                    app.append(f'{commands.get(opcode):0{bits}{form}}')
                else:
                    print(f'\033[31mUnknow command: {opcode}\033[m')
                    errors += 1
            # ----

            # Se é uma definição de variável:
            elif var == 0:
                var_name = item.split('!')[1]
                variables.append(var_name)
            # ----

            # Se faltar operando em um comando que deveria ter:
            else:
                print(f'\033[31mSyntaxError: {item} <- Miss operand\033[m')
                errors += 1
            # ----

    # Verificador de erros:
    if errors > 0:
        print(f'\nWarning: foram encontrados {errors} durante a compilação, corriga-os e compile novamente\n')
        raise SyntaxError

    # Aplicando variáveis:
    global livre
    if len(variables) <= livre:

        for variable in variables:
            app.append('ZZ')
            var_addrs = app.index('ZZ') + (len(starter) + variables.index(variable))

            if var_addrs < 256:
                for item in app:
                    if item == variable:
                        app[app.index(item)] = '00'
                        app[app.index(item)] = f'{var_addrs:0{bits}{form}}'

            elif var_addrs < 9999:
                for item in app:
                    if item == variable:
                        app[app.index(item)] = str(f'{int(var_addrs):04x}')[0:2]
                        app[app.index(item)] = str(f'{int(var_addrs):04x}')[2:4]
            elif var_addrs >= 10000:
                for item in app:
                    if item == variable:
                        app[app.index(item)] = str(f'{int(var_addrs):04x}')[0:2]
                        app[app.index(item)] = str(f'{int(var_addrs):04x}')[2:4]

    # Aplicando o APP dentro o EXE:
    if len(app) <= livre:
        index_exe = len(starter)
        index_app = 0
        for value in range(len(app)):
            exe[index_exe] = app[index_app]
            index_exe += 1
            index_app += 1
        livre -= len(app)
    else:
        print(f"\033[31mERROR: There is not enough memory space for this APP\033[m" )
    
    return app


app = compilar(assembly)

print()
# print(f'\033[32m{exe}\033[m', end=' ')
# print(f'\033[32mTamanho: {len(exe)}\033[m')
print(f'\033[34m{app}\033[m', end=' ')
print(f'\033[34mTamanho: {len(app)}\033[m')

# testes:
# x = 0
# for addr in range(memory):
#     # print(f'{x}: 0x{(exe[addr]):0{bits}{form}}')
#     x += 1


# print(f'\n\033[7;33m {livre} b livre(s) de {memory} b \033[m\n')
print(f'\n\033[7;33m {(livre/1000):.2f} kb livre(s) de {(memory/1000):.2f} kb \033[m\n')

with open("executavel.hex", "w") as arquivo:
    for x in exe:
        arquivo.write(f'0{form}{x}\n')

print(f'\033[3;32mSuccess!\033[m\n')
