# BiqQuery Best Practices and Example Queries

There are several techniques that can be used to improve query efficiency. A full list of recommendations from Google can be found here, and below is a summary of the most effective.

## Target Specific Columns

Avoid using "Select *" wherever possible. If you are selecting from a table, you can utilize data previewing to decide what columns to use ahead of time. You can find the preview tab by searching for the table via BigQuery in the Google Cloud Console.

### Example:

```sql
--Inefficient, returns the entire table
select * from `ml-mps-adl-intfhr-phi-p-3b6e.phi_primary_use_fhir_clinicnumber_us_p.Patient`


--Instead, use something like this
select DATE_DIFF(CURRENT_DATE, SAFE_CAST(pat.birth_date AS DATE), YEAR) AS Age,
  pat.us_core_birthsex AS Sex,
  pat.marital_status,
  pat.us_core_race_text,
  pat.address_home_line1,
  pat.id AS PatID,
  pat.clinic_number,
  pat.family_name,
  pat.given_name,
  pat.general_practitioner
from `ml-mps-adl-intfhr-phi-p-3b6e.phi_primary_use_fhir_clinicnumber_us_p.Patient` pat
```

## Joining Tables

Though there are several connecting fields between tables, i.e. patient_id and encounter_id, it is best to use the partitioned field wherever possible. For all tables with patient data, this is the clinic_number(MRN).

To find what field(s) are partitioned or clustered, go to BigQuery in Google Cloud Console > Search for your table and open it in a new tab > Select the Details tab > If a partition exists, you will find the field under "Partitioned on field." If a cluster exists, you will find the field(s) under "Clustered by."

### Joining on Partitioned Value Example:

```sql
select DATE_DIFF(CURRENT_DATE, SAFE_CAST(pat.birth_date AS DATE), YEAR) AS Age,
  pat.us_core_birthsex AS Sex,
  pat.marital_status,
  pat.us_core_race_text,
  pat.address_home_line1,
  pat.id AS PatID,
  pat.clinic_number,
  pat.family_name,
  pat.given_name,
  pat.general_practitioner,
  enc.id AS EncID,
  SAFE_CAST(enc.period_start AS DATE) AS encounter_start,
  SAFE_CAST(enc.period_end AS DATE) AS encounter_end,
from `ml-mps-adl-intfhr-phi-p-3b6e.phi_primary_use_fhir_clinicnumber_us_p.Encounter` enc
inner join `ml-mps-adl-intfhr-phi-p-3b6e.phi_primary_use_fhir_clinicnumber_us_p.Patient` pat on enc.clinic_number = pat.clinic_number
```
### Multiple Joins

Avoid using Outer Joins when possible. When not possible, use Inner Joins before Outer Joins as this will reduce the number of records sooner.

Always join the largest table to the smallest table and then decreasing size after (ex: 1000, 5, 500, 300, 200). In the example below, Encounter is the largest of the three tables, hence its position as the FROM table. Encounter is joined to Patient, the smallest of the three tables, followed by DiagnosticReport.

#### Multiple Joins Example

```sql
select DATE_DIFF(CURRENT_DATE, SAFE_CAST(pat.birth_date AS DATE), YEAR) AS Age,
  pat.us_core_birthsex AS Sex,
  pat.marital_status,
  pat.us_core_race_text,
  pat.address_home_line1,
  pat.id AS PatID,
  pat.clinic_number,
  pat.family_name,
  pat.given_name,
  pat.general_practitioner,
  enc.id AS EncID,
  SAFE_CAST(enc.period_start AS DATE) AS encounter_start,
  SAFE_CAST(enc.period_end AS DATE) AS encounter_end,
  dr.id,
  dr.code_text
from `ml-mps-adl-intfhr-phi-p-3b6e.phi_primary_use_fhir_clinicnumber_us_p.Encounter` enc --501,860,067 rows
inner join `ml-mps-adl-intfhr-phi-p-3b6e.phi_primary_use_fhir_clinicnumber_us_p.Patient` pat on enc.clinic_number = pat.clinic_number --11,662,759 rows
inner join `ml-mps-adl-intfhr-phi-p-3b6e.phi_primary_use_fhir_clinicnumber_us_p.DiagnosticReport` dr on dr.clinic_number = pat.clinic_number and dr.encounter_number = enc.encounter_number --135,676,715 rows
```

