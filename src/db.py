"""
Database connections
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

import mysql.connector
import redis
import config
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

# optimization: on utilise un pool de connections
# https://redis.io/docs/latest/develop/clients/pools-and-muxing/
pool = redis.ConnectionPool(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB, decode_responses=True)

engine = create_engine(
    URL.create(
        "mysql+mysqlconnector",
        username=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT,
        database=config.DB_NAME,
    ),
    connect_args={"auth_plugin": "caching_sha2_password"},
    pool_pre_ping=True,
)
Session = sessionmaker(bind=engine)

def get_mysql_conn():
    """Get a MySQL connection using env variables"""
    return mysql.connector.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        auth_plugin='caching_sha2_password'
    )

def get_redis_conn():
    """Get a Redis connection using env variables"""
    return redis.Redis(connection_pool=pool, decode_responses=True)

def get_sqlalchemy_session():
    """Get an SQLAlchemy ORM session using env variables"""
    return Session()
