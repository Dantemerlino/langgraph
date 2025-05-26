# CommonMapping

## Characteristics

| Attribute | Value |
|---|---|
| FHIR Version | [R4 (4.0.1)](https://www.hl7.org/fhir/r4/datatypes.html) |
| US Core Profile Id | [NA](http://hl7.org/fhir/us/core/STU4/general-guidance.html) |
| Source System | Epic |
| Source Format | HL7v2 |
| Epic Bridge ID | See main resource specification |

## Notes

- This is a "pseudo-specification" is used to capture common / re-usable mapping patterns and is not aFHIR Resource. This pseudo-specification may be referenced by actual FHIR Resource mapping specificationsto improve consistency and re-use.

## Supported Attributes

### address[]
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** Address
- **Inputs:** XXX-X
- **Logic:** See main resource specification for actual Min, Max.The main resource specification overrides these common specifications.See child nodes for mapping.Component numbering applies to the input segment and field from the main resourcespecifications. For example, if the main resource sheet indicated an input of PID-11, thenXXX-X.7 in the child nodes would refer to PID-11.7.Do not map if `use` is the only child node mapped.See child attributes for additional mapping logic.

### address[].country
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** XXX-X.6
- **Logic:** Do not map if the field is blank, otherwise set to the contents of the field.

### address[].district
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** XXX-X.9
- **Logic:** Do not map if the field is blank, otherwise set to the contents of the field.

### address[].line[]
**Cardinality:** Optional

- **Cardinality:** 0..2
- **Type:** string
- **Inputs:** XXX-X.1.1XXX-X.1.2XXX-X.2.1
- **Logic:** Set first `address[].line[]` as follows:-- Concatenate XXX-X.1.1, a single space, XXX-X.1.2. Trim the resulting string of leading andtrailing spaces.-- Set to the resulting trimmed concatenation IFF the resulting trimmed concatenation is not blank.Set second `address[].line[]` as follows:-- Trim XXX-X.2.1 of leading and trailing whitespace.-- Set to the resulting trimmed value IFF the resulting trimmed value is not blank.Ignore additional address that may be received from Epic.

### address[].city
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** XXX-X.3
- **Logic:** Do not map if the field is blank, otherwise set to the contents of the field.

### address[].postalCode
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** XXX-X.5
- **Logic:** Do not map if the field is blank, otherwise set to the contents of the field.

### address[].state
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** XXX-X.4
- **Logic:** Do not map if the field is blank, otherwise set to the contents of the field.

### address[].use
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** XXX-X.7
- **Logic:** See main resource specification.

### meta
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Meta
- **Logic:** See child attributes for additional mapping logic.

### meta.source
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/mcc/datasource/epic"

### name[]
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** HumanName
- **Inputs:** XXX-X
- **Logic:** See main resource specification for actual Min, Max.The main resource specification overrides these common specifications.See child nodes for mapping.Component numbering applies to the input segment and field from the main resourcespecifications. For example, if the main resource sheet indicated an input of PID-5, thenXXX-X.3 in the child nodes would refer to PID-5.3.Although both HL7 and FHIR support name as a repeatable entity, we will only ever take thefirst iteration of name from the HL7 and we will not add name iterations on the FHIR record(even in the case of name changes). We will always only retain the most current name and relyupon provenance and _history records for any previous names.Do not map this attribute if only `name[].use` is set.See child attributes for additional mapping logic.

### name[].family
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** XXX-X.1.1
- **Logic:** Set to value found in XXX-X.1.1, ignoring any other subcomponents (XXX-X.1.2, XXX-X.1.3, etc.).

### name[].given[]
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** string
- **Inputs:** XXX-X.2 first nameXXX-X.3 middle name(s)
- **Logic:** Set the first item of `given[]` to the first name in XXX-X.2.Set subsequent items of `given[]` to the middle names found in XXX-X.3 (&-delimited) in order, one name per item.

### name[].prefix[]
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** string
- **Inputs:** XXX-X.5
- **Logic:** Set to name prefixes in order from XXX-X.5 (&-delimited).

### name[].suffix[]
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** string
- **Inputs:** XXX-X.4 name suffix(es)XXX-X.6 degree(s)
- **Logic:** Set to name suffix(es) in order from XXX-X.4 (&-delimited), followed by degree(s) in order from XXX-X.6 (&-delimited).

### name[].use
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** Hard coded to constant value.
- **Constant Value:** "usual"

### telecom[]
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** ContactPoint
- **Inputs:** XXX-X
- **Logic:** See main resource specification for actual Min, Max.The main resource specification overrides these common specifications.See child nodes for mapping.Component numbering applies to the input segment and field from the main resourcespecifications. For example, if the main resource sheet indicated an input of PID-13, thenXXX-X.3 in the child nodes would refer to PID-13.3.See child attributes for additional mapping logic.

### telecom[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** XXX-X.3
- **Concept Map:** `http://terms.mayo.edu/mccfhir/conceptmap/epic.communication.type.has.fhir.contact.point`
- **Logic:** Set using concept map.If the input does not have an entry in the Concept Map, execute the following action: Throw UnexpectedCodeExceptionIf the input is blank Concept Map, execute the following action: Default to "other"

### telecom[].use
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** code
- **Inputs:** XXX-X.2, XXX-X.3, YYY-Y.2, YYY-Y.3
- **Concept Map:** `http://terms.mayo.edu/systemid/terms/termsconceptmap/id`
- **Logic:** If XXX-X.2 is "T", set to "temp"If XXX-X.2 and XXX-X.3 are empty, or XXX-X.2 is "NET", do not setif XXX-X.3 is empty, set to "home"if XXX-X.3 is not empty, look value up in concept map and set to resultIf YYY-Y.2 is "T", set to "temp"If YYY-Y.2 and YYY-Y.3 are empty, or YYY-Y.2 is "NET", do not setif YYY-Y.2 is empty, set to "work"if YYY-Y.2 is not empty, look value up in concept map and set to resultOtherwise, throw UnexpectedCodeExceptionIf the input does not have an entry in the Concept Map, execute the following action: EXCEPTION
- **Notes:** XXX-X.X refers to the segment and field containing the "home" telecom systemYYY-Y.Y refers to the segment and field containing the "work" telecom system

### telecom[].value
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** XXX-X.1XXX-X.4
- **Logic:** Set to XXX-X.4 if `telecom[].system` = "email", else set to XXX-X.1.If value is blank, do not create an element in the telecom array (skip this repetition).

## Unsupported Attributes

| Attribute | Cardinality |
|---|---|
| address[].extension[] Cardinality0..0TypeExtensionLogicNot mapped. | Not Supported |
| [http://hl7.org/fhirpath/System.String](http://hl7.org/fhirpath/System.String) | Not Supported |
| address[].period Cardinality0..0TypePeriodLogicNot mapped.NotesWe exclude period because we only track the current address. | Not Supported |
| address[].text Cardinality0..0TypestringLogicNot mapped. | Not Supported |
| address[].type Cardinality0..0TypecodeLogicNot mapped.NotesThere is nothing in the HL7 message that indicates what type of address it is. | Not Supported |
| [http://hl7.org/fhirpath/System.String](http://hl7.org/fhirpath/System.String) | Not Supported |
| name[].extension[] Cardinality0..0TypeExtensionLogicNot mapped. | Not Supported |
| name[].period Cardinality0..0TypePeriodLogicNot mapped. | Not Supported |
| name[].text Cardinality0..0TypestringLogicNot mapped. | Not Supported |
| [http://hl7.org/fhirpath/System.String](http://hl7.org/fhirpath/System.String) | Not Supported |
| telecom[].extension[] Cardinality0..0TypeExtensionLogicNot mapped. | Not Supported |
| telecom[].period Cardinality0..0TypePeriodLogicNot mapped. | Not Supported |
| telecom[].rank Cardinality0..0TypepositiveIntLogicNot mapped. | Not Supported |

## Known Issues

None