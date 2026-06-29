import time
import psycopg
from app.config.settings import settings

# Strip the SQLAlchemy dialect prefix if present
db_url = settings.database_url
if db_url.startswith("postgresql+psycopg://"):
    db_url = db_url.replace("postgresql+psycopg://", "postgresql://", 1)

print("Waiting for database to be ready...")
for i in range(60):
    try:
        conn = psycopg.connect(db_url)
        conn.close()
        print("Database is ready! Continuing.")
        break
    except psycopg.OperationalError:
        time.sleep(1)
else:
    print("Database connection timed out. Exiting.")
    exit(1)