Joins should be done on Bool or Int fields instead of Strings.

## Filters

Additionally, filters on Joined tables should be placed within the Join as part of the ON condition to drop records sooner rather than later as seen below.

### Filters within joins example

```sql
select DATE_DIFF(CURRENT_DATE, SAFE_CAST(pat.birth_date AS DATE), YEAR) AS Age,
  pat.us_core_birthsex AS Sex,
  pat.marital_status,
  pat.us_core_race_text,
  pat.address_home_line1,
  pat.id AS PatID,
  pat.clinic_number,
  pat.family_name,
  pat.given_name,
  pat.general_practitioner,
  enc.id AS EncID,
  SAFE_CAST(enc.period_start AS DATE) AS encounter_start,
  SAFE_CAST(enc.period_end AS DATE) AS encounter_end,
  dr.id,
  dr.code_text
from `ml-mps-adl-intfhr-phi-p-3b6e.phi_primary_use_fhir_clinicnumber_us_p.Encounter` enc
inner join `ml-mps-adl-intfhr-phi-p-3b6e.phi_primary_use_fhir_clinicnumber_us_p.Patient` pat on enc.clinic_number = pat.clinic_number and DATE_DIFF(CURRENT_DATE, SAFE_CAST(pat.birth_date AS DATE), YEAR) = 40 and pat.clinic_number > 14000000
inner join `ml-mps-adl-intfhr-phi-p-3b6e.phi_primary_use_fhir_clinicnumber_us_p.DiagnosticReport` dr on dr.clinic_number = pat.clinic_number and dr.encounter_number = enc.encounter_number
```
### Filters Best Practices

Filters should be ordered by type: Partition, Cluster, Bool, Int, Float, Date, String. Filters should also be ordered by most selective (=, !=) before least selective (In, >, <, Like).

When filtering, if a table has a partition, the partition must be the first field filtered or you will likely see degredation. Even if you aren't querying on a partitioned field, you should still include it in the filter as it will improve query efficiency. Then, any clustered fields should be filtered in order by how they are listed in the BQ Console (to find the partition or clustered fields, see the section under Joining Tables).

#### Order of Filters Example

```sql
select DATE_DIFF(CURRENT_DATE, SAFE_CAST(pat.birth_date AS DATE), YEAR) AS Age,
  pat.us_core_birthsex AS Sex,
  pat.marital_status,
  pat.us_core_race_text,
  pat.address_home_line1,
  pat.id AS PatID,
  pat.clinic_number,
  pat.family_name,
  pat.given_name,
  pat.general_practitioner
from `ml-mps-adl-intfhr-phi-p-3b6e.phi_primary_use_fhir_clinicnumber_us_p.Patient` pat 
where pat.clinic_number > 14000000
AND DATE_DIFF(CURRENT_DATE, SAFE_CAST(pat.birth_date AS DATE), YEAR) = 40
AND UPPER(pat.marital_status) = 'MARRIED'
AND UPPER(pat.address_home_state) IN ('MINNESOTA', 'WISCONSIN','MN','WI')
```
If you have to convert a value to filter on it (ex: Int = String), cast the String if possible because Integer comparisons are more efficient. Similarly, if filtering on a Date field, pass a Date instead of a String.

```sql
select DATE_DIFF(CURRENT_DATE, SAFE_CAST(pat.birth_date AS DATE), YEAR) AS Age,
SAFE_CAST(pat.birth_date AS DATE),
  pat.us_core_birthsex AS Sex,
  pat.marital_status,
  pat.us_core_race_text,
  pat.address_home_line1,
  pat.address_home_postal_code,
  pat.id AS PatID,
  pat.clinic_number,
  pat.family_name,
  pat.given_name,
  pat.general_practitioner
from `ml-mps-adl-intfhr-phi-p-3b6e.phi_primary_use_fhir_clinicnumber_us_p.Patient` pat 
where pat.clinic_number = 12007729 and pat.birth_date = DATE('1980-12-13') and SAFE_CAST(pat.address_home_postal_code AS INT) = 54670
```
## Temporary Tables

