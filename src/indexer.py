import operator

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
    return table_list


def sort_table(INDEX, column):
    if INDEX != sorted(INDEX, key=operator.itemgetter(column)):
        reversed_sort = False
    else:
        reversed_sort = True

    if column == 0:
        return sorted(INDEX, key=operator.itemgetter(column), reverse=reversed_sort)
    elif column == 1:
        return sorted(INDEX, key=operator.itemgetter(column), reverse=reversed_sort)
    elif column == 2:
        return sorted(INDEX, key=operator.itemgetter(column), reverse=reversed_sort)
