The MongoDB API was implemented using Flask and PyMongo to expose REST endpoints that interact with the MongoDB Atlas cloud database containing the climate-health time series dataset. The application first establishes a connection to the climate_health_db database and the climate_data collection, allowing the API to perform database operations through HTTP requests. The endpoints support CRUD operations as well as the required time-series queries defined in the assignment. These endpoints were tested using Postman to ensure that records can be created, retrieved, updated, deleted, and queried based on time conditions.

GET / – Confirms that the API server is running and accessible.

POST /api/mongo/create – Inserts a new document into the MongoDB collection by receiving JSON data and converting the date field into a proper datetime format.

GET /api/mongo/latest/<country_name> – Retrieves the most recent record for a specified country by sorting the dataset by date in descending order.

GET /api/mongo/range/<country_name>?start=YYYY-MM-DD&end=YYYY-MM-DD – Returns all records for a country within a specified date range, enabling time-series analysis queries.

PUT /api/mongo/update/<record_id> – Updates an existing record in the database using its MongoDB ObjectId and the $set update operator.

DELETE /api/mongo/delete/<record_id> – Removes a specific document from the database using its unique ObjectId.