Like the WHERE clause in the first example, Temp Tables or CTEs (Common Table Expressions) can be used to filter data before it is used in a larger query. A Temp Table or CTE should be used instead of sub-queries, when you need to join to the same data more than once, or any time you need to join to a large table.

A Temp Table is stored in tempdb and can be indexed and have column statistics. The table will be automatically removed from memory 24 hours after creation. A CTE is a temporary result set used within a query - it cannot be reused in multiple queries like a Temp Table.

Below is an example of using multiple Temp Tables and CTEs in a query to limit the data to encounters from 2019.

Although one may seem more appropriate for your needs, the other may still perform better for your specific query (as you can see in the examples below), so try both and see which is more efficient for your query.

Note the use of filters within the the Temp Tables and CTEs. Using filters in this way reduces the total rows faster - decreasing the overall cost of the query.

### Temporary Tables Example

```sql
--Average Slot Usage: 35 slots
--Average Elapsed Time: 6 seconds
CREATE TEMP TABLE encounter_temp AS (
  SELECT
    enc.encounter_number,
    enc.patient_id,
    enc.id AS EncID,
    SAFE_CAST(enc.period_start AS DATE) AS encounter_start,
    SAFE_CAST(enc.period_end AS DATE) AS encounter_end,
    enc.clinic_number
  FROM `ml-mps-adl-intfhr-phi-p-3b6e.phi_primary_use_fhir_clinicnumber_us_p.Encounter` enc
  WHERE enc.clinic_number > 14000000
  AND DATE(enc.period_start) >= DATE('2019-01-01') AND DATE(enc.period_end) <= DATE('2019-12-31')
);
CREATE TEMP TABLE patient_temp AS (
  SELECT
    DATE_DIFF(CURRENT_DATE, SAFE_CAST(pat.birth_date AS DATE), YEAR) AS Age,
    pat.us_core_birthsex AS Sex,
    pat.marital_status,
    pat.us_core_race_text,
    pat.address_home_line1,
    pat.id AS PatID,
    pat.clinic_number,
    pat.family_name,
    pat.given_name,
    pat.general_practitioner,
  FROM `ml-mps-adl-intfhr-phi-p-3b6e.phi_primary_use_fhir_clinicnumber_us_p.Patient` pat
  WHERE pat.clinic_number > 14000000
  AND UPPER(pat.address_home_state) IN ('MINNESOTA', 'WISCONSIN', 'MN', 'WI')
);
select
  enc.encounter_number,
  enc.patient_id,
  enc.EncID,
  enc.encounter_start,
  enc.encounter_end,
  enc.clinic_number,
  pat.Age,
  pat.Sex,
  pat.marital_status,
  pat.us_core_race_text,
  pat.address_home_line1,
  pat.PatID,
  pat.clinic_number,
  pat.family_name,
  pat.given_name,
  pat.general_practitioner,
  dr.id,
  dr.code_text
from encounter_temp enc
inner join  patient_temp pat on enc.clinic_number = pat.clinic_number
INNER JOIN `ml-mps-adl-intfhr-phi-p-3b6e.phi_primary_use_fhir_clinicnumber_us_p.DiagnosticReport` dr on dr.clinic_number = pat.clinic_number and dr.encounter_number = enc.encounter_number
```
### Multiple CTE Example:

```sql
--Average Slot Usage: 52 slots
--Average Elapsed Time: 2 seconds
WITH encounter_cte AS (
  SELECT
    enc.encounter_number,
    enc.patient_id,
    enc.id AS EncID,
    SAFE_CAST(enc.period_start AS DATE) AS encounter_start,
    SAFE_CAST(enc.period_end AS DATE) AS encounter_end,
    enc.clinic_number
  FROM `ml-mps-adl-intfhr-phi-p-3b6e.phi_primary_use_fhir_clinicnumber_us_p.Encounter` enc
  WHERE enc.clinic_number > 14000000
  AND DATE(enc.period_start) >= DATE('2019-01-01') AND DATE(enc.period_end) <= DATE('2019-12-31')
),
 patient_cte AS (
  SELECT
    DATE_DIFF(CURRENT_DATE, SAFE_CAST(pat.birth_date AS DATE), YEAR) AS Age,
    pat.us_core_birthsex AS Sex,
    pat.marital_status,
    pat.us_core_race_text,
    pat.address_home_line1,
    pat.id AS PatID,
    pat.clinic_number,
    pat.family_name,
    pat.given_name,
    pat.general_practitioner,
  FROM `ml-mps-adl-intfhr-phi-p-3b6e.phi_primary_use_fhir_clinicnumber_us_p.Patient` pat
  WHERE pat.clinic_number > 14000000
  AND UPPER(pat.address_home_state) IN ('MINNESOTA', 'WISCONSIN', 'MN', 'WI')
)
select
  enc.encounter_number,
  enc.patient_id,
  enc.EncID,
  enc.encounter_start,
  enc.encounter_end,
  enc.clinic_number,
  pat.Age,
  pat.Sex,
  pat.marital_status,
  pat.us_core_race_text,
  pat.address_home_line1,
  pat.PatID,
  pat.clinic_number,
  pat.family_name,
  pat.given_name,
  pat.general_practitioner,
  dr.id,
  dr.code_text
from encounter_cte enc
inner join  patient_cte pat on enc.clinic_number = pat.clinic_number
INNER JOIN `ml-mps-adl-intfhr-phi-p-3b6e.phi_primary_use_fhir_clinicnumber_us_p.DiagnosticReport` dr on dr.clinic_number = pat.clinic_number and dr.encounter_number = enc.encounter_number
```
## Miscellaneous

Instead of DISTINCT, do a GROUP BY of any selected fields. In BigQuery, DISTINCT does a distinct of every field selected which is non-performant.

### Group By Example

```sql
select MAX(pat.last_updated),
  pat.id AS PatID,
  pat.clinic_number,
from `ml-mps-adl-intfhr-phi-p-3b6e.phi_primary_use_fhir_clinicnumber_us_p.Patient` pat 
group by PatID, pat.clinic_number
having pat.clinic_number > 14000000
```

### Group By All Example

```sql
select DATE_DIFF(CURRENT_DATE, SAFE_CAST(pat.birth_date AS DATE), YEAR) AS Age,
  pat.us_core_birthsex AS Sex,
  pat.marital_status,
  pat.us_core_race_text,
  pat.address_home_line1,
  pat.id AS PatID,
  pat.clinic_number,
from `ml-mps-adl-intfhr-phi-p-3b6e.phi_primary_use_fhir_clinicnumber_us_p.Patient` pat 
group by all
having pat.clinic_number > 14000000
```

Instead of traditional expressions (i.e. CURRENT_DATE - 5) use BQ functions (i.e. DATE_SUB(CURRENT_DATE, INTERVAL 5 DAY)). A list of functions can be found here.

Instead of Row_Number, use Array_Agg when trying to get just the first or last field. Array_Agg runs more efficiently because the ORDER BY is allowed to drop everything except the top record on each GROUP BY.

### Array_agg Example

```sql
//Returns the latest update by patient
select
  DATE_DIFF(CURRENT_DATE, SAFE_CAST(pat_latest_update.birth_date AS DATE), YEAR) AS Age,
  pat_latest_update.us_core_birthsex AS Sex,
  pat_latest_update.marital_status,
  pat_latest_update.us_core_race_text,
  pat_latest_update.address_home_line1,
  pat_latest_update.id AS PatID,
  pat_latest_update.clinic_number
from (
  select array_agg(
    pat order by pat.last_updated desc limit 1
  )[offset(0)] pat_latest_update
  from 
    `ml-mps-adl-intfhr-phi-p-3b6e.phi_primary_use_fhir_clinicnumber_us_p.Patient` pat
  group by 
    pat.clinic_number
)
```

The LIMIT function only limits the amount of records returned not the amount searched. As such, it will not reduce the cost of a query.