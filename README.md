# Climate & Health Time-Series Database Assignment

A comprehensive database project analyzing the relationship between climate factors and health outcomes using MySQL and MongoDB, with machine learning predictions.

##  Project Overview

This project implements a full-stack solution for storing, analyzing, and predicting health outcomes based on climate data. It includes:

- **MySQL Database**: Structured relational database with star schema design
- **MongoDB Database**: NoSQL document-based storage for flexible data handling
- **REST APIs**: Full CRUD operations for both databases
- **Machine Learning**: XGBoost model for respiratory disease rate predictions
- **Data Analysis**: Jupyter notebooks with exploratory data analysis

## Contributions

- David Birenzi
- Anjeline Noel 
- Kumi Yunis
- Henriette Utatsineza 

##  Project Structure

```
db-timeseries-assignment/
├── data/
│   └── data.csv
├── models/
│   └── xgboost_tuned.pkl
├── MongoDB/
│   ├── app.py
│   ├── predict.py
│   ├── MongoDB_Queries/
│   └── requests_summary.md
├── mysql_api/
│   ├── mysql_crud_api.py
│   ├── requirements.txt
│   ├── .env
│   └── README.md
├── notebooks/
│   ├── task1_climate_health.ipynb
│   └── README.md
├── prediction/
│   ├── mysql_predict.py
│   ├── MySQL_prediction_result.txt
│   ├── MongoDB_predict.py
│   └── MongoDB_prediction_result.txt
├── screenshots/
│   ├── task_2_MongoDB_Screenshots/
│   ├── task_3_MongoDB_Screenshots/
│   ├── task_3_MYSQL_screenshots/
│   ├── task_4_MongoDB_Screenshots/
│   └── task_4_mysql_screenshots/
├── sql/
│   ├── schema.sql
│   ├── load_data.sql
│   ├── queries.sql
│   └── MySQL_ERD.jpeg
├── data.csv
└── README.md
```

##  Quick Start

### Prerequisites

