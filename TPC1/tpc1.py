import os
import matplotlib.pyplot as plt


def read_data(file):
    with open(file) as file:
        content = file.readlines()

    data = []

    for line in content[1:]: #remove header
        idade,sexo,tensão,colesterol,batimento,temDoença = line.strip().split(",")
        data.append((int(idade),sexo,int(tensão),int(colesterol),int(batimento),bool(int(temDoença))))

    return data

def dist_gender(data):
    totalgender = {"F":0,"M":0}
    distgender = {}
    for d in data:
        totalgender[d[1]]+=1
        if d[-1]:
            if d[1] not in distgender:
                distgender[d[1]] = 0
            distgender[d[1]]+=1
    distgender["F"] = (distgender["F"]/totalgender["F"])*100
    distgender["M"] = (distgender["M"]/totalgender["M"])*100
    
    return distgender
    
def dist_idade(data):
    distidade = {}
    maxIdade = max([d[0] for d in data])
    
    for idade in range(30,maxIdade,5):
        total = [d for d in data if d[0] in range(idade,idade+5)]#intervalos de 5 em 5
        doentes = [d for d in total if d[5]] #doentes pertencentes ao intervalo de idade
        distidade[(idade,idade+4)] = (len(doentes) / len(total)) * 100
    
    return distidade
        

def dist_colesterol(data):
    distcolesterol = {}
    maxColesterol = max([d[3] for d in data])
    minColesterol = min([d[3] for d in data if d[3] != 0 and d[5]]) #desconsidero dados que contém 0 de colesterol

    
    for colesterol in range(minColesterol, maxColesterol,10):
        total = [d for d in data if d[3] in range(colesterol,colesterol+10) and d[3] != 0] #intervalos de 10 em 10
        doentes = [d for d in total if d[5] and d[3] != 0] 
        if doentes:
            distcolesterol[(colesterol,colesterol+9)] = (len(doentes) / len(total)) * 100
    
    return distcolesterol
    
    
    
def print_table(dist, metric):
    i = 0
    if metric == "género": i = 23
    elif metric == "colesterol": i = 27
    else: i = 22
        
    print("+" + "-"*i + "+")
    print(f"|  {metric}  | doentes(%) |")
    print("+" + "-"*i + "+")
    for pair in dist.items():
        if metric == "idade":
            print(f"| [{pair[0][0]}-{pair[0][1]}] |   {pair[1]:.2f}%   |") 
        elif metric == "género":
            print(f"|   {pair[0]}      |    {pair[1]:.2f}%  |") 
        else:
            if pair[0][0] < 100:
                print(f"|  [{pair[0][0]}-{pair[0][1]}]    |   {pair[1]:.2f}%   |") 
            else:
                if pair[1] < 100: 
                    print(f"|  [{pair[0][0]}-{pair[0][1]}]   |   {pair[1]:.2f}%   |")
                else: print(f"|  [{pair[0][0]}-{pair[0][1]}]   |   {pair[1]:.2f}%  |")
    print("+" + "-"*i + "+")



def grafico(dist, metric):
    values = list(map(str,dist.keys()))
    percentages = list(dist.values())

    fig = plt.figure(figsize=(10, 5))

    fig, ax = plt.subplots()

    ax.set_title(f"No. of people with disease by {metric}")
    ax.set_ylabel("No. of people")
    ax.set_xlabel(f"{metric}")

    ax.bar(values, percentages, color ='pink',
        width = 0.4)

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
            print_table(dist_gender(data), "género");
         elif saida == 2:
            print_table(dist_idade(data), "idade");
         elif saida == 3:
            print_table(dist_colesterol(data), "colesterol");
         elif saida == 4:
            grafico(dist_gender(data), "Sexo")
         elif saida == 5:
            grafico(dist_idade(data), "Escalões etários")
         elif saida == 6:
            grafico(dist_colesterol(data), "Níveis de colesterol")
         else:
            print("you didn't add anything")
         if saida != 0 :
            l = input("prima enter para continuar") 

         os.system('clear')

    

main()
    

