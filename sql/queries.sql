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

-- --------------------------------------------
-- QUERY 3: Moving Average (4-week)
-- Purpose: Calculate rolling average of respiratory disease rate for Kenya
-- Required: Assignment requires lagged features/moving averages
-- --------------------------------------------

mysql> SELECT
    ->     c.country_name,
    ->     d.date,
    ->     hm.respiratory_disease_rate,
    ->     AVG(hm.respiratory_disease_rate) OVER (
    ->         ORDER BY d.date
    ->         ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
    ->     ) as moving_avg_4week
    -> FROM health_measurements hm
    -> JOIN countries c ON hm.country_id = c.country_id
    -> JOIN dates d ON hm.date_id = d.date_id
    -> WHERE c.country_code = 'KEN'
    -> ORDER BY d.date
    -> LIMIT 10;
+--------------+------------+--------------------------+------------------+
| country_name | date       | respiratory_disease_rate | moving_avg_4week |
+--------------+------------+--------------------------+------------------+
| Kenya        | 2015-01-04 |                    99.40 |        99.400000 |
| Kenya        | 2015-01-11 |                    82.60 |        91.000000 |
| Kenya        | 2015-01-18 |                    65.00 |        82.333333 |
| Kenya        | 2015-01-25 |                    77.60 |        81.150000 |
| Kenya        | 2015-02-01 |                    65.20 |        72.600000 |
| Kenya        | 2015-02-08 |                    90.70 |        74.625000 |
| Kenya        | 2015-02-15 |                    76.10 |        77.400000 |
| Kenya        | 2015-02-22 |                    79.60 |        77.900000 |
| Kenya        | 2015-03-01 |                    79.60 |        81.500000 |
| Kenya        | 2015-03-08 |                    85.70 |        80.250000 |
+--------------+------------+--------------------------+------------------+
10 rows in set (0.03 sec)