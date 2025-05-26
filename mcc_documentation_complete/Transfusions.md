# Data Mart

## Description

Transfusion data and blood product details of a transfusion event for a patient.

## Diagram

[![Transfusions Data Model](/assets/images/fact_transfusions-194ae013e93f688f11f648fcf561af9c.PNG)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Data%20Models/37%29%20Transfusion/FACT_TRANSFUSION_MCC.pdf)

## Dataset Information

- **Project Id:** `ml-mps-adl-intudp-phi-p-d5cb`
- **Dataset:** `phi_udpwh_etl_us_p`
- **Entitlement:** `MCC Live - AIDE UDP General Marts PROD Analytics`
  - [User Access](/docs/data-analytics/user-access) | [Service Account Access](/docs/data-analytics/service-account-access)

**Former DB2 Database:** EDT4P
**Update Frequency:** Updated Nightly
**Support Group:** UDP Data Integration

## Mapping Specifications

- [Epic](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Transfusion/Epic_Transfusion_Source_2_Target.xlsx?d=w2a0020a6ac1e40d5a22cb70e42d00b69)

## Example Query

### Fact Table Indexed Columns

**Note:** Subject to changes. Please use the following column(s) in your query filter for faster and more efficient data retrieval.

- `TRANSFUSION_FPK`
- `SOURCE_SYSTEM_KEY + ROW_SOURCE_ID`

### Sample Query: 

This is a sample query to get you started. Query you need for your use case may be different than this sample.


RETRIEVE BLOOD UNIT INFORMATION
```sql
SELECT
  FT.PATIENT_DK,        -----PATIENTS UNIT(S) WERE GIVEN TO
  FT.BLOOD_UNIT_NUMBER,
  FT.UNIT_SPLIT_NUMBER, -----THE NUMBER OF TMES A UNIT MAY HAVE BEEN SPLIT BETWEEN PATIENTS
                        -----00 INDICATES NO SPLIT OF THE UNIT, A0 or AA INDICATES ONE SPLIT ECT.
                        -----NOT ALL WILL BE CORRECT, for example they will show a 00 even though they have been split between patients
  FT.BLOOD_UNIT_ABO,
  FT.BLOOD_UNIT_RHESUS
FROM EDTWH.FACT_TRANSFUSION FT
where FT.SITE_CODE = 'RST'
  AND FT.UNIT_ISSUE_DATE_DK >= '20210101'
  and FT. UNIT_ISSUE_DATE_DK < '20220115'
  ```

RETRIEVE THE TYPE OF TRANSFUSION PRODUCT RECEIVED and BLOOD TYPE
```sql
SELECT
  FT.PATIENT_DK,
  TP.PRODUCT_DESCRIPTION,
  TP.BLOOD_CELL_TYPE,
  FT.UNIT_ISSUE_DTM, ------THIS DATE WILL ALWAYS BE POPULATED
  FT.TRANSFUSION_START_DTM, -----DATE MAY NOT BE POPULATED IF TRANSFUSION OCCURED IN ER OR OTHER EMERGENCY SITUATION
  FT.TRANSFUSION_END_DTM, -----DATE MAY NOT BE POPULATED IF TRANSFUSION OCCURED IN ER OR OTHER EMERGENCY SITUATION
  FT.BLOOD_UNIT_ABO,
  FT.BLOOD_UNIT_RHESUS
FROM EDTWH.FACT_TRANSFUSION FT
  INNER JOIN EDTWH.DIM_TRANSFUSION_PRODUCT TP
    ON FT.BLOOD_PRODUCT_CODE = TP.BLOOD_PRODUCT_CODE
WHERE TP.BLOOD_PRODUCT_CODE = 'E0336'
```