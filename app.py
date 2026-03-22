import streamlit as st
from database.connection import get_connection
from database.queries import create_tables, get_all_capsules

# 페이지 설정 및 DB 초기화
st.set_page_config(page_title="Coffee Dashboard", page_icon="🏠", layout="centered")

conn = get_connection()
create_tables(conn)

# 데이터 프리로드 및 분석
capsules = get_all_capsules(conn)
total_capsules = len(capsules)
total_stock = sum((c['stock_count'] or 0) for c in capsules) if capsules else 0
out_of_stock = [c for c in capsules if c['stock_count'] == 0]
low_stock = [c for c in capsules if 0 < c['stock_count'] < 5]

# 헤더 섹션
st.title("☕ 나의 커피 캡슐 리포트")
st.markdown(f"**{st.session_state.get('user_name', '재묵')}**님의 소중한 홈카페 기록장입니다.")
st.divider()

# 상단 핵심 지표 (Metrics)
col1, col2, col3 = st.columns(3)
col1.metric("보유 캡슐", f"{total_capsules}종")
col2.metric("전체 재고", f"{total_stock}개")
# 품절 품목 수를 delta로 표시 (inverse는 빨간색이 증가를 의미하게 함)
col3.metric("구매 필요", f"{len(out_of_stock) + len(low_stock)}종", 
           delta=len(out_of_stock), delta_color="inverse")

st.divider()

# 스마트 알림 섹션 (품절 및 임박 리스트 합치기)
st.subheader("실시간 재고 알림")
if not out_of_stock and not low_stock:
    st.success("✅ 모든 캡슐의 재고가 넉넉합니다. 카페인이 충분하네요!")
else:
    warn_col1, warn_col2 = st.columns(2)
    with warn_col1:
        if out_of_stock:
            st.error("**🚫 당장 마실 수 없어요 (재고 부족)**")
            for c in out_of_stock:
                st.write(f"- {c['name']} ({c['brand']})")
        else:
            st.info("👍 현재 재고가 없는 캡슐은 없습니다.")

    with warn_col2:
        if low_stock:
            st.warning("**⚠️ 곧 다 떨어져요 (5개 미만)**")
            for c in low_stock:
                st.write(f"- {c['name']}: **{c['stock_count']}개** 남음")
        else:
            st.info("✨ 수량이 부족한 캡슐이 없습니다.")

st.divider()

# 현황 요약
left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("📌 캡슐 창고 요약")
    if capsules:
        st.dataframe(capsules, use_container_width=True, hide_index=True)
    else:
        st.info("등록된 캡슐이 없습니다. 'Inventory'에서 등록해 보세요!")

with right_col:
    st.subheader("💡 추출 가이드")
    with st.container(border=True):
        st.write("**illy Y3.3 추천 세팅**")
        st.write("- 추출 시간: **25~28초**")
        st.caption("가장 풍부한 향을 즐길 수 있는 골든 타임입니다. ☕")

# 하단 바로가기 메뉴
st.write("") 
c1, c2 = st.columns(2)
with c1:
    if st.button("📦 재고 관리하러 가기", use_container_width=True):
        st.switch_page("pages/1_Inventory.py")
with c2:
    if st.button("☕ 커피 기록하러 가기", use_container_width=True):
        st.switch_page("pages/2_Consumption.py")