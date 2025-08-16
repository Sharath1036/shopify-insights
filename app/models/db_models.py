from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.types import JSON
import datetime
from dotenv import load_dotenv
import os

load_dotenv(override=True)
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

Base = declarative_base()
Base.metadata.create_all(engine)

class BrandInsightsDB(Base):
    __tablename__ = "brand_insights"
    id = Column(Integer, primary_key=True, autoincrement=True)
    store_url = Column(String(255), unique=True, nullable=False)
    privacy_policy = Column(LONGTEXT)
    return_refund_policy = Column(LONGTEXT)
    about_brand = Column(LONGTEXT)
    extracted_at = Column(DateTime, default=datetime.datetime.utcnow)
    important_links = Column(JSON)

    # Relationships
    products = relationship("ProductDB", back_populates="brand", cascade="all, delete-orphan")
    hero_products = relationship("HeroProductDB", back_populates="brand", cascade="all, delete-orphan")
    faqs = relationship("FAQDB", back_populates="brand", cascade="all, delete-orphan")
    social_handles = relationship("SocialHandleDB", back_populates="brand", cascade="all, delete-orphan")
    contact_info = relationship("ContactInfoDB", uselist=False, back_populates="brand", cascade="all, delete-orphan")

class ProductDB(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey("brand_insights.id"))
    product_id = Column(String(64))
    title = Column(String(255))
    description = Column(LONGTEXT)
    price = Column(String(64))
    available = Column(String(16))
    url = Column(String(255))
    image_url = Column(String(255))
    brand = relationship("BrandInsightsDB", back_populates="products")

class HeroProductDB(Base):
    __tablename__ = "hero_products"
    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey("brand_insights.id"))
    product_id = Column(String(64))
    title = Column(String(255))
    description = Column(LONGTEXT)
    price = Column(String(64))
    available = Column(String(16))
    url = Column(String(255))
    image_url = Column(String(255))
    brand = relationship("BrandInsightsDB", back_populates="hero_products")

class FAQDB(Base):
    __tablename__ = "faqs"
    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey("brand_insights.id"))
    question = Column(LONGTEXT)
    answer = Column(LONGTEXT)
    brand = relationship("BrandInsightsDB", back_populates="faqs")

class SocialHandleDB(Base):
    __tablename__ = "social_handles"
    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey("brand_insights.id"))
    platform = Column(String(64))
    url = Column(String(255))
    handle = Column(String(128))
    brand = relationship("BrandInsightsDB", back_populates="social_handles")

class ContactInfoDB(Base):
    __tablename__ = "contact_info"
    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey("brand_insights.id"))
    emails = Column(JSON)
    phone_numbers = Column(JSON)
    addresses = Column(JSON)
    brand = relationship("BrandInsightsDB", back_populates="contact_info")