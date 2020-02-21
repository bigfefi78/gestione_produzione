import json

with open('json_file\info.json') as json_file:
    data = json.load(json_file)

print(json.dumps(data, indent=6))

# with open('dump.txt', 'w') as outfile:
#     json.dump(data, outfile)

#     json.dump(data, outfile)

    # for p in data:
    #     print(p)# data = {}

# data['people'] = []
# data['people'].append({
#     'name': 'Scott',
#     'website': 'stackabuse.com',
#     'from': 'Nebraska'
# })
# data['people'].append({
#     'name': 'Larry',
#     'website': 'google.com',
#     'from': 'Michigan'
# })
# data['people'].append({
#     'name': 'Tim',
#     'website': 'apple.com',
#     'from': 'Alabama'
# })
#
# with open('data.txt', 'w') as outfile:
#     json.dump(data, outfile)
# # data = Db("test")
# # data.name = "ciccio"
# # data.create_connection(data.name + ".db")
# # sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS elenco_codici (
#                                         codice  text PRIMARY KEY,
#                                         tipo text NOT NULL,
#                                         descrizione text
#                                     ); """