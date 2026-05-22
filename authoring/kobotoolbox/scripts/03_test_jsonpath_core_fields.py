import json
from jsonpath_ng.ext import parse

with open("record_136_input.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def test_path(path):
    matches = [m.value for m in parse(path).find(data)]
    print("\nPATH:", path)
    print("MATCHES:", len(matches))
    print(matches[:3])

test_path("$.datasets[*]['control_group/id']")
test_path("$.datasets[*]['dublin_core_group/title']")
test_path("$.datasets[*]['dublin_core_group/description']")
test_path("$.datasets[*]['dublin_core_group/doi']")
test_path("$.datasets[*]['etl_group/source']")