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