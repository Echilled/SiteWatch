import json


def json_hash_indexer(location="WebHash.Json"):
    with open(location, "r") as file:
        try:
            index = {}
            data = json.load(file)
            for url, properties in data['URLs'].items():
                index[url] = [properties['properties']['hash'], properties['properties']['archival_date']]
                # print(properties)
            return index
        except Exception as e:
            pass


def json_construct(id, hash, date, times_it_changed):
    website_dic = {id: {'properties': {}}}
    values = [{'hash': hash}, {'archival_date': date}, {'number of times URL content change': times_it_changed}]
    for val in values:
        website_dic[id]['properties'].update(val)
    return website_dic


def update_json(filename, data_dict):
    with open(filename, "w") as outfile:
        json_object = json.dumps(data_dict, indent=4)
        outfile.write(json_object)
