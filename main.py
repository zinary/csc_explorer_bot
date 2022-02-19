import json

with open('db/db.json', 'r') as db:
    data = json.load(db)
    dapps = data["dapps"]

for index, item in enumerate(dapps):
    text = f"""
    <b>✅ {item}</b>
    """
    print(item['name'])

