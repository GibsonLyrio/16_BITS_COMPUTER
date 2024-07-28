total_steps = 16
lista = []
memory = 65536

HLT = 0b100000000000000000000000000000000000
AI  = 0b010000000000000000000000000000000000
AO  = 0b001000000000000000000000000000000000
SS  = 0b000100000000000000000000000000000000
SO  = 0b000010000000000000000000000000000000
TI  = 0b000001000000000000000000000000000000
TO  = 0b000000100000000000000000000000000000
BI  = 0b000000010000000000000000000000000000
BO  = 0b000000001000000000000000000000000000
CI  = 0b000000000100000000000000000000000000
CO  = 0b000000000010000000000000000000000000
RI  = 0b000000000001000000000000000000000000
RO  = 0b000000000000100000000000000000000000
MI  = 0b000000000000010000000000000000000000
II  = 0b000000000000001000000000000000000000
# IO  = 0b000000000000000100000000000000000000
RF  = 0b000000000000000100000000000000000000
OI  = 0b000000000000000010000000000000000000
PCE = 0b000000000000000001000000000000000000
PCO = 0b000000000000000000100000000000000000
J   = 0b000000000000000000010000000000000000
JZ  = 0b000000000000000000001000000000000000
JC  = 0b000000000000000000000100000000000000
AD1 = 0b000000000000000000000010000000000000
AD2 = 0b000000000000000000000001000000000000
ADO = 0b000000000000000000000000100000000000
STR = 0b000000000000000000000000010000000000
BYI = 0b000000000000000000000000001000000000
BYO = 0b000000000000000000000000000100000000
DCI = 0b000000000000000000000000000010000000
INC = 0b000000000000000000000000000001000000
CDE = 0b000000000000000000000000000000100000
CDO = 0b000000000000000000000000000000010000
XO  = 0b000000000000000000000000000000001000
RT  = 0b000000000000000000000000000000000100
XYY = 0b000000000000000000000000000000000010
YYY = 0b000000000000000000000000000000000001

# Definindo padrão de formatação final
form = 9
tipo = 'x'

# Definindo fatch cycle:
fatch_1 = PCO | MI
fatch_2 = RO  | II | PCE

# Definindo search do próximo endereço, Big_endian:
search_1 = PCO | MI
search_2 = RO  | AD1 | PCE
search_3 = PCO | MI
search_4 = RO  | AD2 | PCE
search_5 = ADO | MI

# Definindo pickup do próximo endereço como um byte:
pick_1 = PCO | MI
pick_2 = RO  | BYI | PCE

# Definindo a finalização:
finish = STR

# Inicia slots da memoria
for addrs in range(memory):
    lista.append('0'*(form))

def montar(code: list, addr, operand: str):
    steps = len(code)

    if addr <= (memory - total_steps):
        if lista[addr] == ('0'*(form)):
            if steps <= total_steps - 3:
                restante = total_steps

                # Adciona fetch cycle no inicio:
                lista[addr] = f'{fatch_1:0{form}{tipo}}'
                addr += 1   # avança o endereço
                lista[addr] = f'{fatch_2:0{form}{tipo}}'
                addr += 1   # avança o endereço

                restante -= 2

                # Adiciona a busca caso operando seja um endereço:
                if operand == 'addr':
                    lista[addr] = f'{search_1:0{form}{tipo}}'
                    addr += 1   # avança o endereço
                    lista[addr] = f'{search_2:0{form}{tipo}}'
                    addr += 1   # avança o endereço
                    lista[addr] = f'{search_3:0{form}{tipo}}'
                    addr += 1   # avança o endereço
                    lista[addr] = f'{search_4:0{form}{tipo}}'
                    addr += 1   # avança o endereço
                    lista[addr] = f'{search_5:0{form}{tipo}}'
                    addr += 1   # avança o endereço
                    restante -= 5

                # Adiciona leitura do próximo byte se operando for um valor:
                if operand == 'byte':
                    lista[addr] = f'{pick_1:0{form}{tipo}}'
                    addr += 1
                    lista[addr] = f'{pick_2:0{form}{tipo}}'
                    addr += 1
                    restante -= 2
                
                if operand == 'reg' or operand == 'not':
                    pass

                # Adiciona as etapas:
                for step in code:
                    lista[addr] = f'{step:0{form}{tipo}}'
                    addr += 1   # avança o endereço
                    restante -= 1

                # Adiciona o finalizador:
                lista[addr]= f'{finish:0{form}{tipo}}'
                addr += 1   # avança o endereço
                restante -= 1

                # Preenche o restante vazio:
                for step in range(restante):
                    lista[addr] = '0'*(form)
                    addr += 1   # avança o endereço
            else:
                print(f'\n\033[3;31mERROR: Você colocou {steps} etapas\nColoque no máximo {total_steps-3}\033[m\n')
                raise TypeError()
        else:
            print(f'\n\033[3;31mERROR: O ultimo comando tenta\nsobrescrever os endereços de 0x{addr:04x} ~ 0x{(addr + total_steps):04x}\033[m\n')
            raise TypeError()
    else:
        print(f'\n\033[3;31mERROR: O ultimo comando estourou a\nmemória, addr max para comando -> 0x{(memory - total_steps):04x}\033[m\n')
        raise TypeError()

