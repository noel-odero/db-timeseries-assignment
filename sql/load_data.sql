-- ==================================================
-- LOAD_DATA.SQL - How I imported the data into MySQL
-- ==================================================

-- Step 1: I Created staging table for raw CSV data
-- --------------------------------------------

mysql> CREATE TABLE temp_staging (
    ->     col1 VARCHAR(255),
    ->     col2 VARCHAR(255),
    ->     col3 VARCHAR(255),
    ->     col4 VARCHAR(255),
    ->     col5 VARCHAR(255),
    ->     col6 VARCHAR(255),
    ->     col7 VARCHAR(255),
    ->     col8 VARCHAR(255),
    ->     col9 VARCHAR(255),
    ->     col10 VARCHAR(255),
    ->     col11 VARCHAR(255),
    ->     col12 VARCHAR(255),
    ->     col13 VARCHAR(255),
    ->     col14 VARCHAR(255),
    ->     col15 VARCHAR(255),
    ->     col16 VARCHAR(255),
    ->     col17 VARCHAR(255),
    ->     col18 VARCHAR(255),
    ->     col19 VARCHAR(255),
    ->     col20 VARCHAR(255),
    ->     col21 VARCHAR(255),
    ->     col22 VARCHAR(255),
    ->     col23 VARCHAR(255),
    ->     col24 VARCHAR(255),
    ->     col25 VARCHAR(255),
    ->     col26 VARCHAR(255),
    ->     col27 VARCHAR(255),
    ->     col28 VARCHAR(255),
    ->     col29 VARCHAR(255),
    ->     col30 VARCHAR(255)
    -> );
Query OK, 0 rows affected (0.04 sec)

-- --------------------------------------------
-- Step 2: Load CSV data into staging table
-- Note: File path will vary by user
-- --------------------------------------------

mysql> LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/global_climate_health_impact_tracker_2015_2025.csv'
    -> INTO TABLE temp_staging
    -> FIELDS TERMINATED BY ','
    -> ENCLOSED BY '"'
    -> LINES TERMINATED BY '\n'
    -> IGNORE 1 ROWS;
Query OK, 14100 rows affected (0.45 sec)
Records: 14100  Deleted: 0  Skipped: 0  Warnings: 0

-- Verify data loaded into staging
mysql> SELECT COUNT(*) AS total_records_loaded FROM temp_staging;
+----------------------+
| total_records_loaded |
+----------------------+
|                14100 |
+----------------------+
1 row in set (0.11 sec)

-- --------------------------------------------
-- Step 3: Populate dimension tables
-- --------------------------------------------
mysql> INSERT IGNORE INTO countries (country_code, country_name, region, income_level, population_millions, latitude, longitude)
    -> SELECT DISTINCT
    ->     col2, col3, col4, col5,
    ->     CAST(col12 AS DECIMAL(10,2)),
    ->     CAST(col10 AS DECIMAL(10,6)),
    ->     CAST(col11 AS DECIMAL(10,6))
    -> FROM temp_staging;
Query OK, 25 rows affected (0.33 sec)
Records: 25  Duplicates: 0  Warnings: 0