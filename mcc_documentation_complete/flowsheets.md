# Flowsheets Data Mart

## Description

Patient measure information taken throughout the duration of a visit or stay, (Observations).

## Diagram

[![Flowsheets Data Model](/assets/images/fact_flowsheets-9045d37abffd9351abaf3afa880a5ff1.PNG)](https://mctools.sharepoint.com/:b:/r/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Data%20Models/6%29%20Flowsheets/FACT_FLOWSHEETS_MCC.pdf)

## Dataset Information

- **Project Id:** `ml-mps-adl-intudp-phi-p-d5cb`
- **Dataset:** `phi_udpwh_etl_us_p`
- **Entitlement:** `MCC Live - AIDE UDP General Marts PROD Analytics`
  - [User Access](/docs/data-analytics/user-access) | [Service Account Access](/docs/data-analytics/service-account-access)

**Former DB2 Database:** EDT4P
**Update Frequency:** Updated Nightly
**Support Group:** UDP Data Integration

## Mapping Specifications

- [MICS (RST)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Flowsheets/Business%20Spec%20and%20S2T/Rochester/Mapping_Flowsheets.xlsx?d=wcc439fec2b774ed5a9197a2e51a99e7b)
- [Cerner (ARZ/FLA)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Flowsheets/Business%20Spec%20and%20S2T/ARZ_FLA/ARZ_FLA_Flowsheet_Source_2_Target.xlsx?d=waa5c3774d6164aca80906f2352ee1bb0)
- [Cerner (MCHS)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Flowsheets/Business%20Spec%20and%20S2T/MCHS/MCHS_Flowsheet_Source_2_Target.xlsx?d=w145802a93346448ea13e4d1626e4f9c1)
- [Epic](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Flowsheets/Business%20Spec%20and%20S2T/Epic/EPIC_Flowsheet_Source_2_Target.xlsx?d=w8a854e96faee42608050f18b9fef1f19)

## Example Query

### Fact Table Indexed Columns

**Note:** Subject to changes. Please use the following column(s) in your query filter for faster and more efficient data retrieval.

- `ROW_LOADED_DTM`
- `PATIENT_DK`
- `FLOWSHEET_ASSESSMENT_DTM`
- `FLOWSHEET_NAME_DK`
- `SOURCE_SYSTEM_KEY + ROW_SOURCE_I`

### Sample Query: 

This is a sample query to get you started. Query you need for your use case may be different than this sample.
```sql
SELECT
--FL.SOURCE_SYSTEM_KEY,
  SYS.SOURCE_SYSTEM_CODE, SYS.SOURCE_SYSTEM_NAME, SYS.SOURCE_SYSTEM_SITE,
  FL.PATIENT_DK,PT.PATIENT_CLINIC_NUMBER, FL.LOCATION_SITE_NAME, FL.FLOWSHEET_ASSESSMENT_DTM, FL.FLOWSHEET_ROW_CAPTURED_DTM, FL.LAST_UPDATE_DTM,
  FL.ENCOUNTER_NBR,FL.FLOWSHEET_TYPE_CODE,
  FL.FLOWSHEET_SERVICE_TYPE_CODE, FL.FLOWSHEET_TYPE_DESCRIPTION,FL.FLOWSHEET_SUBTYPE_CODE,--FL.FLOWSHEET_SUBTYPE_DESCRIPTION,
  FN.FLOWSHEET_TYPE_CODE AS DIM_FN_FLOWSHEET_TYPE, FN.FLOWSHEET_TYPE_DESCRIPTION AS DIM_FN_FLOWSHEET_DESC,
  FRN.FLOWSHEET_ROW_CODE, FRN.FLOWSHEET_ROW_DESCRIPTION,
  FL.FLOWSHEET_UNIT_OF_MEASURE_TXT, FL.FLOWSHEET_RESULT_TXT, FL.FLOWSHEET_RESULT_VAL,PROV.PROVIDER_FIRST_NAME, PROV.PROVIDER_LAST_NAME,
  L.LOCATION_DESCRIPTION
FROM EDTWH.FACT_FLOWSHEETS FL
  INNER JOIN EDTWH.DIM_PATIENT PT
    ON (PT.PATIENT_DK = FL.PATIENT_DK)
  INNER JOIN EDTWH.DIM_HEALTHCARE_PROVIDER PROV
    ON (FL.PROVIDER_DK = PROV.PROVIDER_DK)
  INNER JOIN EDTWH.DIM_LOCATION L
    ON (FL.LOCATION_DK = L.LOCATION_DK)
  INNER JOIN EDTWH.DIM_FLOWSHEET_NAME FN
    ON (FL.FLOWSHEET_NAME_DK = FN.FLOWSHEET_NAME_DK)
  INNER JOIN EDTWH.DIM_FLOWSHEET_ROW_NAME FRN
    ON (FL.FLOWSHEET_ROW_NAME_DK = FRN.FLOWSHEET_ROW_NAME_DK)
  INNER JOIN EDTWH.DIM_SOURCE_SYSTEM SYS
    ON (FL.SOURCE_SYSTEM_DK=SYS.SOURCE_SYSTEM_DK)
WHERE FL.FLOWSHEET_ASSESSMENT_DTM BETWEEN '2015-06-01 00:00:00' AND '2015-06-30 23:59:59'
```