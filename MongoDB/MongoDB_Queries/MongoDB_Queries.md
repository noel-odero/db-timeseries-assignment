use climate_health_db
switched to db climate_health_db
db.climate_data.find(
  { "country_name": "Kenya" }
).limit(5)

{
  _id: ObjectId('69a89d6063b80aee2ef065a8'),
  record_id: 5641,
  country_code: 'KEN',
  country_name: 'Kenya',
  region: 'Africa',
  income_level: 'Lower-Middle',
  date: 2015-01-04T00:00:00.000Z,
  year: 2015,
  month: 1,
  week: 1,
  latitude: -0.02,
  longitude: 37.9,
  population_millions: 54,
  temperature_celsius: 25.47,
  temp_anomaly_celsius: 0.28,
  precipitation_mm: 117.8,
  heat_wave_days: 0,
  drought_indicator: 0,
  flood_indicator: 0,
  extreme_weather_events: 0,
  pm25_ugm3: 136.8,
  air_quality_index: 207,
  respiratory_disease_rate: 99.4,
  cardio_mortality_rate: 26,
  vector_disease_risk_score: 43.6,
  waterborne_disease_incidents: 22.7,
  heat_related_admissions: 6.1,
  healthcare_access_index: 50.2,
  gdp_per_capita_usd: 2124,
  mental_health_index: 78.6,
  food_security_index: 100
}
{
  _id: ObjectId('69a89d6063b80aee2ef065a9'),
  record_id: 5642,
  country_code: 'KEN',
  country_name: 'Kenya',
  region: 'Africa',
  income_level: 'Lower-Middle',
  date: 2015-01-11T00:00:00.000Z,
  year: 2015,
  month: 1,
  week: 2,
  latitude: -0.02,
  longitude: 37.9,
  population_millions: 54,
  temperature_celsius: 28.74,
  temp_anomaly_celsius: -0.86,
  precipitation_mm: 33.9,
  heat_wave_days: 0,
  drought_indicator: 0,
  flood_indicator: 0,
  extreme_weather_events: 0,
  pm25_ugm3: 91.5,
  air_quality_index: 118,
  respiratory_disease_rate: 82.6,
  cardio_mortality_rate: 34.4,
  vector_disease_risk_score: 49.7,
  waterborne_disease_incidents: 22.2,
  heat_related_admissions: 9,
  healthcare_access_index: 47.1,
  gdp_per_capita_usd: 2124,
  mental_health_index: 66.4,
  food_security_index: 86.6
}
{
  _id: ObjectId('69a89d6063b80aee2ef065aa'),
  record_id: 5643,
  country_code: 'KEN',
  country_name: 'Kenya',
  region: 'Africa',
  income_level: 'Lower-Middle',
  date: 2015-01-18T00:00:00.000Z,
  year: 2015,
  month: 1,
  week: 3,
  latitude: -0.02,
  longitude: 37.9,
  population_millions: 54,
  temperature_celsius: 28.21,
  temp_anomaly_celsius: -0.83,
  precipitation_mm: 31.3,
  heat_wave_days: 0,
  drought_indicator: 0,
  flood_indicator: 0,
  extreme_weather_events: 0,
  pm25_ugm3: 92.3,
  air_quality_index: 146,
  respiratory_disease_rate: 65,
  cardio_mortality_rate: 35,
  vector_disease_risk_score: 56.3,
  waterborne_disease_incidents: 28.8,
  heat_related_admissions: 10.7,
  healthcare_access_index: 51.4,
  gdp_per_capita_usd: 2124,
  mental_health_index: 72.1,
  food_security_index: 91.8
}
{
  _id: ObjectId('69a89d6063b80aee2ef065ab'),
  record_id: 5644,
  country_code: 'KEN',
  country_name: 'Kenya',
  region: 'Africa',
  income_level: 'Lower-Middle',
  date: 2015-01-25T00:00:00.000Z,
  year: 2015,
  month: 1,
  week: 4,
  latitude: -0.02,
  longitude: 37.9,
  population_millions: 54,
  temperature_celsius: 30.33,
  temp_anomaly_celsius: 0.15,
  precipitation_mm: 154.4,
  heat_wave_days: 0,
  drought_indicator: 0,
  flood_indicator: 0,
  extreme_weather_events: 0,
  pm25_ugm3: 52,
  air_quality_index: 67,
  respiratory_disease_rate: 77.6,
  cardio_mortality_rate: 30.6,
  vector_disease_risk_score: 71.2,
  waterborne_disease_incidents: 25.9,
  heat_related_admissions: 4.7,
  healthcare_access_index: 46.4,
  gdp_per_capita_usd: 2124,
  mental_health_index: 68.6,
  food_security_index: 85.1
}
{
  _id: ObjectId('69a89d6063b80aee2ef065ac'),
  record_id: 5645,
  country_code: 'KEN',
  country_name: 'Kenya',
  region: 'Africa',
  income_level: 'Lower-Middle',
  date: 2015-02-01T00:00:00.000Z,
  year: 2015,
  month: 2,
  week: 5,
  latitude: -0.02,
  longitude: 37.9,
  population_millions: 54,
  temperature_celsius: 27.4,
  temp_anomaly_celsius: 0.24,
  precipitation_mm: 125.3,
  heat_wave_days: 0,
  drought_indicator: 0,
  flood_indicator: 0,
  extreme_weather_events: 0,
  pm25_ugm3: 95.8,
  air_quality_index: 114,
  respiratory_disease_rate: 65.2,
  cardio_mortality_rate: 34.5,
  vector_disease_risk_score: 47.2,
  waterborne_disease_incidents: 21.7,
  heat_related_admissions: 5.2,
  healthcare_access_index: 44.9,
  gdp_per_capita_usd: 2127,
  mental_health_index: 66.1,
  food_security_index: 78.7
}
db.climate_data.aggregate([
  { 
    $group: { 
      _id: "$country_name",
      total_records: { $sum: 1 },
      avg_respiratory_rate: { $avg: "$respiratory_disease_rate" },
      latest_record_date: { $max: "$date" }
    }
  },
  { $sort: { _id: 1 } }  // Sort alphabetically by country name
])
{
  _id: 'Argentina',
  total_records: 564,
  avg_respiratory_rate: 64.48191489361703,
  latest_record_date: 2025-10-19T00:00:00.000Z
}
{
  _id: 'Australia',
  total_records: 564,
  avg_respiratory_rate: 62.88475177304964,
  latest_record_date: 2025-10-19T00:00:00.000Z
}
{
  _id: 'Bangladesh',
  total_records: 564,
  avg_respiratory_rate: 81.91117021276597,
  latest_record_date: 2025-10-19T00:00:00.000Z
}
{
  _id: 'Brazil',
  total_records: 564,
  avg_respiratory_rate: 62.78847517730496,
  latest_record_date: 2025-10-19T00:00:00.000Z
}
{
  _id: 'Canada',
  total_records: 564,
  avg_respiratory_rate: 63.43847517730497,
  latest_record_date: 2025-10-19T00:00:00.000Z
}
{
  _id: 'China',
  total_records: 564,
  avg_respiratory_rate: 63.609219858156024,
  latest_record_date: 2025-10-19T00:00:00.000Z
}
{
  _id: 'Colombia',
  total_records: 564,
  avg_respiratory_rate: 62.90939716312057,
  latest_record_date: 2025-10-19T00:00:00.000Z
}
{
  _id: 'Egypt',
  total_records: 564,
  avg_respiratory_rate: 81.28031914893617,
  latest_record_date: 2025-10-19T00:00:00.000Z
}
{
  _id: 'France',
  total_records: 564,
  avg_respiratory_rate: 64.21950354609929,
  latest_record_date: 2025-10-19T00:00:00.000Z
}
{
  _id: 'Germany',
  total_records: 564,
  avg_respiratory_rate: 63.637943262411355,
  latest_record_date: 2025-10-19T00:00:00.000Z
}
{
  _id: 'India',
  total_records: 564,
  avg_respiratory_rate: 81.17819148936171,
  latest_record_date: 2025-10-19T00:00:00.000Z
}
{
  _id: 'Indonesia',
  total_records: 564,
  avg_respiratory_rate: 81.96081560283689,
  latest_record_date: 2025-10-19T00:00:00.000Z
}
{
  _id: 'Italy',
  total_records: 564,
  avg_respiratory_rate: 63.42482269503546,
  latest_record_date: 2025-10-19T00:00:00.000Z
}
{
  _id: 'Japan',
  total_records: 564,
  avg_respiratory_rate: 63.87570921985816,
  latest_record_date: 2025-10-19T00:00:00.000Z
}
{
  _id: 'Kenya',
  total_records: 564,
  avg_respiratory_rate: 81.61117021276596,
  latest_record_date: 2025-10-19T00:00:00.000Z
}
{
  _id: 'Mexico',
  total_records: 564,
  avg_respiratory_rate: 64.64645390070922,
  latest_record_date: 2025-10-19T00:00:00.000Z
}
{
  _id: 'Nigeria',
  total_records: 564,
  avg_respiratory_rate: 81.54645390070921,
  latest_record_date: 2025-10-19T00:00:00.000Z
}
{
  _id: 'Pakistan',
  total_records: 564,
  avg_respiratory_rate: 81.05035460992909,
  latest_record_date: 2025-10-19T00:00:00.000Z
}
{
  _id: 'Philippines',
  total_records: 564,
  avg_respiratory_rate: 81.50017730496454,
  latest_record_date: 2025-10-19T00:00:00.000Z
}
{
  _id: 'South Africa',
  total_records: 564,
  avg_respiratory_rate: 63.33102836879432,
  latest_record_date: 2025-10-19T00:00:00.000Z
}
Type "it" for more
db.climate_data.find(
  { "country_name": "Kenya" }
).sort({ "date": -1 }).limit(1)

