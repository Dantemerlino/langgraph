# Radiology Data Mart

## Description

Diagnostic procedures and results, i.e. MRI, CT Scan.

## Diagram

[![Radiology Data Model](/assets/images/fact_radiology-7bf5fc9f3732378615ccca52c444843f.PNG)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Data%20Models/18%29%20Radiology/FACT_RADIOLOGY_MCC.pdf)

## Dataset Information

- **Project Id:** `ml-mps-adl-intudp-phi-p-d5cb`
- **Dataset:** `phi_udpwh_etl_us_p`
- **Entitlement:** `MCC Live - AIDE UDP General Marts PROD Analytics`
  - [User Access](/docs/data-analytics/user-access) | [Service Account Access](/docs/data-analytics/service-account-access)

**Former DB2 Database:** EDT4P
**Update Frequency:** Updated Nightly
**Support Group:** UDP Data Integration

## Mapping Specifications

- RIMS (RST/ARZ/FLA) - was migrated to Epic
- [Cerner (MCHS)] - was migrated to Epic
- [Epic](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Radiology/Business%20Spec%20and%20S2T/Epic/EPIC_Radiology_Source_2_Target.xlsx?d=w5751047555aa4fbc997252f7f62d304c)

## Example Query

### Fact Table Indexed Columns

**Note:** Subject to changes. Please use the following column(s) in your query filter for faster and more efficient data retrieval.

- `PATIENT_DK`
- `ENCOUNTER_NUMBER`
- `RADIOLOGY_DTM`
- `ORDER_ID`
- `SERVICE_MODALITY_CODE`
- `RADIOLOGY_FPK`

### Sample Query: 

This is a sample query to get you started. Query you need for your use case may be different than this sample.
```sql
SELECT RAD.PATIENT_DK, RAD.PATIENT_AGE_AT_EVENT, RAD.LOCATION_SITE_NAME, RAD.RADIOLOGY_DTM, RAD.RADIOLOGY_REVIEW_DTM, RAD.ENCOUNTER_NUMBER, RAD.ORDER_ID,
  RAD.ACCESSION_NBR, RAD.SERVICE_MODALITY_CODE, RAD.SERVICE_MODALITY_DESCRIPTION, RAD.SERVICE_STATUS, RAD.SERVICE_RESULT_STATUS,
  RAD.CONTRIBUTOR_SYSTEM, RAD.RADIOLOGY_REPORT_ID, RAD.RADIOLOGY_REPORT_VERSION,
  PROV.PROVIDER_FIRST_NAME, PROV.PROVIDER_MIDDLE_NAME,
  RADLOC.LOCATION_CODE, RADLOC.LOCATION_DESCRIPTION,
  RADTST.RADIOLOGY_TEST_CODE, RADTST.RADIOLOGY_TEST_DESCRIPTION
FROM EDTWH.FACT_RADIOLOGY RAD
  JOIN EDTWH.DIM_PATIENT PT
    ON (RAD.PATIENT_DK = PT.PATIENT_DK)
  JOIN EDTWH.DIM_HEALTHCARE_PROVIDER PROV
    ON (RAD.ORDERING_PROVIDER_DK=PROV.PROVIDER_DK)
  JOIN EDTWH.DIM_HEALTHCARE_PROVIDER RPROV
    ON (RAD.RESULT_PROVIDER_DK=RPROV.PROVIDER_DK)
  JOIN EDTWH.DIM_LOCATION RADLOC
    ON (RAD.LOCATION_DK=RADLOC.LOCATION_DK)
  JOIN EDTWH.DIM_SOURCE_SYSTEM SYS
    ON (RAD.SOURCE_SYSTEM_DK = SYS.SOURCE_SYSTEM_DK)
  JOIN EDTWH.DIM_RADIOLOGY_TEST_NAME RADTST
    ON (RAD.RADIOLOGY_TEST_NAME_DK = RADTST.RADIOLOGY_TEST_NAME_DK)
WHERE RAD.RADIOLOGY_DTM BETWEEN '2016-06-01 00:00:00' AND '2016-12-31 23:59:59'
  AND RAD.ORDER_ID IN ('19423631','19234039','18365329')
  AND RAD.SERVICE_MODALITY_CODE IN ('DG','NR','NM')
  ```