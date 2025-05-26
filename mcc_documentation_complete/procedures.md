# Procedures Data Mart

## Description

Represents the billing and internal coding related to the medical procedures.

## Diagram

![Procedures Data Model](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Data%20Models/8%29%20Procedures/FACT_PROCEDURES_MCC.pdf)

## Dataset Information

- **Project Id:** `ml-mps-adl-intudp-phi-p-d5cb`
- **Dataset:** `phi_udpwh_etl_us_p`
- **Entitlement:** `MCC Live - AIDE UDP General Marts PROD Analytics`
  - [User Access](/docs/data-analytics/user-access) | [Service Account Access](/docs/data-analytics/service-account-access)

**Former DB2 Database:** EDT4P  
**Update Frequency:** Updated Nightly  
**Support Group:** UDP Data Integration

## Mapping Specifications

- [HealthQuest/MRIS (RST/ARZ/FLA)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Procedures/Business%20Spec%20and%20S2T/Rochester/x_Mapping_Procedures.xlsx?d=w4cb62dbbc67f418a8980419f11d6d574)
- [BEACH (MCHS)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Procedures/Business%20Spec%20and%20S2T/MCHS/MCHS_Procedures_Mart_Source_2_Target.xlsx?d=we14c8507a8974e1c84332783a2028b8b)
- [Epic](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Procedures/Business%20Spec%20and%20S2T/Epic/EPIC_Procedure_Source_2_Target.xlsx?d=w113f4264fddf47dba565b0466de46ee9)

## Example Query

### Fact Table Indexed Columns

**Note:** Subject to changes. Please use the following column(s) in your query filter for faster and more efficient data retrieval.

- `PATIENT_DK + PROCEDURE_CODE_DK`
- `PROCEDURE_CODE_DK`
- `PROCEDURE_CODE + PROCEDURE_METHOD_CODE + PROCEDURE_DTM + PATIENT_DK + PROCEDURE_CODE_DK`
- `PROCEDURE_DTM + PROCEDURE_CODE_DK + PATIENT_DK`
- `SOURCE_SYSTEM_KEY`

### Sample Query:

This is a sample query to get you started. Query you need for your use case may be different than this sample.

```sql
SELECT PROC.PATIENT_DK,PT.PATIENT_CLINIC_NUMBER,
  SRC.SOURCE_SYSTEM_DESCRIPTION,
  SRV_PROV.PROVIDER_FIRST_NAME||' '||SRV_PROV.PROVIDER_LAST_NAME AS SERVICING_PROVIDER_NAME,
  ORD_PROV.PROVIDER_FIRST_NAME||' '||ORD_PROV.PROVIDER_LAST_NAME AS SERVICING_PROVIDER_NAME,
  REF_PROV.PROVIDER_FIRST_NAME||' '||REF_PROV.PROVIDER_LAST_NAME AS SERVICING_PROVIDER_NAME,
  LOC.LOCATION_CODE PROC_LOC_CODE, LOC.LOCATION_DESCRIPTION AS PROC_LOC_DESC,
  PROC.PROCEDURE_DTM, PROC.PROCEDURE_CODE,PROC_CD.PROCEDURE_NAME, PROC_CD.PROCEDURE_DESCRIPTION,
  PROC.PROCEDURE_VISIT_NBR, PROC.ENCOUNTER_NUMBER,
  PROC.PROCEDURE_MODIFIER_1
FROM FACT_PROCEDURES PROC
  INNER JOIN EDTWH.DIM_PATIENT PT
    ON (PROC.PATIENT_DK = PT.PATIENT_DK)
  INNER JOIN EDTWH.DIM_SOURCE_SYSTEM SRC
    ON (PROC.ROW_SOURCE_ID=SRC.SOURCE_SYSTEM_DK)
  INNER JOIN EDTWH.DIM_HEALTHCARE_PROVIDER SRV_PROV
    ON (PROC.SERVICING_PROVIDER_DK=SRV_PROV.PROVIDER_DK)
  INNER JOIN EDTWH.DIM_HEALTHCARE_PROVIDER ORD_PROV
    ON (PROC.ORDERING_PROVIDER_DK =ORD_PROV.PROVIDER_DK)
  INNER JOIN EDTWH.DIM_HEALTHCARE_PROVIDER REF_PROV
    ON (PROC.REFERRING_PROVIDER_DK =REF_PROV.PROVIDER_DK)
  INNER JOIN EDTWH.DIM_LOCATION LOC
    ON (PROC.LOCATION_DK = LOC.LOCATION_DK)
  INNER JOIN EDTWH.DIM_PROCEDURE_CODE PROC_CD
    ON (PROC.PROCEDURE_CODE_DK = PROC_CD.PROCEDURE_CODE_DK)
WHERE PROC.PROCEDURE_DTM BETWEEN '2017-01-01-00.00.00.000000' AND '2017-03-31-23.59.59.999999'
  AND PT.PATIENT_CLINIC_NUMBER IN (123456) /* INSERT YOUR CLINIC NUMBER HERE*/
```
