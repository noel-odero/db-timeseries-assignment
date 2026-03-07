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
-- Insert into countries
mysql> INSERT IGNORE INTO countries (country_code, country_name, region, income_level, population_millions, latitude, longitude)
    -> SELECT DISTINCT
    ->     col2, col3, col4, col5,
    ->     CAST(col12 AS DECIMAL(10,2)),
    ->     CAST(col10 AS DECIMAL(10,6)),
    ->     CAST(col11 AS DECIMAL(10,6))
    -> FROM temp_staging;
Query OK, 25 rows affected (0.33 sec)
Records: 25  Duplicates: 0  Warnings: 0

-- Insert into dates
mysql> INSERT IGNORE INTO dates (date, year, month, week, quarter, day_of_week, is_weekend)
    -> SELECT DISTINCT
    ->     col6,
    ->     CAST(col7 AS UNSIGNED),
    ->     CAST(col8 AS UNSIGNED),
    ->     CAST(col9 AS UNSIGNED),
    ->     QUARTER(col6),
    ->     DAYOFWEEK(col6) - 1,
    ->     CASE WHEN DAYOFWEEK(col6) IN (1,7) THEN TRUE ELSE FALSE END
    -> FROM temp_staging;
Query OK, 564 rows affected (0.22 sec)
Records: 564  Duplicates: 0  Warnings: 0


-- --------------------------------------------
-- Step 4: Populate fact tables
-- --------------------------------------------

-- Insert into climate_measurements
mysql> INSERT INTO climate_measurements (
    ->     country_id, date_id, temperature_celsius, temp_anomaly_celsius,
    ->     precipitation_mm, heat_wave_days, drought_indicator,
    ->     flood_indicator, extreme_weather_events, pm25_ugm3, air_quality_index
    -> )
    -> SELECT
    ->     c.country_id,
    ->     d.date_id,
    ->     CAST(t.col13 AS DECIMAL(5,2)),
    ->     CAST(t.col14 AS DECIMAL(4,2)),
    ->     CAST(t.col15 AS DECIMAL(6,2)),
    ->     CAST(t.col16 AS UNSIGNED),
    ->     CAST(t.col17 AS UNSIGNED),
    ->     CAST(t.col18 AS UNSIGNED),
    ->     CAST(t.col19 AS UNSIGNED),
    ->     CAST(t.col20 AS DECIMAL(6,2)),
    ->     CAST(t.col21 AS DECIMAL(6,2))  -- Changed from UNSIGNED to DECIMAL(6,2)
    -> FROM temp_staging t
    -> JOIN countries c ON t.col2 = c.country_code
    -> JOIN dates d ON t.col6 = d.date
    -> ON DUPLICATE KEY UPDATE
    ->     temperature_celsius = VALUES(temperature_celsius);
Query OK, 14100 rows affected, 1 warning (1.42 sec)
Records: 14100  Duplicates: 0  Warnings: 1

-- Insert into health_measurements

mysql> INSERT INTO health_measurements (
    ->     country_id, date_id, respiratory_disease_rate,
    ->     cardio_mortality_rate, vector_disease_risk_score,
    ->     waterborne_disease_incidents, heat_related_admissions,
    ->     mental_health_index, food_security_index,
    ->     healthcare_access_index, gdp_per_capita_usd
    -> )
    -> SELECT
    ->     c.country_id,
    ->     d.date_id,
    ->     CAST(t.col22 AS DECIMAL(8,2)),
    ->     CAST(t.col23 AS DECIMAL(8,2)),
    ->     CAST(t.col24 AS DECIMAL(5,2)),
    ->     CAST(t.col25 AS DECIMAL(8,2)),
    ->     CAST(t.col26 AS DECIMAL(8,2)),
    ->     CAST(t.col29 AS DECIMAL(5,2)),
    ->     CAST(t.col30 AS DECIMAL(5,2)),
    ->     CAST(t.col27 AS DECIMAL(5,2)),
    ->     CAST(t.col28 AS DECIMAL(10,2))
    -> FROM temp_staging t
    -> JOIN countries c ON t.col2 = c.country_code
    -> JOIN dates d ON t.col6 = d.date
    -> ON DUPLICATE KEY UPDATE
    ->     respiratory_disease_rate = VALUES(respiratory_disease_rate);
Query OK, 14100 rows affected, 1 warning (1.54 sec)
Records: 14100  Duplicates: 0  Warnings: 1