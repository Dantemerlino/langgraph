# Lab Tests Data Mart

## Description

Lab results performed for the patient, the results are textual and numerical, (Does not contain pictures, video, or audio results).

## Diagram

[![Lab_Test Data Model](/assets/images/fact_lab-8078e9c3f4a25ca89eae3ec16998a1f9.PNG)](https://mctools.sharepoint.com/:b:/r/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Data%20Models/4%29%20Lab_Tests/FACT_LAB_MCC.pdf)

## Dataset Information

- **Project Id:** `ml-mps-adl-intudp-phi-p-d5cb`
- **Dataset:** `phi_udpwh_etl_us_p`
- **Entitlement:** `MCC Live - AIDE UDP General Marts PROD Analytics`
  - [User Access](/docs/data-analytics/user-access) | [Service Account Access](/docs/data-analytics/service-account-access)

**Former DB2 Database:** EDT4P
**Update Frequency:** Updated Nightly
**Support Group:** UDP Data Integration

## Mapping Specifications

- [MICS (RST)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Lab%20Tests/Business%20Spec%20and%20S2T/Rochester/Mapping_Lab%20Tests.xlsx?d=wc544148fccc747f5a9147185e3c59736)
- [Cerner (ARZ/FLA)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Lab%20Tests/Business%20Spec%20and%20S2T/ARZ_FLA/MCFLAZ_Lab_Test_Source_2_Target%20-%20Copy.xlsx?d=w6f3a3c7d2cdb4f56ad174ad5598c0fc6)
- [Cerner (MCHS)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Lab%20Tests/Business%20Spec%20and%20S2T/MCHS/MCHS_Lab_Test_Source_2_Target.xlsx?d=w92034d40536d4a62966138620875796d)
- [Epic](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Lab%20Tests/Business%20Spec%20and%20S2T/Epic/Epic_Lab_Source_2_Target.xlsx?d=w16dd42e56dee4bac83d29bb44de6200c)

## Example Query

### Fact Table Indexed Columns

**Note:** Subject to changes. Please use the following column(s) in your query filter for faster and more efficient data retrieval.


### Sample Query: 

This is a sample query to get you started. Query you need for your use case may be different than this sample.
```sql
SELECT PAT.PATIENT_DK, PAT.PATIENT_CLINIC_NUMBER,LAB.LAB_ORDER_DTM, LAB.LAB_COLLECTION_DTM, LAB.LAB_RESULT_DTM,
  LAB.LAB_ACCESSION_NBR, LAB.LAB_SERVICE_TYPE_CODE, LAB.LAB_TYPE_CODE, LAB.LAB_SUBTYPE_CODE, LAB.LAB_STATUS,
  HP.PROVIDER_FIRST_NAME, HP.PROVIDER_LAST_NAME,
  LOC.LOCATION_CODE, LOC.LOCATION_DESCRIPTION,
  ANA.ANATOMIC_LOCATION_CODE, ANA.ANATOMIC_LOCATION_DESCRIPTION,
  LT.LAB_TEST_CODE, LT.LAB_TEST_DESCRIPTION,
  LPT.LAB_PANEL_TEST_CODE, LPT.LAB_PANEL_TEST_DESCRIPTION,
  STYP.SAMPLE_TYPE_CODE, STYP.SAMPLE_TYPE_DESCRIPTION,
  ABC.LAB_ABNORMAL_CODE, ABC.LAB_ABNORMAL_DESCRIPTION,
  LAB.RESULT_TXT, LAB.RESULT_VAL, LAB.UNIT_OF_MEASURE_TXT, LAB.NORMAL_RANGE_TXT
FROM EDTWH.FACT_LAB_TEST LAB
  INNER JOIN EDTWH.DIM_PATIENT PAT
    ON (LAB.PATIENT_DK = PAT.PATIENT_DK)
  INNER JOIN EDTWH.DIM_HEALTHCARE_PROVIDER HP
    ON (LAB.PRIMARY_PROVIDER_DK=HP.PROVIDER_DK)
  INNER JOIN EDTWH.DIM_LOCATION LOC
    ON (LAB.LOCATION_DK=LOC.LOCATION_DK)
  INNER JOIN EDTWH.DIM_ANATOMIC_LOCATION ANA
    ON (ANA.ANATOMIC_LOCATION_DK = LAB.ANATOMIC_LOCATION_DK)
  INNER JOIN EDTWH.DIM_LAB_TEST LT
    ON (LAB.LAB_TEST_DK = LT.LAB_TEST_DK)
  INNER JOIN EDTWH.DIM_LAB_PANEL_TEST LPT
    ON (LAB.LAB_PANEL_TEST_DK = LPT.LAB_PANEL_TEST_DK)
  INNER JOIN EDTWH.DIM_SAMPLE_TYPE STYP
    ON (LAB.SAMPLE_TYPE_DK = STYP.SAMPLE_TYPE_DK)
  INNER JOIN EDTWH.DIM_LAB_ABNORMAL_CODES ABC
    ON (LAB.LAB_ABNORMAL_CODES_DK = ABC.LAB_ABNORMAL_CODES_DK)
WHERE LAB.LAB_RESULT_DTM BETWEEN '2015-06-01 00:00:00' AND '2015-06-30 23:59:59'
  AND PAT.PATIENT_CLINIC_NUMBER = '123456'
  ```