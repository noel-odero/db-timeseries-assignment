-- ============================================
-- QUERIES.SQL - Analytical Queries for Task 2
-- ============================================

-- --------------------------------------------
-- QUERY 1: Latest Record for a Country
-- Purpose: Get the most recent climate and health data for USA
-- Used in: Task 2 required endpoint
-- --------------------------------------------

mysql> 
mysql> SELECT
    ->     c.country_name,
    ->     d.date,
    ->     cm.temperature_celsius,
    ->     cm.precipitation_mm,
    ->     hm.respiratory_disease_rate,
    ->     hm.heat_related_admissions
    -> FROM health_measurements hm
    -> JOIN climate_measurements cm ON hm.country_id = cm.country_id AND hm.date_id = cm.date_id
    -> JOIN countries c ON hm.country_id = c.country_id
    -> JOIN dates d ON hm.date_id = d.date_id
    -> WHERE c.country_code = 'USA'
    -> ORDER BY d.date DESC
    -> LIMIT 1;
+---------------+------------+---------------------+------------------+--------------------------+-------------------------+
| country_name  | date       | temperature_celsius | precipitation_mm | respiratory_disease_rate | heat_related_admissions |
+---------------+------------+---------------------+------------------+--------------------------+-------------------------+
| United States | 2025-10-19 |               -4.71 |            73.70 |                    70.60 |                    0.00 |
+---------------+------------+---------------------+------------------+--------------------------+-------------------------+
1 row in set (0.00 sec)

-- --------------------------------------------
-- QUERY 2: Records by Date Range
-- Purpose: Get all records for India during Summer 2024
-- Used in: Task 2 required endpoint
-- --------------------------------------------

mysql> SELECT
    ->     c.country_name,
    ->     d.date,
    ->     cm.temperature_celsius,
    ->     hm.respiratory_disease_rate,
    ->     hm.heat_related_admissions
    -> FROM health_measurements hm
    -> JOIN climate_measurements cm ON hm.country_id = cm.country_id AND hm.date_id = cm.date_id
    -> JOIN countries c ON hm.country_id = c.country_id
    -> JOIN dates d ON hm.date_id = d.date_id
    -> WHERE c.country_code = 'IND'
    ->   AND d.date BETWEEN '2024-06-01' AND '2024-08-31'
    -> ORDER BY d.date;
+--------------+------------+---------------------+--------------------------+-------------------------+
| country_name | date       | temperature_celsius | respiratory_disease_rate | heat_related_admissions |
+--------------+------------+---------------------+--------------------------+-------------------------+
| India        | 2024-06-02 |               17.51 |                    87.60 |                   14.80 |
| India        | 2024-06-09 |               16.65 |                    85.50 |                   12.70 |
| India        | 2024-06-16 |               15.84 |                    72.20 |                    4.50 |
| India        | 2024-06-23 |               13.48 |                    76.10 |                    0.00 |
| India        | 2024-06-30 |               11.39 |                    69.70 |                    0.00 |
| India        | 2024-07-07 |               13.56 |                    98.30 |                    0.50 |
| India        | 2024-07-14 |                5.76 |                    72.60 |                    0.00 |
| India        | 2024-07-21 |               13.00 |                    80.90 |                    0.00 |
| India        | 2024-07-28 |               10.42 |                    72.80 |                    0.00 |
| India        | 2024-08-04 |                7.14 |                    63.80 |                    0.00 |
| India        | 2024-08-11 |                9.30 |                   110.20 |                    0.00 |
| India        | 2024-08-18 |                5.82 |                    66.90 |                    0.00 |
| India        | 2024-08-25 |                7.72 |                    70.50 |                    0.00 |
+--------------+------------+---------------------+--------------------------+-------------------------+
13 rows in set (0.04 sec)
