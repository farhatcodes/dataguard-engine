import json
from .engine import validate

schema={"id":{"required":True,"type":"integer"},"score":{"type":"number","min":0,"max":100}}
rows=[{"id":1,"score":90},{"id":None,"score":110}]
print(json.dumps([v.to_dict() for v in validate(rows,schema)],indent=2))
