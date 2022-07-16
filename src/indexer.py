def add(INDEX, domain):
    if domain not in INDEX:
        INDEX[domain] = []
    return INDEX


def delete(INDEX, domain):
    try:
        INDEX.pop(domain, None)
    except KeyError:
        print("Unable to find Domain!")


def table(INDEX):
    table_list = []
    for website in INDEX.keys():
        temp_list = [website]
        temp_list += INDEX[website]
        table_list.append(temp_list)
    print(table_list)
    return table_list

