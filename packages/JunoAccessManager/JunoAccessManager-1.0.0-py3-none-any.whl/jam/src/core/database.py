from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import create_database, database_exists
from jam.src.settings import settings

engine_mysql = create_engine(
    settings.SQLALCHEMY_MYSQL_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=100,
    max_overflow=20,
    pool_recycle=60 * 60 * 2,
)
if not database_exists(engine_mysql.url):
    create_database(engine_mysql.url)
    with engine_mysql.connect() as conn:

        conn.execute(text("ALTER DATABASE junoaccess CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"))
SessionLocal_mysql = sessionmaker(autocommit=False, autoflush=False, bind=engine_mysql)
Base_mysql = declarative_base()
