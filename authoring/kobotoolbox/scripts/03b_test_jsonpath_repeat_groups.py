import json
from pathlib import Path
from jsonpath_ng.ext import parse


# -------------------------------------------------------------------
# 1. Locate input file
# -------------------------------------------------------------------
# This assumes record_136_input.json is in the same folder where you run the script.
# If it is in another folder, update this path.
INPUT_FILE = Path("record_136_input.json")

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Could not find {INPUT_FILE.resolve()}\n"
        "Make sure record_136_input.json is in this folder, or update INPUT_FILE."
    )


# -------------------------------------------------------------------
# 2. Load wrapped Kobo JSON
# -------------------------------------------------------------------
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)


# -------------------------------------------------------------------
# 3. Helper function to test JSONPath expressions
# -------------------------------------------------------------------
def test_path(path):
    matches = [m.value for m in parse(path).find(data)]

    print("\nPATH:", path)
    print("MATCHES:", len(matches))

    if len(matches) == 0:
        print("RESULT: No matches found")
    else:
        print("FIRST 3 RESULTS:")
        for item in matches[:3]:
            print("-", item)


# -------------------------------------------------------------------
# 4. Test repeat groups and key fields
# -------------------------------------------------------------------

print("\n=== CREATOR ===")
test_path("$.datasets[*]['dublin_core_group/creator_group'][*]['dublin_core_group/creator_group/creator_name']")

print("\n=== PUBLISHER ===")
test_path("$.datasets[*]['dublin_core_group/publisher_group'][*]['dublin_core_group/publisher_group/publisher_name']")

print("\n=== COVERAGE ===")
test_path("$.datasets[*]['dublin_core_group/coverage_group'][*]['dublin_core_group/coverage_group/coverage_name']")

print("\n=== SUBJECT / KEYWORDS ===")
test_path("$.datasets[*]['dublin_core_group/subject_group'][*]['dublin_core_group/subject_group/subject_term']")

print("\n=== ATTRIBUTE NAMES ===")
test_path("$.datasets[*]['cartography_group/attributes_group'][*]['cartography_group/attributes_group/attribute_name']")

print("\n=== COLLECTIONS ===")
test_path("$.datasets[*]['collection_group/collections']")

print("\n=== ISO / GEOGRAPHY ===")
test_path("$.datasets[*]['iso_group/structure']")
test_path("$.datasets[*]['iso_group/geometry']")
test_path("$.datasets[*]['iso_group/epsg']")

print("\n=== ETL FIELDS ===")
test_path("$.datasets[*]['etl_group/table_name']")
test_path("$.datasets[*]['etl_group/extension']")
test_path("$.datasets[*]['etl_group/format']")
test_path("$.datasets[*]['etl_group/last_updated']")
test_path("$.datasets[*]['etl_group/update_frequency']")