- Python 3.8+
- MySQL Server 8.0+
- MongoDB Atlas account (or local MongoDB)
- Postman (for API testing)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/noel-odero/db-timeseries-assignment
cd db-timeseries-assignment
```

2. **Install Python dependencies**
```bash
cd mysql_api
pip install -r requirements.txt
```

3. **Set up MySQL database**
```bash
mysql -u root -p < sql/schema.sql
mysql -u root -p < sql/load_data.sql
```

4. **Configure environment variables**

Create a `.env` file in `mysql_api/` folder:
```
MYSQL_PASSWORD=your_mysql_password
```

5. **Run the MySQL API**
```bash
cd mysql_api
python mysql_crud_api.py
```

6. **Run the MongoDB API** 
```bash
cd MongoDB
python app.py
```

##  Database Design

### MySQL Schema (Star Schema)

**Fact Tables:**
- `health_measurements` - Health metrics linked to countries and dates
- `climate_measurements` - Climate data linked to countries and dates

**Dimension Tables:**
- `countries` - Country information (name, code, income level)
- `dates` - Date dimension with temporal attributes

### MongoDB Schema

Document-based structure with embedded climate and health data:
```json
{
  "country_name": "USA",
  "date": ISODate("2024-01-01"),
  "temperature_celsius": 15.2,
  "pm25_ugm3": 8.5,
  "respiratory_disease_rate": 45.3
}
```

##  API Endpoints

### MySQL API (Port 5000)

**Test Connection:**
```
GET http://127.0.0.1:5000/api/mysql/test
```

**Create Health Record:**
```
POST http://127.0.0.1:5000/api/mysql/health
Body: {
  "country_code": "USA",
  "date": "2024-01-15",
  "respiratory_rate": 45.2,
  "cardio_mortality": 120.5,
  "gdp_per_capita": 63000
}
```

**Read All Records:**
```
GET http://127.0.0.1:5000/api/mysql/health?country=USA&limit=50
```

**Read Single Record:**
```
GET http://127.0.0.1:5000/api/mysql/health/1
```

**Update Record:**
```
PUT http://127.0.0.1:5000/api/mysql/health/1
Body: {"respiratory_rate": 46.5}
```

**Delete Record:**
```
DELETE http://127.0.0.1:5000/api/mysql/health/1
```

**Latest Record by Country:**
```
GET http://127.0.0.1:5000/api/mysql/latest/USA
```

**Date Range Query:**
```
GET http://127.0.0.1:5000/api/mysql/range?country=IND&start=2024-06-01&end=2024-08-31
```

### MongoDB API (Port 5000)

**Create Record:**
```
POST http://127.0.0.1:5000/api/mongo/create
```

**Latest Record:**
```
GET http://127.0.0.1:5000/api/mongo/latest/Kenya
```

**Date Range:**
```
GET http://127.0.0.1:5000/api/mongo/range/Kenya?start=2024-02-01&end=2025-05-31
```

**Update Record:**
```
PUT http://127.0.0.1:5000/api/mongo/update/<record_id>
```

**Delete Record:**
```
DELETE http://127.0.0.1:5000/api/mongo/delete/<record_id>
```

##  Machine Learning Predictions

### Model Information

- **Algorithm**: XGBoost Regressor (tuned)
- **Target**: Respiratory disease rate per 100,000 population
- **Features**: 38 engineered features including climate variables, lag features, moving averages, and seasonal encodings

### Running Predictions

**MySQL-based prediction:**
```bash
cd prediction
python mysql_predict.py
```

**MongoDB-based prediction:**
```bash
cd prediction
python MongoDB_predict.py
```

The script will:
1. Fetch latest data from the API
2. Load the trained XGBoost model
3. Preprocess features
4. Generate prediction
5. Save results to `prediction_result.txt`

##  Data Analysis

Open the Jupyter notebook for exploratory data analysis:
```bash
cd notebooks
jupyter notebook task1_climate_health.ipynb
```

##  Testing

All API endpoints have been tested using Postman. Screenshots are available in:
- `screenshots/task_2_MongoDB_Screenshots/` - MongoDB shell operations
- `screenshots/task_3_MongoDB_Screenshots/` - MongoDB API CRUD tests
- `screenshots/task_3_MYSQL_screenshots/` - MySQL API CRUD operations
- `screenshots/task_4_MongoDB_Screenshots/` - MongoDB prediction workflow
- `screenshots/task_4_mysql_screenshots/` - MySQL prediction workflow

##  Dependencies

```
flask
mysql-connector-python
flask-cors
requests
pandas
numpy
scikit-learn
joblib
xgboost
pymongo
matplotlib
```

Install all dependencies:
```bash
pip install -r mysql_api/requirements.txt
```

##  Configuration

### MySQL Configuration
Edit connection settings in `mysql_api/mysql_crud_api.py`:
```python
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': 'climate_health_db'
}
```

### MongoDB Configuration
Edit connection string in `MongoDB/app.py`:
```python
MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.xxx.mongodb.net/"
```

##  Key Features

### Database Features
-  Star schema design for efficient querying
-  Proper indexing on foreign keys and date columns
-  Normalized dimension tables
-  Automatic date dimension population

### API Features
-  Full CRUD operations
-  Error handling and validation
-  JSON response format
-  CORS enabled for frontend integration
-  Query parameters for filtering

### ML Features
-  Time-series feature engineering
-  Lag features for temporal dependencies
-  Seasonal encoding
-  Hyperparameter tuning
-  Model persistence with joblib

##  Use Cases

1. **Public Health Monitoring**: Track respiratory disease rates across countries
2. **Climate Impact Analysis**: Correlate climate changes with health outcomes
3. **Predictive Healthcare**: Forecast disease rates for resource planning
4. **Policy Making**: Data-driven insights for environmental health policies

##  Troubleshooting

**API Connection Error:**
- Ensure MySQL/MongoDB server is running
- Check credentials in `.env` file
- Verify port 5000 is not in use

**Model Loading Error:**
- Ensure `xgboost_tuned.pkl` exists in `models/` folder
- Check Python version compatibility
- Reinstall scikit-learn and xgboost

**Database Connection Error:**
- Verify MySQL service is running: `mysql -u root -p`
- Check database exists: `SHOW DATABASES;`
- Ensure user has proper permissions


##  License

This project is for educational purposes as part of a database course assignment.

---

