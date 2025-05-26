# Problem List Data Mart

## Description

Represents the problems noted for a patient and internal coding related to the problem list.

## Diagram

[![Problem List Data Model](/assets/images/fact_problem_list-38e72b4de342dc87edb0e62313db6587.PNG)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Data%20Models/38%29%20Problem%20List/FACT_PROBLEM_LIST_MCC.pdf)

## Dataset Information

- **Project Id:** `ml-mps-adl-intudp-phi-p-d5cb`
- **Dataset:** `phi_udpwh_etl_us_p`
- **Entitlement:** `MCC Live - AIDE UDP General Marts PROD Analytics`
  - [User Access](/docs/data-analytics/user-access) | [Service Account Access](/docs/data-analytics/service-account-access)

**Former DB2 Database:** EDT4P
**Update Frequency:** Updated Nightly
**Support Group:** UDP Data Integration

## Mapping Specifications

- [Cerner (ARZ/FLA)](https://mctools.sharepoint.com)
- [Cerner (MCHS)](https://mctools.sharepoint.com)
- [Epic](https://mctools.sharepoint.com)

## Example Query

### Fact Table Indexed Columns

**Note:** Subject to changes. Please use the following column(s) in your query filter for faster and more efficient data retrieval.

- `PROBLEM_NAME_DK + PATIENT_DK`
- `PROBLEM_ENTRY_DTM + PROBLEM_NAME_DK + PATIENT_DK`
- `PATIENT_DK + PROBLEM_NAME_DK`
- `ENCOUNTER_NUMBER + PATIENT_DK + PROBLEM_NAME_DK`
- `ROW_LOADED_DTM + PATIENT_DK`
- `SOURCE_SYSTEM_KEY + ROW_SOURCE_ID`

### Sample Query:

 This is a sample query to get you started. Query you need for your use case may be different than this sample.
```sql
 SELECT
  P.PATIENT_DK,
  t.PATIENT_CLINIC_NUMBER,
  p.ENCOUNTER_NUMBER,
  p.PRINCIPAL_PROBLEM_YN_FLAG,
  p.HOSPITAL_PROBLEM_YN_FLAG,
  p.PROBLEM_STATUS,
  p.CHRONIC_YN_FLAG,
  p.PROBLEM_COMMENT,
  p.PROBLEM_STATUS,
  p.PROBLEM_ENTRY_DTM,
  p.PROBLEM_ENTRY_date_dk,
  p.PROBLEM_ENTRY_time_dk,
  p.PROBLEM_NOTED_DTM,
  p.PROBLEM_NOTED_date_dk,
  p.PROBLEM_NOTED_time_dk,
  p.PROBLEM_RESOLVED_DTM,
  p.PROBLEM_RESOLVED_date_dk,
  p.PROBLEM_RESOLVED_time_dk,
  p.INACTIVE_DTM,
  p.INACTIVE_DATE_DK,
  p.INACTIVE_TIME_DK,
  p.PROBLEM_PRIORITY,
  p.PROBLEM_CLASS,
  p.PROBLEM_PRESENT_ON_ADM,
  n.PROBLEM_NAME,
  n.MAPPED_ICD9_CODE,
  n.MAPPED_ICD10_CODE,
  n.PROBLEM_GROUP_NAME,
  n.PROBLEM_NAME_TYPE
FROM EDTWH.FACT_PROBLEM_LIST p
  INNER JOIN EDTWH.DIM_PROBLEM_NAME n
    ON p.PROBLEM_NAME_DK = n.PROBLEM_NAME_DK
  INNER JOIN EDTWH.DIM_PATIENT t 
    ON p.PATIENT_DK = t.PATIENT_DK
  INNER JOIN edtwh.dim_location l 
    ON p.LOCATION_DK = l.LOCATION_DK
  INNER JOIN EDTWH.DIM_HEALTHCARE_PROVIDER h
    ON h.PROVIDER_DK = p.ENTERING_PROVIDER_DK
WHERE upper (n.PROBLEM_NAME) LIKE '%AMYLOID%'
  AND p.PROBLEM_NOTED_DTM BETWEEN '2021-01-01 00:00:00'
  AND '2021-04-01 00:00:00'
```