# Shopify Insights

## Setup
OS: `Windows 11`<br>
Python: `3.11.0`

Clone the repository
```
https://github.com/Sharath1036/shopify-insights
```

Create a `.env` file and add the following secrets. The database used here is MySQL
```
GROQ_API_KEY
DATABASE_URL= "mysql://username:password@hostname:port/database_name"
DB_HOST
DB_USER
DB_PASSWORD
DB_NAME
```

Activate virtual environment
```
python -m venv myenv
```
```
myenv\Scripts\activate
```

Install dependencies
```
pip install -r requirements.txt
```

Create database schema
```
python app/create_tables_mysql_connector.py
```

Run the FastAPI server
```
cd app
```
```
uvicorn main:app --reload
```

In the `/api/v1/insights` click on Try it Out and add any website URL and click on Execute.