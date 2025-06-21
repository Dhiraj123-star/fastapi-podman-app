import os
import time
import redis
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# Load environment variables
load_dotenv()

# PostgreSQL Config
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Retry logic for connecting to PostgreSQL
MAX_RETRIES = 10
RETRY_DELAY = 2  # seconds

for attempt in range(1, MAX_RETRIES + 1):
    try:
        engine = create_engine(DATABASE_URL)
        # Attempt a test connection
        with engine.connect() as conn:
            print("✅ Successfully connected to the database.")
        break
    except OperationalError as e:
        print(f"⏳ Attempt {attempt}/{MAX_RETRIES} - Database not ready yet: {e}")
        time.sleep(RETRY_DELAY)
else:
    raise Exception("❌ Failed to connect to the database after several retries.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis Config
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# ✅ Add get_db() function for use in Depends()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
