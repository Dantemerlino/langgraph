# Patient Provided Information (PPI) Data Mart

## Description

Patient provided information containing questions and answers from Mayo forms. It is similar to Social History.

## Diagram

[![PPI Data Model](/assets/images/fact_ppi-9c463a39d53ee31cb6e37d8d7fd9e670.PNG)](https://mctools.sharepoint.com/:b:/r/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Data%20Models/3%29%20PPI/FACT_PPI_MCC.pdf)

## Dataset Information

- **Project Id:** `ml-mps-adl-intudp-phi-p-d5cb`
- **Dataset:** `phi_udpwh_etl_us_p`
- **Entitlement:** `MCC Live - AIDE UDP General Marts PROD Analytics`
  - [User Access](/docs/data-analytics/user-access) | [Service Account Access](/docs/data-analytics/service-account-access)

**Former DB2 Database:** EDT4P
**Update Frequency:** Updated Nightly
**Support Group:** UDP Data Integration

## Mapping Specifications

- [PPI](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/PPI/Business%20Spec%20and%20S2T/Rochester/Mapping_PPI.xlsx?d=w83dc0ed800e84960a8f630d1037abe72)
- [Epic](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/PPI/Business%20Spec%20and%20S2T/EPIC/Mapping_PPI.xlsx?d=w70b2252d98e649b69c771ecd6d6775d0)

## Example Query

### Fact Table Indexed Columns

**Note:** Subject to changes. Please use the following column(s) in your query filter for faster and more efficient data retrieval.

- `ROW_LOADED_DTM + PATIENT_DK`
- `SOURCE_SYSTEM_KEY + PATIENT_DK`
- `PATIENT_DK + QUESTION_DK`
- `QUESTION_DK + PATIENT_DK`
- `ANSWER_DTM + PATIENT_DK`

### Sample Query: 

This is a sample query to get you started. Query you need for your use case may be different than this sample.
```sql
SELECT ppia.ROW_ITERATION_NUMBER,
  ppia.ROW_CURRENT_INDICATOR,
  ppia.ROW_FROM_DTM,
  ppia.ROW_TO_DTM,
  ppia.ROW_SOURCE_ID,
  ppia.ROW_LOADED_DTM,
  ppia.SOURCE_SYSTEM_KEY,
  ppia.PATIENT_DK,
  ppia.PATIENT_AGE_AT_EVENT,
  ppia.PATIENT_GEO_CODE_AT_EVENT,
  ppia.PROVIDER_DK,
  ppia.LOCATION_DK,
  ppia.LOCATION_SITE_NAME,
  ppia.SOURCE_SYSTEM_DK,
  ppia.ANSWER_DATE_DK,
  ppia.ANSWER_TIME_DK,
  ppia.ANSWER_DTM,
  ppia.FORM_DK,
  ppia.QUESTION_DK,
  ppia.SHEET_NBR,
  ppia.ANSWER_PROVIDED_FLAG,
  ppia.ANSWER_VALUE,
  ppia.ANSWER_TXT,
  ppia.ANSWER_COUNT
FROM FACT_PPI_ANSWERS ppia
  JOIN EDTWH.DIM_PATIENT PT 
    ON (ppia.PATIENT_DK = PT.PATIENT_DK)
  JOIN EDTWH.DIM_HEALTHCARE_PROVIDER PROV
    ON (ppia.PROVIDER_DK = PROV.PROVIDER_DK)
  JOIN EDTWH.DIM_LOCATION LOC 
    ON (ppia.LOCATION_DK = LOC.LOCATION_DK)
  JOIN EDTWH.DIM_SOURCE_SYSTEM SRC
    ON (ppia.SOURCE_SYSTEM_DK = SRC.SOURCE_SYSTEM_DK)
  JOIN EDTWH.DIM_PPI_FORMS PPIF 
    ON (ppia.FORM_DK = PPIF.FORM_DK)
  JOIN EDTWH.DIM_PPI_QUESTIONS PPIQ
    ON (ppia.QUESTION_DK = PPIQ.QUESTION_DK)

--WHERE pt.PATIENT_CLINIC_NUMBER IN (123456, 876543) /* INSERT YOUR LIST OF CLINIC NUMBERS HERE) */
WHERE pt.PATIENT_DK IN (2478172, 2006140) /* INSERT YOUR LIST OF PATIENT_DK HERE) */
```