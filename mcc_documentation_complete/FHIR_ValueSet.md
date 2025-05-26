# ValueSet

## Characteristics

| Attribute | Value |
|---|---|
| FHIR Version | [R4 4.0.1](http://hl7.org/fhir/R4/valueset.html) |
| US Core Profile Id | [NA](http://hl7.org/fhir/us/core/STU4/general-guidance.html) |
| Source System | TERMS DB |
| Source Format | Custom Schema |
| Epic Bridge ID | Not Applicable |

## Notes

- The following lists table aliases and the underlying database tables to which they refer:-- dtvn -> EDTWH.DIM_TERMS_VS_NAME-- FTVM -> edtwh.FACT_TERMS_VS_MEMBER-- DTC -> EDTWH.DIM_TERMS_CONCEPT-- DTCS -> EDTWH.DIM_TERMS_CODE_SYSTEM
- [https://docs.google.com/spreadsheets/d/1Y6QZguBPPxtjxs4cDSBP14vLNqTgyFrFu0_tgvcFWh4/edit#gid=1504490245](https://docs.google.com/spreadsheets/d/1Y6QZguBPPxtjxs4cDSBP14vLNqTgyFrFu0_tgvcFWh4/edit#gid=1504490245)
- The following common attributes are not supported for any element unless explicitly included in the specification:`Element.id``Element.extension[]``BackboneElement.modifierExtension[]`
- In the FHIR R4 standard, the `:in` search modifier used with a query parameter, such as `code:in=`, allows API consumers to filter the specified query parameter by a certain ValueSet. Due to a limitation in the Google Healthcare API implementation, FHIR queries searching large ValueSets may fail if the ValueSets contain too many items. The LPR team has implemented a workaround to overcome this limitation. Please see FHIR Search in ValueSet for more information.

## Supported Attributes

### compose
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** BackboneElement
- **Logic:** See child fields for mapping logic.See child attributes for additional mapping logic.

### compose.include[]
**Cardinality:** Required

- **Cardinality:** 1..*
- **Type:** BackboneElement
- **Logic:** See child fields for mapping logic (one BackboneElement added per unique system/value combination).See child attributes for additional mapping logic.

### compose.include[].concept[]
**Cardinality:** Required

- **Cardinality:** 1..*
- **Type:** BackboneElement
- **Logic:** See child fields for mapping logic (one BackboneElement added per unique code within system/version).See child attributes for additional mapping logic.

### compose.include[].concept[].display
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** dtc.terms_concept_name
- **Logic:** Set value directly from input value.

### compose.include[].concept[].extension[]
**Cardinality:** Required

- **Cardinality:** 1..*
- **Type:** BackboneElement
- **Logic:** See child fields for mapping logic (one BackboneElement added per unique system/value combination).See child attributes for additional mapping logic.

### compose.include[].concept[].extension[].url
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** Hard coded to constant value.
- **Constant Value:** "status"

### compose.include[].concept[].extension[].valueString
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** dtc.TERMS_CONCEPT_START_DATETIMEdtc.TERMS_CONCEPT_END_DATETIME
- **Logic:** If the start datetime is after the current datetime, the value is set to "Draft"If the start datetime is at or before the current time and the end datetime is at or after the current datetime, the value is set to "Active"If the end datetime is before the current datetime, the value is set to "Retired"

### compose.include[].concept[].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** dtc.terms_concept_code
- **Logic:** Set value directly from input value.

### compose.include[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Inputs:** dtcs.terms_code_system_fhir_designated_uniform_resource_identifier
- **Logic:** Set value directly from input value.

### compose.include[].version
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** dtcs.terms_code_system_version
- **Logic:** If blank or only whitespace, do not set FHIR field. Otherwise, set value directly from input value.

### contact[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** ContactDetail
- **Logic:** See child fields for mapping logic.See child attributes for additional mapping logic.

### contact[].name
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** Hard coded to constant value.
- **Constant Value:** "TERMS Team"

### contact[].telecom[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** ContactPoint
- **Logic:** See child fields for mapping logic.See child attributes for additional mapping logic.

### contact[].telecom[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "email"

### contact[].telecom[].value
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** Hard coded to constant value.
- **Constant Value:** "TERMS@mayo.edu"

### date
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** dateTime
- **Inputs:** ftvm.terms_valueset_start_datetime
- **Logic:** Convert value directly from input value.

### description
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** markdown
- **Inputs:** dtvn.terms_valueset_description
- **Logic:** If blank or only whitespace, do not set FHIR field. Otherwise, set value directly from input value.

### extension[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Extension
- **Logic:** See child fields for mapping logic.See child attributes for additional mapping logic.

### extension[].url
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Extension
- **Logic:** Hard coded to constant value.
- **Constant Value:** "endDate"

### extension[].valueDateTime
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Extension
- **Inputs:** ftvm.terms_valueset_end_datetime
- **Logic:** Convert value directly from input value.

### id
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** id
- **Inputs:** dtvn.terms_valueset_dkftvm.terms_valueset_revision_name
- **Logic:** Set to a hash of the concatenated input field values.
- **Post Reconciliation Logic:** An existing ValueSet to update is found by searching by id.

### identifier[]
**Cardinality:** Required

- **Cardinality:** 1..2
- **Type:** Identifier
- **Logic:** See child fields for mapping logic.An offical Identifier (with its unique values represented by the identifier[o].system, identifier[o].use, and identifier[o].value fields) will always be added.A usual Identifier (with its unique values represented by the identifier[u].system, identifier[u].use, and identifier[u].value fields) will be added only if it has a non-blank value.The offical Identifier and the usual Identifier both use the same values for the other child fields of identifier[].See child attributes for additional mapping logic.

### identifier[o]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Identifier
- **Logic:** See child attributes for additional mapping logic.

### identifier[o].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "urn:ietf:rfc:3986"

### identifier[o].type
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** CodeableConcept
- **Logic:** See child fields for mapping logic.See child attributes for additional mapping logic.

### identifier[o].type.coding[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Coding
- **Logic:** See child fields for mapping logic.See child attributes for additional mapping logic.

### identifier[o].type.coding[].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** Hard coded to constant value.
- **Constant Value:** "value_set_oid"

### identifier[o].type.coding[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/mcc/assigned_identifier"

### identifier[o].type.coding[].display
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** Hard coded to constant value.
- **Constant Value:** "Value Set OID"

### identifier[o].type.text
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** Hard coded to constant value.
- **Constant Value:** "Value Set OID"

### identifier[o].use
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** Hard coded to constant value.
- **Constant Value:** "official"

### identifier[o].value
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** dtvn.terms_valueset_identifier
- **Logic:** Set value directly from input value.

### identifier[u]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Identifier
- **Logic:** See child attributes for additional mapping logic.

### identifier[u].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/systemid/terms/termsvalueset/id"

### identifier[u].type
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** CodeableConcept
- **Logic:** See child fields for mapping logic.See child attributes for additional mapping logic.

### identifier[u].type.coding[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Coding
- **Logic:** See child fields for mapping logic.See child attributes for additional mapping logic.

### identifier[u].type.coding[].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** Hard coded to constant value.
- **Constant Value:** "terms_value_set_id"

### identifier[u].type.coding[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/mcc/assigned_identifier"

### identifier[u].type.coding[].display
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** Hard coded to constant value.
- **Constant Value:** "TERMS Value Set ID"

### identifier[u].type.text
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** Hard coded to constant value.
- **Constant Value:** "TERMS Value Set ID"

### identifier[u].use
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** Hard coded to constant value.
- **Constant Value:** "usual"

### identifier[u].value
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** dtvn.TERMS_VALUESET_MC_UNIFORM_RESOURCE_IDENTIFIER
- **Logic:** Set value directly from input value.

### name
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** dtvn.terms_valueset_identifier
- **Logic:** If blank or only whitespace, do not set FHIR field. Otherwise, set value directly from input value.

### status
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** ftvm.TERMS_VALUESET_START_DATETIMEFTVM.TERMS_VALUESET_END_DATETIME
- **Logic:** WHEN ftvm.TERMS_VALUESET_START_DATETIME >= CURRENT TIMESTAMP AND FTVM.TERMS_VALUESET_END_DATETIME >= CURRENT TIMESTAMP THEN "draft"WHEN ftvm.TERMS_VALUESET_START_DATETIME <= CURRENT TIMESTAMP AND FTVM.TERMS_VALUESET_END_DATETIME >= CURRENT TIMESTAMP THEN "active"ELSE "retired"

### title
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** dtvn.terms_valueset_name
- **Logic:** Set value directly from input value.

### url
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Inputs:** dtvn.TERMS_VALUESET_MC_UNIFORM_RESOURCE_IDENTIFIER
- **Logic:** Set value directly from input value.

### useContext[]
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** UsageContext
- **Logic:** See child fields for mapping logic (at most one UsageContext is created, if the optional child fields are not all blank).See child attributes for additional mapping logic.

### useContext[].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** See child fields for mapping logic.See child attributes for additional mapping logic.

### useContext[].code.display
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** dtvn.terms_valueset_mc_context_of_use
- **Logic:** If blank or only whitespace, do not set FHIR field. Otherwise, set value directly from input value.

### useContext[].valueCodeableConcept
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** CodeableConcept
- **Logic:** See child fields for mapping logic.See child attributes for additional mapping logic.

### useContext[].valueCodeableConcept.text
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** dtvn.terms_valueset_mc_context_of_use
- **Logic:** If blank or only whitespace, do not set FHIR field. Otherwise, set value directly from input value.

### version
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** ftvm.terms_valueset_revision_name
- **Logic:** Set value directly from input value.

## Unsupported Attributes

| Attribute | Cardinality |
|---|---|
| compose.inactive Cardinality0..0TypebooleanLogicNot mapped. | Not Supported |
| compose.include[].filter[] Cardinality0..0TypeBackboneElementLogicNot mapped. | Not Supported |
| compose.include[].concept[].designation[] Cardinality0..0TypeBackboneElementLogicNot mapped. | Not Supported |
| compose.include[].valueSet[] Cardinality0..0TypecanonicalLogicNot mapped. | Not Supported |
| compose.lockedDate Cardinality0..0TypedateLogicNot mapped. | Not Supported |
| compose.exclude[] Cardinality0..0TypeBackboneElementLogicNot mapped. | Not Supported |
| contact[].telecom[].period Cardinality0..0TypePeriodLogicNot mapped. | Not Supported |
| contact[].telecom[].rank Cardinality0..0TypepositiveIntLogicNot mapped. | Not Supported |
| contact[].telecom[].use Cardinality0..0TypecodeLogicNot mapped. | Not Supported |
| copyright Cardinality0..0TypemarkdownLogicNot mapped. | Not Supported |
| expansion Cardinality0..0TypeBackboneElementLogicNot mapped. | Not Supported |
| experimental Cardinality0..0TypebooleanLogicNot mapped. | Not Supported |
| identifier[].assigner Cardinality0..0TypeReferenceLogicNot mapped. | Not Supported |
| identifier[o].type.coding[].userSelected Cardinality0..0TypestringLogicNot mapped. | Not Supported |
| identifier[o].type.coding[].version Cardinality0..0TypestringLogicNot mapped. | Not Supported |
| immutable Cardinality0..0TypebooleanLogicNot mapped. | Not Supported |
| jurisdiction[] Cardinality0..0TypeCodeableConceptLogicNot mapped. | Not Supported |
| publisher Cardinality0..0TypestringLogicNot mapped. | Not Supported |
| purpose Cardinality0..0TypemarkdownLogicNot mapped. | Not Supported |
| useContext[].valueCodeableConcept.coding[] Cardinality0..0TypeCodingLogicNot mapped. | Not Supported |

## Known Issues

None