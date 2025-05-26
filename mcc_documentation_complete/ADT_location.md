# ADT Locations Data Mart

## Description

Shows the Admission, Discharge and Transfer movement throughout the EMR as the patient moves from an event status of inpatient, transfer, outpatient status with time and physical service or location of that movement.

## Diagram

[![ADT Location Data Model](/assets/images/fact_adt-2ccc09e7927f5e087190f7e7e3167fef.PNG)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Data%20Models/9%29%20Admit_Discharge_Transfer/FACT_ADT_MCC.pdf)

## Dataset Information

- **Project Id:** `ml-mps-adl-intudp-phi-p-d5cb`
- **Dataset:** `phi_udpwh_etl_us_p`
- **Entitlement:** `MCC Live - AIDE UDP General Marts PROD Analytics`
  - [User Access](/docs/data-analytics/user-access) | [Service Account Access](/docs/data-analytics/service-account-access)

**Former DB2 Database:** EDT4P
**Update Frequency:** Updated Nightly
**Support Group:** UDP Data Integration

## Mapping Specifications

- [HealthQuest(via MICS) (RST)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Admit%20Discharge%20Transfer/Business%20Spec%20and%20S2T/Rochester/RST_MICS_Admit_Discharge_Transfer_Source_2_Target%20(1).xlsx?d=wa2800b9455874921aefb2a06199dbbff)
- [Cerner (ARZ/FLA)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Admit%20Discharge%20Transfer/Business%20Spec%20and%20S2T/ARZ_FLA/CERNER_ADT%20S2T%20Stage_to_Mart.xlsx?d=wf9e565d4d5f34831aea40042f4f6aee6)
- [Cerner (MCHS)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Admit%20Discharge%20Transfer/Business%20Spec%20and%20S2T/MCHS/MCHS_Admit_Discharge_Source_2_Target.xlsx?d=w8e92fcb7c1eb4582bd73b807c976e362)
- [IDX (ARZ)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Admit%20Discharge%20Transfer/Business%20Spec%20and%20S2T/ARZ_FLA/IDX_Hx_ADT%20S2T%20Stage_to_Mart.xlsx?d=w4d8e0e5435d84c589a3f476aec698064)
- [Epic](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Admit%20Discharge%20Transfer/Business%20Spec%20and%20S2T/Epic/Epic_Admit_Discharge_Transfer_Source_2_Target.xlsx?d=w4b475c07d9bd411b896047de3368cd62)

## Example Query

### Fact Table Indexed Columns

**Note:** Subject to changes. Please use the following column(s) in your query filter for faster and more efficient data retrieval.

- `ADMIT_DISCHARGE_TRANSFER_FPK`
- `VISIT_NBR+PATIENT_DK`
- `PATIENT_DK`
- `ADMIT_DTM+PATIENT_DK`
- `ADISCHARGE_DTM+PATIENT_DK`
- `SOURCE_SYSTEM_KEY`

### Sample Query: 

This is a sample query to get you started. Query you need for your use case may be different than this sample.

```sql
SELECT ADT.PATIENT_DK, ADT.LOCATION_SITE_NAME,SRC.SOURCE_SYSTEM_NAME, ADT.ADMIT_DTM, 
    ADT.DISCHARGE_DTM, ADT.TRANSFER_DTM, ADT.VISIT_NBR,
    PROV.PROVIDER_FIRST_NAME||' '||PROV.PROVIDER_LAST_NAME AS PROVIDER_NAME,
    EVT.EVENT_TYPE_CODE, EVT.EVENT_TYPE_DESCRIPTION,
    C_SVC.CLINICAL_SERVICE_CODE , C_SVC.CLINICAL_SERVICE_DESCRIPTION,
    AM.ADMIT_MODE_CODE, AM.ADMIT_MODE_DESCRIPTION,
    ASRC.ADMIT_SOURCE_CODE, ASRC.ADMIT_SOURCE_DESCRIPTION,
    ATYP.ADMIT_TYPE_CODE, ATYP.ADMIT_TYPE_DESCRIPTION,
    DS.DISCHARGE_DISPOSITION_CODE, DS.DISCHARGE_DISPOSITION_DESCRIPTION,
    ADT.PATIENT_PROCESS_TYPE,ADT.ACCOMMODATION_CODE

FROM EDTWH.FACT_ADMIT_DISCHARGE_TRANSFER_LOCATION ADT
    INNER JOIN EDTWH.DIM_PATIENT PT
      ON (ADT.PATIENT_DK = PT.PATIENT_DK)
    INNER JOIN EDTWH.DIM_SOURCE_SYSTEM SRC
      ON (ADT.SOURCE_SYSTEM_DK=SRC.SOURCE_SYSTEM_DK)
    INNER JOIN EDTWH.DIM_HEALTHCARE_PROVIDER PROV
      ON (ADT.PROVIDER_DK = PROV.PROVIDER_DK)
    JOIN EDTWH.DIM_LOCATION LOC
      ON (ADT.LOCATION_DK = LOC.LOCATION_DK)
    JOIN EDTWH.DIM_DATE DT
      ON (ADT.ADMIT_DATE_DK=DT.DATE_DK)
    INNER JOIN EDTWH.DIM_HEALTHCARE_PROVIDER TRANS_FROM_PROV
      ON (ADT.TRANSFER_FROM_PROVIDER_DK=TRANS_FROM_PROV.PROVIDER_DK)
    INNER JOIN EDTWH.DIM_ADMIT_DISCHARGE_TRANSFER_EVENT_TYPE EVT
      ON (ADT.EVENT_TYPE_DK = EVT.EVENT_TYPE_DK)
    INNER JOIN EDTWH.DIM_CLINICAL_SERVICE C_SVC
      ON (ADT.CLINICAL_SERVICE_DK =C_SVC.CLINICAL_SERVICE_DK)
    INNER JOIN EDTWH.DIM_ADMIT_MODE AM
      ON (ADT.ADMIT_MODE_DK = AM.ADMIT_MODE_DK)
    INNER JOIN EDTWH.DIM_ADMIT_SOURCE ASRC
      ON (ADT.ADMIT_SOURCE_DK = ASRC.ADMIT_SOURCE_DK)
    INNER JOIN EDTWH.DIM_ADMIT_TYPE ATYP
      ON (ADT.ADMIT_TYPE_DK = ATYP.ADMIT_TYPE_DK)
    INNER JOIN EDTWH.DIM_DISCHARGE_DISPOSITION DS
      ON (ADT.DISCHARGE_DISPOSITION_DK = DS.DISCHARGE_DISPOSITION_DK)
```