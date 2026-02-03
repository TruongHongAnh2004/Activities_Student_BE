from neo4j import GraphDatabase
from pymongo import MongoClient
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

def connect_neo4j():
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")

    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver


def query_neo4j(driver, cypher):
    with driver.session() as session:
        result = session.run(cypher)
        return [record.data() for record in result]


def connect_mongo():
    client = MongoClient(os.getenv("MONGO_CONNECTION"))
    db = client[os.getenv("MONGO_DB")]
    collection = db[os.getenv("MONGO_COLLECTION")]
    return collection


def query_mongodb(collection, filter_query):
    return list(collection.find(filter_query))


def connect_postgre():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        database=os.getenv("POSTGRES_DATABASE"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv('POSTGRES_PASSWORD'),
        port=os.getenv("POSTGRES_PORT")
    )
    return conn


def query_postgre(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    return rows