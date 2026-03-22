import streamlit as st
from database.connection import get_connection
from database.queries import create_tables, get_all_capsules

st.set_page_config(page_title="Coffee Dashboard", page_icon="🏠", layout="centered")

# DB 초기화
conn = get_connection()
create_tables(conn)

# 헤더 섹션
st.title("나의 커피 캡슐 리포트")
st.markdown(f"**{st.session_state.get('user_name', '재묵')}**님의 소중한 홈카페 기록장입니다.")
st.divider()

# 데이터 가져오기
capsules = get_all_capsules(conn)
total_capsules = len(capsules)
total_stock = sum(c['stock_count'] for c in capsules) if capsules else 0
low_stock_count = len([c for c in capsules if c['stock_count'] < 5]) if capsules else 0

# --- 핵심 지표 (Metrics) ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("보유 중인 캡슐 종류", f"{total_capsules}종")
with col2:
    st.metric("전체 남은 개수", f"{total_stock}개")
with col3:
    # 재고가 5개 미만인 캡슐이 있으면 경고 표시
    st.metric("품절 임박 (5개 미만)", f"{low_stock_count}종", delta=-low_stock_count, delta_color="inverse")

st.divider()

# --- 대시보드 메인 레이아웃 ---
left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("📌 캡슐 창고 현황 요약")
    if capsules:
        # 간단한 표 형태로 상위 5개만 보여주거나 전체 보여주기
        st.dataframe(capsules, use_container_width=True, hide_index=True)
    else:
        st.info("아직 등록된 캡슐이 없네요. 'Inventory' 페이지에서 첫 캡슐을 등록해 보세요!")

with right_col:
    st.subheader("🔔 알림 및 팁")
    if low_stock_count > 0:
        st.warning("⚠️ 재고가 부족한 캡슐이 있습니다! 주문을 서두르세요.")
    else:
        st.success("✅ 모든 캡슐의 재고가 넉넉합니다.")
    
    with st.expander("💡 오늘의 커피 팁"):
        st.write("""
        일리 Y3.3 머신을 쓰신다면, 
        추출 시간을 **25~28초** 사이로 맞춰보세요! 
        가장 풍부한 향을 즐기실 수 있습니다.
        """)

# 하단 바로가기 버튼
st.divider()
c1, c2 = st.columns(2)
with c1:
    if st.button("📦 재고 관리하러 가기", use_container_width=True):
        st.switch_page("pages/1_Inventory.py")
with c2:
    if st.button("☕ 커피 기록하러 가기", use_container_width=True):
        st.switch_page("pages/2_Consumption.py")