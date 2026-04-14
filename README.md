#  GIS Metadata Template (Schema.org JSON-LD)

This repository defines a reusable metadata model for geospatial datasets in the OHDSI GIS ecosystem.

It provides JSON-LD templates that align with:

* **Schema.org / Science-on-Schema.org (SoSO)** for dataset discovery
* **GeoCroissant** for geospatial and ML-ready data representation
* **OHDSI GIS (gaiaDB)** architecture for analytical workflows

---

## 🔗 Related Work

This work is part of the OHDSI GIS initiative:

https://github.com/orgs/OHDSI/projects/26/views/22?pane=issue&itemId=139343663&issue=OHDSI%7CGIS%7C326

---

## 🧠 Key Concept

The template models datasets as a **table structure** using `variableMeasured`.

Each dataset is standardized into:

* A **location component** (geometry column)
* One or more **measurement variables** (data columns)

This aligns directly with:

* gaiaDB structure:

  * `geom_index` → location
  * `attr_index` → measurements
* GeoCroissant dataset modeling
* FAIR machine-readable metadata principles

---

## 📦 Example Datasets

The template has been tested across multiple dataset types:

### Vector datasets

* Global PM2.5 concentrations (1998–2016)
* Massachusetts CDC Social Vulnerability Index (SVI), 2020

### Raster datasets

* Tanzania 2m Temperature (Copernicus ERA5-Land, 1984–1985)

---

## 🧩 Repository Structure

* `templates/` → JSON-LD metadata implementations
* `images/` → conceptual architecture diagrams
* `notes/` → design rationale and modeling decisions
* `index.html` → human-readable overview

---

## 🧭 Conceptual Model

The implementation follows the architecture shown in the diagrams:

### 1. End-to-End Workflow

`images/catalog_workflow_v5.png`

* Schema.org metadata
  → gaiaDB
  → OMOP CDM
  → ML/AI workflows

---

### 2. Metadata Structure

`images/schemaDataset_v5.png`

Defines:

* Dataset-level metadata (SoSO)
* `variableMeasured` as a **table schema**
* Separation of:

  * location (geometry)
  * measurements (attributes)
* Provenance via `about`
* Agent components via `hasPart`

---

## ⚙️ Design Principles

* Consistent structure across raster and vector datasets
* Separation of:

  * discovery metadata (Dataset level)
  * data schema (variableMeasured)
* Structured location modeling using `PropertyValue + valueReference`
* Extensible toward GeoCroissant and SHACL validation
* Alignment with FAIR and machine-actionable metadata

---

## 🔄 Metadata as a Data Model

This repository demonstrates that metadata is not only descriptive.

It acts as a **structural blueprint** that enables transformation into:

* OMOP external exposure tables
* ML-ready Croissant datasets
* Analytical pipelines and research workflows

---

## 🚀 Why this matters

This approach enables:

* Standardized metadata across heterogeneous datasets
* Machine-readable and interoperable data
* Integration with OHDSI GIS workflows
* Reproducible and scalable data pipelines

---

## 👤 Maintainer

David Amadi


GitHub Pages site: https://daakiv.github.io/jsonld-templates/
