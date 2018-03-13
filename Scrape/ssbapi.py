from pyjstat import pyjstat
import requests
from collections import OrderedDict

EXAMPLE_URL = 'http://data.ssb.no/api/v0/en/table/03024'

#payload = {"query": [{"code": "VareGrupper2", "selection": {"filter": "item", "values": ["01", "02"] } }
#                   , {"code": "ContentsCode", "selection": {"filter": "item", "values": ["Vekt", "Kilopris"] } }
#                   , {"code": "Tid", "selection": {"filter": "top", "values": ["53"] } }
#                    ]
#        , "response": {"format": "json-stat"} }

payload = {"query" : [{"code": "VareGrupper2", "selection": {"filter": "item", "values": ["01", "02"]}}
                      ] }

data = requests.post(EXAMPLE_URL, json = payload)

results = pyjstat.from_json_stat(data.json(object_pairs_hook=OrderedDict))
# results[0].to_csv("03024.csv", sep=';', encoding='utf-8') # save .csv

print(results)