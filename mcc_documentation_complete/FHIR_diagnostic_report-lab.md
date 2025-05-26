# DiagnosticReport-Lab

## Characteristics

| Attribute | Value |
|---|---|
| FHIR Version | [R4 (4.0.1)](http://hl7.org/fhir/R4/diagnosticreport.html) |
| US Core Profile Id | [us-core-diagnosticreport-lab (4.0.0)](http://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-diagnosticreport-lab.html) |
| Source System | Epic |
| Source Format | HL7v2 |
| Epic Bridge ID | 609300 |

## Notes

- The following common attributes are not supported for any nested elements unless explicitly included in the specification:`Element.id``Element.version``Element.userSelected``Element.extension[]`
- Backload History: Stage: Latest full backload performed on 2024-03-26 Latest partial backload performed on 2024-06-10 (2023-01-01 to 2024-06-11) Production: Latest full backload performed on 2024-05-09
- Stage: Latest full backload performed on 2024-03-26 Latest partial backload performed on 2024-06-10 (2023-01-01 to 2024-06-11)
- Latest full backload performed on 2024-03-26
- Latest partial backload performed on 2024-06-10 (2023-01-01 to 2024-06-11)
- Production: Latest full backload performed on 2024-05-09
- Latest full backload performed on 2024-05-09

## Supported Attributes

### basedOn[]
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** Reference
- **Inputs:** ORC-2.1
- **Logic:** See child nodes for mappingOnly set if ORC-2.1 is not blankSee child attributes for additional mapping logic.

### basedOn[].identifier
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Identifier
- **Inputs:** ORC-2.1
- **Logic:** See child attributes for details.See child attributes for additional mapping logic.

### basedOn[].identifier.value
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** ORC-2.1
- **Notes:** A lab order initiated from Soft/RALS instead of entered in Epic will not triggeran HL7 ORM message for a ServiceRequest. Because there is no data in the HL7ORU message to indicate when this happens, this basedOn link is created anyway.

### basedOn[].identifier.system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/epic/service_request_id"
- **Notes:** A lab order initiated from Soft/RALS instead of entered in Epic will not triggeran HL7 ORM message for a ServiceRequest. Because there is no data in the HL7ORU message to indicate when this happens, this basedOn link is created anyway.

### basedOn[].type
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "ServiceRequest"

### category[a]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** CodeableConcept
- **Logic:** See child nodes for mappingSee child attributes for additional mapping logic.

### category[a].coding[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Coding
- **Logic:** See child nodes for mappingSee child attributes for additional mapping logic.

### category[a].coding[].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** Hard coded to constant value.
- **Constant Value:** "LAB"

### category[a].coding[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terminology.hl7.org/CodeSystem/v2-0074"

### category[a].coding[].display
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** Hard coded to constant value.
- **Constant Value:** "Laboratory"

### category[a].text
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** Hard coded to constant value.
- **Constant Value:** "Laboratory"

### category[ab]
**Cardinality:** Required

- **Cardinality:** 2..2
- **Type:** CodeableConcept
- **Logic:** (a)Must have 1 LAB category(b)Must have 1 other category

### category[b]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** CodeableConcept
- **Logic:** See child nodes for mappingSee child attributes for additional mapping logic.

### category[b].coding[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Coding
- **Logic:** See child nodes for mappingSee child attributes for additional mapping logic.

### category[b].coding[].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** OBR-24
- **Logic:** Use value OBR-24

### category[b].coding[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/codesystem/EPIC_ORDER_TYPE_CODE"

### category[b].coding[].display
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** OBR-24
- **Concept Map:** `http://terms.mayo.edu/mccfhir/translate/epic.order.type.code.to.name`
- **Logic:** If OBR-24 is blank, do not map.Lookup code from OBR-24 in concept map, and set to target displayIf the input does not have an entry in the Concept Map, execute the following action: Throw UnexpectedCodeExceptionIf the input is blank Concept Map, execute the following action: NONE

### category[b].text
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** If OBR-24 is not blank, set to same value as `category[b].coding[].display`

### code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** CodeableConcept
- **Inputs:** OBR-4
- **Logic:** See child nodes for mappingSee child attributes for additional mapping logic.
- **Notes:** 09-Dec-2021-12-09 Mapping coding from to LOINC omitted, because obtaining the map requires an enterprise-level request with wide-ranging impact across multiple systems

### code.coding[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Coding
- **Inputs:** OBR-4
- **Logic:** If OBR-4 is empty throw ExceptionIf OBR-4.1, OBR-4.2, OBR-4.3, OBR-4.5, OBR-4.9 are all missing throw ExceptionSee child attributes for additional mapping logic.

### code.coding[].code
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** code
- **Inputs:** OBR-4.1
- **Logic:** Use OBR-4.1Leave unpopulated if OBR-4.1 is blank

### code.coding[].system
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** uri
- **Inputs:** OBR-4.3
- **Logic:** If OBR 4.3 is blank do not setOtherwise, set to "http://terms.mayo.edu/mccfhir/lab/system/" + value of OBR 4.3. Example http://terms.mayo.edu/mccfhir/lab/system/CLEAP

### code.coding[].display
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** OBR-4.2, OBR-4.5, OBR-4.9
- **Logic:** Use OBR-4.2Use OBR-4.5 if OBR-4.2 is blankUse OBR-4.9 if OBR-4.5 is blankLeave unpopulated if OBR-4.9 is blank

### code.text
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** OBR-4.2, OBR-4.5, OBR-4.9
- **Logic:** Populate with the value of code.coding[].displayLeave unpopulated if code.coding[].display is not populated

### effectiveDateTime
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** dateTime
- **Inputs:** SPM-17, OBR-7, MSH-7
- **Logic:** Use SPM-17 if not blank and not all zerosUse OBR-7 if SPM-17 is blank or all zerosUse MSH-7 if OBR-7 is blank or all zerosThrow error if an invalid datetime except for the zeros aboveFormat as mapped value as YYYY-MM-DDThh:mm:ss+zz:zzConvert values to Central Time if necessary
- **Notes:** HL7DateParser.getFormattedDate() handles errant datetime strings wiht an exceptionHL7 DTM (datetime) format is `YYYY[MM[DD[HH[MM[SS[.S[S[S[S]]]]]]]]](+/-ZZZZ)`

### encounter
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Reference
- **Inputs:** PV1-19
- **Logic:** See child nodes for mappingThrow exception if PV1-19 is blankSee child attributes for additional mapping logic.

### encounter.identifier
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Identifier
- **Inputs:** PV1-19
- **Logic:** Throw exception if PV1-19 is blankSee child attributes for additional mapping logic.

### encounter.identifier.value
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** PV1-19

### encounter.identifier.system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/epic/csn"

### encounter.reference
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** Not mapped. Set during reconciliation of the resource.
- **Post Reconciliation Logic:** The literal reference is constructed as `Encounter/<resource id>` where the resource idis determined by querying the FHIR store for the `encounter.identifier.value` and `encounter.identifier.system`value provided by the mapper.`encounter.identifier` is not removed during reconciliation.

### encounter.type
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "Encounter"

### id
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** http://hl7.org/fhirpath/System.String
- **Logic:** Assigned by server on post

### identifier[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Identifier
- **Logic:** See child nodes for mappingSee child attributes for additional mapping logic.

### identifier[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/epic/diagnosticreport_id"

### identifier[].type
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** CodeableConcept
- **Logic:** See child nodes for mappingSee child attributes for additional mapping logic.

### identifier[].type.coding[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Coding
- **Logic:** See child nodes for mappingSee child attributes for additional mapping logic.

### identifier[].type.coding[].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** Hard coded to constant value.
- **Constant Value:** "diagnosticReport"

### identifier[].type.coding[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/mcc/assigned_identifier"

### identifier[].type.coding[].display
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** Hard coded to constant value.
- **Constant Value:** "DiagnosticReport"

### identifier[].type.text
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** Hard coded to constant value.
- **Constant Value:** "DiagnosticReport"

### identifier[].use
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** Hard coded to constant value.
- **Constant Value:** "usual"

### identifier[].value
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** OBR-2
- **Logic:** Throw exception if blank
- **Notes:** Placer order number

### issued
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** instant
- **Inputs:** OBR-22, MSH-7
- **Logic:** Use OBR-22 if not blankUse MSH-7 if OBR-22 is blankThrow an exception if MSH-7 is blank or not a valid timestampFormat as mapped value as YYYY-MM-DDThh:mm:ss+zz:zzConvert OBR-22/MSH-7 values to Central Time if necessary
- **Notes:** Time of verification (if present), otherwise last_update timestampHL7DateParser.getFormattedDate() handles errant datetime strings with an exceptionHL7 DTM (datetime) format is `YYYY[MM[DD[HH[MM[SS[.S[S[S[S]]]]]]]]](+/-ZZZZ)`

### meta
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Meta
- **Logic:** See child nodes for mappingSee child attributes for additional mapping logic.

### meta.lastUpdated
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** instant
- **Logic:** Assigned by server

### meta.source
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/mcc/datasource/epic"

### meta.tag[]
**Cardinality:** Optional

- **Cardinality:** 0..2
- **Type:** Coding
- **Logic:** See child nodes for mapping.

### meta.tag[a]
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** Coding
- **Logic:** See child nodes for mapping.See child attributes for additional mapping logic.

### meta.tag[a].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** MSH-7

### meta.tag[a].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/hl7v2-timestamp"

### meta.tag[b]
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** Coding
- **Logic:** See child nodes for mapping.See child attributes for additional mapping logic.

### meta.tag[b].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** MSH-10

### meta.tag[b].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/hl7v2-control-id"

### meta.versionId
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** id
- **Logic:** Assigned by server

### presentedForm[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Attachment
- **Logic:** Not mappedSee child attributes for additional mapping logic.

### presentedForm[].data
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** base64Binary
- **Logic:** The report includes the following information as available:-- Code, category-- Subject's MRN, last name, first name-- Effective datetime of the report-- Status-- Issued datetime-- For each observation: test name, value, interprestation, reference range, effective datetime of the observation

### presentedForm[].contentType
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** Hard coded to constant value.
- **Constant Value:** "text/plain"

### presentedForm[].title
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** Hard coded to constant value.
- **Constant Value:** "Laboratory Report"

### result[]
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** Reference
- **Inputs:** OBXs
- **Logic:** See child nodes for mappingThere will be one result[] for each OBX segment.See child attributes for additional mapping logic.

### result[].reference
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Logic:** No logic in mapping stage; see Reconcile
- **Post Reconciliation Logic:** Add literal reference to each Observation ID, e.g., `Observation/<actual obs id>`

### result[].type
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "Observation"

### specimen[]
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** Reference
- **Logic:** See child nodes for mappingSee child attributes for additional mapping logic.

### specimen[].display
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** SPM-4.9 or SPM-8.9
- **Logic:** Use SPM-4.9 if not blankElse, use SPM- 8.9 if not blankElse, leave unpopulated

### specimen[].type
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** uri
- **Inputs:** SPM-4.9, SPM-8.9
- **Logic:** Leave blank if SPM-4.9 and SPM-8.9 are both blank, otherwise set to "Specimen"

### status
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** OBR-25
- **Concept Map:** `mc.epic.out.res.ord.obr.res.status.has.fhir.diag.rpt.status`
- **Logic:** If OBR-25 is blank, set to REGISTEREDIf OBR-25 is X, set to CANCELLEDFor all other OBR-25, lookup code in concept map; throw an exception if OBR-25 is not found in the concept mapIf the input does not have an entry in the Concept Map, execute the following action: VARIES
- **Notes:** Internal: 2022-03-15 Clarity: use table ZC_LAB_STATUS

### subject
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Reference
- **Inputs:** PID-3.1
- **Logic:** See child nodes for mappingThrow exception if PID-3.1 is blankSee child attributes for additional mapping logic.

### subject.identifier
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** Identifier
- **Logic:** See child nodes for mappingSee child attributes for additional mapping logic.
- **Post Reconciliation Logic:** Removed during reconciliation.

### subject.identifier.value
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** PID-3.1
- **Logic:** Populate with PID-3.1Throw exception if PID-3.1 is blank
- **Post Reconciliation Logic:** Removed at time of reconcile in favor of `subject.reference`.Supported internally (for initial mapping / ingestion only).

### subject.identifier.system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/epic/mayo_clinic_number"
- **Post Reconciliation Logic:** Removed at time of reconcile in favor of `subject.reference`.Supported internally (for initial mapping / ingestion only).

### subject.reference
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Post Reconciliation Logic:** The subject.identifier.value and subject.identifier.system are used to identify the matching FHIR Patient resource.The resolved Patient/<FHIR ID> are placed into the subject.reference value and the subject.identifer attribute is removed.
- **Notes:** BigQuery column: `subject.patientId`

## Unsupported Attributes

| Attribute | Cardinality |
|---|---|
| basedOn[].reference Cardinality0..0TypestringLogicNot mapped | Not Supported |
| conclusion Cardinality0..0TypestringLogicNot mapped | Not Supported |
| conclusionCode[] Cardinality0..0TypeCodeableConceptLogicNot mapped | Not Supported |
| contained[] Cardinality0..0TypeResourceLogicNot mapped | Not Supported |
| extension[] Cardinality0..0TypeExtensionLogicNot mapped | Not Supported |
| imagingStudy[] Cardinality0..0TypeReferenceLogicNot mapped | Not Supported |
| implicitRules Cardinality0..0TypeuriLogicNot mapped | Not Supported |
| language Cardinality0..0TypecodeLogicNot mapped | Not Supported |
| media[] Cardinality0..0TypeBackboneElementLogicNot mapped | Not Supported |
| performer[] Cardinality0..0TypeReferenceLogicNot mapped | Not Supported |
| resultsInterpreter[] Cardinality0..0TypeReferenceLogicNot mapped | Not Supported |
| text Cardinality0..0TypeNarrativeLogicNot mapped. | Not Supported |

## Known Issues

None