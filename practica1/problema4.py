escrito = int(input("Escriba un número\n"))

primero = 0
segundo = 1
for numero in range(0, escrito):
    tercero = primero + segundo
    primero = segundo
    segundo = tercero

f = open("fibonacci.txt", "w")
f.write("Número correspondiente: "+ str(tercero) + "\n")
print("Escrito con éxito")