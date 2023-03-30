import re, sys, json

data = {}



def process_head(head):
    pattern = re.compile(r'(?i)((?P<column>[a-z]+[^a-z,{]*[a-z]*)(\{(?P<range>\d+(,\d+)?)\})?(::(?P<function>media|sum|))?)')
    data = {}
    pattern_head = r'^'

    for column, *_ in re.findall(pattern, head):
        if column != '':
            columns = re.match(pattern, column).groupdict()
            column_name = columns['column']
            data[column_name] = {}

            if columns['range'] is not None:
                ranges = [int(i) for i in columns['range'].split(',')]
                data[column_name]['range'] = range(ranges[0], ranges[-1]+1)
                pattern_head += fr"(?P<{columns['column']}>([^,]*,?){{{columns['range']}}})"
            else:
                pattern_head += fr'((?P<{column}>[^,]*),?)'

            if columns['function'] is not None:
                data[column_name]['function'] = [columns['function']]
    pattern_head += r'$'
    return pattern_head,data

def process_tail(data, line, pattern):
    result = {}
    line = line.strip('\n')
    pline = pattern.fullmatch(line)
    if (pline):
        columns = pline.groupdict()
        for column, value in columns.items():
            items = []
            for i in value.split(','):
                if i != '':
                    items.append(i)
            result[column] = value

            if data[column] != {} and 'range' in data[column] and len(items) in data[column]['range']:
                result[column] = [int(i) for i in items]
                if 'function' in data[column]:

                    function = data[column]['function']

                    match function[0]:
                        case "sum":
                            result[f"{column}_{function[0]}"] = sum(result[column])
                        case "media":
                            result[f"{column}_{function[0]}"] = sum(result[column]) / len(result[column])
    return result



def main():
    with open(sys.argv[1]) as file:
        head, *tail = file.readlines()
        data_json = []
        pattern_str, data = process_head(head.strip('\n'))
        pattern = re.compile(pattern_str)

        for line in tail:
            result = process_tail(data,line,pattern)
            if result != {}:
                data_json.append(result)


        with open(f"./{sys.argv[1].split('.')[0]}.json", "w") as f:
            json.dump(data_json, f, indent=4, ensure_ascii=False)


main()

