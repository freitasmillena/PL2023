import os
import matplotlib.pyplot as plt


class Dist:
    def __init__(self, data={}, metric=""):
        # data should be a list of tuples
        # where first element is the value and second element is the frequency
        self.data = data
        # name of the distribution
        self.name = metric

    def __repr__(self):
        i = 0
        if self.name == "género":
            i = 23
        elif self.name == "colesterol":
            i = 27
        else:
            i = 22

        print("+" + "-" * i + "+")
        print(f"|  {self.name}  | doentes(%) |")
        print("+" + "-" * i + "+")
        for pair in self.data.items():
            if self.name == "idade":
                print(f"| [{pair[0][0]}-{pair[0][1]}] |   {pair[1]:.2f}%   |")
            elif self.name == "género":
                print(f"|   {pair[0]}      |    {pair[1]:.2f}%  |")
            else:
                if pair[0][0] < 100:
                    print(f"|  [{pair[0][0]}-{pair[0][1]}]    |   {pair[1]:.2f}%   |")
                else:
                    if pair[1] < 100:
                        print(f"|  [{pair[0][0]}-{pair[0][1]}]   |   {pair[1]:.2f}%   |")
                    else:
                        print(f"|  [{pair[0][0]}-{pair[0][1]}]   |   {pair[1]:.2f}%  |")
        print("+" + "-" * i + "+")


def read_data(file):
    with open(file) as file:
        content = file.readlines()

    data = []

    for line in content[1:]:  # remove header
        idade, sexo, tensão, colesterol, batimento, temDoença = line.strip().split(",")
        data.append((int(idade), sexo, int(tensão), int(colesterol), int(batimento), bool(int(temDoença))))

    return data


def dist_gender(data):
    totalgender = {"F": 0, "M": 0}
    distgender = {}
    for d in data:
        totalgender[d[1]] += 1
        if d[-1]:
            if d[1] not in distgender:
                distgender[d[1]] = 0
            distgender[d[1]] += 1
    distgender["F"] = (distgender["F"] / totalgender["F"]) * 100
    distgender["M"] = (distgender["M"] / totalgender["M"]) * 100

    return distgender


def dist_idade(data):
    distidade = {}
    maxIdade = max([d[0] for d in data])

    for idade in range(30, maxIdade, 5):
        total = [d for d in data if d[0] in range(idade, idade + 5)]  # intervalos de 5 em 5
        doentes = [d for d in total if d[5]]  # doentes pertencentes ao intervalo de idade
        distidade[(idade, idade + 4)] = (len(doentes) / len(total)) * 100

    return distidade


def dist_colesterol(data):
    distcolesterol = {}
    maxColesterol = max([d[3] for d in data])
    minColesterol = min([d[3] for d in data if d[3] != 0 and d[5]])  # desconsidero dados que contém 0 de colesterol

    for colesterol in range(minColesterol, maxColesterol, 10):
        total = [d for d in data if d[3] in range(colesterol, colesterol + 10) and d[3] != 0]  # intervalos de 10 em 10
        doentes = [d for d in total if d[5] and d[3] != 0]
        if doentes:
            distcolesterol[(colesterol, colesterol + 9)] = (len(doentes) / len(total)) * 100

    return distcolesterol


def grafico(dist, metric):
    values = list(map(str, dist.keys()))
    percentages = list(dist.values())

    fig = plt.figure(figsize=(10, 5))

    fig, ax = plt.subplots()

<<<<<<< HEAD
    ax.set_title(f"No. of people with disease by {metric}")
    ax.set_ylabel("No. of people")
=======
    ax.set_title(f"Distribuição da doença por {metric}")
    ax.set_ylabel("Número de pessoas")
>>>>>>> 367b9678ceae77e7f9ef2d0b558a8de5e78e53af
    ax.set_xlabel(f"{metric}")

    ax.bar(values, percentages, color='pink',
           width=0.4)

    # set the x-tick labels with more space between them
    ax.set_xticks(range(len(dist)))
    ax.set_xticklabels(dist.keys(), rotation=45, ha='right')

    # add padding to the bottom of the plot
    plt.tight_layout(pad=3)

    # display the graph
    plt.show()


def main():
    data = read_data("myheart.csv")
    saida = -1
    ageDist = Dist()
    genderDist = Dist()
    colesterolDist = Dist()
    while saida != 0:
        print("")
        print("1. Distribuição da doença por sexo")
        print("2. Distribuição da doença por escalões etários")
        print("3. Distribuição da doença por níveis de colesterol")
        print("4. Gráficos da distribuição da doença por sexo")
        print("5. Gráficos da distribuição da doença por escalões etários")
        print("6. Gráficos da distribuição da doença por níveis de colesterol")
        print("0. Sair")

        saida = int(input("introduza a sua opção-> "))

        if saida == 0:
            print("saindo.......")
        elif saida == 1:
            genderDist.data = dist_gender(data)
            genderDist.name = "género"
            genderDist.__repr__()
        elif saida == 2:
            ageDist.data = dist_idade(data)
            ageDist.name = "idade"
            ageDist.__repr__()
        elif saida == 3:
            colesterolDist.data = dist_colesterol(data)
            colesterolDist.name = "colesterol"
            colesterolDist.__repr__()
        elif saida == 4:
            if genderDist.name == "":
                genderDist.data = dist_gender(data)
                genderDist.name = "género"
<<<<<<< HEAD
            grafico(genderDist.data, "Sexo")
=======
            grafico(genderDist.data, "sexo")
>>>>>>> 367b9678ceae77e7f9ef2d0b558a8de5e78e53af
        elif saida == 5:
            if ageDist.name == "":
                ageDist.data = dist_idade(data)
                ageDist.name = "idade"
<<<<<<< HEAD
            grafico(ageDist.data, "Escalões etários")
=======
            grafico(ageDist.data, "escalões etários")
>>>>>>> 367b9678ceae77e7f9ef2d0b558a8de5e78e53af
        elif saida == 6:
            if colesterolDist.name == "":
                colesterolDist.data = dist_colesterol(data)
                colesterolDist.name = "colesterol"
<<<<<<< HEAD
            grafico(colesterolDist.data, "Níveis de colesterol")
=======
            grafico(colesterolDist.data, "níveis de colesterol")
>>>>>>> 367b9678ceae77e7f9ef2d0b558a8de5e78e53af
        else:
            print("you didn't add anything")
        if saida != 0:
            l = input("prima enter para continuar")

        os.system('clear')


main()
