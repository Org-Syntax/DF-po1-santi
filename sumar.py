import random

def main():
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)
    suma = num1 + num2
    
    print("----------------------------------------")
    print("🚀 EJECUCIÓN DESDE GITHUB ACTIONS 🚀")
    print("----------------------------------------")
    print(f"Número 1 asignado: {num1}")
    print(f"Número 2 asignado: {num2}")
    print(f"Resultado de la suma: {num1} + {num2} = {suma}")
    print("----------------------------------------")

if __name__ == "__main__":
    main()
