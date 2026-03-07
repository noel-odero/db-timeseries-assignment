# API endpoints using flask for MYSQL CRUD operations on health and climate data

from flask import Flask, app, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app)

# ============================================
# MYSQL CONNECTION CONFIG
# ============================================
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': os.getenv('MYSQL_PASSWORD'),  # Gets password from .env file
    'database': 'climate_health_db'
}

# Test connection on startupc
try:
    conn = mysql.connector.connect(**mysql_config)
    print("MySQL Connected successfully!")
    conn.close()
except Exception as e:
    print(f" MySQL Connection failed: {e}")

def get_db_connection():
    """Create and return a MySQL connection"""
    return mysql.connector.connect(**mysql_config)

# ============================================
# HELPER FUNCTION TO GET COUNTRY_ID AND DATE_ID
# ============================================
def get_country_id(country_code):
    """Get country_id from country_code"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT country_id FROM countries WHERE country_code = %s", (country_code.upper(),))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def get_date_id(date_str):
    """Get date_id from date string (YYYY-MM-DD)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT date_id FROM dates WHERE date = %s", (date_str,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    # If date doesn't exist, we'll need to insert it
    if not result:
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert the new date
            insert_query = """
                INSERT INTO dates (date, year, month, week, quarter, day_of_week, is_weekend)
                VALUES (%s, YEAR(%s), MONTH(%s), WEEK(%s, 3), QUARTER(%s), 
                        DAYOFWEEK(%s)-1, CASE WHEN DAYOFWEEK(%s) IN (1,7) THEN TRUE ELSE FALSE END)
            """
            cursor.execute(insert_query, (date_str, date_str, date_str, date_str, date_str, date_str, date_str))
            conn.commit()
            
            # Get the new date_id
            cursor.execute("SELECT date_id FROM dates WHERE date = %s", (date_str,))
            result = cursor.fetchone()
        except Exception as e:
            print(f"Error inserting date: {e}")
        finally:
            cursor.close()
            conn.close()
            
    return result[0] if result else None
