from dataguard.engine import validate

def test_required_and_range():
    schema={"id":{"required":True},"score":{"type":"number","max":100}}
    found=validate([{"score":101}],schema)
    assert {(v.field,v.rule) for v in found}=={("id","required"),("score","max")}

def test_bool_not_integer():
    assert validate([{"id":True}],{"id":{"type":"integer"}})[0].rule=="type"

def test_valid():
    assert not validate([{"id":2}],{"id":{"required":True,"type":"integer"}})
