# Appointment

## Characteristics

| Attribute | Value |
|---|---|
| FHIR Version | [R4 (4.0.1)](http://hl7.org/fhir/R4/appointment.html) |
| US Core Profile Id | None Assigned |
| Source System | Epic |
| Source Format | HL7v2 |
| Epic Bridge ID | 609502 |

## Notes

- Message Type (MSH-3.2): SIU_SURGICAL_UDP
- Trigger Type (MSH-9.1): SIU (This will always be SIU)
- The following common attributes are not supported for any nested elements unless explicitly included in the specification:`Element.id``Element.version``Element.userSelected``Element.extension[]``Element.modifierExtension[]`
- Backload History: Stage: Latest full backload performed on 2024-07-10 Production: Latest full backload performed on 2024-07-11 Latest full backload performed on 2024-08-18
- Stage: Latest full backload performed on 2024-07-10
- Latest full backload performed on 2024-07-10
- Production: Latest full backload performed on 2024-07-11 Latest full backload performed on 2024-08-18
- Latest full backload performed on 2024-07-11
- Latest full backload performed on 2024-08-18

## Supported Attributes

### appointmentType
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** CodeableConcept
- **Logic:** Nearly always available, but there is an extremely small amount of historical data that may not have this.See children attributes for detailsSee child attributes for additional mapping logic.

#### appointmentType.coding[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Coding
- **Logic:** See children attributes for detailsSee child attributes for additional mapping logic.

#### appointmentType.coding[].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** PV1-2.1
- **Concept Map:** `http://terms.mayo.edu/systemid/terms/termsconceptmap/id`
- **Logic:** NOTE: Refer to Encounter's parser (encounterClass) for code implementation and temporary workarounds.Lookup PV1-2.1 in the specified ConceptMaps.Set this to the value from the ConceptMap `code` value for the matching concept.If the input does not have an entry in the Concept Map, execute the following action: EXCEPTION

#### appointmentType.coding[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Inputs:** PV1-2.1
- **Concept Map:** `http://terms.mayo.edu/systemid/terms/termsconceptmap/id`
- **Logic:** NOTE: Refer to Encounter's parser (encounterClass) for code implementation and temporary workarounds.Lookup PV1-2.1 in the specified ConceptMaps.Set this to the value from the ConceptMap `system` value for the matching concept.If the input does not have an entry in the Concept Map, execute the following action: EXCEPTION

#### appointmentType.coding[].display
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** PV1-2.1
- **Concept Map:** `http://terms.mayo.edu/systemid/terms/termsconceptmap/id`
- **Logic:** NOTE: Refer to Encounter's parser (encounterClass) for code implementation and temporary workarounds.Lookup PV1-2.1 in the specified ConceptMaps.Set this to the value from the ConceptMap `display` value for the matching concept.If the input does not have an entry in the Concept Map, execute the following action: EXCEPTION

### basedOn[]
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** Reference
- **Inputs:** SCH-26
- **Logic:** There will be a `basedOn` element if SCH-26 is populated. If it is blank/empty, `basedOn` will not be provided.See child attributes for additional mapping logic.

#### basedOn[].identifier
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Identifier
- **Logic:** See child attributes for details.See child attributes for additional mapping logic.

#### basedOn[].identifier.value
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** SCH-26
- **Logic:** Use the value from SCH-26 if present.The parent `basedOn` attribute will not be set if SCH-26 is blank/empty.These identifiers are not resolved to literal ServiceRequest references.

#### basedOn[].identifier.system
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
- **Logic:** Only populated if `status` is "cancelled" and if "SCH-6" is non-empty.Some possible values (not an exhaustive list)`Clinic: Appt``Clinic: Equi``Clinic: Requ``Clinic: Sche``COVID``Patient: Hos``Patient: Req``Patient: Tra``Provider: Re``Provider: Te`If the input does not have an entry in the Concept Map, execute the following action: NONE

### cancelationReason.coding[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/epic/cancelation_reason"

### end
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** instant
- **Inputs:** SCH-9.1SCH-10.1
- **Logic:** The `end` time will be calculated -- Add the `minutesDuration` to the `start` time to determine the `end` time.As `start` is optional (in the case of unscheduled or canceled appointments), the `end` time is also optionalThe timezone should be consistent with the `start` timezone.

### id
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** http://hl7.org/fhirpath/System.String
- **Post Reconciliation Logic:** Assigned by server on post.

### identifier[]
**Cardinality:** Required

- **Cardinality:** 1..2
- **Type:** Identifier
- **Inputs:** PV1-19OBX-3.1OBX-5
- **Logic:** There will always be at least one identifier (representing the appointment id) and optionally an identifier for the contact serial number (CSN / encounter number). These are generally the same, but can differ if the appointment has been rescheduled.For the purposes of this specification, `identifier[a]` refers to the appointment identifier while `identifier[b]` refers to the CSN identifier.See child attributes for details

### identifier[a]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Identifier
- **Logic:** This represents the appointment id identifier.See child attributes for detailsSee child attributes for additional mapping logic.

### identifier[a].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/epic/appointment_id"

### identifier[a].value
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** SCH-2
- **Logic:** Use the value as is from SCH-2 (this is the unique business key identifying for the appointment)Throw exception if empty/blankThe reconciler's lock will be placed on this identifier

### identifier[b]
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** Identifier
- **Logic:** This represents the contact serial number (CSN / encounter number) identifier.This identifier is generally available, but not guaranteedSee child attributes for detailsSee child attributes for additional mapping logic.

### identifier[b].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** uri
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/epic/csn"

### identifier[b].value
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** PV1-19OBX-3.1OBX-5
- **Logic:** Use the value from PV1-19 if PV1-19 is non-empty.If PV1-19 is empty, iterate through the OBX segments following the PV1 segment. Select the OBX segment that has an OBX-3.1 value equal to "SURG_CSN" if present. Use the value from OBX-5 from this segment.If PV1-19 is empty and no OBX segment matching the desired criteria is found, do not set this identifier.

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
- **Logic:** SCH-9.1 is the appointment duration value (in either seconds or minutes) -- If the value is blank/empty or zero, `minutesDuration` will not be populated (e.g., unscheduled or canceled appointment); If the value is a negative number, throw TransformExceptionIf SCH-10.1 is "MIN", then the duration value is already represented in minutes. Use SCH-9.1 as is.If SCH-10.1 is "S", then the duration value is represented in "seconds". Convert the SCH-9.1 value from seconds to minutes.For any other SCH-10.1 value, throw TransformException

### participant[Location]
**Cardinality:** Optional

- **Cardinality:** 0..3
- **Type:** BackboneElement
- **Inputs:** AIL-3.4PV1-3.4AIL-3.2
- **Logic:** If AIL-3.4 is available, there will be a "Location" item in the array and its children attributes will be populated -- This represents the OR location.If PV1-3.4 is available, there will be a "Location" item in the array and its children attributes will be populated -- This represents the facility.If AIL-3.2 is available, there will be a "Location" item in the array and its children attributes will be populated -- This represents the OR room and bed description.Otherwise, there will not be a "Location" item in the `participant` array.See child attributes for additional mapping logic.

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
- **Inputs:** AIL-3.4PV1-3.4AIL-3.2
- **Logic:** For the parent `Location` mapped by AIL, populate with value from AIL-3.4 if present -- If not present, there will not be a "Location" item in the parent `participant` array (This identifier will be resolved to a literal reference at this time).For the parent `Location` mapped by PV1, populate with value from PV1-3.4 if present -- If not present, there will not be a "Location" item in the parent `participant` array (This identifier will not be resolved to a literal reference at this time).For the parent `Location` mapped by AIL, populate with value from AIL-3.2 if present -- If not present, there will not be a "Location" item in the parent `participant` array (This identifier will not be resolved to a literal reference at this time).
- **Post Reconciliation Logic:** This location identifier will be resolved to a literal location reference during reconciliation for identifier.system value "http://terms.mayo.edu/mccfhir/systemid/epic/location/department_id".

### participant[Location].actor.display
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** string
- **Inputs:** AIL-3.4PV1-3.4AIL-3.2
- **Logic:** For the parent `Location` mapped by AIL, populate with AIL-3.4 if the value is not blank/empty.For the parent `Location` mapped by PV1, populate with PV1-3.4 if the value is not blank/empty.For the parent `Location` mapped by AIL, populate with AIL-3.2 if the value is not blank/empty.

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
- **Logic:** For the parent `Location` mapped by AIL, populate with "http://terms.mayo.edu/mccfhir/systemid/epic/location/department_id"For the parent `Location` mapped by PV1, populate with "http://terms.mayo.edu/mccfhir/systemid/epic/location/facility_id"
- **Post Reconciliation Logic:** This person ID will be resolved to a literal practitioner reference during reconciliation.

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
- **Logic:** For the parent `Location` mapped by AIL, populate with "LOC"For the parent `Location` mapped by PV1, populate with "LOC"

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
- **Logic:** For the parent `Location` mapped by AIL, populate with "location"For the parent `Location` mapped by PV1, populate with "location"

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
- **Inputs:** AIP-3PV1-8
- **Logic:** There may be up to 2 Practitioner participants; one for AIP-3 and PV1-8 if presentNot all fields will always be presentMapping each field:-- AIP-3 and PV1-8 can be a repeated fields with '' as the separater character-- If a person has multiple IDs (for different systems), the field will be repeated-- The ID value comes from component 1 (AIP-3.1 and PV1-8.1)-- Take the value identified as a "PERID" in component 9 (AIP-3.9 and PV1-8.9)-- Example: 12345678^McTester^Test^T^^^^^PERID^^^^PERID9876543^McTester^Test^T^^^^^PROVID^^^^PROVIDThe person identifiers will not be resolved to literal Practitioner resource references during reconciliationparticipant.actor(practitioner).identifier.value = AIP-3.1participant.actor(practitioner).identifier.value - PV1-8.1See child attributes for additional mapping logic.

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
- **Inputs:** AIP-3.1PV1-8.1
- **Logic:** For the parent `Practitioner` mapped by AIP, populate with value from AIP-3.4 if present -- If not present, there will not be a "Practitioner" item in the parent `participant` array (This identifier will be resolved to a literal reference at this time).For the parent `Practitioner` mapped by PV1, populate with value from PV1-8.1 if present -- If not present, there will not be a "Practitioner" item in the parent `participant` array (This identifier will be resolved to a literal reference at this time).For each field (above) present in the HL7 message, there will be a participant.This person ID will be resolved to a literal practitioner reference during reconciliation.
- **Post Reconciliation Logic:** This person ID will be resolved to a literal practitioner reference during reconciliation.

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
- **Inputs:** AIP-3PV1-8
- **Logic:** For the participant populated for AIP-3, the value will be "PPRF"For the participant populated for PV1-8, the value will be "REF"See parent `participant[Practitioner]` attribute for details.Code values from: https://terminology.hl7.org/3.1.0/CodeSystem-v3-ParticipationType.html

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
- **Inputs:** AIP-3PV1-8
- **Logic:** For the participant populated for AIP-3, the value will be "primary performer"For the participant populated for PV1-8, the value will be "referrer"See parent `participant[Practitioner]` attribute for details.Display values from: https://terminology.hl7.org/3.1.0/CodeSystem-v3-ParticipationType.html

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
- **Constant Value:** "surgery"

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
- **Constant Value:** "Surgery"

### serviceCategory[].text
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** CodeableConcept
- **Logic:** Hard coded to constant value.
- **Constant Value:** "Surgery"

### serviceType[]
**Cardinality:** Required

- **Cardinality:** 1..*
- **Type:** CodeableConcept
- **Logic:** An HL7 message may have multiple `AIS` segmentsThere will be an item in the `serviceType[]` array for each `AIS` segmentSee child attributes for details.INI: ORPSee child attributes for additional mapping logic.

### serviceType[].coding[]
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** Coding
- **Logic:** See child attributes for details.See child attributes for additional mapping logic.

### serviceType[].coding[].code
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** AIS-3.1
- **Logic:** Populate with AIS-3.1If blank/empty, throw TranformationException

### serviceType[].coding[].system
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Logic:** Hard coded to constant value.
- **Constant Value:** "http://terms.mayo.edu/mccfhir/systemid/epic/service_type"

### serviceType[].coding[].display
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** AIS-3.2
- **Logic:** Populate with AIS-3.2 if available. Do not set this if AIS-3.2 is blank/empty.

### serviceType[].text
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** string
- **Inputs:** NTE-3
- **Logic:** Only examine the NTE segment immediately following the corresponding AIS segmentPopulate with NTE-3If there is no NTE segment or if NTE-3 is blank/empty, then `text` will not be populated

### start
**Cardinality:** Optional

- **Cardinality:** 0..1
- **Type:** instant
- **Inputs:** SCH-11.4PV1-3.4MSH-5
- **Logic:** Start time is taken from SCH-11.4 -- This may be blank/empty if the appointment is unschedule or if it has been canceled.Timezone will default to US Central time.Timezone code should also handle Daylight Savings adjustments

### status
**Cardinality:** Required

- **Cardinality:** 1..1
- **Type:** code
- **Inputs:** SCH-25.1SCH-25.4OBX-3OBX-5SCH-11.4
- **Concept Map:** `http://terms.mayo.edu/systemid/terms/termsconceptmap/id|10001413`
- **Logic:** First if there is an OBX segment which has an OBX-3 value of "SchedulingStatus" -- Map the OBX-5 value to concept map 10001413 (If the mapping is not found use local mapping)Second if SCH-25.4 is populated -- If the start time (SCH-11.4) is available, set to `fulfilled`; If start time is not available, set to `proposed`Third if SCH-25.1 is populated -- Map the SCH-25.1 value to concept map 10001413 (If the mapping is not found use local mapping)If nothing is available, throw TransformExceptionINI info:-- SCH-25.4 is populated from ORC 512-- SCH-25.1 is populated from ORC 510 and ORL 510, but for the purposes of this mapping only ORC 510 is consideredClarity Info:-- SCH-25.4 values from: `SELECT ABBR, NAME FROM ZC_OR_PAT_STATUS ORDER BY CASE_PROGRESS_C`-- SCH-25.1 values from: `SELECT ABBR, NAME FROM ZC_OR_SCHED_STATUS ORDER BY SCHED_STATUS_C`If the input does not have an entry in the Concept Map, execute the following action: TransformException

## Unsupported Attributes

| Attribute | Cardinality |
|---|---|
| basedOn[].reference Cardinality0..0TypestringLogicidentifiers are not resolved to literal ServiceRequest references.Post Reconciliation LogicNot currently resolved to literal references | Not Supported |
| basedOn[].type Cardinality0..0Typeuri | Not Supported |
| cancelationReason.coding[].display Cardinality0..0TypestringInputsSCH-6.1Concept Maphttp://terms.mayo.edu/mccfhir/translate/epic.cancel.reason.code.to.nameLogicDo not set if SCH-6.1 is blank.Translate the SCH-6.1 value to a human-readable value and set to this attribute (A ConceptMap can be created based on the Clarity ZC_CANCEL_REASON table -- SELECT ABBR AS SOURCE, ABBR AS TARGET_CODE, NAME AS TARGET_DISPLAY FROM ZC_CANCEL_REASON)If the translation lookup doesn't find a match, set this attribute as SCH-6.1 valueIf the input does not have an entry in the Concept Map, execute the following action: NONE | Not Supported |
| cancelationReason.text Cardinality0..0TypeCodingInputsSCH-6LogicValue from cancelationReason.coding[].display | Not Supported |
| comment Cardinality0..0Typestring | Not Supported |
| created Cardinality0..0TypedateTime | Not Supported |
| description Cardinality0..0Typestring | Not Supported |
| meta.profile[] Cardinality0..0Typecanonical | Not Supported |
| meta.security[] Cardinality0..0TypeCoding | Not Supported |
| participant[Patient].actor.display Cardinality0..0Typestring | Not Supported |
| participant[Practitioner].actor.display Cardinality0..0Typestring | Not Supported |
| participant[Practitioner].actor.reference Cardinality0..0TypestringLogicThe person's ID will be resolved to a literal practitioner resource referencePost Reconciliation LogicThe person's ID will be resolved to a literal practitioner resource reference | Not Supported |
| patientInstruction Cardinality0..0Typestring | Not Supported |
| priority Cardinality0..0TypeunsignedInt | Not Supported |
| reasonCode[] Cardinality0..0TypeCodeableConceptLogicCan be enhanced with DG1 if needed | Not Supported |
| reasonReference[] Cardinality0..0TypeReference | Not Supported |
| requestedPeriod[] Cardinality0..0TypePeriod | Not Supported |
| slot[] Cardinality0..0TypeReference | Not Supported |
| specialty[] Cardinality0..0TypeCodeableConceptLogicWhile this attribute isn't supported, the department's specialty can be found by checking the referenced location resource. | Not Supported |
| text Cardinality0..0TypeNarrative | Not Supported |

## Known Issues

None