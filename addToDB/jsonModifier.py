import json
with open('nst.json') as file:
	original = json.load(file)

modified = [{'Category': key,'News': value} for key, value in original.items()]
output = json.dumps(modified)

with open('modified.json', 'w+') as file:
	file.write(output)

