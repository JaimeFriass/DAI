import random
numerako = random.randint(1,100)

print("Hola crack :D")
print("Tienes k adivinar un numero")

eskrita = int(input())
oportunidades = 1

while eskrita != numerako and oportunidades != 10:
    oportunidades = oportunidades + 1
    if eskrita > numerako:
        print("Es menor")
    elif eskrita < numerako:
        print("Es mayor")

    eskrita = int(input())

    
if oportunidades > 9:
    print("El numerako era ", numerako)
else:
    print("Eres un máquina, puto amo, fenómeno mastodonte")