# Definindo comandos:
ADD_B = [
    ( RT ),
    ( RF ),
    ( RO | TI ),
    ( SO | AI )
]
montar(ADD_B, 0x0010, 'addr')
montar(ADD_B, 0x1010, 'addr')
montar(ADD_B, 0x2010, 'addr')
montar(ADD_B, 0x3010, 'addr')
montar(ADD_B, 0x4010, 'addr')
montar(ADD_B, 0x5010, 'addr')
montar(ADD_B, 0x6010, 'addr')
montar(ADD_B, 0x7010, 'addr')

# testes:
NOP = [
]
montar(NOP, 0x0000, 'nop')   # Formato do endereço: F/CC/S
montar(NOP, 0x1000, 'nop')   # F  = 4 bits de Flag
montar(NOP, 0x2000, 'nop')   # CC = 8 bits de Comandos
montar(NOP, 0x3000, 'nop')   # S  = 4 bits de Steps
montar(NOP, 0x4000, 'nop')
montar(NOP, 0x5000, 'nop')
montar(NOP, 0x6000, 'nop')
montar(NOP, 0x7000, 'nop')

JPZ_1 = [
    ( PCE ),
    ( PCE ),
]
montar(JPZ_1, 0x0020, 'not')
montar(JPZ_1, 0x1020, 'not')
montar(JPZ_1, 0x2020, 'not')
montar(JPZ_1, 0x3020, 'not')

JPZ_2 = [
    ( ADO | J ),
]
montar(JPZ_2, 0x4020, 'addr')
montar(JPZ_2, 0x5020, 'addr')
montar(JPZ_2, 0x6020, 'addr')
montar(JPZ_2, 0x7020, 'addr')

DCL = [
    ( ADO | DCI )
]
montar(DCL, 0x0030, 'addr')
montar(DCL, 0x1030, 'addr')
montar(DCL, 0x2030, 'addr')
montar(DCL, 0x3030, 'addr')
montar(DCL, 0x4030, 'addr')
montar(DCL, 0x5030, 'addr')
montar(DCL, 0x6030, 'addr')
montar(DCL, 0x7030, 'addr')

SFT = [
    ( CDO | MI ),
    ( XO  | RI ),
]
montar(SFT, 0x0040, 'nop')
montar(SFT, 0x1040, 'nop')
montar(SFT, 0x2040, 'nop')
montar(SFT, 0x3040, 'nop')
montar(SFT, 0x4040, 'nop')
montar(SFT, 0x5040, 'nop')
montar(SFT, 0x6040, 'nop')
montar(SFT, 0x7040, 'nop')

DCS = [( CDE )]
montar(DCS, 0x0050, 'nop')
montar(DCS, 0x1050, 'nop')
montar(DCS, 0x2050, 'nop')
montar(DCS, 0x3050, 'nop')
montar(DCS, 0x4050, 'nop')
montar(DCS, 0x5050, 'nop')
montar(DCS, 0x6050, 'nop')
montar(DCS, 0x7050, 'nop')

HLT = [( HLT )]
montar(HLT, 0x0060, 'nop')
montar(HLT, 0x1060, 'nop')
montar(HLT, 0x2060, 'nop')
montar(HLT, 0x3060, 'nop')
montar(HLT, 0x4060, 'nop')
montar(HLT, 0x5060, 'nop')
montar(HLT, 0x6060, 'nop')
montar(HLT, 0x7060, 'nop')

JM_addr = [
    ( ADO | J )
]
montar(JM_addr, 0x0070, 'addr')
montar(JM_addr, 0x1070, 'addr')
montar(JM_addr, 0x2070, 'addr')
montar(JM_addr, 0x3070, 'addr')
montar(JM_addr, 0x4070, 'addr')
montar(JM_addr, 0x5070, 'addr')
montar(JM_addr, 0x6070, 'addr')
montar(JM_addr, 0x7070, 'addr')

