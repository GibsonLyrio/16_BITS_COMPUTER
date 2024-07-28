# A = 0b000000000010
# B = 0b000100000000

# C = A | B   # Aplica a operação OR bit a bit entre A e B

# print(f"C = {C:012b}")  # Imprime o resultado em formato binário

# while True:
#     x = 0
#     y = 1
#     while x < 255:
#         print(x)
#         z = x + y
#         x = y
#         y = z


x = 'ff'

# z = int(x, base=16)

print(type(x))
print(f'{int(x, base=16):02x}')

