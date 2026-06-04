# KoboToolbox Metadata Authoring

This folder documents the KoboToolbox/XLSForm-based metadata authoring workflow being developed for the [Gaia Catalog](https://github.com/OHDSI/gaiaCatalog) and OHDSI GIS metadata pipeline.

The workflow supports the transition from a legacy spreadsheet-based metadata process into a more structured, reusable, and machine-actionable authoring approach. It uses:

- **KoboToolbox** for structured metadata capture
- **Raw Kobo JSON exports** as the source record
- **SSSOM-style mapping files** for semantic transformation
- **JSON-LD outputs** aligned with [Schema.org](https://schema.org) / [Science-on-Schema.org](https://github.com/ESIPFed/science-on-schema.org/blob/main/guides/Dataset.md#roles-of-people) patterns

---

## Purpose

The KoboToolbox form serves as a structured metadata authoring interface for geospatial datasets intended for Gaia Catalog ingestion and downstream machine-readable metadata generation.

The goal is to support consistent metadata capture across geospatial use cases — including vector, raster, tabular, and sensor-based datasets — while reducing manual transformation work and improving the reproducibility of metadata outputs.

---

## Why this approach

The previous workflow relied on manually maintained spreadsheet templates. The KoboToolbox-based workflow improves:

| Aspect | Benefit |
|---|---|
| **Consistency** | Structured form fields reduce free-text variation |
| **Validation** | Entry-time checks catch errors before export |
| **Controlled vocabularies** | Dropdown and select responses enforce standard terms |
| **Scalability** | Supports multiple contributors and dataset types |
| **Interoperability** | Outputs align with JSON-LD / Schema.org standards |
| **Traceability** | Clear chain from raw record → mapping → output |

---

## Current workflow

```
KoboToolbox XLSForm
        ↓
Kobo metadata submission
        ↓
Raw Kobo JSON export
        ↓
AI-assisted and manually reviewed SSSOM mapping
        ↓
SSSOM-to-JSON-LD transformation
        ↓
Schema.org / Science-on-Schema.org JSON-LD output
        ↓
Gaia Catalog review and ingestion
```

---

## Main assets

| Folder / file | Purpose |
|---|---|
| `docs/` | Workflow notes, architecture documentation, and concept notes |
| `forms/` | KoboToolbox/XLSForm authoring templates and related form assets |
| `prompts/` | AI prompt templates used to support SSSOM mapping generation and review |
| `records/` | Raw Kobo records, generated outputs, and validation/comparison outputs |
| `scripts/` | Python scripts for pulling Kobo records and transforming SSSOM mappings into JSON-LD |
| `sssom/` | SSSOM-style TSV mapping files defining how Kobo JSON fields map to Schema.org / JSON-LD properties |
| `.env.example` | Example configuration showing required environment variables (no secrets exposed) |
| `README.md` | This document |

> Each subfolder contains its own `README.md` with further detail. For Science-on-Schema.org guidance on dataset roles, see the [official Dataset guide](https://github.com/ESIPFed/science-on-schema.org/blob/main/guides/Dataset.md#roles-of-people).
