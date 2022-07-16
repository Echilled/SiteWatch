def add(INDEX, domain):
    if domain not in INDEX:
        INDEX[domain] = []
    return INDEX


def delete(INDEX, domain):
    try:
        INDEX.pop(domain, None)
    except KeyError:
        print("Unable to find Domain!")
    return
