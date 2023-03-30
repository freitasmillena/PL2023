import re
import json
from prettytable import PrettyTable


def dist_year(data):
    years = {}
    total = 0
    pattern = re.compile(r'(\d+)')
    myTable = PrettyTable(["Year", "%"])
    for person in data:
        total += 1
        y = pattern.match(person['date']).groups(1)[0]
        if y not in years:
            years[y] = 0
        years[y] += 1
    for key, value in years.items():
        years[key] = (value / total) * 100
        row = []
        row.append(key)
        row.append("{:.4f}".format(years[key]))
        myTable.add_row(row)


    #Table
    for year,freq in sorted(years.items(), key=lambda y: (y[1]), reverse=True):
        row = []
        row.append(year)
        row.append("{:.4f}".format(freq))
        myTable.add_row(row)

    print(myTable)


def dist_names(data):
    centuries = {}
    pattern = re.compile(r'(\d+)')
    for person in data:
        year = int(pattern.match(person['date']).groups(1)[0])
        century = ""
        if (year % 100 == 0):
            century = str(year // 100)
        else:
            century = str((year // 100) + 1)
        if century not in centuries:
            centuries[century] = {"names": {}, "surnames": {}}

        names = [person['name'], person['father'], person['mother']]
        for p in person['obs']:
            names.append(p[0])

        for n in names:
            first = n.split(" ")[0]
            last = n.split(" ")[-1]
            if first not in centuries[century]['names']:
                centuries[century]['names'][first] = 0
            centuries[century]['names'][first] += 1
            if last not in centuries[century]['surnames']:
                centuries[century]['surnames'][last] = 0
            centuries[century]['surnames'][last] += 1

    for key,value in centuries.items():
        allnames = value['names'].items() #todos os nomes do século
        allsurnames = value['surnames'].items() #todos os apelidos do século
        totalnames = sum(list(value['names'].values()))
        totalsurnames = sum(list(value['surnames'].values()))
        for kname, vname in allnames:
            value['names'][kname] = (vname/totalnames) * 100
        for ksurname, vsurname in allsurnames:
            value['surnames'][ksurname] = (vsurname/totalsurnames) * 100
        centuries[key]['names'] = sorted(centuries[key]['names'].items(), key=lambda y: (y[1]), reverse=True)[:5]
        centuries[key]['surnames'] = sorted(centuries[key]['surnames'].items(), key=lambda y: (y[1]), reverse=True)[:5]


    #Table
    for key,value in centuries.items():
        print(f"{key}th Century")
        myTableNames = PrettyTable(["Name", "%"])
        myTableSurnames = PrettyTable(["Surname", "%"])
        for name, freqname in value['names']:
            row = []
            row.append(name)
            row.append("{:.4f}".format(freqname))
            myTableNames.add_row(row)
        for surname, freqsurname in value['surnames']:
            row = []
            row.append(surname)
            row.append("{:.4f}".format(freqsurname))
            myTableSurnames.add_row(row)
        print(myTableNames)
        print(myTableSurnames)







def distrelations(data):
    relations = {}
    total = 0
    myTable = PrettyTable(["Relation", "%"])
    for person in data:
        for relation in person['obs']:
            if relation[1] not in relations:
                relations[relation[1]] = 0
            relations[relation[1]] +=1
            total +=1


    for key,value in relations.items():
        relations[key] = (value/total) * 100

    sortRelations = sorted(relations.items(), key=lambda y: (y[1]), reverse=True)
    del sortRelations[-1]
    for relation,freq in sortRelations:
        row = []
        row.append(relation)
        row.append("{:.4f}".format(freq))
        myTable.add_row(row)

    print(myTable)

def main():
    data = []
    pattern = re.compile(
        r'^(?P<folder>\d+)::(?P<date>\d{4}-\d{2}-\d{2})::(?P<name>((?i)[a-z]+\s)+(?i)[a-z]+)::(?P<father>((?i)[a-z]+\s)+(?i)[a-z]+)::(?P<mother>((?i)[a-z]+\s)+(?i)[a-z]+)::(?P<obs>.*)::$')
    pattern_obs = re.compile(r'(([A-Z][a-z]+\s?)+),(([A-Z][a-z]+\s?)+)')
    with open('processos.txt', 'r') as f:
        for line in f:
            if line.strip() != '':
                if re.match(pattern, line):
                    person = pattern.search(line).groupdict()
                    obs = []
                    if person['obs'] != '' and re.match(pattern_obs, person['obs']):
                        for name, _, relation, _ in re.findall(pattern_obs, person['obs']):
                            obs.append((name, relation))
                    person['obs'] = obs
                    data.append(person)


    jsonDict = {}
    jsonDict['Process'] = []

    for i in range(20):

        if len(data[i]['obs']) > 0:

            relations = []
            for name, relation in data[i]['obs']:
                relations.append({"name": name, "relation": relation})

            jsonDict['Process'].append({"folder": data[i]['folder'], "date": data[i]['date'], "name": data[i]['name'], "father": data[i]['father'], "mother": data[i]['mother'],
                                        "obs": relations})
        else:
            jsonDict['Process'].append({"folder": data[i]['folder'], "date": data[i]['date'], "name": data[i]['name'],
                                        "father": data[i]['father'], "mother": data[i]['mother'],
                                        "obs": data[i]['obs']})

    with open('first20.json', 'w') as f:
        f.write(json.dumps(jsonDict, indent=4))
main()

