# Diagnosis Data Mart

## Description

Patient diagnoses based on billing and internal codes representing the medical diagnosis.

## Diagram

[![Diagnosis Data Model](/assets/images/fact_diagnosis-38878885a8573fa2c3d08c1565f34acf.PNG)](https://mctools.sharepoint.com/:b:/r/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Data%20Models/5%29%20Diagnosis/FACT_DX_MCC.pdf)

## Dataset Information

- **Project Id:** `ml-mps-adl-intudp-phi-p-d5cb`
- **Dataset:** `phi_udpwh_etl_us_p`
- **Entitlement:** `MCC Live - AIDE UDP General Marts PROD Analytics`
  - [User Access](/docs/data-analytics/user-access) | [Service Account Access](/docs/data-analytics/service-account-access)

**Former DB2 Database:** EDT4P
**Update Frequency:** Updated Nightly
**Support Group:** UDP Data Integration

## Mapping Specifications

Billing Diagnosis from
- [HealthQuest/MRIS - RST/ARZ/FLA](https://mctools.sharepoint.com/:x:/r/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Diagnosis/Business%20Spec%20and%20S2T/Rochester/Mappings_Diagnosis.xlsx?d=w66e7454ec6d34c1783f4872260d86e66&csf=1&web=1&e=dXhDcp)
- [MCHS BEACH - Hospital](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Diagnosis/Business%20Spec%20and%20S2T/MCHS/MCHS_Hospital_Billing_Diagnosis_Source_2_Target.xlsx?d=w0d067ed7503c43e7ac73cb299d7beb77)
- [MCHS BEACH - Clinic](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Diagnosis/Business%20Spec%20and%20S2T/MCHS/MCHS_Clinic_Billing_Diagnosis_Source_2_Target.xlsx?d=w8ee543208d864035a6bbe703d14c64ad)
- [IPDB - HURD - All sites](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Diagnosis/Business%20Spec%20and%20S2T/Rochester/RST_mapping_Hurd_stage_to_mart.xlsx?d=w9bbc3561bc154dd08dbb371dec00b85e)
- [Medical Index - All sites](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Diagnosis/Business%20Spec%20and%20S2T/Rochester/MedicalIndex_Mapping.xlsx?d=wf90ab1ffdbba44f297e1508c0740d5b0)
- [Epic - All sites](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Diagnosis/Business%20Spec%20and%20S2T/Epic/Epic_Billing_Diagnosis_Source_2_Target.xlsx?d=wddcd9f59faf74607b7307fccf0c60825)

## Example Query

### Fact Table Indexed Columns

**Note:** Subject to changes. Please use the following column(s) in your query filter for faster and more efficient data retrieval.

- `DIAGNOSIS_CODE_DK`
- `DIAGNOSIS_CODE + DIAGNOSIS_METHOD_CODE + DIAGNOSIS_DTM+PATIENT_DK`
- `DIAGNOSIS_DTM+DIAGNOSIS_CODE_DK`
- `PATIENT_DK + DIAGNOSIS_CODE_DK`
- `PATIENT_DK + DIAGNOSIS_CODE_DK + DIAGNOSIS_CODE + DIAGNOSIS_DTM+ROW_SOURCE_ID + ENCOUNTER_NUMBER`

### Sample Query:

 This is a sample query to get you started. Query you need for your use case may be different than this sample.
```sql
SELECT DISTINCT DIAG.PATIENT_DK,PT.PATIENT_CLINIC_NUMBER,DIAG.LOCATION_SITE_NAME,SRC.SOURCE_SYSTEM_NAME, DIAG.PATIENT_AGE_AT_EVENT,
  DIAG.LOCATION_SITE_NAME, DIAG.DIAGNOSIS_DTM,
  DIAG.ONSET_DTM, DIAG.DIAGNOSIS_CODE, DIAG.DIAGNOSIS_VISIT_NBR, DIAG.DIAGNOSIS_RANK_SEQ, DIAG.ENCOUNTER_NUMBER,
  DCODE.DIAGNOSIS_NAME, DCODE.DIAGNOSIS_METHOD_NAME,
  PROV.PROVIDER_FIRST_NAME, PROV.PROVIDER_LAST_NAME,
  LOC.LOCATION_CODE, LOC.LOCATION_DESCRIPTION
FROM EDTWH.FACT_DIAGNOSIS DIAG
  JOIN EDTWH.DIM_PATIENT PT
    ON (DIAG.PATIENT_DK = PT.PATIENT_DK)
  INNER JOIN EDTWH.DIM_SOURCE_SYSTEM SRC
    ON (DIAG.SOURCE_SYSTEM_DK=SRC.SOURCE_SYSTEM_DK)
  INNER JOIN EDTWH.DIM_HEALTHCARE_PROVIDER PROV
    ON (DIAG.SERVICING_PROVIDER_DK= PROV.PROVIDER_DK)
  JOIN EDTWH.DIM_LOCATION LOC
    ON (DIAG.LOCATION_DK = LOC.LOCATION_DK)
  JOIN EDTWH.DIM_DATE DT
    ON (DIAG.DIAGNOSIS_DATE_DK =DT.DATE_DK)
  INNER JOIN EDTWH.DIM_DIAGNOSIS_CODE DCODE
    ON (DIAG.DIAGNOSIS_CODE_DK = DCODE.DIAGNOSIS_CODE_DK)

--where DIAG.SOURCE_SYSTEM_DK=13447 --use this filter for Rochester problem List
--where DIAG.SOURCE_SYSTEM_DK=29298 --use this filter for MCHS problem List
--where DIAG.SOURCE_SYSTEM_DK=32974 --use this filter for Arizona/Florida problem List
--WHERE PT.PATIENT_CLINIC_NUMBER=123456 /* INSERT YOUR CLINIC NUMBER HERE*/
```