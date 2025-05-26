# Appointments Data Mart

## Description

Shows the scheduled appointments for patients historically and in the future. Contains status of whether they arrived or didn't for their scheduled appointments and what service they attended. May also have a diagnosis, referral or provider information assigned to the appointment as well.

## Diagram

[![Appointment Data Model](/assets/images/fact_appt-95ace774426ebd4d2d7ebfdbe92fb35c.PNG)](https://mctools.sharepoint.com/:b:/r/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Data%20Models/21%29Appointment/FACT_APPT_MCC.pdf)

## Dataset Information

- **Project Id:** `ml-mps-adl-intudp-phi-p-d5cb`
- **Dataset:** `phi_udpwh_etl_us_p`
- **Entitlement:** `MCC Live - AIDE UDP General Marts PROD Analytics`
  - [User Access](/docs/data-analytics/user-access) | [Service Account Access](/docs/data-analytics/service-account-access)

**Former DB2 Database:** EDT4P
**Update Frequency:** Updated Nightly
**Support Group:** UDP Data Integration

## Mapping Specifications

- [RST (MSS)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Appointments/Business%20Spec%20and%20S2T/Rochester/RST_MICS_MSS_Appointment_Source_2_Target.xlsx?d=w0bb60369b5824e839e921ad054c984f9)
- [RST (PAMA)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Appointments/Business%20Spec%20and%20S2T/Rochester/RST_MICS_PAMA_Appointment_Source_2_Target.xlsx?d=w8fd5b7a171e54382996dee1d7cce9aed)
- [ARZ/FLA (Cerner)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Appointments/Business%20Spec%20and%20S2T/ARZ_FLA/AZ_FL_Appointments_Source_Target.xlsx?d=w41c90cddc00f4f158a370c60013c0c8a)
- [MCHS (Cerner)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Appointments/Business%20Spec%20and%20S2T/MCHS/MCHS%20Appointments_Source_2_Target.xlsx?d=w727dd312335f4453893f4d331b6b46b4)
- [Epic](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Appointments/Business%20Spec%20and%20S2T/Epic/Epic_Appointments_Source_2_Target.xlsx?d=w983946a2037c49198a9baa152c819ee4)

## Example Query

### Fact Table Indexed Columns

**Note:** Subject to changes. Please use the following column(s) in your query filter for faster and more efficient data retrieval.

- `APPOINTMENT_ID + PATIENT_DK`
- `APPOINTMENT_FPK`
- `APPOINTMENT_LAST_UPDATE_DTM`
- `APPOINTMENT_BEGIN_DTM`
- `SOURCE_SYSTEM_KEY+ROW_SOURCE_ID`

### Sample Query: 

This is a sample query to get you started. Query you need for your use case may be different than this sample.
```sql
SELECT PT.PATIENT_CLINIC_NUMBER,LOC.LOCATION_DESCRIPTION,H.PROVIDER_FIRST_NAME, H.PROVIDER_LAST_NAME,
AT.APPOINTMENT_TYPE_DESCRIPTION, ARSC.APPOINTMENT_RESOURCE_DESCRIPTION,
ADISP.APPOINTMENT_DISPOSITION_DESCRIPTION,CS.CLINICAL_SERVICE_DESCRIPTION,
AP.APPOINTMENT_CREATE_DTM, AP.APPOINTMENT_REPORT_DTM, AP.APPOINTMENT_BEGIN_DTM, AP.APPOINTMENT_END_DTM, AP.APPOINTMENT_ID, AP.APPOINTMENT_DESCRIPTION, AP.APPOINTMENT_COMMENT, AP.APPOINTMENT_DISPOSITION_NOTE, AP.APPOINTMENT_REASON_TEXT

FROM EDTWH.FACT_APPOINTMENT AP
  JOIN EDTWH.DIM_PATIENT PT
    ON (AP.PATIENT_DK = PT.PATIENT_DK)
  JOIN EDTWH.DIM_LOCATION LOC
    ON (AP.LOCATION_DK = LOC.LOCATION_DK)
  JOIN EDTWH.DIM_HEALTHCARE_PROVIDER H
    ON (AP.PROVIDER_DK = H.PROVIDER_DK)
  JOIN EDTWH.DIM_APPOINTMENT_TYPE AT
    ON (AP.APPOINTMENT_TYPE_DK = AT.APPOINTMENT_TYPE_DK)
  JOIN EDTWH.DIM_APPOINTMENT_RESOURCE ARSC
    ON (AP.APPOINTMENT_RESOURCE_DK = ARSC.APPOINTMENT_RESOURCE_DK)
  JOIN EDTWH.DIM_APPOINTMENT_DISPOSITION ADISP
    ON (AP.APPOINTMENT_DISPOSITION_DK = ADISP.APPOINTMENT_DISPOSITION_DK)
  JOIN EDTWH.DIM_CLINICAL_SERVICE CS
    ON (AP.CLINICAL_SERVICE_DK = CS.CLINICAL_SERVICE_DK)

  -- USE only when you need to retrieve Appointment Indication information.
  LEFT JOIN EDTWH.DIM_APPOINTMENT_INDICATION_BRIDGE AIND
    ON (AP.APPOINTMENT_FPK = AIND.APPOINTMENT_FPK)
  LEFT JOIN EDTWH.DIM_DIAGNOSIS_CODE DC
    ON (AIND.DIAGNOSIS_CODE_DK = DC.DIAGNOSIS_CODE_DK)
WHERE AP.APPOINTMENT_BEGIN_DTM BETWEEN '2016-01-01-00.00.00.000000' AND '2016-01-05-23.59.59.999999'
```

