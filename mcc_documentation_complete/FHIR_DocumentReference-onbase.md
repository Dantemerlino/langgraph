# DocumentReference-onbase

## Characteristics

| Attribute | Value |
|---|---|
| FHIR Version | [R4 4.0.1](http://hl7.org/fhir/R4/documentreference.html) |
| US Core Profile Id | [us-core-documentreference](https://hl7.org/fhir/us/core/STU4/StructureDefinition-us-core-documentreference.html) |
| Source System | Onbase |
| Source Format | TXT, PDF |
| Epic Bridge ID | NA |

## Notes

- All source field names are OnBase document metadata key names.
- [known issues](/docs/data-analytics/longitudinal-patient-record/lpr-bugs)
- [known issues](/docs/data-analytics/longitudinal-patient-record/lpr-bugs)
- [known issues](/docs/data-analytics/longitudinal-patient-record/lpr-bugs)

## Supported Attributes

### category[]
**Cardinality:** Optional

- **Cardinality:** 0..4
- **Type:** CodeableConcept
- **Logic:** See child attributes for mapping information.
- **Notes:** The category[] list supports up to four categories with no specific ordering:where system = 'http://terms.mayo.edu/mccfhir/systemdata/onbase/keyitem_document_sub_type', represented in the specification as identifier[subtype].where system = 'http://terms.mayo.edu/mccfhir/systemdata/onbase/keyitem_legacy_document_type', represented in the specification as identifier[legacy_type].where system = 'http://terms.mayo.edu/mccfhir/systemdata/onbase/keyitem_legacy_document_sub_type', represented in the specification as identifier[legacy_subtype].where system = 'http://terms.mayo.edu/mccfhir/systemdata/onbase/keyitem_legacy_system', represented in the specification as identifier[legacy].

### category[legacy]
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** CodeableConcept
- **Logic:** See child attributes for additional mapping logic.

### category[legacy].coding[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Coding
- **Logic:** See child attributes for additional mapping.See child attributes for additional mapping logic.

### category[legacy].coding[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemdata/onbase/keyitem_legacy_system"

### category[legacy].coding[].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** Legacy System
- **Logic:** Replace any repeated occurrences of whitespace with a single occurrence (e.g., " " becomes " ")

### category[legacy].text
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** Legacy System

### category[legacy_subtype]
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** CodeableConcept
- **Logic:** See child attributes for additional mapping logic.

### category[legacy_subtype].coding[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Coding
- **Logic:** See child attributes for additional mapping.See child attributes for additional mapping logic.

### category[legacy_subtype].coding[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemdata/onbase/keyitem_legacy_document_sub_type"

### category[legacy_subtype].coding[].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** Legacy Document Sub Type
- **Logic:** Replace any repeated occurrences of whitespace with a single occurrence (e.g., " " becomes " ")

### category[legacy_subtype].text
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** Legacy Document Sub Type

### category[legacy_type]
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** CodeableConcept
- **Logic:** See child attributes for additional mapping logic.

### category[legacy_type].coding[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Coding
- **Logic:** See child attributes for additional mapping.See child attributes for additional mapping logic.

### category[legacy_type].coding[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemdata/onbase/keyitem_legacy_document_type"

### category[legacy_type].coding[].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** Legacy Document Type
- **Logic:** Replace any repeated occurrences of whitespace with a single occurrence (e.g., " " becomes " ")

### category[legacy_type].text
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** Legacy Document Type

### category[subtype]
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** CodeableConcept
- **Logic:** See child attributes for additional mapping logic.

### category[subtype].coding[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Coding
- **Logic:** See child attributes for additional mapping.See child attributes for additional mapping logic.

### category[subtype].coding[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemdata/onbase/keyitem_document_sub_type"

### category[subtype].coding[].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** Doc Sub Type
- **Logic:** Replace any repeated occurrences of whitespace with a single occurrence (e.g., " " becomes " ")

### category[subtype].text
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** Doc Sub Type

### content[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** BackboneElement
- **Logic:** There must be at least 1 content and a max of 1 contentSee child attributes for additional mapping logic.

### content[].attachment
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Attachment
- **Logic:** See child attributes for additional mapping logic.

### content[].attachment.url
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** url
- **Logic:** URL of the content in gcs.The value of the destination is determined by the pipeline based upon the document type. The logic for that determination is internal and users should not rely upon any convention in paths or file naming.Throw an exception if it cannot be obtained.

### content[].attachment.contentType
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** content type of the object in gcsThrow an exception if it cannot be obtained.

### context
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** BackboneElement
- **Logic:** See children attributes for specific mapping.If no child attributes are mapped, do not create context.See child attributes for additional mapping logic.

### context.encounter[]
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** Reference
- **Inputs:** CSN
- **Logic:** If CSN is blank or empty, do not include context.encounterSee child attributes for additional mapping logic.

### context.encounter[].identifier
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Identifier
- **Logic:** See child attributes for additional mapping logic.

### context.encounter[].identifier.system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/epic/csn"

### context.encounter[].reference
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Post Reconciliation Logic:** The reference to the patient (in format Patient/<FHIR ENCOUNTER ID>) will be added as part of the reconciliation process.

### context.encounter[].type
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "Encounter"

### context.encounter[].identifier.value
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** CSN
- **Logic:** If CSN is not blank, use itIf CSN is blank, do not include a encounter reference in context

### context.practiceSetting
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** CodeableConcept
- **Inputs:** Facility Name
- **Logic:** If Facility Name is blank, do not create a practice setting entry.See child attributes for additional mapping logic.

### context.practiceSetting.coding[]
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** Coding
- **Inputs:** Facility Name
- **Logic:** Only include a value for practice setting if Facility Name is not blankSee child attributes for additional mapping logic.

### context.practiceSetting.coding[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemdata/onbase/keyitem_facility_name"

### context.practiceSetting.coding[].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** Facility Name
- **Logic:** If Facility Name is blank, do not create a practice setting entry.

### context.practiceSetting.text
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** Facility Name
- **Notes:** This will be the same value as context.practiceSetting.coding[0].display

### date
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** instant
- **Inputs:** Document Date
- **Notes:** This date is sourced from the OnBase Document Date field, which is actually the closest approximation of the date and time that the document was indexed into OnBase. This is the datetime at which consumers of the OnBase application are capable of viewing / searching the document. On certain documents, the time component may be truncated.

### extension
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Extension
- **Logic:** See child attributes for additional mapping logic.

### extension.extension[]
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** Extension
- **Logic:** Create one extension for each keyword that is valued in the OnBase metadata for the document and is one of the following:"Admit Date""Admit Type""Assigning Authority""Assistant Result Interpreter ID""Assistant Result Interpreter ID Type""Assistant Result Interpreter Last Name""Case #""CC - Pending Relationship""Chart Facility""Chart Site""Collection Date Time""CSN""Date of Service""DC - Correction Reason""DC - Correction Relationship""DC - Import Source""DC - Parent Document Handle""DC - Previous Doc Type""Department""Description""Discharge Date""DocName""Doc Type Code""Document Handle""Document Type""Due Date""Encounter Type""Epic Capture Department""Epic Capture Location""External Import Source""External Integration Status""Fax From Number""Fax Received Date Time""Fax Receiving Location""Fax Unique ID""HAR""Image ID""Import Location""Indexed By""LAB Case #""LAB Diagnosis""LAB Diagnosis (2)""LAB Diagnosis (3)""LAB Diagnosis (4)""LAB Diagnosis (5)""LAB DOB""LAB Legacy Document Type""LAB Pathology Date""LAB Pathology Date (formatted)""LAB Pathology Report Text (1)""LAB Pathology Report Text (2)""LAB Pathology Report Text (3)""LAB Pathology Report Text (4)""LAB Pathology Report Text (5)""LAB Pathology Report Text (6)""LAB Pathology Report Text (7)""LAB Tissue Source""LAB Tissue Source (2)""Legacy Batch Number""Legacy Commit User""Legacy Conversion ID""Legacy Department""Legacy Discharge Date""Legacy Document Event""Legacy Document Event Description""Legacy Document ID""Legacy Document Number""Legacy Document Source""Legacy Document Type""Legacy Document Type Code""Legacy Encounter""Legacy End DateTime""Legacy Facility Code""Legacy MRN Facility Code""Legacy Note""Legacy Original Source""Legacy Provider""Observation Date""Observation Date Time""Ordering Provider ID""Ordering Provider ID Type""Ordering Provider Last Name""Patient Class""Physician ID""Principal Result Interpreter ID""Principal Result Interpreter ID Type""Principal Result Interpreter Last Name""Procedure Code""Provider Service Code""QA Reviewed By""RC Correspondence Date""RC Legacy Appt or Print Date""RC Legacy Auth Scan Location""RC Legacy Auth Type""RC Legacy Cert Number""RC Legacy ICN Number""RC Legacy Visit Number""RC Site""Result Date""Result Date Time""Result Status""ROI AM/PM""ROI External Complete""ROI Internal Mayo""ROI Note""ROI Patient Present""ROI Release ID""ROI Requester""ROI Sent To Epic""ROI Site""ROI Special Task Type""ROI Unknown DOB""ROI Unknown First Name""ROI Unknown Last Name""ROI User""Scan Date Time""Scan User""Sending Application""Sent to Epic""Service/Type""Universal Service Identifier"See child attributes for additional mapping logic.
- **Notes:** Any extensions whose values are Dates or Date and Time are represented as strings without timezone. The times are captured exactly as presented in the OnBase source system metadata which also have no time zones. Users relying on these extensions must interpret the dates and times based upon the context of the document, such as which site it was performed in. Generally speaking, documents with dates of 2023 and newer represent central time.Numeric values are stored with valueDecimal.All other values are stored as strings.

### extension.extension[].valueString
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Coding
- **Logic:** Use the keyword / metadata value as-is

### extension.extension[].url
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** url
- **Logic:** Use the keyword / metadata key as-is

### extension.url
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** url
- **Logic:** Hard coded to constant value.
- **Constant Value:** "gs://keywords/definitions/"

### id
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** id
- **Post Reconciliation Logic:** Assigned by server.
- **Notes:** Users MUST NOT rely upon the formatting of this attribute or expect deterministic values across DocumentReference resources for this attribute. Specifically, this id may be assigned or randomly generated as a UUID. In some cases it may match the internal OnBase DocHandle for some periods of time, but in general shall not.

### identifier[]
**Cardinality:** Required

- **Cardinality:** 1..3
- **Type:** Identifier
- **Logic:** 
- **Notes:** The identifier[] list supports three identifiers with no specific ordering:where system = 'http://terms.mayo.edu/mccfhir/systemid/onbase/document_id', represented in the specification as identifier[docid]. This is the unique business key for OnBase DocumentReference resources.where system = 'http://terms.mayo.edu/mccfhir/systemid/epic/iims/exam_id', represented in the specification as identifier[order].where system = 'http://terms.mayo.edu/mccfhir/systemid/epic/accession', represented in the specification as identifier[accession].

### identifier[accession]
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** Identifier
- **Inputs:** Accession #
- **Logic:** See child attributes for additional mapping logic.
- **Notes:** If no 'Accession #' key is present, do not create this identifier instance.See child attributes for additional mapping.

### identifier[accession].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/epic/accession"

### identifier[accession].value
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** Accession #

### identifier[docid]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Identifier
- **Inputs:** DocHandle
- **Logic:** See child attributes for additional mapping logic.

### identifier[docid].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/onbase/document_id"

### identifier[docid].value
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** DocHandle

### identifier[order]
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** Identifier
- **Inputs:** Order #
- **Logic:** If no 'Order #' key is present, do not create this identifier instance.See child attributes for additional mapping.See child attributes for additional mapping logic.
- **Notes:** See subfields for mapping details.

### identifier[order].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/epic/iims/exam_id"

### identifier[order].value
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** Order #

### meta
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Meta
- **Logic:** See child attributes for additional mapping logic.
- **Notes:** See subfields for mapping logic

### meta.lastUpdated
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** instant
- **Logic:** Set by server, do not map

### meta.versionId
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** id
- **Logic:** Added by server. Do not map

### status
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** If created/updated then "current"If deleted then "entered-in-error"

### subject
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Reference
- **Inputs:** MRN
- **Logic:** See child attributes for additional mapping logic.

### subject.identifier
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Identifier
- **Logic:** See child attributes for additional mapping logic.

### subject.identifier.value
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** MRN

### subject.identifier.system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/originating-patient-identifier"

### subject.reference
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Post Reconciliation Logic:** The reference to the patient (in format Patient/<FHIR PATIENT ID>) will be added as part of the reconciliation process based upon the subject.identifier.system and subject.identifier.value values.

### subject.type
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "Patient"

### type
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** CodeableConcept
- **Inputs:** Document Type
- **Logic:** See child attributes for additional mapping logic.

### type.coding[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Coding
- **Logic:** See child attributes for additional mapping logic.

### type.coding[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/codesystem/ONBASE_DOCTYPE"

### type.coding[].display
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** Document Type

### type.text
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** Document Type

## Unsupported Attributes

| Attribute | Cardinality |
|---|---|

## Known Issues

None