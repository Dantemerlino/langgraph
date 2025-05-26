# SmartForm Data Mart

## Description

SmartForms are a collection of various data that EPIC databases collect for the Mayo Clinic.

## Diagram

[![SmartForm Data Model](/assets/images/fact_smartform-19b21e2c24a4686838ed63263a0166a7.PNG)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Data%20Models/31%29%20SmartForm/FACT_SMARTFORM_MCC.pdf)

## Dataset Information

- **Project Id:** `ml-mps-adl-intudp-phi-p-d5cb`
- **Dataset:** `phi_udpwh_etl_us_p`
- **Entitlement:** `MCC Live - AIDE UDP General Marts PROD Analytics`
  - [User Access](/docs/data-analytics/user-access) | [Service Account Access](/docs/data-analytics/service-account-access)

**Former DB2 Database:** EDT4P
**Update Frequency:** Updated Nightly
**Support Group:** UDP Data Integration

## Mapping Specifications

- [Epic](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/SmartForm/SmartForms_Source_2_Target.xlsx?d=w8883a8af93c14cccbdea8040b73eb80b)

## Example Query

### Fact Table Indexed Columns

**Note:** Subject to changes. Please use the following column(s) in your query filter for faster and more efficient data retrieval.

- `SMARTFORM_FPK + PATIENT_DK`
- `SOURCE_SYSTEM_KEY + ROW_SOURCE_ID`

### Sample Query: 

This is a sample query to get you started. Query you need for your use case may be different than this sample.
```sql
SELECT
  P.PATIENT_CLINIC_NUMBER
  ,P.PATIENT_FULL_NAME
  ,HP.PROVIDER_LAST_NAME||', '|| HP.PROVIDER_FIRST_NAME AS SMARTFORM_PROVIDER
  ,LOC.LOCATION_DESCRIPTION AS LOCATION
  ,SF.SITE_NAME
  ,SF.SMARTFORM_ORIGINAL_DTM
  ,SF.SMARTFORM_UPDATE_DTM
  ,SF.ENCOUNTER_NUMBER
  ,DS.SOURCE_SYSTEM_KEY AS SMARTFORM_CODE
  ,SF.SMARTFORM_NAME
  ,SC.SOURCE_SYSTEM_KEY AS SMARTFORM_CONCEPT_CODE
  ,SF.SMARTFORM_CONCEPT_NAME
  ,SF.SMARTFORM_ANSWER
  ,SF.SMARTFORM_SOURCE
FROM FACT_SMARTFORM SF
  INNER JOIN DIM_PATIENT P 
    ON SF.PATIENT_DK = P.PATIENT_DK
  INNER JOIN DIM_HEALTHCARE_PROVIDER HP 
    ON SF.PROVIDER_DK = HP.PROVIDER_DK
  INNER JOIN DIM_LOCATION LOC 
    ON SF.LOCATION_DK = LOC.LOCATION_DK
  INNER JOIN DIM_SMARTFORM_CONCEPT SC 
    ON SF.SMARTFORM_CONCEPT_DK = SC.SMARTFORM_CONCEPT_DK
  INNER JOIN DIM_SMARTFORM DS 
    ON SF.SMARTFORM_DK = DS.SMARTFORM_DK
WHERE P.PATIENT_CLINIC_NUMBER = '' -- TO SEE ALL SMARTFORM ENTRIES BY MRN
ORDER BY P.PATIENT_DK, SF.SMARTFORM_ANSWER_HEADER, SF.SMARTFORM_ANSWER_SEQUENCE -- THIS WILL LIST THE ANSWERS IN A CORRECT ORDER BY PATIENT MRN
```
Search Smartforms
```sql
SELECT
SMARTFORM_DK
,SOURCE_SYSTEM_KEY AS SMARTFORM_CODE
,SMARTFORM_NAME
FROM DIM_SMARTFORM
WHERE SMARTFORM_NAME = 'MC PROCEDURE SKIN LESION EXCISION ADVANCED' -- IF YOU KNOW THE SMARTFORM NAME
```

Search for a Concept
```sql
SELECT
SMARTFORM_CONCEPT_DK
,SOURCE_SYSTEM_KEY AS SMARTFORM_CONCEPT_CODE
,SMARTFORM_CONCEPT_NAME
,SMARTFORM_CONCEPT_DATA_TYPE
,SMARTFORM_CONCEPT_INI_LINK
,SMARTFORM_CONCEPT_CATEGORY_LINK
FROM DIM_SMARTFORM_CONCEPT
WHERE SOURCE_SYSTEM_KEY = 'EPIC#PROC0168' -- IF YOU KNOW THE CONCEPT CODE
```