JPC_1 = [
    (PCE),
    (PCE)
]
montar(JPC_1, 0x0080, 'nop')
montar(JPC_1, 0x2080, 'nop')
montar(JPC_1, 0x4080, 'nop')
montar(JPC_1, 0x6080, 'nop')

JPC_2 = [
    ( ADO | J ),
    ( RF )
]
montar(JPC_2, 0x1080, 'addr')
montar(JPC_2, 0x3080, 'addr')
montar(JPC_2, 0x5080, 'addr')
montar(JPC_2, 0x7080, 'addr')


OUT_addr = [
    ( RO | OI )
]
montar(OUT_addr, 0x0090, 'addr')
montar(OUT_addr, 0x1090, 'addr')
montar(OUT_addr, 0x2090, 'addr')
montar(OUT_addr, 0x3090, 'addr')
montar(OUT_addr, 0x4090, 'addr')
montar(OUT_addr, 0x5090, 'addr')
montar(OUT_addr, 0x6090, 'addr')
montar(OUT_addr, 0x7090, 'addr')
# ----

# ADD_C = [
    
# ]

# ANA_B = [

# ]

# ANA_C = [

# ]

# ANI_byte = [

# ]

# CALL_addr = [

# ]

# CMA = [

# ]

# DCR_A = [

# ]

# DCR_B = []

# DCR_C = []

# HLT = []

# IN_byte = []

INR_A = [
    ( RO | AI )
]
montar(INR_A, 0x00a0, 'addr')
montar(INR_A, 0x10a0, 'addr')
montar(INR_A, 0x20a0, 'addr')
montar(INR_A, 0x30a0, 'addr')
montar(INR_A, 0x40a0, 'addr')
montar(INR_A, 0x50a0, 'addr')
montar(INR_A, 0x60a0, 'addr')
montar(INR_A, 0x70a0, 'addr')

# INR_B = []

# INR_C = []

# JM_addr = [
#     ( ADO | J )
# ]
# montar(JM_addr, 0x0010, 'addr')
# montar(JM_addr, 0x1010, 'addr')
# montar(JM_addr, 0x2010, 'addr')
# montar(JM_addr, 0x3010, 'addr')
# montar(JM_addr, 0x4010, 'addr')
# montar(JM_addr, 0x5010, 'addr')
# montar(JM_addr, 0x6010, 'addr')
# montar(JM_addr, 0x7010, 'addr')

# JMP_addr = []

# JNZ_addr = []

# JZ_addr = []

# LDA_addr = []

# MOV_Ab = []

# MOV_Ac = []

# MOV_Ba = []

# MOV_Bc = []

# MOV_Ca = []

# MOV_Cb = []

MVI_A_byte = [
    ( BYO | AI )
]
montar(MVI_A_byte, 0x00b0, 'byte')
montar(MVI_A_byte, 0x10b0, 'byte')
montar(MVI_A_byte, 0x20b0, 'byte')
montar(MVI_A_byte, 0x30b0, 'byte')
montar(MVI_A_byte, 0x40b0, 'byte')
montar(MVI_A_byte, 0x50b0, 'byte')
montar(MVI_A_byte, 0x60b0, 'byte')
montar(MVI_A_byte, 0x70b0, 'byte')

# MVI_B_byte = []

# MVI_C_byte = []

# NOP = []

# ORA_B = []

# ORA_C = []

# ORI_byte = []

# OUT_byte = []

# RAL = []

# RAR = []

# RET = []

STA_addr = [
    ( AO | RI )
]
montar(STA_addr, 0x00c0, 'addr')
montar(STA_addr, 0x10c0, 'addr')
montar(STA_addr, 0x20c0, 'addr')
montar(STA_addr, 0x30c0, 'addr')
montar(STA_addr, 0x40c0, 'addr')
montar(STA_addr, 0x50c0, 'addr')
montar(STA_addr, 0x60c0, 'addr')
montar(STA_addr, 0x70c0, 'addr')
# SUB_B = []

# SUB_C = []

# XRA_B = []

# XRA_C = []

# XRI_byte = []
# ^^ Adcione novos comando a partir daqui ^^ #


with open("16_BITS_COMPUTER/teste.hex", "w") as arquivo:
    for x in lista:
        arquivo.write(f'0{tipo}{x}\n')

print(f'\n\033[3;32mSuccess!\033[m\n')


''' Transferindo da ROM pra RAM:

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


