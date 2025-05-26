# Appointment

## Characteristics

| Attribute | Value |
|---|---|
| FHIR Version | [R4 (4.0.1)](http://hl7.org/fhir/R4/appointment.html) |
| US Core Profile Id | None Assigned |
| Source System | Epic |
| Source Format | HL7v2 |
| Epic Bridge ID | 609500 |

## Notes

- Latest backload (PROD): 2024.02.25 (full)
- Message Type (MSH-3.2): SIU_GENERIC
- Trigger Type (MSH-9.1): SIU (This will always be SIU)
- The following common attributes are not supported for any nested elements unless explicitly included in the specification:<br />`Element.id`<br />`Element.version`<br />`Element.userSelected`<br />`Element.extension[]`<br />`Element.modifierExtension[]`
- If an appointment is rescheduled, the LPR FHIR resource will be associated with the original CSN.
- Backload History: Stage: Latest full backload performed on 2024-01-27 Latest partial backload performed on 2024-06-13 (2016-01-01 to 2024-06-10) Production: Latest full backload performed on 2024-02-25 Latest full backload performed on 2024-08-18
- Stage: Latest full backload performed on 2024-01-27 Latest partial backload performed on 2024-06-13 (2016-01-01 to 2024-06-10)
- Latest full backload performed on 2024-01-27
- Latest partial backload performed on 2024-06-13 (2016-01-01 to 2024-06-10)
- Production: Latest full backload performed on 2024-02-25 Latest full backload performed on 2024-08-18
- Latest full backload performed on 2024-02-25
- Latest full backload performed on 2024-08-18

## Supported Attributes

### appointmentType
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** CodeableConcept
- **Logic:** See children attributes for detailsSee child attributes for additional mapping logic.
- **Notes:** Represents the patient class at the time the appointment was scheduled or appointment was updated. Does not reflect encounter class changes over time (e.g., if the patient changed from emergency to inpatient) where-as EAPIS/Epic does reflect change over time.

### appointmentType.coding[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Coding
- **Logic:** See children attributes for detailsSee child attributes for additional mapping logic.

### appointmentType.coding[].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** PV1-2.1
- **Concept Map:** `http://terms.mayo.edu/systemid/terms/termsconceptmap/id|10001293, http://terms.mayo.edu/systemid/terms/termsconceptmap/id|10001187, http://terms.mayo.edu/systemid/terms/termsconceptmap/id|10001294, http://terms.mayo.edu/systemid/terms/termsconceptmap/id|10001190`
- **Logic:** NOTE: Refer to Encounter's parser (encounterClass) for code implementation and temporary workarounds.Lookup PV1-2.1 in the specified ConceptMaps.Set this to the value from the ConceptMap `code` value for the matching concept.If the input does not have an entry in the Concept Map, execute the following action: EXCEPTION

### appointmentType.coding[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Inputs:** PV1-2.1
- **Concept Map:** `http://terms.mayo.edu/systemid/terms/termsconceptmap/id|10001293, http://terms.mayo.edu/systemid/terms/termsconceptmap/id|10001187, http://terms.mayo.edu/systemid/terms/termsconceptmap/id|10001294, http://terms.mayo.edu/systemid/terms/termsconceptmap/id|10001190`
- **Logic:** NOTE: Refer to Encounter's parser (encounterClass) for code implementation and temporary workarounds.Lookup PV1-2.1 in the specified ConceptMaps.Set this to the value from the ConceptMap `system` value for the matching concept.If the input does not have an entry in the Concept Map, execute the following action: EXCEPTION

### appointmentType.coding[].display
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** PV1-2.1
- **Concept Map:** `http://terms.mayo.edu/systemid/terms/termsconceptmap/id|10001293, http://terms.mayo.edu/systemid/terms/termsconceptmap/id|10001187, http://terms.mayo.edu/systemid/terms/termsconceptmap/id|10001294, http://terms.mayo.edu/systemid/terms/termsconceptmap/id|10001190`
- **Logic:** NOTE: Refer to Encounter's parser (encounterClass) for code implementation and temporary workarounds.Lookup PV1-2.1 in the specified ConceptMaps.Set this to the value from the ConceptMap `display` value for the matching concept.If the input does not have an entry in the Concept Map, execute the following action: EXCEPTION

### basedOn[]
**Cardinality:** Optional

- **Cardinality:** 0..*
- **Type:** Reference
- **Inputs:** ZOR[x]-1SCH-26
- **Logic:** ZOR can be a repeated segment. Take the order # (ZOR-1) from all ZOR segments.ZOR-1 and SCH-26 are likely the same if both are providedTake the distinct placer order numbers from these fields. These are the ServiceRequest identifiers.Note: Not referencing the ZOR-8 for now. This is a parent order #. I would expect the child order, represented by a ServiceRequest resource, to have a reference to the parent order. Therefore, we don't need the parent order referenced by the Appointment resource.See child attributes for additional mapping logic.
- **Post Reconciliation Logic:** Resolve the identifiers to literal ServiceRequest resource references during reconciliation.

### basedOn[].identifier
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Identifier
- **Logic:** See child attributes for details.See child attributes for additional mapping logic.

### basedOn[].identifier.value
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** ZOR[x]-1SCH-26
- **Logic:** ZOR can be a repeated segment. Take the order # (ZOR-1) from all ZOR segments.Take the distinct placer order numbers from these fields.These identifiers are not resolved to literal ServiceRequest references.See parent `basedOn` attribute for more details.

### basedOn[].identifier.system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/epic/service_request_id"

### cancelationReason
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** CodeableConcept
- **Inputs:** SCH-6.1
- **Logic:** This attribute will be populated if the appointment status is "cancelled" and SCH-6.1 is not empty/blank.Otherwise, it will not be populated.See child attributes for additional mapping logic.

### cancelationReason.coding[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Coding
- **Logic:** This attribute will always be present if the parent `cancelationReason` attribute is present.See child attributes for details.See child attributes for additional mapping logic.

### cancelationReason.coding[].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** SCH-6.1
- **Concept Map:** `http://terms.mayo.edu/mccfhir/translate/epic.cancel.reason.code.to.name`
- **Logic:** Only populated if `status` is "cancelled" and if "SCH-6.1" is non-empty. Lookup TARGET_CODE.Some possible values (not an exhaustive list)`Clinic: Appt``Clinic: Equi``Clinic: Requ``Clinic: Sche``COVID``Patient: Hos``Patient: Req``Patient: Tra``Provider: Re``Provider: Te`If the input does not have an entry in the Concept Map, execute the following action: NONE

### cancelationReason.coding[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/epic/cancelation_reason"

### comment
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** NTE-3
- **Logic:** Parse NTE segments immediately following the SCH segment.Do not include other NTE segments found elsewhere in the HL7 message.Can be multiple NTE segments, concatenate comments with \r\n

### end
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** instant
- **Inputs:** SCH-11.5SCH-9.1SCH-10.1
- **Logic:** If SCH-11.5 is present, this represents the appointment's end time. This field is not populated for a large number of HL7 messages.If SCH-11.5 is not present, the `end` time will be calculated (Add the `durationMinutes` to the `start` time to determine the `end` time).As `start` is optional (in the case of unscheduled or canceled appointments), the `end` time is also optionalThe timezone should be consistent with the `start` timezone.

### id
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** http://hl7.org/fhirpath/System.String
- **Post Reconciliation Logic:** Assigned by server on post.

### identifier[]
**Cardinality:** Required

- **Cardinality:** 1..2
- **Type:** Identifier
- **Logic:** `identifier[a]` details the CSN identifier (This identifier will be always available).`identifier[b]` details the appointment ID identifier (This identifier will only be available for rescheduled Appointment resources).See child attributes for details.
- **Notes:** `identifier[b]` details the appointment ID identifier, however this identifier will only be available for rescheduled Appointment resources.

### identifier[a]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Identifier
- **Logic:** `identifier[a]` details the CSN identifierThis identifier will be always available.See child attributes for detailsSee child attributes for additional mapping logic.

### identifier[a].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/epic/csn"

### identifier[a].use
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** Hard coded to constant value.
- **Constant Value:** "usual"

### identifier[a].value
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** PV1-19
- **Logic:** PV1-19 is the contact serial number (CSN)As this is the only identifier, if PV1-19 is blank/empty the pipeline will be throwing and exception.

### identifier[b]
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** Identifier
- **Logic:** `identifier[b]` details the appointment ID identifierThis identifier will only be available for rescheduled Appointment resources.See child attributes for detailsSee child attributes for additional mapping logic.

### identifier[b].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/epic/appointment_id"

### identifier[b].use
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** Hard coded to constant value.
- **Constant Value:** "old"

### identifier[b].value
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** SCH-2
- **Logic:** SCH-2 is the appointment IDThis identifier is required for rescheduled appointments, so if SCH-2 is blank/empty for a rescheduled appointment the pipeline will be throw an exception.

### meta
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Meta
- **Logic:** See child attributes for additional mapping logic.

### meta.lastUpdated
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** instant
- **Post Reconciliation Logic:** Updated automatically by the FHIR server each time the resource is updated / edited.

### meta.security[]
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** Coding
- **Inputs:** ZPL-3
- **Logic:** If ZPL-3 is "Yes", this `security` attribute will be populated.Otherwise ("No", blank, any other value), this `security` attribute will not be populated.See child attributes for additional mapping logic.

### meta.security[].display
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** Hard coded to constant value.
- **Constant Value:** "no disclosure without organizational authorization"

### meta.security[].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** ZPL-3
- **Logic:** If ZPL-3 is "Yes", set to "NOORGPOL"Otherwise ("No", blank, any other value), the parent `security` attribute will not be populated.

### meta.security[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terminology.hl7.org/CodeSystem/v3-ActCode"

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

### meta.tag[c]
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** Coding
- **Logic:** See child nodes for mapping.See child attributes for additional mapping logic.

### meta.tag[c].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** MSH-6.1

### meta.tag[c].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/epic/rec_fac_id"

### meta.tag[d]
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** Coding
- **Logic:** See child nodes for mapping.See child attributes for additional mapping logic.

### meta.tag[d].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** MSH-3.2

### meta.tag[d].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/epic/sending_app_id"

### meta.versionId
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** id
- **Logic:** Assigned as a unique version identifier when the resource is created or updated.

### minutesDuration
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** positiveInt
- **Inputs:** SCH-9.1SCH-10.1SCH-10.1
- **Logic:** SCH-9.1 is the appointment duration value -- If the value is blank/empty or zero, `minutesDuration` will not be populated (e.g., unscheduled or canceled appointment); If the value is a negative number, throw TransformException.If SCH-10.1 is "MIN", then the duration value is already represented in minutes. Use SCH-9.1 as is.If SCH-10.1 is "S", then the duration value is represented in "seconds". Convert the SCH-9.1 value from seconds to minutes.For any other SCH-10.1 value, throw TransformException

### participant[Location]
**Cardinality:** Optional

- **Cardinality:** 0..3
- **Type:** BackboneElement
- **Inputs:** RGS-3.1PV1-3.4ZPL-2.1
- **Logic:** If RGS-3.1 is available, there will be a "Location" item in the array and its children attributes will be populated -- This represents the department (For example: "101002028" which represents "RST GIM ROGO" or "Division of General Internal Medicine in Rochester, Minnesota" at the Gonda Building)RGS-3.1 (HL7) = DEP .1 ID (INI)RGS-3.2 (HL7) = DEP .2 Department Name (INI)If PV1-3.4 is available, there will be a "Location" item in the array and its children attributes will be populated -- This represents the facility (For example: "ROSMC").If ZPL-2.1 is available, there will be a "Location" item in the array and its children attributes will be populated -- This represents the patient's check-in or arrival location (For example: "ROGO 17 DESK 17S" which stands for "Gonda Building, Seventeenth Floor, Desk 17 South")ZPL-2.1 (HL7) = PLF .2 (INI) = Clarity's CL_PLF.RECORD_NAME WHERE PT_LOC_TYPE_C = 11 (arrival location)Otherwise, if none of the above are available, there will not be a "Location" item in the `participant` array.See child attributes for additional mapping logic.

### participant[Location].actor
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Reference
- **Logic:** See child attributes for details.See child attributes for additional mapping logic.

### participant[Location].actor.identifier
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Identifier
- **Logic:** See child attributes for details.See child attributes for additional mapping logic.

### participant[Location].actor.identifier.value
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** RGS-3.1PV1-3.4ZPL-2.1AIG-3.1
- **Logic:** For the parent `Location` mapped by RGS, populate with value from RGS-3.1 if present -- If not present, there will not be a "Location" item in the parent `participant` array (This identifier will be resolved to a literal reference at this time).For the parent `Location` mapped by PV1, populate with value from PV1-3.4 if present -- If not present, there will not be a "Location" item in the parent `participant` array (This identifier will not be resolved to a literal reference at this time).For the parent `Location` mapped by ZPL, populate with value from ZPL-2.1 if present -- If not present, there will not be a "Location" item in the parent `participant` array (This identifier will not be resolved to a literal reference at this time).For the parent `Location` mapped by AIG, populate with value from AIG-3.1 if present -- If not present, there will not be a "Location" item in the parent `participant` array (This identifier will not be resolved to a literal reference at this time).
- **Post Reconciliation Logic:** This person ID will be resolved to a literal practitioner reference during reconciliation, except for the participant derived from AIG segment.

### participant[Location].actor.display
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** RGS-3.2PV1-3.4ZPL-2.2AIG-3.2
- **Logic:** For the parent `Location` mapped by RGS, populate with RGS-3.2 if the value is not blank/empty.For the parent `Location` mapped by PV1, populate with PV1-3.4 if the value is not blank/empty.For the parent `Location` mapped by ZPL, populate with ZPL-2.2 if the value is not blank/empty.For the parent `Location` mapped by AIG, populate with AIG-3.2 if the value is not blank/empty.
- **Post Reconciliation Logic:** Only

### participant[Location].actor.type
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "Location"

### participant[Location].actor.identifier.system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** For the parent `Location` mapped by RGS, populate with "http://terms.mayo.edu/mccfhir/systemid/epic/location/department_id"For the parent `Location` mapped by PV1, populate with "http://terms.mayo.edu/mccfhir/systemid/epic/location/facility_id"For the parent `Location` mapped by ZPL, populate with "http://terms.mayo.edu/mccfhir/systemid/epic/location/arrival_id"For the parent `Location` mapped by AIG, populate with "http://terms.mayo.edu/mccfhir/systemid/epic/provid"
- **Post Reconciliation Logic:** This location identifier will be resolved to a literal location reference during reconciliation, if the system value among any values mentioned in logic section except "http://terms.mayo.edu/mccfhir/systemid/epic/provid". If unresolvable then we should encounter an exception.

### participant[Location].status
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Reference
- **Logic:** Hard coded to constant value.
- **Constant Value:** "accepted"

### participant[Location].type[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** CodeableConcept
- **Logic:** See child and parent `participant[Location]` attributes for details.See child attributes for additional mapping logic.

### participant[Location].type[].coding[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Coding
- **Logic:** See child attributes for details.See child attributes for additional mapping logic.

### participant[Location].type[].coding[].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** For the parent `Location` mapped by RGS, populate with "LOC"For the parent `Location` mapped by PV1, populate with "LOC"For the parent `Location` mapped by ZPL, populate with "LOC"

### participant[Location].type[].coding[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terminology.hl7.org/CodeSystem/v3-ParticipationType"

### participant[Location].type[].coding[].display
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** For the parent `Location` mapped by RGS, populate with "location"For the parent `Location` mapped by PV1, populate with "location"For the parent `Location` mapped by ZPL, populate with "location"

### participant[Patient]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** BackboneElement
- **Inputs:** PID-3.1
- **Logic:** There will always be one Patient participantPID-3.1 (patient's MRN) will be resolved to a literal FHIR referenceparticipant.actor(practitioner).identifier.value = PID-3.1See child attributes for additional mapping logic.

### participant[Patient].actor
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Reference
- **Logic:** See child attributes for details.See child attributes for additional mapping logic.

### participant[Patient].actor.identifier
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Identifier
- **Logic:** This identifier will not be present in the final FHIR resource as the reference will be resolved to a literal reference (rather than logical).See child attributes for details.See child attributes for additional mapping logic.

### participant[Patient].actor.identifier.value
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** PID-3.1
- **Logic:** There will be one Patient-typed participantThe patient's MRN from PID-3.1 is required. Throw TransformException if not available.This patient's MRN will be resolved to a literal patient reference during reconciliation.If the identifier cannot be resolved to a patient resource, throw TransformException
- **Post Reconciliation Logic:** This patient's MRN will be resolved to a literal practitioner reference during reconciliation.If the identifier cannot be resolved to a patient resource, throw TransformException

### participant[Patient].actor.reference
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** The patient's MRN will be resolved to a literal patient resource referenceIf the identifier cannot be resolved to a patient resource, throw TransformException
- **Post Reconciliation Logic:** The patient's MRN will be resolved to a literal practitioner resource referenceIf the identifier cannot be resolved to a patient resource, throw TransformException

### participant[Patient].actor.type
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "Patient"

### participant[Patient].actor.identifier.system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/epic/mayo_clinic_number"

### participant[Patient].status
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Reference
- **Logic:** Hard coded to constant value.
- **Constant Value:** "accepted"

### participant[Patient].type[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** CodeableConcept
- **Logic:** See child and parent `participant` attributes for details.See child attributes for additional mapping logic.

### participant[Patient].type[].coding[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Coding
- **Logic:** See child attributes for details.See child attributes for additional mapping logic.

### participant[Patient].type[].coding[].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** Hard coded to constant value.
- **Constant Value:** "SBJ"

### participant[Patient].type[].coding[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terminology.hl7.org/CodeSystem/v3-ParticipationType"

### participant[Patient].type[].coding[].display
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** Hard coded to constant value.
- **Constant Value:** "subject"

### participant[Practitioner]
**Cardinality:** Required

- **Cardinality:** 1..4
- **Type:** BackboneElement
- **Inputs:** SCH-20PV1-7PV1-8PV1-9
- **Logic:** There may be up to 4 Practitioner participants; one for each of SCH-20, PV1-7, PV1-8, and PV1-9 (if present)Not all fields will always be presentMapping each field:The person identifiers will not be resolved to literal Practitioner resource references during reconciliationparticipant.actor(practitioner).identifier.value = SCH-20.1participant.actor(practitioner).identifier.value = PV1-7.1participant.actor(practitioner).identifier.value - PV1-8.1participant.actor(practitioner).identifier.value = PV1-9.1See child attributes for additional mapping logic.

### participant[Practitioner].actor
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Reference
- **Logic:** See child attributes for details.See child attributes for additional mapping logic.

### participant[Practitioner].actor.identifier
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Identifier
- **Logic:** See child attributes for details.See child attributes for additional mapping logic.

### participant[Practitioner].actor.identifier.value
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** SCH-20.1PV1-7.1PV1-8.1PV1-9.1AIG-3.1
- **Logic:** For the parent `Practitioner` mapped by RGS, populate with value from SCH-20.1 if present -- If not present, there will not be a "Practitioner" item in the parent `participant` array (This identifier will be resolved to a literal reference at this time).For the parent `Practitioner` mapped by PV1, populate with value from PV1-7.1 if present -- If not present, there will not be a "Practitioner" item in the parent `participant` array (This identifier will be resolved to a literal reference at this time).For the parent `Practitioner` mapped by ZPL, populate with value from PV1-8.1 if present -- If not present, there will not be a "Practitioner" item in the parent `participant` array (This identifier will be resolved to a literal reference at this time).For the parent `Practitioner` mapped by AIG, populate with value from PV1-9.1 if present -- If not present, there will not be a "Practitioner" item in the parent `participant` array (This identifier will be resolved to a literal reference at this time).For the parent `Practitioner` mapped by AIG, populate with value from AIG-3.1 if present -- If not present, there will not be a "Practitioner" item in the parent `participant` array (This identifier will not be resolved to a literal reference at this time).For AIG-3.1 will be Practitioner identifier if AIG-4.1 is 1.This person ID will be resolved to a literal practitioner reference during reconciliation for all mappings except AIG-3.1.

### participant[Practitioner].actor.type
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "Practitioner"

### participant[Practitioner].actor.identifier.system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/epic/perid"

### participant[Practitioner].status
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Reference
- **Logic:** Hard coded to constant value.
- **Constant Value:** "accepted"

### participant[Practitioner].type[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** CodeableConcept
- **Logic:** See parent `participant` attribute for details.See child attributes for additional mapping logic.

### participant[Practitioner].type[].coding[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Coding
- **Logic:** See child attributes for details.See child attributes for additional mapping logic.

### participant[Practitioner].type[].coding[].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** See parent `participant[Practitioner]` attribute for details.Code values from: https://terminology.hl7.org/3.1.0/CodeSystem-v3-ParticipationType.html

### participant[Practitioner].type[].coding[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terminology.hl7.org/CodeSystem/v3-ParticipationType"

### participant[Practitioner].type[].coding[].display
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** See parent `participant[Practitioner]` attribute for details.Display values from: https://terminology.hl7.org/3.1.0/CodeSystem-v3-ParticipationType.html

### participant[Practitioner].type[].text
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Coding
- **Logic:** Value from `participant[Practitioner].type[].coding[].display`See parent `participant[Practitioner]` attribute for details.

### participant[]
**Cardinality:** Required

- **Cardinality:** 2..7
- **Type:** BackboneElement
- **Inputs:** SCH-20PV1-7PV1-8PV1-9
- **Logic:** There are 3 types of participants associated with an appointment (Patient, Practitioner, HealthcareService)Patient - represents the patient whom this appointment is forPractitioner - represents healthcare professionals involved in the appointmentHealthcareService - represents the department that the appointment falls underSee the attribute titled `participant[](ResourceType)` for details specific to these participantsWhen searching for appointment resources by patient, the FHIR server will interpret the `patient` query parameter and search for the patient-typed participantWhen searching for appointment resources by practitioner, the FHIR server will interpret the `practitioner` query parameter and search for the patient-typed participantThe `actor` query parameter can more generically be used to search for any type of participant

### serviceCategory[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** CodeableConcept
- **Logic:** See child attributes for more detail.See child attributes for additional mapping logic.

### serviceCategory[].coding[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Coding
- **Logic:** See child attributesSee child attributes for additional mapping logic.

### serviceCategory[].coding[].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** Hard coded to constant value.
- **Constant Value:** "appointment"

### serviceCategory[].coding[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/codesystem/appointment-service-category"

### serviceCategory[].coding[].display
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Logic:** Hard coded to constant value.
- **Constant Value:** "Appointment"

### serviceCategory[].text
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** CodeableConcept
- **Logic:** Hard coded to constant value.
- **Constant Value:** "Appointment"

### serviceType[]
**Cardinality:** Optional

- **Cardinality:** 0..2
- **Type:** CodeableConcept
- **Logic:** Nearly always available, but there is an extremely small amount of historical data that may not have this.First coding is for local/raw HL7 code, and second coding is for code looked up from concept map.See child attributes for details.Create map based on PRC (INI) / CLARITY_PRC (Clarity)Map HL7 value to EPT 7100 values to get something friendlier. EPT 7100 ID points to PRC INI.Don't give SCH-7.1 (abbreviation) value in the resource as many things have the same abbr.Lookup SCH-7.2 in PRC .2 -- SELECT PRC_ID, PRC_NAME, EXTERNAL_NAME FROM CLARITY_PRC WHERE PRC_NAME = "`SCH-7.2`"-- Populate serviceType.coding.code = PRC_ID-- Populate serviceType.coding.display = SCH-7.2-- Populate serviceType.text = EXTERNAL_NAME (PRC 901). If null default to PRC_NAMESee child attributes for additional mapping logic.

### serviceType[].coding[0]
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** Coding
- **Logic:** This coding is direct from the HL7, and is first in the array of codings.See child attributes for details.See child attributes for additional mapping logic.

### serviceType[].coding[0].code
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** code
- **Inputs:** SCH-7.1
- **Logic:** Populate with SCH-7.1If blank/empty, log warning

### serviceType[].coding[0].system
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** code
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/epic/local_service_type"

### serviceType[].coding[1]
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** Coding
- **Logic:** This coding is the looked up value from the HL7, and is second in the array of codings.See child attributes for details.See child attributes for additional mapping logic.

### serviceType[].coding[1].display
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** SCH-7.2
- **Concept Map:** `http://terms.mayo.edu/mccfhir/translate/epic.clarity.prc.code.to.name`
- **Logic:** Populate with lookup from SCH-7.2.If the returned lookup returns a blank value for display, populate with "SCH-7.2".If blank/empty, log warningIf the input does not have an entry in the Concept Map, execute the following action: NONE

### serviceType[].coding[1].code
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** code
- **Inputs:** SCH-7.2
- **Concept Map:** `http://terms.mayo.edu/mccfhir/translate/epic.clarity.prc.code.to.name`
- **Logic:** If blank/empty, log warningSCH-7.1 is not used here as multiple different codings can have the same SCH-7.1 value (abbrevation)Populate with lookup based on SCH-7.2 -- SELECT PRC_ID, PRC_NAME, EXTERNAL_NAME FROM CLARITY_PRC WHERE PRC_NAME = "`SCH-7.2`" (Populate serviceType.coding.code = PRC_ID (PRC .1))If the input does not have an entry in the Concept Map, execute the following action: NONE

### serviceType[].coding[1].system
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** code
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/epic/service_type"

### serviceType[].coding[]
**Cardinality:** Optional

- **Cardinality:** 0..2
- **Type:** Coding
- **Logic:** The first coding is direct from the HL7, the second coding is the result of the lookup.See child attributes for details.

### serviceType[].coding[0].display
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** SCH-7.2
- **Logic:** Populate with SCH-7.2If blank/empty, log warning

### start
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** instant
- **Inputs:** SCH-11.4
- **Logic:** Start time is taken from SCH-11.4This may be blank/empty if the appointment is unschedule or if it has been canceled.Timezone will default to US Central time.

### status
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** AIS-10AIS-10
- **Concept Map:** `http://terms.mayo.edu/systemid/terms/termsconceptmap/id 10001363`
- **Logic:** If AIS-10 is blank/empty, default to "proposed" -- Nearly always available, but there is an extremely small amount of historical data that may not have this.Map AIS-10 value based on the table below. Evaluate as case-insensitive just to be safe.EPT 7020https://datahandbook.epic.com/ClarityDictionary/Details?tblName=ZC_APPT_STATUSMapping is hardcoded for nowNeed to ingest TERMS mapping from UDP into a ConceptMap once it is ready.If the input does not have an entry in the Concept Map, execute the following action: UnexpectedCodeException
- **Notes:** Certain source status values will not be represented as fulfilled in the LPR resource. Most notably this will affect visit types of Hospice and e-visits.

## Unsupported Attributes

| Attribute | Cardinality |
|---|---|
| basedOn[].reference Cardinality0..0TypestringLogicidentifiers are not resolved to literal ServiceRequest references.Post Reconciliation LogicNot currently resolved to literal references | Not Supported |
| basedOn[].type Cardinality0..0Typeuri | Not Supported |
| cancelationReason.coding[].display Cardinality0..0TypestringInputsSCH-6.1Concept Maphttp://terms.mayo.edu/mccfhir/translate/epic.cancel.reason.code.to.nameLogicDo not set if SCH-6.1 is blank. Lookup TARGET_DISPLAY.Translate the SCH-6.1 value to a human-readable value and set to this attribute (A ConceptMap can be created based on the Clarity ZC_CANCEL_REASON table -- SELECT ABBR AS SOURCE, ABBR AS TARGET_CODE, NAME AS TARGET_DISPLAY FROM ZC_CANCEL_REASON)If the translation lookup doesn't find a match, set this attribute as SCH-6.1 valueIf the input does not have an entry in the Concept Map, execute the following action: NONE | Not Supported |
| cancelationReason.text Cardinality0..0TypeCodingInputsSCH-6.1LogicValue from cancelationReason.coding[].display | Not Supported |
| created Cardinality0..0TypedateTime | Not Supported |
| description Cardinality0..0Typestring | Not Supported |
| meta.profile[] Cardinality0..0Typecanonical | Not Supported |
| participant[Patient].actor.display Cardinality0..0Typestring | Not Supported |
| participant[Practitioner].actor.display Cardinality0..0Typestring | Not Supported |
| participant[Practitioner].actor.reference Cardinality0..0TypestringLogicThe person's ID will be resolved to a literal practitioner resource referencePost Reconciliation LogicThe person's ID will be resolved to a literal practitioner resource reference | Not Supported |
| patientInstruction Cardinality0..0TypestringLogicNot availableDeferred workINI: PRC 910Clarity: CL_PRC_PT_INSTR | Not Supported |
| priority Cardinality0..0TypeunsignedInt | Not Supported |
| reasonCode[] Cardinality0..0TypeCodeableConcept | Not Supported |
| reasonReference[] Cardinality0..0TypeReference | Not Supported |
| requestedPeriod[] Cardinality0..0TypePeriod | Not Supported |
| serviceType[].text Cardinality0..0TypestringInputsSCH-7.2Concept Maphttp://terms.mayo.edu/mccfhir/translate/epic.clarity.prc.code.to.nameLogicUse SCH-7.2 to lookup EXTERNAL_NAME (PRC 901) or TARGET_DISPLAY. If EXTERNAL_NAME is null PRC_NAME is the default value.Refer to parent serviceType for more details.If the input does not have an entry in the Concept Map, execute the following action: NONE | Not Supported |
| slot[] Cardinality0..0TypeReference | Not Supported |
| specialty[] Cardinality0..0TypeCodeableConceptLogicWhile this attribute isn't supported, the department's specialty can be found by checking the referenced location resource. | Not Supported |
| supportingInformation[] Cardinality0..0TypeReference | Not Supported |
| text Cardinality0..0TypeNarrative | Not Supported |

## Known Issues

None