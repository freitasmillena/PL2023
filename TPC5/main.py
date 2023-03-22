import re

moedasValidas = {
    "5c": 5,
    "10c": 10,
    "15c": 15,
    "20c": 20,
    "50c": 50,
    "1e": 100,
    "2e": 200
}

custo_chamada = {
    r'^00\d+$': 150, #internacionais
    r'^800\d{6}$': 0,
    r'^2\d{8}$': 25, #nacionais fixo
    r'^808\d{6}$': 10,
    r'^9(1|2|3|6)\d{7}$': 15, #nacionais móvel
    r'^6[04]1\d{6}$': -2
}

estado = {
    "levantou": False,
    "saldo": 0
}

def custo(str):
    for k,v in custo_chamada.items():
        if re.match(k,str):
            return v

    return -1

def levantar(str):
    if estado["levantou"]:
        print("Operação Inválida: Telefone já se encontra levantado.")
        return
    estado["levantou"] = True

def pousar(str):
    if not estado["levantou"]:
        print("Operação Inválida: Telefone já se encontra pousado.")
        return
    troco(estado["saldo"])
    estado["levantou"] = False
    estado["saldo"] = 0

def troco(quantia):
    moedas = {5: 0, 10: 0, 20: 0, 50: 0, 100: 0, 200: 0}
    for moeda in sorted(moedas, reverse=True):
        while quantia > 0:
            moedas[moeda] +=1
            quantia -= moedas[moeda]
    total = [f'{key}x{moedas[value]}' for key, value in moedas if moedas[value]]
    print(f"Troco = {', '.join(total)}")

def abortar(str):
    if not estado["levantou"]:
        print("Operação Inválida: Telefone não se encontra levantado.")
        return
    troco(estado["saldo"])
    estado["saldo"] = 0

def moedas(str):
    if not estado["levantou"]:
        print("Operação Inválida: Telefone não se encontra levantado.")
        return
    moedasInseridas = re.findall(r"\d+[ce]", str)
    for moeda in moedasInseridas:
        if moeda not in moedasValidas:
            print(f"Moeda inválida: {moeda}")
        else:
            estado["saldo"] += moedasValidas[moeda]

def telefonar(str):
    if not estado["levantou"]:
        print("Operação Inválida: Telefone não se encontra levantado.")
        return

    numero = str[2:]
    custo_total = custo(numero)
    if custo_total == -1:
        print('Operação Inválida: Número iválido.')
    elif custo_total == -2:
        print('Operação Inválida: Esse número não é permitido neste telefone.')
    else:
        estado["saldo"] -= custo
        print(f'Custo total da operação: {(custo / 100):.2f}€; Saldo atual: {(estado["saldo"] / 100):.2f}€')

def sair(str, state):
    exit(0)

def main():
    operacoes = {
        "LEVANTAR": levantar,
        "POUSAR": pousar,
        "MOEDA": moedas,
        "T": telefonar,
        "ABORTAR": abortar,
        "SAIR": sair
    }

    while True:
        line = input()

        for k, v in operacoes.items():
            if line.startswith(k):
                v(line)


if __name__ == "main":
    main()