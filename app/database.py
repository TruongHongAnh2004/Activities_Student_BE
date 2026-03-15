from neo4j import AsyncGraphDatabase
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


# In production, use environment variables!
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:honganh123@localhost:5432/student_management"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession)

Base = declarative_base()

        
async def get_postgres_db():
    async with AsyncSessionLocal() as session:
        yield session


NEO4J_URI = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "14042004")

neo4j_driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=("neo4j", "14042004"))

async def close_neo4j():
    await neo4j_driver.close()
    
async def get_neo4j_session():
    async with neo4j_driver.session() as session:
        yield session