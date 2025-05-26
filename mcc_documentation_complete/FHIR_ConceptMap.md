# ConceptMap

## Characteristics

| Attribute | Value |
|---|---|
| FHIR Version | [R4 (4.0.1)](http://hl7.org/fhir/R4/conceptmap.html) |
| US Core Profile Id | [NA](http://hl7.org/fhir/us/core/STU4/general-guidance.html) |
| Source System | TERMS Database |
| Source Format | Custom Schema |
| Epic Bridge ID | Not Applicable |

## Notes

- This specification is DRAFT and may contain mapping logic descriptions that are confusing or incomplete.
- The following lists table aliases and the underlying database tables to which they refer:-- `MR` - `EDTWH.FACT_TERMS_MAP`-- `CC` - `EDTWH.DIM_TERMS_CONCEPT`-- `CCS` - `EDTWH.DIM_TERMS_CODE_SYSTEM`-- `CCTAR` - `EDTWH.DIM_TERMS_CONCEPT`-- `CCSTAR` - `EDTWH.DIM_TERMS_CODE_SYSTEM`-- `MM` - `EDTWH.DIM_TERMS_MAP_METADATA`
- [https://docs.google.com/spreadsheets/d/1Y6QZguBPPxtjxs4cDSBP14vLNqTgyFrFu0_tgvcFWh4/edit#gid=1504490245](https://docs.google.com/spreadsheets/d/1Y6QZguBPPxtjxs4cDSBP14vLNqTgyFrFu0_tgvcFWh4/edit#gid=1504490245)

## Supported Attributes

### contact[0]
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** ContactDetail
- **Logic:** See child attributes for additional mapping logic.
- **Notes:** Contact details for the publisher

### contact[0].telecom[0]
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** ContactPoint
- **Logic:** See child attributes for additional mapping logic.

### contact[0].telecom[0].system
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** code
- **Logic:** Hard coded to constant value.
- **Constant Value:** "email"

### contact[0].telecom[0].value
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Logic:** Hard coded to constant value.
- **Constant Value:** "TERMS@mayo.edu"

### copyright
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** markdown
- **Inputs:** EDTWH.DIM_TERMS_MAP_METADATA.TERMS_MAP_METADATA_LICENSE_CONDITION
- **Notes:** Use and/or publishing restrictions

### date
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** dateTime
- **Inputs:** TERMS_MAP_METADATA_START_DATETIME
- **Notes:** Date last changed

### description
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** markdown
- **Inputs:** EDTWH.DIM_TERMS_MAP_METADATA.TERMS_MAP_METADATA_DESCRIPTION
- **Notes:** Natural language description of the concept map

### extension[0]
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** Extension
- **Logic:** See child attributes for additional mapping logic.
- **Notes:** End date extension

### extension[0].url
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** Extension
- **Inputs:** TERMS_MAP_METADATA_END_DATETIME
- **Notes:** End date extension

### extension[0].value
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** Extension
- **Inputs:** TERMS_MAP_METADATA_END_DATETIME
- **Notes:** End date extension

### group[0]
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** BackboneElement
- **Logic:** See child attributes for additional mapping logic.

### group[0].element[0]
**Cardinality:** Required

- **Cardinality:** 1..*
- **Type:** BackboneElement
- **Inputs:** EDTWH.DIM_TERMS_MAP_METADATA.TERMS_MAP_METADATA_VERSION
- **Logic:** See child attributes for additional mapping logic.
- **Notes:** Specific version of the code system

### group[0].element[0].code
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** code
- **Inputs:** CC.TERMS_CONCEPT_CODE AS sourcecode
- **Notes:** Identifies element being mapped

### group[0].element[0].target[0]
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** BackboneElement
- **Logic:** See child attributes for additional mapping logic.
- **Notes:** Concept in target system for elementRule: If the map is narrower or inexact, there SHALL be some comments

### group[0].element[0].target[0].display
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** CCTAR.TERMS_CONCEPT_NAME AS targetname
- **Notes:** Display for the code

### group[0].element[0].target[0].equivalence
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** EDTWH.DIM_TERMS_MAP_METADATA.TERMS_MAP_METADATA_FHIR_EQUIVALENCE_CODE
- **Notes:** relatedto | equivalent | equal | wider | subsumes | narrower | specializes | inexact | unmatched | disjointConceptMapEquivalence (Required only if target is populated)

### group[0].element[0].target[0].code
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** code
- **Inputs:** CCTAR.TERMS_CONCEPT_CODE AS targetcode
- **Notes:** Code that identifies the target element

### group[0].element[0].display
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** CC.TERMS_CONCEPT_NAME AS sourcename
- **Notes:** Display for the code

### group[0].source
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** uri
- **Inputs:** EDTWH.DIM_TERMS_MAP_METADATA.TERMS_MAP_METADATA_SOURCE_CODE_SYSTEM_FHIR_DESIGNATED_UNIFORM_RESOURCE_IDENTIFIER
- **Notes:** Source system where concepts to be mapped are defined

### group[0].sourceVersion
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** EDTWH.DIM_TERMS_MAP_METADATA.TERMS_MAP_METADATA_VERSION
- **Notes:** Specific version of the code system

### group[0].target
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** uri
- **Inputs:** EDTWH.DIM_TERMS_MAP_METADATA.TERMS_MAP_METADATA_TARGET_CODE_SYSTEM_FHIR_DESIGNATED_UNIFORM_RESOURCE_IDENTIFIER
- **Notes:** Target system that the concepts are to be mapped to

### identifier
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** Identifier
- **Logic:** See child attributes for additional mapping logic.
- **Notes:** identifier for the concept map

### identifier.system
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** uri
- **Logic:** When a conceptmap is provided by TERMs set to "http://terms.mayo.edu/systemid/terms/termsconceptmap/id" else "urn:ietf:rfc:3986"
- **Notes:** Assumption: URI is a unique identifier for a ConceptMap and is used as the primary identifier

### identifier.value
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** EDTWH.DIM_TERMS_MAP_METADATA.TERMS_MAP_METADATA_TERMINOLOGY_REGISTRY_IDENTIFIER
- **Logic:** The value will be a custom URL when not from TERMs.

### name
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** EDTWH.DIM_TERMS_MAP_METADATA.TERMS_MAP_METADATA_NICKNAME
- **Notes:** Name for this concept map (computer friendly)From FHIR standard: + Warning: Name should be usable as an identifier for the module by machine processing applications such as code generation

### sourceUri
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** uri
- **Inputs:** EDTWH.DIM_TERMS_MAP_METADATA.TERMS_MAP_METADATA_SOURCE_CODE_SYSTEM_FHIR_DESIGNATED_UNIFORM_RESOURCE_IDENTIFIER

### status
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** WHEN MM.TERMS_MAP_METADATA_START_DATETIME >= CURRENT TIMESTAMP AND MM.TERMS_MAP_METADATA_END_DATETIME >= CURRENT TIMESTAMP THEN "draft"WHEN MM.TERMS_MAP_METADATA_START_DATETIME <= CURRENT TIMESTAMP AND MM.TERMS_MAP_METADATA_END_DATETIME >= CURRENT TIMESTAMP THEN "active"ELSE "retired"

### targetUri
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** uri
- **Inputs:** EDTWH.DIM_TERMS_MAP_METADATA.TERMS_MAP_METADATA_TARGET_CODE_SYSTEM_FHIR_DESIGNATED_UNIFORM_RESOURCE_IDENTIFIER

### title
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** EDTWH.DIM_TERMS_MAP_METADATA.TERMS_MAP_METADATA_NAME
- **Notes:** Name for this concept map (human friendly)

### url
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** uri
- **Inputs:** EDTWH.DIM_TERMS_MAP_METADATA.TERMS_MAP_METADATA_MC_UNIFORM_RESOURCE_IDENTIFIER AS MAP_TYPE_URI
- **Notes:** Canonical identifier for this concept map, represented as a URI (globally unique)

### version
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** EDTWH.DIM_TERMS_MAP_METADATA.TERMS_MAP_METADATA_VERSION
- **Notes:** Business version of the concept mapNo version provided -- a few rows populated with the value "None", but no version numbering.

## Unsupported Attributes

| Attribute | Cardinality |
|---|---|

## Known Issues

None