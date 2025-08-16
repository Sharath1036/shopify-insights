import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

TABLES = {}

TABLES['brand_insights'] = (
    """
    CREATE TABLE IF NOT EXISTS brand_insights (
        id INT AUTO_INCREMENT PRIMARY KEY,
        store_url VARCHAR(255) UNIQUE NOT NULL,
        privacy_policy LONGTEXT,
        return_refund_policy LONGTEXT,
        about_brand LONGTEXT,
        extracted_at DATETIME,
        important_links JSON
    ) ENGINE=InnoDB;
    """
)

TABLES['products'] = (
    """
    CREATE TABLE IF NOT EXISTS products (
        id VARCHAR(64) PRIMARY KEY,
        brand_id INT,
        product_id VARCHAR(64),
        title VARCHAR(255),
        description LONGTEXT,
        price VARCHAR(64),
        available VARCHAR(16),
        url VARCHAR(255),
        image_url VARCHAR(255),
        FOREIGN KEY (brand_id) REFERENCES brand_insights(id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """
)

TABLES['hero_products'] = (
    """
    CREATE TABLE IF NOT EXISTS hero_products (
        id VARCHAR(64) PRIMARY KEY,
        brand_id INT,
        product_id VARCHAR(64),
        title VARCHAR(255),
        description LONGTEXT,
        price VARCHAR(64),
        available VARCHAR(16),
        url VARCHAR(255),
        image_url VARCHAR(255),
        FOREIGN KEY (brand_id) REFERENCES brand_insights(id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """
)

TABLES['faqs'] = (
    """
    CREATE TABLE IF NOT EXISTS faqs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        brand_id INT,
        question LONGTEXT,
        answer LONGTEXT,
        FOREIGN KEY (brand_id) REFERENCES brand_insights(id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """
)

TABLES['social_handles'] = (
    """
    CREATE TABLE IF NOT EXISTS social_handles (
        id INT AUTO_INCREMENT PRIMARY KEY,
        brand_id INT,
        platform VARCHAR(64),
        url VARCHAR(255),
        handle VARCHAR(128),
        FOREIGN KEY (brand_id) REFERENCES brand_insights(id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """
)

TABLES['contact_info'] = (
    """
    CREATE TABLE IF NOT EXISTS contact_info (
        id INT AUTO_INCREMENT PRIMARY KEY,
        brand_id INT,
        emails JSON,
        phone_numbers JSON,
        addresses JSON,
        FOREIGN KEY (brand_id) REFERENCES brand_insights(id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """
)

def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8mb4'")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

def main():
    cnx = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = cnx.cursor()
    create_database(cursor)
    cnx.database = DB_NAME
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print(f"Creating table {table_name}...")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            print(f"Failed creating table {table_name}: {err}")
    cursor.close()
    cnx.close()
    print("All tables created!")

if __name__ == "__main__":
    main()
