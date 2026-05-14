# System Architecture and Mapping Workflow

## Overview

The current workflow represents the transition from a spreadsheet-driven metadata authoring process to a more structured and scalable KoboToolbox-based authoring approach for the Gaia Catalog. The workflow is designed to support machine-readable metadata generation while improving consistency, maintainability, and interoperability across different geospatial data use cases.

![Kobo JSONPath SSSOM Workflow](https://github.com/daakiv/ohdsi-gis-metadata-template/blob/main/images/kobo_jsonpath_sssom_workflow.png)

---

## Authoring Layer

The authoring layer focuses on structured metadata capture using KoboToolbox forms developed through the XLSForm standard. This replaces the earlier manual spreadsheet-based process and introduces a more controlled metadata authoring environment.

Metadata fields are organized into logical sections aligned with the existing Gaia Catalog metadata structure, including:

- Dataset identification and descriptive metadata
- Spatial and temporal coverage
- Distribution and access information
- Cartographic and geospatial metadata
- ETL and provenance-related metadata

The KoboToolbox workflow introduces:

- Controlled field definitions
- Standardized metadata entry
- Validation and required field handling
- Repeat groups for complex metadata structures
- Improved consistency across datasets and projects

The objective of this layer is to create a reusable metadata authoring framework that can support multiple data modalities, including tabular, vector, raster, and sensor-based datasets.

---

## Extraction and Intermediate Transformation

Once metadata records are authored and submitted in KoboToolbox, the workflow retrieves the raw JSON response through the KoboToolbox API. JSONPath expressions are then used to isolate and extract relevant metadata elements from the nested Kobo JSON structure.

This intermediate step supports:

- Normalization of Kobo responses
- Simplification of nested structures
- Preparation for downstream semantic mapping
- Reduction of manual metadata transformation work

The extracted metadata currently serves as an intermediate representation before harmonization into target metadata structures.

---

## Mapping Layer (Under Review)

The mapping layer is currently being refined and remains under active review. The objective is to establish a harmonized mapping strategy capable of supporting reusable metadata transformations across multiple standards and schemas.

Current work is exploring:

- JSONPath-driven extraction logic
- SSSOM-inspired field mappings
- Alignment with Schema.org and Science-on-Schema.org concepts
- Standardized handling of geospatial metadata elements

This layer is intended to evolve into a reusable semantic mapping framework capable of supporting machine-readable FAIR metadata generation across heterogeneous geospatial data use cases.

