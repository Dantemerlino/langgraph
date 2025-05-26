# Claims Data Mart

## Description

Claims data compiled together with diagnosis and procedures for patient services.

## Diagram

[![Claims Data Model](/assets/images/fact_claims-ceeaae051e3b046457fc23113f00656c.PNG)](https://mctools.sharepoint.com/:b:/r/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Data%20Models/25%29%20Claims/FACT_CLAIMS_MCC.pdf)

## Dataset Information

- **Project Id:** `ml-mps-adl-intudp-phi-p-d5cb`
- **Dataset:** `phi_udpwh_etl_us_p`
- **Entitlement:** `MCC Live - AIDE UDP General Marts PROD Analytics`
  - [User Access](/docs/data-analytics/user-access) | [Service Account Access](/docs/data-analytics/service-account-access)

**Former DB2 Database:** EDT4P
**Update Frequency:** Updated Nightly
**Support Group:** UDP Data Integration

## Mapping Specifications

- [Claims - Epic](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Claims/Business%20Spec%20and%20S2T/EPIC/EPIC_CLAIMS.xlsx?d=w0f42c508394b479eaf81aea190c4f314)
- [MCMS_HCFA](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Claims/Business%20Spec%20and%20S2T/MCMS/MCMS_HCFA.xlsx?d=wc10569d69c9c4da6bba828f9826907de)
- [MCMS_UB](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Claims/Business%20Spec%20and%20S2T/MCMS/MCMS_UB.xlsx?d=w1331508511cd4f098d9607190422c6b5)

## Example Query

### Fact Table Indexed Columns

**Note:** Subject to changes. Please use the following column(s) in your query filter for faster and more efficient data retrieval.

- `ROW_LOADED_DTM + PATIENT_DK`
- `CLAIMS_DTM + PATIENT_DK`
- `ADMISSION_DTM + PATIENT_DK`
- `DISCHARGE_DTM + PATIENT_DK`
- `CLAIM_ID + PATIENT_DK`
- `ENCOUNTER_NUMBER + PATIENT_DK`
- `CLAIMS_FPK + PATIENT_DK`
- `SOURCE_SYSTEM_KEY + ROW_SOURCE_ID`
- `PATIENT_DK`

### Sample Query: 

This is a sample query to get you started. Query you need for your use case may be different than this sample.
```sql
SELECT 
  dss.SOURCE_SYSTEM_NAME,
  fc.CLAIMS_FPK,
  dhp1.PROVIDER_LAST_NAME AS ADMISSION_PROVIDER,
  dhp2.PROVIDER_LAST_NAME AS ATTENDING_PROVIDER,
  dhp3.PROVIDER_LAST_NAME AS BILLING_PROVIDER,
  dl.LOCATION_SITE_NAME,
  fc.CLAIMS_DTM,
  fc.ADMISSION_DTM,
  fc.DISCHARGE_DTM,
  dip.INSURANCE_PAYOR_NAME,
  fc.PATIENT_GUARANTOR_NAME,
  fc.PATIENT_GUARANTOR_ID_TYPE,
  fc.CLAIM_CLASS_NAME,
  fc.CLAIMS_TYPE_NAME,
  fc.CLAIMS_STATUS,
  fc.CLAIM_ID,
  fc.CLAIM_FILING_ORDER,
  fc.CLAIM_CONDITION_CODES,
  fc.DRG_CODE,
  fc.FINANCIAL_CLASS,
  fc.ENCOUNTER_NUMBER,
  fc.VISIT_NUMBER
FROM FACT_CLAIMS fc
  INNER JOIN DIM_SOURCE_SYSTEM dss
    ON fc.ROW_SOURCE_ID = dss.SOURCE_SYSTEM_DK
  INNER JOIN DIM_PATIENT p 
    ON fc.PATIENT_DK = p.PATIENT_DK
  INNER JOIN DIM_HEALTHCARE_PROVIDER dhp1
    ON fc.ADMISSION_PROVIDER_DK = dhp1.PROVIDER_DK
  INNER JOIN DIM_HEALTHCARE_PROVIDER dhp2
    ON fc.ATTENDING_PROVIDER_DK = dhp2.PROVIDER_DK
  INNER JOIN DIM_HEALTHCARE_PROVIDER dhp3
    ON fc.BILLING_PROVIDER_DK = dhp3.PROVIDER_DK
  INNER JOIN DIM_LOCATION dl
    ON fc.LOCATION_DK = dl.LOCATION_DK
  INNER JOIN DIM_INSURANCE_PAYOR dip
    ON fc.INSURANCE_PAYER_DK = dip.INSURANCE_PAYOR_DK
Where p.PATIENT_CLINIC_NUMBER = -- ENTER Patient MRN here
```