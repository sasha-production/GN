import json
inData = '{"one": ["http", "yandex.ru"], "two" : ["https", "google.com"]}'
res = json.loads(inData)
print(res['one'])