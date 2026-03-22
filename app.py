import streamlit as st
from database.connection import get_connection
from database.queries import create_tables
from database.queries import get_all_capsules

create_tables(conn)
data = get_all_capsules(conn)

try:
    conn = get_connection()
    print("DB 연결 성공!")
    conn.close()
except Exception as e:
    print(f"연결 실패: {e}")


st.title("coffee log")

