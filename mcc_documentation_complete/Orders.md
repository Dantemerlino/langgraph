# Orders Data Mart

## Description

Medicines and other items ordered for a patient.

## Diagram

[![Orders Data Model](/assets/images/fact_order-6289abcec90ec35cd1573f7f94531928.PNG)](https://mctools.sharepoint.com/:b:/r/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Data%20Models/7%29%20Orders/FACT_ORDER_MCC.pdf)

## Dataset Information

- **Project Id:** `ml-mps-adl-intudp-phi-p-d5cb`
- **Dataset:** `phi_udpwh_etl_us_p`
- **Entitlement:** `MCC Live - AIDE UDP General Marts PROD Analytics`
  - [User Access](/docs/data-analytics/user-access) | [Service Account Access](/docs/data-analytics/service-account-access)

**Former DB2 Database:** EDT4P
**Update Frequency:** Updated Nightly
**Support Group:** UDP Data Integration

## Mapping Specifications

- [MICS (RST)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Orders/Business%20Spec%20and%20S2T/Rochester/MCR%20Orders_Source_2_Target%20by%20MJY.xlsx?d=wa26c2da6450e4e52be403b1b935afa6f)
- [Cerner (ARZ/FLA)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Orders/Business%20Spec%20and%20S2T/ARZ_FLA/MGP_Orders_Source_2_Target.xlsx?d=w11bbf19cada248f784c52742937b326f)
- [Cerner (MCHS)](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Orders/Business%20Spec%20and%20S2T/MCHS/MCHS_Orders_Source_2_Target.xlsx?d=wa35fc5d3b6fa46a2a0fc2d754054cc8e)
- [Epic](https://mctools.sharepoint.com/teams/UDPDAIS/Shared%20Documents/UDP%20Data%20Mart%20Documents/Z_S2T_Model_for_Website/Orders/Business%20Spec%20and%20S2T/Epic/Epic_ORDERS_Source_2_Target.xlsx?d=w9375cf891e294cbf862f5ee56425afc0)

## Example Query

### Fact Table Indexed Columns

**Note:** Subject to changes. Please use the following column(s) in your query filter for faster and more efficient data retrieval.

- `SOURCE_SYSTEM_KEY`
- `PATIENT_DK + ORDER_ITEM_DK`
- `ORDER_ID`
- `ORDER_ITEM_DK + ORDER_DTM`
- `ORDER_DTM + PATIENT_DK`
- `ORDER_START_DTM + PATIENT_DK`
- `ENCOUNTER_NUMBER + PATIENT_D`

### Sample Query: 

This is a sample query to get you started. Query you need for your use case may be different than this sample.
```sql
SELECT
  ORS.SOURCE_SYSTEM_KEY, PT.PATIENT_CLINIC_NUMBER, ORS.PATIENT_AGE_AT_EVENT,ORS.ORDERING_PROVIDER_DK, OI.ORDER_CODE, OI.ORDER_NAME, OI.ORDER_DESCRIPTION,
  ORS.LOCATION_SITE_NAME,
  ORS.ORDERING_LOCATION_DK,
  LOC.LOCATION_CODE,
  LOC.LOCATION_DESCRIPTION AS ORDER_LOC,
  LOC.LOCATION_SITE_CODE, LOC.LOCATION_SITE_NAME, LOC.LOCATION_STATE_CODE, LOC.LOCATION_STATE_NAME,
  LOC.LOCATION_LEVEL, LOC.SOURCE_SYSTEM_KEY AS LOC_SRC_SYSTEM,
  DLOC.LOCATION_DESCRIPTION AS DISPENSE_LOC,
  ORS.ORDER_DTM,ORS.ORDER_TIME_DK, ORS.ORDER_DATE_DK, ORS.ORDER_APPROVE_DTM, ORS.ORDER_EFFECTIVE_DTM,
  ORS.ORDER_EXPIRATION_DTM,ORS.ORDER_STOP_DTM, ORS.ORDER_ID,
  ORS.ORDER_TYPE_CODE, ORS.ORDER_TYPE_DESCRIPTION, ORS.ORDER_SUBTYPE_CODE, ORS.ORDER_DOSE_AMOUNT, ORS.ORDER_DOSE_UNITS,
  ORS.ORDER_DISPENSE_AMOUNT, ORS.ORDER_QUANTITY, ORS.ORDER_DURATION_AMOUNT, ORS.ORDER_VOLUME,
  ORS.ORDER_FORM_DESCRIPTION,
  ORS.ORDER_ROUTE_CODE, ORS.ORDER_ROUTE_DESCRIPTION, ORS.ORDER_DOSE_FORM_ROUTE_DESCRIPTION, ORS.ORDER_STRENGTH,
  ORS.ORDER_STRENGTH_UNITS, ORS.ORDER_DISPENSE_MODE_CODE, ORS.ORDER_DISPENSE_MODE_DESCRIPTION, ORS.ORDER_DESCRIPTION,
  ORS.MED_GENERIC, ORS.ORDER_INSTRUCTIONS
FROM EDTWH.FACT_ORDERS ORS
  JOIN EDTWH.DIM_PATIENT PT
    ON (ORS.PATIENT_DK = PT.PATIENT_DK)
  JOIN EDTWH.DIM_HEALTHCARE_PROVIDER OP
    ON (ORS.ORDERING_PROVIDER_DK=OP.PROVIDER_DK)
  JOIN EDTWH.DIM_LOCATION LOC
    ON (ORS.ORDERING_LOCATION_DK=LOC.LOCATION_DK)
  JOIN EDTWH.DIM_LOCATION DLOC
    ON (ORS.DISPENSING_LOCATION_DK=DLOC.LOCATION_DK)
  JOIN EDTWH.DIM_SOURCE_SYSTEM SYS
    ON (ORS.SOURCE_SYSTEM_DK = SYS.SOURCE_SYSTEM_DK)
  JOIN EDTWH.DIM_ORDER_ITEM OI
    ON (OI.ORDER_ITEM_DK = ORS.ORDER_ITEM_DK)
WHERE ORS.ORDER_DTM between '2002-06-01 00:00:00' AND '2002-12-31 23:59:59'
  AND ORS.ENCOUNTER_NUMBER IN (3908743,3908960)
  AND ORS.ORDER_ID IN (3853743993,3853743997,3853744001)
```