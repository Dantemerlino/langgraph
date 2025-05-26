# Social Determinants of Health Data Mart

## Description

Social determinants of health (SDOH) are the nonmedical factors that influence health outcomes. They are the conditions in which people are born, grow, work, live, and age. These forces and systems include a wide set of forces and systems that shape daily life such as economic policies and systems, development agendas, social norms, social policies, and political systems.
This mart contains SDOH related data gathered from the EPIC medical record. This release does not include historic data (Pre-EPIC) sources.

## Diagram

[![Social Determinants of Health Data Mart](/assets/images/fact_sdoh-fea6d849ef7915ecdb298fb77c81c5ce.PNG)](/assets/files/FACT_SDOH-6137d34850d36305ac1c22248e7b1b47.pdf)

## Dataset Information

- **Project Id:** `ml-mps-adl-intudp-phi-p-d5cb`
- **Dataset:** `phi_udpwh_etl_us_p`
- **Entitlement:** `MCC Live - AIDE UDP General Marts PROD Analytics`
  - [User Access](/docs/data-analytics/user-access) | [Service Account Access](/docs/data-analytics/service-account-access)
**Update Frequency:** Updated Nightly
**Support Group:** UDP Data Integration

## Mapping Specifications

- [Epic](/assets/files/Social_Determinants_Of_Health_Source_2_Target-827241345638d37f12895c90d48fe175.xlsx)

## Example Query

### Sample Query:

```sql
SELECT fs.SOURCE_SYSTEM_KEY
  ,fs.PATIENT_DK
  ,p.PATIENT_CLINIC_NUMBER
  ,p.PATIENT_FULL_NAME
  ,fs.ENCOUNTER_NUMBER
  ,fs.SDOH_DATA_ID
  ,fs.SDOH_ENTRY_PROVIDER_DK
  ,dhp.PROVIDER_LAST_NAME
  ,fs.SITE_NAME
  ,fs.SDOH_CONTACT_DTM
  ,fs.SDOH_DISPLAY_NAME
  ,fs.SDOH_DOMAIN_DK
  ,dsd.SDOH_DOMAIN
  ,fs.SDOH_RULE_DK
  ,dsr.SDOH_RULE_NAME
  ,fs.SDOH_ANSWER_VALUE
  ,fs.SDOH_ANSWER
  ,fs.SDOH_ENTRY_INTERPRETATION_EXTERNAL
  ,fs.SDOH_CONCERNS_PRESENT_YN
FROM `ml-mps-adl-intudp-phi-p-d5cb.phi_udpwh_etl_us_p.FACT_SDOH` fs
  Inner Join `ml-mps-adl-intudp-phi-p-d5cb.phi_udpwh_etl_us_p.DIM_PATIENT` p On fs.PATIENT_DK = p.PATIENT_DK
  Inner Join `ml-mps-adl-intudp-phi-p-d5cb.phi_udpwh_etl_us_p.DIM_HEALTHCARE_PROVIDER` dhp On fs.SDOH_ENTRY_PROVIDER_DK = dhp.PROVIDER_DK
  Inner Join `ml-mps-adl-intudp-phi-p-d5cb.phi_udpwh_etl_us_p.DIM_SDOH_DOMAIN` dsd On fs.SDOH_DOMAIN_DK = dsd.SDOH_DOMAIN_DK
  Inner Join `ml-mps-adl-intudp-phi-p-d5cb.phi_udpwh_etl_us_p.DIM_SDOH_RULE` dsr On fs.SDOH_RULE_DK = dsr.SDOH_RULE_DK
--Where fs.SDOH_DATA_ID =
--Where fs.PATIENT_DK =
Order By fs.SDOH_DATA_ID, fs.SDOH_CONTACT_DTM
```
