import sys

if __name__ == '__main__':
    on = True
    number = ""
    sum = 0
    print("Insira o texto desejado: ")
    print("[Para terminar, carregue Ctrl + D]")
    line = sys.stdin.read().lower()
    for i in range(0, len(line)):
        if line[i].isdigit() and on:
            number += line[i]
        elif on:
            sum += int(number) if number != "" else 0
            number = ""
        if line[i] == '=':
            print(f"""A soma total é: {sum}""")
        elif line[i:].startswith("on"):
            on = True
        elif line[i:].startswith("off"):
            on = False

