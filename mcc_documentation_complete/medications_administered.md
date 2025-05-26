# Medications Administered (MAR) Data Mart

## Description

Drugs administered to a patient in an in-patient setting; including route, form, and amount.

## Diagram

[![Medications_Administered Data Model](/assets/images/fact_meds_admin-578d18218ada85081102e623b80387d3.PNG)](https://mctools.sharepoint.com/:b:/r/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Data%20Models/15%29%20%20Meds%20Administered/FACT_MEDS_ADMIN_MCC.pdf)

## Dataset Information

- **Project Id:** `ml-mps-adl-intudp-phi-p-d5cb`
- **Dataset:** `phi_udpwh_etl_us_p`
- **Entitlement:** `MCC Live - AIDE UDP General Marts PROD Analytics`
  - [User Access](/docs/data-analytics/user-access) | [Service Account Access](/docs/data-analytics/service-account-access)

**Former DB2 Database:** EDT4P
**Update Frequency:** Updated Nightly
**Support Group:** UDP Data Integration

## Mapping Specifications

- [MICS (RST)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Meds%20Administered/Business%20Spec%20and%20S2T/Rochester/MCR%20MedsAdmin_Source_2_Target%20by%20MJY.xlsx?d=w5448598caa6443a4bedea0badcbceab1)
- [Cerner (ARZ/FLA)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Meds%20Administered/Business%20Spec%20and%20S2T/ARZ_FLA/AZFL_MedsAdmin_Source_2_Target.xlsx?d=wb0311f3c5af24578b9ff2cc2cd5f537b)
- [Cerner (MCHS)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Meds%20Administered/Business%20Spec%20and%20S2T/MCHS/MCHS_MedsAdmin_Source_2_Target.xlsx?d=wa11c642fb94b46d5adbf54f98b397251)
- [Epic](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Meds%20Administered/Business%20Spec%20and%20S2T/Epic/MedsAdmin_Source_2_Target%20for%20Epic.xlsx?d=w8adb3507a28a46e9b1adb5f992b04004)

## Example Query

### Fact Table Indexed Columns

**Note:** Subject to changes. Please use the following column(s) in your query filter for faster and more efficient data retrieval.

- `ADMINISTERED_DTM + PATIENT_DK`
- `ENCOUNTER_NUMBER`
- `MED_ADMINISTERED_FPK + PATIENT_DK`
- `ORDER_NUMBER`
- `PATIENT_DK + ADMINISTERED_DTM`
- `SOURCE_SYSTEM_KEY`

### Sample Query: 

This is a sample query to get you started. Query you need for your use case may be different than this sample.
```sql
SELECT PT.PATIENT_CLINIC_NUMBER, PT.PATIENT_FIRST_NAME, PT.PATIENT_LAST_NAME,
  H.PROVIDER_FIRST_NAME, H.PROVIDER_LAST_NAME,
  LOC.LOCATION_DESCRIPTION AS ORDERING_LOCATION,
  DEPT_LOC.LOCATION_DESCRIPTION AS DEPARTMENT_LOCATION,
  FLOC.LOCATION_DESCRIPTION AS FACILITY_LOCATION,
  MED.STARTED_DTM, MED.ENDED_DTM, MED.ADMINISTERED_DTM,
  MEDNM.MED_NAME_CODE, MEDNM.MED_BRAND_NAME_DESCRIPTION, MEDNM.MED_GENERIC_NAME_DESCRIPTION,
  MED.ADMINISTERED_STATUS, MED.ADMINISTERED_FREQUENCY, MED.ADMINISTERED_ROUTE, MED.ADMINISTERED_FORM, MED.ADMINISTERED_DOSE,
  MED.ADMINISTERED_DOSE_UNITS, MED.ORDER_NUMBER, MED.ENCOUNTER_NUMBER, MED.CHARTED_RESULT, MED.ADMINISTERED_MEDS_COMMENTS
FROM EDTWH.FACT_MEDS_ADMINISTERED MED
  JOIN EDTWH.DIM_PATIENT PT
    ON (MED.PATIENT_DK = PT.PATIENT_DK)
  JOIN EDTWH.DIM_HEALTHCARE_PROVIDER H
    ON (MED.ORDERING_PROVIDER_DK=H.PROVIDER_DK)
  JOIN EDTWH.DIM_LOCATION LOC
    ON (MED.LOCATION_DK=LOC.LOCATION_DK)
  JOIN EDTWH.DIM_LOCATION DEPT_LOC
    ON (MED.DEPARTMENT_LOCATION_DK=DEPT_LOC.LOCATION_DK)
  JOIN EDTWH.DIM_LOCATION FLOC
    ON (MED.FACILITY_LOCATION_DK=FLOC.LOCATION_DK)
  JOIN EDTWH.DIM_MED_NAME MEDNM
    ON (MED.MED_NAME_DK=MEDNM.MED_NAME_DK)
```