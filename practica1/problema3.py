escrito = int(input("Hasta que numero: "))
numeros = []
for n in range(2, escrito + 2):
    numeros.append(n)

numero_elegido = 2
i = 0
salir = 0

while numero_elegido < escrito:
    print("Numero elegido: " + str(numero_elegido))
    i = 0
    multiplicado = 0
    while multiplicado < escrito:
        multiplicado = numero_elegido*i
        print("Multiplicado: " + str(multiplicado))
        if (multiplicado >= escrito):
            break
        numeros[multiplicado] = 1
        i = i + 1
        

    if numero_elegido*numero_elegido > escrito:
        break

    while 1:
        numero_elegido = numero_elegido + 1
        print(numeros[numero_elegido])
        if (numeros[numero_elegido] == 0):
            break

    print("SADADSAD")