import json
from pathlib import Path

# Explicit paths on your machine
RAW_FILE = Path("/Users/davidamadi/Documents/Projects/ohdsi-gis-metadata-template/authoring/kobotoolbox/scripts/kobo_output/record_136_raw.json")
INPUT_FILE = Path("/Users/davidamadi/Documents/Projects/ohdsi-gis-metadata-template/authoring/kobotoolbox/scripts/record_136_input.json")

print(f"Reading raw data from: {RAW_FILE}")

# Read raw Kobo file
with open(RAW_FILE, "r", encoding="utf-8") as f:
    raw_record = json.load(f)

# Wrap it in the 'datasets' array format Doug's pipeline expects
wrapped_data = {
    "datasets": [raw_record]
}

# Save it to the main scripts folder
with open(INPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(wrapped_data, f, indent=2, ensure_ascii=False)

print(f"Success! Created pipeline-ready file at: {INPUT_FILE}")