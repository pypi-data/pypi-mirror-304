from jam.src.core.database import SessionLocal_mysql


def get_mysql_db():
    db = SessionLocal_mysql()
    try:
        yield db
    finally:
        db.close()
