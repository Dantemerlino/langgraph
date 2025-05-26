# Pathology Data Mart

## Description

Pathology tests within biopsy and autopsy reports.

## Diagram

[![Pathology Data Model](/assets/images/fact_pathology-4be0da0a6ea502390e3fb15febdd2e53.PNG)](https://mctools.sharepoint.com/:b:/r/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Data%20Models/19%29%20Pathology/FACT_PATHOLOGY_MCC.pdf?csf=1&web=1&e=ztCbvT)

## Dataset Information

- **Project Id:** `ml-mps-adl-intudp-phi-p-d5cb`
- **Dataset:** `phi_udpwh_etl_us_p`
- **Entitlement:** `MCC Live - AIDE UDP General Marts PROD Analytics`
  - [User Access](/docs/data-analytics/user-access) | [Service Account Access](/docs/data-analytics/service-account-access)

**Former DB2 Database:** EDT4P
**Update Frequency:** Updated Nightly
**Support Group:** UDP Data Integration

## Mapping Specifications

- [Copath (RST/ARZ)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Pathology/Business%20Spec%20and%20S2T/Rochester_ARZ/Rochester-Arizona_Copath/RST_AZ_Pathology_Source_2_Target_NEW_MODEL.xlsx?d=w8eef1cac8aad466991784e50e640c31d)
- [MICS (RST)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Pathology/Business%20Spec%20and%20S2T/Rochester_ARZ/Rochester%20-%20MICS/RST_Pathology_Source_2_Target_NEW_MODEL.xlsx?d=we8d9144e56894e09aac1bb69f2ef615f)
- [Cerner (ARZ)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Pathology/Business%20Spec%20and%20S2T/ARZ/MCARZ_Pathology_Source_2_Target.xlsx?d=w15ee7a3a86024ee28f19488e9a7d0205)
- [Cerner (FLA)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Pathology/Business%20Spec%20and%20S2T/FLA/MCFLA_Pathology_Source_2_Target.xlsx?d=w3b88bd7d03ad4a569890d01d6f297ae4)
- [Cerner (MCHS)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Pathology/Business%20Spec%20and%20S2T/MCHS/MCHS_Pathology_Source_2_Target_NEW_MODEL.xlsx?d=wdfaffb68dd1944c0a3f8e8fcd9949961)
- [Epic](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Pathology/Business%20Spec%20and%20S2T/Epic/EPIC_Pathology_Source_2_Target.xlsx?d=w59d34b543a57435b82d3e2d952a3fc30)

## Example Query

### Fact Table Indexed Columns

**Note:** Subject to changes. Please use the following column(s) in your query filter for faster and more efficient data retrieval.


EDTWH.FACT_PATHOLOGY PATIENT_DK SPECIMEN_COLLECTION_DTM PATHOLOGY_FPK SPECIMEN_NUMBER


EDTWH.FACT_PATHOLOGY_SPECIMEN_DETAIL PATIENT_DK PATHOLOGY_FPK SPECIMEN_NUMBER


EDTWH.FACT_PATHOLOGY_EXTENDED_REPORT PATIENT_DK PATHOLOGY_FPK SPECIMEN_NUMBER


### Sample Query: 

This is a sample query to get you started. Query you need for your use case may be different than this sample.
```sql
  SELECT PATH.PATIENT_DK, PATH.PATIENT_AGE_AT_EVENT, PATH.LOCATION_SITE_NAME, PATH.SPECIMEN_ACCESSION_DTM, PATH.SPECIMEN_COLLECTION_DTM, PATH.SPECIMEN_UPDATE_DTM, PATH.SPECIMEN_RESULT_DTM, PATH.SPECIMEN_NUMBER,
  PATH.SPECIMEN_ACCESSION_NUMBER, PATH.ENCOUNTER_ID, PATH.SPECIMEN_CLIENT, PATH.SPECIMEN_SERVICE_DESCRIPTION,
  PROV.PROVIDER_FIRST_NAME, PROV.PROVIDER_MIDDLE_NAME,
  PLOC.LOCATION_CODE,PLOC.LOCATION_DESCRIPTION,
  PDTL.BLOCK_INSTANCE, PDTL.BLOCK_STATUS, PDTL.BLOCK_COMMENT, PDTL.PART_INSTANCE, PDTL.PART_DESCRIPTION, PDTL.STAIN_INSTANCE, PDTL.STAIN_LABEL, PDTL.STAIN_PROCESS,
  DGC.DIAGNOSIS_CODE, DGC.DIAGNOSIS_NAME,
  SPCLS.SPECIMEN_CLASS_NAME,
  SPRT.SPECIMEN_PRIORITY_NAME,
  SPSTS.SPECIMEN_STATUS_NAME
FROM EDTWH.FACT_PATHOLOGY PATH
  JOIN EDTWH.DIM_PATIENT PT
    ON (PATH.PATIENT_DK = PT.PATIENT_DK)
  JOIN EDTWH.DIM_HEALTHCARE_PROVIDER PROV
    ON (PATH.PROVIDER_DK = PROV.PROVIDER_DK)
  JOIN EDTWH.DIM_HEALTHCARE_PROVIDER OPROV
    ON (PATH.ORDERING_PROVIDER_DK=OPROV.PROVIDER_DK)
  JOIN EDTWH.DIM_LOCATION PLOC
    ON (PATH.LOCATION_DK=PLOC.LOCATION_DK)
  JOIN EDTWH.DIM_SOURCE_SYSTEM SYS
    ON (PATH.SOURCE_SYSTEM_DK = SYS.SOURCE_SYSTEM_DK)
  JOIN EDTWH.FACT_PATHOLOGY_SPECIMEN_DETAIL PDTL
    ON (PATH.PATHOLOGY_FPK = PDTL.PATHOLOGY_FPK)
  JOIN EDTWH.DIM_PATHOLOGY_DIAGNOSIS_CODE_BRIDGE PBRDG
    ON (PATH.PATHOLOGY_FPK = PBRDG.PATHOLOGY_FPK)
  JOIN EDTWH.DIM_DIAGNOSIS_CODE DGC
    ON (PBRDG.DIAGNOSIS_CODE_DK = DGC.DIAGNOSIS_CODE_DK)
  JOIN EDTWH.DIM_SPECIMEN_CLASS SPCLS
    ON (PATH.SPECIMEN_CLASS_DK = SPCLS.SPECIMEN_CLASS_DK)
  JOIN EDTWH.DIM_SPECIMEN_PRIORITY SPRT
    ON (PATH.SPECIMEN_PRIORITY_DK = SPRT.SPECIMEN_PRIORITY_DK)
  JOIN EDTWH.DIM_SPECIMEN_STATUS SPSTS
    ON (PATH.SPECIMEN_STATUS_DK = SPSTS.SPECIMEN_STATUS_DK)

-- TO Get Specimen Detail such as Parts, Blocks and Stains
-- Only applicable to Copath
  JOIN EDTWH.FACT_PATHOLOGY_SPECIMEN_DETAIL PATHD
    ON (PATH.PATHOLOGY_FPK = PATHD.PATHOLOGY_FPK)
  JOIN EDTWH.DIM_SPECIMEN_PART_TYPE PTYP
    ON (PATHD.SPECIMEN_PART_TYPE_DK=PTYP.SPECIMEN_PART_TYPE_DK)

-- Use this join only Get Specimen Notes
  JOIN EDTWH.FACT_PATHOLOGY_EXTENDED_REPORT PATHRPT
    ON (PATH.PATHOLOGY_FPK = PATHRPT.PATHOLOGY_FPK)

WHERE
  PATH.SPECIMEN_COLLECTION_DTM BETWEEN '2015-06-01 00:00:00' AND '2015-12-31 23:59:59'
  --AND PATH.SPECIMEN_NUMBER IN ('PR15-4011','PR15-40730','PR15-42284')
```