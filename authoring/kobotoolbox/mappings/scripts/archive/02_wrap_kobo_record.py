from pathlib import Path
import json


def find_repo_root(start_path=None):
    start_path = Path(start_path or Path.cwd()).resolve()

    for path in [start_path, *start_path.parents]:
        if (path / ".git").exists():
            return path

    raise RuntimeError("Could not find repo root.")


REPO_ROOT = find_repo_root()
KOBO_DIR = REPO_ROOT / "authoring" / "kobotoolbox"

EXAMPLE_INPUT_DIR = KOBO_DIR / "examples" / "pm25_record_136" / "input"

RAW_RECORD_FILE = EXAMPLE_INPUT_DIR / "record_136_raw.json"
WRAPPED_RECORD_FILE = EXAMPLE_INPUT_DIR / "record_136_input.json"

with open(RAW_RECORD_FILE, "r", encoding="utf-8") as f:
    raw_record = json.load(f)

wrapped = {
    "datasets": [raw_record]
}

with open(WRAPPED_RECORD_FILE, "w", encoding="utf-8") as f:
    json.dump(wrapped, f, indent=2, ensure_ascii=False)

print("Created wrapped input:")
print(WRAPPED_RECORD_FILE)