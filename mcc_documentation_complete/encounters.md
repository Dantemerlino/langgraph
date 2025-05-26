# Encounters Data Mart

## Description

Encounters are similar to ADT Location, telling one something happened somewhere in the system at some time.

## Diagram

[![Encounters Data Model](/assets/images/fact_encounter-d8d821c01bc0c81b7c0a23fab66bbaf8.PNG)](https://mctools.sharepoint.com/:b:/r/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Data%20Models/24%29%20Encounter/FACT_ENCOUNTER_MCC.pdf)

## Dataset Information

- **Project Id:** `ml-mps-adl-intudp-phi-p-d5cb`
- **Dataset:** `phi_udpwh_etl_us_p`
- **Entitlement:** `MCC Live - AIDE UDP General Marts PROD Analytics`
  - [User Access](/docs/data-analytics/user-access) | [Service Account Access](/docs/data-analytics/service-account-access)

**Former DB2 Database:** EDT4P
**Update Frequency:** Updated Nightly
**Support Group:** UDP Data Integration

## Mapping Specifications

- [RST - MICS](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Encounters/Business%20Spec%20and%20S2T/Rochester/MCR%20Encounters_Source_2_Target.xlsx?d=wff233e968d104f5292858cc0b43491f4)
- [ARZ/FLA - Cerner](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Encounters/Business%20Spec%20and%20S2T/Arizona_Florida/MCFLAZ_Cerner_Encounter_Source_2_Target.xlsx?d=w7a433daada3141bd9b535ed6e0fcb47f)
- [MCHS - Cerner](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Encounters/Business%20Spec%20and%20S2T/MCHS/MCHS_Cerner_Encounter_Source_2_Target.xlsx?d=w1090f415a6964df48447bd7a248fe206)
- [Epic](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Encounters/Business%20Spec%20and%20S2T/Epic/Epic_Encounters_Source_2_Target.xlsx?d=w3050ac0a22d44e8c8b30154428215598)

## Example Query

### Fact Table Indexed Columns

**Note:** Subject to changes. Please use the following column(s) in your query filter for faster and more efficient data retrieval.

- `ENCOUNTER_FPK + PATIENT_DK`
- `SOURCE_SYSTEM_KEY + PATIENT_DK`
- `PATIENT_DK`
- `ADMIT_DTM + DISCHARGE_DTM + PATIENT_DK`
- `EHR_ENCOUNTER_NUMBER + PATIENT_DK`
- `BILLING_ENCOUNTER_NUMBER + PATIENT_DK`
- `VISIT_NUMBER + PATIENT_DK`

### Sample Query: 

This is a sample query to get you started. Query you need for your use case may be different than this sample.
```sql
SELECT PT.PATIENT_CLINIC_NUMBER,EN.PATIENT_AGE_AT_EVENT,
  EN.LOCATION_SITE_NAME, EN.ADMIT_DTM, EN.DISCHARGE_DTM, EN.ENCOUNTER_CREATE_DTM, EN.ENCOUNTER_ARRIVE_DTM, EN.ENCOUNTER_UPDATE_DTM,
  ADM_PROV.PROVIDER_FIRST_NAME AS ADMIT_PROVIDER_FIRST_NAME, ADM_PROV.PROVIDER_LAST_NAME AS ADMIT_PROVIDER_LAST_NAME,
  DSCH_PROV.PROVIDER_FIRST_NAME AS DISCHARGE_PROVIDER_FIRST_NAME, DSCH_PROV.PROVIDER_LAST_NAME AS DISCHARGE_PROVIDER_LAST_NAME,
  LOC.LOCATION_CODE, LOC.LOCATION_DESCRIPTION,
  ATYP.ADMIT_TYPE_DESCRIPTION,
  SVC.CLINICAL_SERVICE_DESCRIPTION,
  DISP.DISCHARGE_DISPOSITION_DESCRIPTION,
  EN.EHR_ENCOUNTER_NUMBER, EN.BILLING_ENCOUNTER_NUMBER, EN.VISIT_NUMBER, EN.ACCOMODATION_CODE, 
  EN.REASON_FOR_VISIT, EN.VALID_FLAG, EN.EMERGENCY_FLAG, EN.LENGTH_OF_STAY
FROM EDTWH.FACT_ENCOUNTERS EN
  JOIN EDTWH.DIM_PATIENT PT
    ON (EN.PATIENT_DK = PT.PATIENT_DK)
  JOIN EDTWH.DIM_HEALTHCARE_PROVIDER ADM_PROV
   ON (EN.ADMIT_PROVIDER_DK=ADM_PROV.PROVIDER_DK)
  JOIN EDTWH.DIM_HEALTHCARE_PROVIDER DSCH_PROV
   ON (EN.DISCHARGE_PROVIDER_DK=DSCH_PROV.PROVIDER_DK)
  JOIN EDTWH.DIM_LOCATION LOC
    ON (EN.ADMIT_LOCATION_DK=LOC.LOCATION_DK)
  JOIN EDTWH.DIM_ADMIT_SOURCE SRC
    ON (EN.ADMIT_SOURCE_DK = SRC.ADMIT_SOURCE_DK)
  JOIN EDTWH.DIM_ADMIT_TYPE ATYP
    ON (EN.ADMIT_TYPE_DK = ATYP.ADMIT_TYPE_DK)
  JOIN EDTWH.DIM_CLINICAL_SERVICE SVC
    ON (EN.ADMIT_SERVICE_DK=SVC.CLINICAL_SERVICE_DK)
  JOIN EDTWH.DIM_DISCHARGE_DISPOSITION DISP
    ON (EN.DISCHARGE_DISPOSITION_DK=DISP.DISCHARGE_DISPOSITION_DK)
WHERE EN.ADMIT_DTM BETWEEN '2017-01-01-00.00.00.000000' AND '2017-01-31-23.59.59.999999'
  AND EHR_ENCOUNTER_NUMBER IN (123456)
  ```