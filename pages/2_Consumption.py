import streamlit as st
from database.connection import get_connection
from database.queries import get_all_capsules, consume_capsule

st.set_page_config(page_title="커피 기록", page_icon="☕")
st.title("☕ 오늘 어떤 커피를 마실까요?")

conn = get_connection()
capsules = get_all_capsules(conn)

if capsules:
    for cap in capsules:
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 2, 2])
            
            with col1:
                st.write(f"### {cap['name']}")
                st.caption(f"{cap['brand']} | 강도: {cap['intensity']} | 산미: {cap['acidity']}")
                
            with col2:
                st.metric("남은 재고", f"{cap['stock_count']}개")
                
            with col3:
                st.write("")
                if st.button(f"마시기 ☕", key=f"consume_{cap['id']}"):
                    if cap['stock_count'] > 0:
                        if consume_capsule(conn, cap['id'], "아메리카노"):
                            st.toast(f"'{cap['name']}' 기록 완료!")
                            st.rerun()
                    else:
                        st.error("재고 부족!")
else:
    st.info("등록된 캡슐이 없습니다. '재고 관리' 페이지에서 먼저 등록해 주세요.")