{

  _id: ObjectId('69a89d6263b80aee2ef067db'),
  record_id: 6204,
  country_code: 'KEN',
  country_name: 'Kenya',
  region: 'Africa',
  income_level: 'Lower-Middle',
  date: 2025-10-19T00:00:00.000Z,
  year: 2025,
  month: 10,
  week: 42,
  latitude: -0.02,
  longitude: 37.9,
  population_millions: 54,
  temperature_celsius: 15.82,
  temp_anomaly_celsius: 0.69,
  precipitation_mm: 47.5,
  heat_wave_days: 0,
  drought_indicator: 0,
  flood_indicator: 0,
  extreme_weather_events: 0,
  pm25_ugm3: 94.1,
  air_quality_index: 124,
  respiratory_disease_rate: 44.9,
  cardio_mortality_rate: 30.3,
  vector_disease_risk_score: 5.2,
  waterborne_disease_incidents: 26.8,
  heat_related_admissions: 0,
  healthcare_access_index: 54.4,
  gdp_per_capita_usd: 2579,
  mental_health_index: 66.6,
  food_security_index: 96.1
}
db.climate_data.aggregate([
  { $match: { "country_name": "Kenya" } },
  { $group: {
      _id: "$year",
      avg_respiratory_rate: { $avg: "$respiratory_disease_rate" }
  }},
  { $sort: { _id: 1 } }
])
{
  _id: 2015,
  avg_respiratory_rate: 80.54038461538462
}
{
  _id: 2015,
  avg_respiratory_rate: 80.54038461538462
}
{
  _id: 2016,
  avg_respiratory_rate: 78.63653846153846
}
{
  _id: 2017,
  avg_respiratory_rate: 84.61698113207547
}
{
  _id: 2018,
  avg_respiratory_rate: 82.18653846153846
}
{
  _id: 2019,
  avg_respiratory_rate: 80.0923076923077
}
{
  _id: 2020,
  avg_respiratory_rate: 82.89038461538462
}
{
  _id: 2021,
  avg_respiratory_rate: 80.30576923076923
}
{
  _id: 2022,
  avg_respiratory_rate: 80.62692307692308
}
{
  _id: 2023,
  avg_respiratory_rate: 81.65849056603773
}
{
  _id: 2024,
  avg_respiratory_rate: 83.56923076923077
}
{
  _id: 2025,
  avg_respiratory_rate: 82.76190476190476
}
db.climate_data.aggregate([
  { $match: { "country_name": "Kenya" } },
  { $project: {
      date: 1,
      respiratory_disease_rate: 1,
      pm25_ugm3: 1
  }},
  { $sort: { date: 1 } }
])
{
  _id: ObjectId('69a89d6063b80aee2ef065a8'),
  date: 2015-01-04T00:00:00.000Z,
  pm25_ugm3: 136.8,
  respiratory_disease_rate: 99.4
}
{
  _id: ObjectId('69a89d6063b80aee2ef065a9'),
  date: 2015-01-11T00:00:00.000Z,
  pm25_ugm3: 91.5,
  respiratory_disease_rate: 82.6
}
{
  _id: ObjectId('69a89d6063b80aee2ef065aa'),
  date: 2015-01-18T00:00:00.000Z,
  pm25_ugm3: 92.3,
  respiratory_disease_rate: 65
}
{
  _id: ObjectId('69a89d6063b80aee2ef065ab'),
  date: 2015-01-25T00:00:00.000Z,
  pm25_ugm3: 52,
  respiratory_disease_rate: 77.6
}
{
  _id: ObjectId('69a89d6063b80aee2ef065ac'),
  date: 2015-02-01T00:00:00.000Z,
  pm25_ugm3: 95.8,
  respiratory_disease_rate: 65.2
}
{
  _id: ObjectId('69a89d6063b80aee2ef065ad'),
  date: 2015-02-08T00:00:00.000Z,
  pm25_ugm3: 97,
  respiratory_disease_rate: 90.7
}
{
  _id: ObjectId('69a89d6063b80aee2ef065ae'),
  date: 2015-02-15T00:00:00.000Z,
  pm25_ugm3: 67.9,
  respiratory_disease_rate: 76.1
}
{
  _id: ObjectId('69a89d6063b80aee2ef065af'),
  date: 2015-02-22T00:00:00.000Z,
  pm25_ugm3: 90,
  respiratory_disease_rate: 79.6
}
{
  _id: ObjectId('69a89d6063b80aee2ef065b0'),
  date: 2015-03-01T00:00:00.000Z,
  pm25_ugm3: 67.8,
  respiratory_disease_rate: 79.6
}
{
  _id: ObjectId('69a89d6063b80aee2ef065b1'),
  date: 2015-03-08T00:00:00.000Z,
  pm25_ugm3: 84.5,
  respiratory_disease_rate: 85.7
}
{
  _id: ObjectId('69a89d6063b80aee2ef065b2'),
  date: 2015-03-15T00:00:00.000Z,
  pm25_ugm3: 85.1,
  respiratory_disease_rate: 84.2
}
{
  _id: ObjectId('69a89d6063b80aee2ef065b3'),
  date: 2015-03-22T00:00:00.000Z,
  pm25_ugm3: 103.3,
  respiratory_disease_rate: 91.6
}
{
  _id: ObjectId('69a89d6063b80aee2ef065b4'),
  date: 2015-03-29T00:00:00.000Z,
  pm25_ugm3: 72.1,
  respiratory_disease_rate: 74.6
}
{
  _id: ObjectId('69a89d6063b80aee2ef065b5'),
  date: 2015-04-05T00:00:00.000Z,
  pm25_ugm3: 88.5,
  respiratory_disease_rate: 81.6
}
{
  _id: ObjectId('69a89d6063b80aee2ef065b6'),
  date: 2015-04-12T00:00:00.000Z,
  pm25_ugm3: 61.9,
  respiratory_disease_rate: 52.7
}
{
  _id: ObjectId('69a89d6063b80aee2ef065b7'),
  date: 2015-04-19T00:00:00.000Z,
  pm25_ugm3: 77.7,
  respiratory_disease_rate: 40.6
}
{
  _id: ObjectId('69a89d6063b80aee2ef065b8'),
  date: 2015-04-26T00:00:00.000Z,
  pm25_ugm3: 101.4,
  respiratory_disease_rate: 93.3
}
{
  _id: ObjectId('69a89d6063b80aee2ef065b9'),
  date: 2015-05-03T00:00:00.000Z,
  pm25_ugm3: 79.7,
  respiratory_disease_rate: 60.8
}
{
  _id: ObjectId('69a89d6063b80aee2ef065ba'),
  date: 2015-05-10T00:00:00.000Z,
  pm25_ugm3: 77,
  respiratory_disease_rate: 82.5
}
{
  _id: ObjectId('69a89d6063b80aee2ef065bb'),
  date: 2015-05-17T00:00:00.000Z,
  pm25_ugm3: 72,
  respiratory_disease_rate: 80.2
}
Type "it" for more
db.climate_data.find(
  {
    country_name: "Kenya",
    date: { $gte: ISODate("2024-02-01"), $lte: ISODate("2025-05-31") }
  },
  {
    _id: 0,                     // hide MongoDB default _id
    country_name: 1,             // include country
    date: 1,                     // include date
    respiratory_disease_rate: 1  // include respiratory disease rate
  }
).sort({ date: 1 })             // sort by date ascending
{
  country_name: 'Kenya',
  date: 2024-02-04T00:00:00.000Z,
  respiratory_disease_rate: 64.9
}
{
  country_name: 'Kenya',
  date: 2024-02-11T00:00:00.000Z,
  respiratory_disease_rate: 76.8
}
{
  country_name: 'Kenya',
  date: 2024-02-18T00:00:00.000Z,
  respiratory_disease_rate: 95.2
}
{
  country_name: 'Kenya',
  date: 2024-02-25T00:00:00.000Z,
  respiratory_disease_rate: 90.8
}
{
  country_name: 'Kenya',
  date: 2024-03-03T00:00:00.000Z,
  respiratory_disease_rate: 71.2
}
{
  country_name: 'Kenya',
  date: 2024-03-10T00:00:00.000Z,
  respiratory_disease_rate: 93.8
}
{
  country_name: 'Kenya',
  date: 2024-03-17T00:00:00.000Z,
  respiratory_disease_rate: 88.6
}
{
  country_name: 'Kenya',
  date: 2024-03-24T00:00:00.000Z,
  respiratory_disease_rate: 68.6
}
{
  country_name: 'Kenya',
  date: 2024-03-31T00:00:00.000Z,
  respiratory_disease_rate: 94
}
{
  country_name: 'Kenya',
  date: 2024-04-07T00:00:00.000Z,
  respiratory_disease_rate: 89.2
}
{
  country_name: 'Kenya',
  date: 2024-04-14T00:00:00.000Z,
  respiratory_disease_rate: 85.5
}
{
  country_name: 'Kenya',
  date: 2024-04-21T00:00:00.000Z,
  respiratory_disease_rate: 75.4
}
{
  country_name: 'Kenya',
  date: 2024-04-28T00:00:00.000Z,
  respiratory_disease_rate: 84
}
{
  country_name: 'Kenya',
  date: 2024-05-05T00:00:00.000Z,
  respiratory_disease_rate: 79.6
}
{
  country_name: 'Kenya',
  date: 2024-05-12T00:00:00.000Z,
  respiratory_disease_rate: 68.1
}
{
  country_name: 'Kenya',
  date: 2024-05-19T00:00:00.000Z,
  respiratory_disease_rate: 107.5
}
{
  country_name: 'Kenya',
  date: 2024-05-26T00:00:00.000Z,
  respiratory_disease_rate: 80.3
}
{
  country_name: 'Kenya',
  date: 2024-06-02T00:00:00.000Z,
  respiratory_disease_rate: 90.6
}
{
  country_name: 'Kenya',
  date: 2024-06-09T00:00:00.000Z,
  respiratory_disease_rate: 57.8
}
{
  country_name: 'Kenya',
  date: 2024-06-16T00:00:00.000Z,
  respiratory_disease_rate: 81.5
}