import streamlit as st
from database.connection import get_connection
from database.queries import add_capsule, get_all_capsules

st.set_page_config(page_title="재고 관리", page_icon="📦")
st.title("📦 캡슐 재고 관리")

conn = get_connection()

# 신규 등록
with st.expander("🆕 새로운 캡슐 등록하기", expanded=True):
    with st.form("capsule_form"):
        name = st.text_input("캡슐 이름 (예: 클래시코, 에티오피아)")
        brand = st.selectbox("브랜드", ["illy", "Nespresso", "Starbucks", "기타"])
        
        col1, col2 = st.columns(2)
        with col1:
            intensity = st.slider("강도 (Intensity)", 1, 10, 5)
        with col2:
            acidity = st.slider("산미 (Acidity)", 1, 5, 3)
            
        stock = st.number_input("현재 재고 수량", min_value=0, value=21)
        
        submitted = st.form_submit_button("창고에 넣기")
        
        if submitted:
            if name:
                if add_capsule(conn, name, brand, intensity, acidity, stock):
                    st.success(f"'{name}' 캡슐이 등록되었습니다!")
            else:
                st.warning("캡슐 이름을 입력해 주세요.")

# 현재 재고 목록 확인
st.divider()
st.subheader("📊 현재 전체 재고")
capsules = get_all_capsules(conn)
if capsules:
    st.dataframe(capsules, use_container_width=True)