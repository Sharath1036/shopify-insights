import os
import mysql.connector
import json
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def insert_brand_insights(data: dict):
    cnx = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = cnx.cursor()
    # Insert into brand_insights
    add_brand = ("""
        INSERT INTO brand_insights
        (store_url, privacy_policy, return_refund_policy, about_brand, extracted_at, important_links)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            privacy_policy=VALUES(privacy_policy),
            return_refund_policy=VALUES(return_refund_policy),
            about_brand=VALUES(about_brand),
            extracted_at=VALUES(extracted_at),
            important_links=VALUES(important_links)
    """)
    extracted_at = data.get("extracted_at")
    if not extracted_at:
        extracted_at = None
    brand_values = (
        data.get("store_url"),
        data.get("privacy_policy"),
        data.get("return_refund_policy"),
        data.get("about_brand"),
        extracted_at,
        json.dumps(data.get("important_links", {}))
    )
    cursor.execute(add_brand, brand_values)
    cnx.commit()
    # Get brand_id
    cursor.execute("SELECT id FROM brand_insights WHERE store_url=%s", (data.get("store_url"),))
    brand_id = cursor.fetchone()[0]
    # Helper to clear and insert child tables
    def clear_and_insert(table, items, columns):
        cursor.execute(f"DELETE FROM {table} WHERE brand_id=%s", (brand_id,))
        if not items:
            return
        for item in items:
            vals = tuple(item.get(col) for col in columns)
            cursor.execute(
                f"INSERT INTO {table} (brand_id, {', '.join(columns)}) VALUES (%s, {', '.join(['%s']*len(columns))})",
                (brand_id, *vals)
            )
    # Products (cast id to str to avoid int overflow)
    import re
    def strip_html(text):
        if not text:
            return text
        return re.sub(r'<[^>]+>', '', text)
    def cast_id_str_and_strip_desc(items):
        for item in items or []:
            if "id" in item:
                item["id"] = str(item["id"])
            if "description" in item:
                item["description"] = strip_html(item["description"])
        return items
    clear_and_insert("products", cast_id_str_and_strip_desc(data.get("product_catalog", [])), ["id", "title", "description", "price", "available", "url", "image_url"])
    # Hero Products
    clear_and_insert("hero_products", cast_id_str_and_strip_desc(data.get("hero_products", [])), ["id", "title", "description", "price", "available", "url", "image_url"])
    # FAQs
    clear_and_insert("faqs", data.get("faqs", []), ["question", "answer"])
    # Social Handles
    clear_and_insert("social_handles", data.get("social_handles", []), ["platform", "url", "handle"])
    # Contact Info (single row)
    cursor.execute("DELETE FROM contact_info WHERE brand_id=%s", (brand_id,))
    contact = data.get("contact_info", {})
    if contact:
        cursor.execute(
            "INSERT INTO contact_info (brand_id, emails, phone_numbers, addresses) VALUES (%s, %s, %s, %s)",
            (brand_id, json.dumps(contact.get("emails", [])), json.dumps(contact.get("phone_numbers", [])), json.dumps(contact.get("addresses", [])))
        )
    cnx.commit()
    cursor.close()
    cnx.close()
    print("Brand insights and all related data inserted!")
