# Care Plan Data Mart

## Description

The Care Plan view pulls all the current patient’s data together on a single page and offers them the treatments (care plans) that the patient is currently receiving. Current diagnosis, current medications, current treatments are displayed. As they are updated, they are dropped/or added in the care plan.

## Diagram

[![Care Plan Data Model](/assets/images/fact_care_plan-12b8efabe2a19f0b5e0e8bf5992374b8.PNG)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Data%20Models/27%29%20Care_Plan/FACT_CARE_PLAN.pdf)

## Dataset Information

- **Project Id:** `ml-mps-adl-intudp-phi-p-d5cb`
- **Dataset:** `phi_udpwh_etl_us_p`
- **Entitlement:** `MCC Live - AIDE UDP General Marts PROD Analytics`
  - [User Access](/docs/data-analytics/user-access) | [Service Account Access](/docs/data-analytics/service-account-access)

**Former DB2 Database:** EDT4P
**Update Frequency:** Updated Nightly
**Support Group:** UDP Data Integration

## Mapping Specifications

- [Epic](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Care%20Plan/Business%20Spec%20and%20S2T/Epic/Epic_CarePlan_Source_2_Target.xlsx?d=w7280c0d8ea604e06bd7b02c1e4285066)

## Example Query

### Sample Query: 

This is a sample query to get you started. Query you need for your use case may be different than this sample.
```sql
SELECT *
FROM EDTWH.FACT_CARE_PLAN CP
  JOIN EDTWH.DIM_PATIENT PT
    ON (CP.PATIENT_DK = PT.PATIENT_DK)
  JOIN EDTWH.DIM_HEALTHCARE_PROVIDER PROV
    ON (CP.PROVIDER_DK=PROV.PROVIDER_DK)
  JOIN EDTWH.DIM_LOCATION LOC
    ON (CP.LOCATION_DK=LOC.LOCATION_DK)
  JOIN EDTWH.DIM_SOURCE_SYSTEM SYS
    ON (CP.SOURCE_SYSTEM_DK = SYS.SOURCE_SYSTEM_DK)
  JOIN EDTWH.DIM_CARE_PLAN_TYPE CT
    ON (CP.CARE_PLAN_TYPE_DK=CP.CARE_PLAN_TYPE_DK)

--***** TO GET CURRENT MEDICATION***************
  LEFT JOIN EDTWH.FACT_CARE_PLAN_CURRENT_MEDICATION CMED
    ON (CP.CARE_PLAN_FPK=CMED.CARE_PLAN_FPK)
  LEFT JOIN EDTWH.DIM_MED_NAME MED
    ON (MED.MED_NAME_DK=CMED.MED_NAME_DK)

--***** TO GET CURRENT DIAGNOSIS***************
  LEFT JOIN EDTWH.FACT_CARE_PLAN_CURRENT_DIAGNOSIS CDIAG
    ON (CDIAG.CARE_PLAN_FPK=CP.CARE_PLAN_FPK)
  LEFT JOIN EDTWH.DIM_DIAGNOSIS_CODE DIAG
    ON (DIAG.DIAGNOSIS_CODE_DK=CDIAG.DIAGNOSIS_CODE_DK)
```