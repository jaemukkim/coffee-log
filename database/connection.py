import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# secrets.toml에서 정보 가져오기
db_info = st.secrets["mysql"]

DB_URL = f"mysql+pymysql://{db_info['user']}:{db_info['password']}@{db_info['host']}:{db_info['port']}/{db_info['database']}"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()