# ============================================
# CREATE (POST) - Add new health record (FULL WORKING VERSION)
# ============================================
@app.route('/api/mysql/health', methods=['POST'])
def create_health_record():
    """Create a new health record in MySQL"""
    data = request.json
    
    # Required fields
    required_fields = ['country_code', 'date']
    for field in required_fields:
        if field not in data:
            return jsonify({
                "success": False,
                "error": f"Missing required field: {field}"
            }), 400
    
    try:
        # Get country_id from country_code
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get country_id
        cursor.execute("SELECT country_id FROM countries WHERE country_code = %s", (data['country_code'].upper(),))
        country_result = cursor.fetchone()
        if not country_result:
            cursor.close()
            conn.close()
            return jsonify({
                "success": False,
                "error": f"Country code {data['country_code']} not found"
            }), 404
        country_id = country_result[0]
        
        # Get or create date_id
        cursor.execute("SELECT date_id FROM dates WHERE date = %s", (data['date'],))
        date_result = cursor.fetchone()
        
        if date_result:
            date_id = date_result[0]
        else:
            # Insert new date
            insert_date_query = """
                INSERT INTO dates (date, year, month, week, quarter, day_of_week, is_weekend)
                VALUES (%s, YEAR(%s), MONTH(%s), WEEK(%s, 3), QUARTER(%s), 
                        DAYOFWEEK(%s)-1, CASE WHEN DAYOFWEEK(%s) IN (1,7) THEN TRUE ELSE FALSE END)
            """
            cursor.execute(insert_date_query, (data['date'], data['date'], data['date'], 
                                              data['date'], data['date'], data['date'], data['date']))
            conn.commit()
            
            # Get the new date_id
            cursor.execute("SELECT date_id FROM dates WHERE date = %s", (data['date'],))
            date_id = cursor.fetchone()[0]
        
        # Insert into health_measurements
        insert_query = """
            INSERT INTO health_measurements (
                country_id, date_id, 
                respiratory_disease_rate, cardio_mortality_rate, 
                vector_disease_risk_score, waterborne_disease_incidents,
                heat_related_admissions, mental_health_index,
                food_security_index, healthcare_access_index,
                gdp_per_capita_usd
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            country_id, date_id,
            data.get('respiratory_rate'),
            data.get('cardio_mortality'),
            data.get('vector_risk'),
            data.get('waterborne_incidents'),
            data.get('heat_admissions'),
            data.get('mental_health'),
            data.get('food_security'),
            data.get('healthcare_access'),
            data.get('gdp_per_capita')
        )
        
        cursor.execute(insert_query, values)
        conn.commit()
        
        # Get the new record ID
        record_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "message": "Health record created successfully",
            "record_id": record_id
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    

# ============================================
# READ (GET) - Get all health records
# ============================================
@app.route('/api/mysql/health', methods=['GET'])
def get_all_health_records():
    """Get all health records with optional filters"""
    country = request.args.get('country')
    limit = request.args.get('limit', 50)
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        if country:
            query = """
                SELECT 
                    hm.measurement_id,
                    c.country_name,
                    c.country_code,
                    d.date,
                    hm.respiratory_disease_rate,
                    hm.cardio_mortality_rate,
                    hm.vector_disease_risk_score,
                    hm.waterborne_disease_incidents,
                    hm.heat_related_admissions,
                    hm.mental_health_index,
                    hm.food_security_index,
                    hm.healthcare_access_index,
                    hm.gdp_per_capita_usd
                FROM health_measurements hm
                JOIN countries c ON hm.country_id = c.country_id
                JOIN dates d ON hm.date_id = d.date_id
                WHERE c.country_code = %s
                ORDER BY d.date DESC
                LIMIT %s
            """
            cursor.execute(query, (country.upper(), int(limit)))
        else:
            query = """
                SELECT 
                    hm.measurement_id,
                    c.country_name,
                    c.country_code,
                    d.date,
                    hm.respiratory_disease_rate,
                    hm.cardio_mortality_rate,
                    hm.vector_disease_risk_score,
                    hm.waterborne_disease_incidents,
                    hm.heat_related_admissions,
                    hm.mental_health_index,
                    hm.food_security_index,
                    hm.healthcare_access_index,
                    hm.gdp_per_capita_usd
                FROM health_measurements hm
                JOIN countries c ON hm.country_id = c.country_id
                JOIN dates d ON hm.date_id = d.date_id
                ORDER BY d.date DESC
                LIMIT %s
            """
            cursor.execute(query, (int(limit),))
        
        results = cursor.fetchall()
        
        # Convert date objects to strings
        for row in results:
            row['date'] = str(row['date'])
        
        return jsonify({
            "success": True,
            "count": len(results),
            "data": results
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ============================================
# READ (GET) - Get single record by ID
# ============================================
@app.route('/api/mysql/health/<int:record_id>', methods=['GET'])
def get_health_record(record_id):
    """Get a single health record by ID"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                hm.measurement_id,
                c.country_name,
                c.country_code,
                d.date,
                hm.respiratory_disease_rate,
                hm.cardio_mortality_rate,
                hm.vector_disease_risk_score,
                hm.waterborne_disease_incidents,
                hm.heat_related_admissions,
                hm.mental_health_index,
                hm.food_security_index,
                hm.healthcare_access_index,
                hm.gdp_per_capita_usd,
                hm.created_at
            FROM health_measurements hm
            JOIN countries c ON hm.country_id = c.country_id
            JOIN dates d ON hm.date_id = d.date_id
            WHERE hm.measurement_id = %s
        """
        
        cursor.execute(query, (record_id,))
        result = cursor.fetchone()
        
        if result:
            result['date'] = str(result['date'])
            result['created_at'] = str(result['created_at'])
            return jsonify({
                "success": True,
                "data": result
            })
        else:
            return jsonify({
                "success": False,
                "error": f"Record {record_id} not found"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ============================================
# UPDATE (PUT) - Update a record
# ============================================
@app.route('/api/mysql/health/<int:record_id>', methods=['PUT'])
def update_health_record(record_id):
    """Update an existing health record"""
    data = request.json
    
    if not data:
        return jsonify({
            "success": False,
            "error": "No data provided for update"
        }), 400
    
    conn = None
    cursor = None
    try:
        # First check if record exists
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM health_measurements WHERE measurement_id = %s", (record_id,))
        existing = cursor.fetchone()
        
        if not existing:
            return jsonify({
                "success": False,
                "error": f"Record {record_id} not found"
            }), 404
        
        # Build dynamic update query based on provided fields
        update_fields = []
        values = []
        
        field_mapping = {
            'respiratory_rate': 'respiratory_disease_rate',
            'cardio_mortality': 'cardio_mortality_rate',
            'vector_risk': 'vector_disease_risk_score',
            'waterborne_incidents': 'waterborne_disease_incidents',
            'heat_admissions': 'heat_related_admissions',
            'mental_health': 'mental_health_index',
            'food_security': 'food_security_index',
            'healthcare_access': 'healthcare_access_index',
            'gdp_per_capita': 'gdp_per_capita_usd'
        }
        
        for json_field, db_field in field_mapping.items():
            if json_field in data:
                update_fields.append(f"{db_field} = %s")
                values.append(data[json_field])
        
        if not update_fields:
            return jsonify({
                "success": False,
                "error": "No valid fields to update"
            }), 400
        
        # Add record_id to values
        values.append(record_id)
        
        # Execute update
        query = f"UPDATE health_measurements SET {', '.join(update_fields)} WHERE measurement_id = %s"
        cursor.execute(query, values)
        conn.commit()
        
        # Get updated record
        cursor.execute("""
            SELECT 
                hm.measurement_id,
                c.country_code,
                d.date,
                hm.respiratory_disease_rate,
                hm.cardio_mortality_rate,
                hm.vector_disease_risk_score,
                hm.waterborne_disease_incidents,
                hm.heat_related_admissions,
                hm.mental_health_index,
                hm.food_security_index,
                hm.healthcare_access_index,
                hm.gdp_per_capita_usd
            FROM health_measurements hm
            JOIN countries c ON hm.country_id = c.country_id
            JOIN dates d ON hm.date_id = d.date_id
            WHERE hm.measurement_id = %s
        """, (record_id,))
        
        updated = cursor.fetchone()
        if updated:
            updated['date'] = str(updated['date'])
        
        return jsonify({
            "success": True,
            "message": "Record updated successfully",
            "data": updated
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ============================================
# DELETE (DELETE) - Delete a record
# ============================================
@app.route('/api/mysql/health/<int:record_id>', methods=['DELETE'])
def delete_health_record(record_id):
    """Delete a health record"""
    conn = None
    cursor = None
    try:
        # First check if record exists
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT measurement_id FROM health_measurements WHERE measurement_id = %s", (record_id,))
        existing = cursor.fetchone()
        
        if not existing:
            return jsonify({
                "success": False,
                "error": f"Record {record_id} not found"
            }), 404
        
        # Delete the record
        cursor.execute("DELETE FROM health_measurements WHERE measurement_id = %s", (record_id,))
        conn.commit()
        
        return jsonify({
            "success": True,
            "message": f"Record {record_id} deleted successfully"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ============================================
# CREATE CLIMATE RECORD (POST)
# ============================================
@app.route('/api/mysql/climate', methods=['POST'])
def create_climate_record():
    """Create a new climate record in MySQL"""
    data = request.json
    
    required_fields = ['country_code', 'date']
    for field in required_fields:
        if field not in data:
            return jsonify({
                "success": False,
                "error": f"Missing required field: {field}"
            }), 400
    
    try:
        country_id = get_country_id(data['country_code'])
        if not country_id:
            return jsonify({
                "success": False,
                "error": f"Country code {data['country_code']} not found"
            }), 404
        
        date_id = get_date_id(data['date'])
        if not date_id:
            return jsonify({
                "success": False,
                "error": f"Could not create/get date_id for {data['date']}"
            }), 500
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO climate_measurements (
                country_id, date_id, temperature_celsius, temp_anomaly_celsius,
                precipitation_mm, heat_wave_days, drought_indicator,
                flood_indicator, extreme_weather_events, pm25_ugm3, air_quality_index
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            country_id, date_id,
            data.get('temperature'),
            data.get('temp_anomaly'),
            data.get('precipitation'),
            data.get('heat_wave_days', 0),
            data.get('drought', False),
            data.get('flood', False),
            data.get('extreme_events', 0),
            data.get('pm25'),
            data.get('aqi')
        )
        
        cursor.execute(query, values)
        conn.commit()
        record_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "message": "Climate record created successfully",
            "record_id": record_id
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================
# REQUIRED ENDPOINTS (Latest & Range)
# ============================================

@app.route('/api/mysql/latest/<country_code>', methods=['GET'])
def get_latest_mysql(country_code):
    """Get latest record for a country (required endpoint)"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                c.country_name,
                d.date,
                cm.temperature_celsius,
                cm.precipitation_mm,
                hm.respiratory_disease_rate,
                hm.heat_related_admissions
            FROM health_measurements hm
            JOIN climate_measurements cm ON hm.country_id = cm.country_id AND hm.date_id = cm.date_id
            JOIN countries c ON hm.country_id = c.country_id
            JOIN dates d ON hm.date_id = d.date_id
            WHERE c.country_code = %s
            ORDER BY d.date DESC
            LIMIT 1
        """
        
        cursor.execute(query, (country_code.upper(),))
        result = cursor.fetchone()
        
        if result:
            result['date'] = str(result['date'])
            return jsonify({
                "success": True,
                "data": result
            })
        else:
            return jsonify({
                "success": False,
                "error": f"No data found for {country_code}"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/mysql/range', methods=['GET'])
def get_range_mysql():
    """Get records by date range (required endpoint)"""
    country = request.args.get('country')
    start = request.args.get('start')
    end = request.args.get('end')
    
    if not all([country, start, end]):
        return jsonify({
            "success": False,
            "error": "Missing parameters. Need: country, start, end"
        }), 400
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT 
                c.country_name,
                d.date,
                cm.temperature_celsius,
                cm.precipitation_mm,
                hm.respiratory_disease_rate,
                hm.heat_related_admissions
            FROM health_measurements hm
            JOIN climate_measurements cm ON hm.country_id = cm.country_id AND hm.date_id = cm.date_id
            JOIN countries c ON hm.country_id = c.country_id
            JOIN dates d ON hm.date_id = d.date_id
            WHERE c.country_code = %s AND d.date BETWEEN %s AND %s
            ORDER BY d.date
        """
        
        cursor.execute(query, (country.upper(), start, end))
        results = cursor.fetchall()
        
        for row in results:
            row['date'] = str(row['date'])
        
        return jsonify({
            "success": True,
            "count": len(results),
            "data": results
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ============================================
# TEST ENDPOINT
# ============================================
@app.route('/api/mysql/test', methods=['GET'])
def test_mysql():
    """Test MySQL connection and show stats"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get counts
        cursor.execute("SELECT COUNT(*) FROM countries")
        countries = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM dates")
        dates = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM health_measurements")
        health = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM climate_measurements")
        climate = cursor.fetchone()[0]
        
        cursor.close()
        
        return jsonify({
            "success": True,
            "mysql_status": "Connected",
            "database": "climate_health_db",
            "stats": {
                "countries": countries,
                "dates": dates,
                "health_records": health,
                "climate_records": climate
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    finally:
        if conn:
            conn.close()

# ============================================
# HOME
# ============================================
@app.route('/')
def home():
    return jsonify({
        "api": "Climate Health API - MySQL Full CRUD",
        "status": "Running",
        "mysql": "Connected",
        "crud_operations": {
            "create": {
                "health": "POST /api/mysql/health",
                "climate": "POST /api/mysql/climate"
            },
            "read": {
                "all": "GET /api/mysql/health",
                "single": "GET /api/mysql/health/{id}",
                "latest": "GET /api/mysql/latest/USA",
                "range": "GET /api/mysql/range?country=IND&start=2024-06-01&end=2024-08-31"
            },
            "update": {
                "health": "PUT /api/mysql/health/{id}"
            },
            "delete": {
                "health": "DELETE /api/mysql/health/{id}"
            }
        },
        "test": "/api/mysql/test"
    })

if __name__ == '__main__':
    print("="*60)
    print(" CLIMATE HEALTH API - FULL MYSQL CRUD")
    print("="*60)
    print("\n DATABASE: MySQL")
    print("   Host: localhost")
    print("   Database: climate_health_db")
    print("\n🔌 Testing connection...")
    
    # Test connection
    try:
        test_conn = mysql.connector.connect(**mysql_config)
        print("    MySQL Connected successfully!")
        test_conn.close()
    except Exception as e:
        print(f"    MySQL Connection failed: {e}")
        print("    Check your password in the code!")
    
    print("\n ENDPOINTS:")
    print("   • Test: http://127.0.0.1:5000/api/mysql/test")
    print("\n    REQUIRED ENDPOINTS:")
    print("   • Latest: http://127.0.0.1:5000/api/mysql/latest/USA")
    print("   • Range: http://127.0.0.1:5000/api/mysql/range?country=IND&start=2024-06-01&end=2024-08-31")
    print("\n    CRUD OPERATIONS:")
    print("   • CREATE (POST): http://127.0.0.1:5000/api/mysql/health")
    print("   • READ ALL (GET): http://127.0.0.1:5000/api/mysql/health")
    print("   • READ ONE (GET): http://127.0.0.1:5000/api/mysql/health/1")
    print("   • UPDATE (PUT): http://127.0.0.1:5000/api/mysql/health/1")
    print("   • DELETE (DELETE): http://127.0.0.1:5000/api/mysql/health/1")
    print("\n Starting server...")
    print("="*60)
    
    app.run(debug=True, port=5000)