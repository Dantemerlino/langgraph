# CodeSystem

## Characteristics

| Attribute | Value |
|---|---|
| FHIR Version | [R4 (4.0.1)](http://hl7.org/fhir/R4/codesystem.html) |
| US Core Profile Id | [NA](http://hl7.org/fhir/us/core/STU4/general-guidance.html) |
| Source System | TERMS Database |
| Source Format | Custom Schema |
| Epic Bridge ID | Not Applicable |

## Notes

- This specification is DRAFT and may contain mapping logic descriptions that are confusing or incomplete.
- The following lists table aliases and the underlying database tables to which they refer:`DTCS - EDTWH.DIM_TERMS_CODE_SYSTEM``DTC - EDTWH.DIM_TERMS_CONCEPT`

## Supported Attributes

### concept[0]
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** BackboneElement
- **Logic:** See child attributes for additional mapping logic.
- **Notes:** Concepts in the code system

### concept[0].display
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** DTC.TERMS_CONCEPT_NAME AS CONCEPT_NAME
- **Notes:** Text to display to the user

### concept[0].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** DTC.TERMS_CONCEPT_CODE
- **Notes:** Code that identifies concept

### concept[0].property[0]
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** BackboneElement
- **Logic:** See child attributes for additional mapping logic.
- **Notes:** Property value for the concept

### concept[0].property[0].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** Hard coded to constant value.
- **Constant Value:** "startDate"

### concept[0].property[0].valueDateTime
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** dateTime
- **Inputs:** CODESYS.CONCEPT_START_TIME

### concept[0].property[1]
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** BackboneElement
- **Logic:** See child attributes for additional mapping logic.
- **Notes:** Property value for the concept

### concept[0].property[1].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** Hard coded to constant value.
- **Constant Value:** "deprecationDate"

### concept[0].property[1].valueDateTime
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** dateTime
- **Inputs:** CODESYS.CONCEPT_END_TIME

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
- **Constant Value:** email

### contact[0].telecom[0].value
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Logic:** Hard coded to constant value.
- **Constant Value:** "TERMS@mayo.edu"

### content
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** Hard coded to constant value.
- **Constant Value:** "complete"
- **Notes:** not-present | example | fragment | complete | supplementCodeSystemContentMode (Required)

### copyright
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** markdown
- **Inputs:** TERMS_CODE_SYSTEM_LICENSE_CONDITION
- **Notes:** Use and/or publishing restrictions

### date
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** dateTime
- **Inputs:** TERMS_CODE_SYSTEM_START_DATETIME
- **Notes:** Date last changed

### description
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** markdown
- **Inputs:** TERMS_CODE_SYSTEM_DESCRIPTION

### extension[0]
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** Extension
- **Logic:** See child attributes for additional mapping logic.

### extension[0].url
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** Extension
- **Logic:** Hard coded to constant value.
- **Constant Value:** "endDate"

### extension[0].value
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** Extension
- **Inputs:** TERMS_CODE_SYSTEM_END_DATETIME

### identifier[0]
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** Identifier
- **Logic:** See child attributes for additional mapping logic.
- **Notes:** Additional identifier for the code system (business identifier)

### identifier[0].system
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/systemid/terms/termscodesystem/id"

### identifier[0].value
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** DTCS.TERMS_CODE_SYSTEM_TERMINOLOGY_REGISTRY_IDENTIFIER

### name
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** TERMS_CODE_SYSTEM_IDENTIFYING_FACET_NICKNAME
- **Notes:** Name for this code system (computer friendly)

### status
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** Hard coded to constant value.
- **Constant Value:** "active"
- **Notes:** draft | active | retired | unknownPublicationStatus (Required)

### title
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** TERMS_CODE_SYSTEM_FULLY_SPECIFIED_NAME
- **Notes:** Name for this code system (human friendly)

### url
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** uri
- **Inputs:** DTCS.TERMS_CODE_SYSTEM_FHIR_DESIGNATED_UNIFORM_RESOURCE_IDENTIFIER
- **Notes:** Canonical identifier for this code system, represented as a URI (globally unique) (Coding.system)

### version
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** DTCS.TERMS_CODE_SYSTEM_VERSION
- **Notes:** Business version of the code system (Coding.version)

## Unsupported Attributes

| Attribute | Cardinality |
|---|---|

## Known Issues

None