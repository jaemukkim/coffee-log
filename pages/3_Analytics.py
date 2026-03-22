import streamlit as st
import pandas as pd
import plotly.express as px
from database.connection import get_connection
from database.queries import get_all_capsules
from database.queries import get_consumption_by_date


# 더미 데이터 생성
import numpy as np 
from datetime import datetime, timedelta

st.set_page_config(page_title="소비 분석", page_icon="📈", layout="centered")
st.title("📈 커피 소비 리포트")

conn = get_connection()
capsules = get_all_capsules(conn)

if capsules:
    df = pd.DataFrame(capsules)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("가장 많이 남은 캡슐", df.loc[df['stock_count'].idxmax(), 'name'])
    with col2:
        st.metric("가장 부족한 캡슐", df.loc[df['stock_count'].idxmin(), 'name'])

    st.divider()

# 재고 현황 그래프 (Plotly 사용)
st.subheader("📊 캡슐별 잔여 재고")

if not df.empty:
    # Plotly로 막대 그래프 생성
    fig = px.bar(
        df, 
        x="name", 
        y="stock_count",
        labels={"name": "캡슐 이름", "stock_count": "잔여 재고"},
        color_discrete_sequence=["#704214"] 
    )

    # 디자인 세부 조절
    fig.update_traces(
        width=0.4, # 0.1~1.0 사이로 막대 두께 조절 (숫자가 작을수록 얇아짐)
        marker_line_color='rgb(8,48,107)', # 테두리 색상 (선택사항)
        marker_line_width=1.5,
        opacity=0.8
    )

    fig.update_layout(
        xaxis_title="캡슐 종류",
        yaxis_title="남은 개수 (개)",
        plot_bgcolor="rgba(0,0,0,0)", 
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    

    # 강도/산미 분포 (산점도)
    st.subheader("내 취향 분석 (강도 vs 산미)")
    st.scatter_chart(data=df, x="intensity", y="acidity", size="stock_count", color="name")
    st.caption("※ 점이 클수록 재고가 많이 남아있는 캡슐입니다.")

else:
    st.info("데이터가 충분하지 않습니다. 먼저 캡슐을 등록해 주세요!")



st.divider()
st.subheader("📅 3월 커피 소비 추이")

# 1. 날짜별 소비 데이터 가져오기
daily_data = get_consumption_by_date(conn)

if daily_data:
    # 2. 데이터프레임 변환 및 전처리
    df_daily = pd.DataFrame(daily_data)
    df_daily['date'] = pd.to_datetime(df_daily['date']) # 날짜 형식 변환
    
    # (3월 1일부터 오늘까지 모든 날짜를 가진 인덱스 생성)
    start_date = '2026-03-01'
    end_date = datetime.now().strftime('%Y-%m-%d')
    all_dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # 기존 데이터프레임을 모든 날짜 기준으로 다시 정렬하고 빈 곳은 0으로 채움
    df_daily = df_daily.set_index('date').reindex(all_dates, fill_value=0).reset_index()
    df_daily.rename(columns={'index': 'date'}, inplace=True)

    # 선 그래프(Line Chart) 생성 
    fig_line = px.line(
        df_daily, 
        x="date", 
        y="count",
        markers=True, # 점 표시
        labels={"date": "날짜", "count": "마신 잔 수"},
        template="plotly_white" # 깔끔한 흰색 배경
    )
    
    fig_line.update_traces(
        line_color='#704214', # 진한 갈색 라인
        line_width=3,         # 굵은 선
        marker_size=8,        # 큰 점
        fill='tozeroy',       # 바닥까지 색 채우기
        fillcolor='rgba(112, 66, 20, 0.15)' # 투명한 커피색 (연하게)
    )
    
    # 레이아웃 세부 설정 (y축 0부터 시작, 호버 모드 변경)
    fig_line.update_layout(
        xaxis_title="3월 날짜",
        yaxis_title="잔 수 (cups)",
        xaxis=dict(tickformat='%m/%d'), # 날짜 형식을 월/일로
        yaxis=dict(tickmode='linear', dtick=1, range=[0, df_daily['count'].max() + 1]), # y축을 1잔 단위로, 0부터 시작
        hovermode="x unified" # 마우스 올리면 날짜와 값이 한꺼번에 보이게
    )
    
    st.plotly_chart(fig_line, use_container_width=True)
    
    avg_drink = df_daily['count'].mean()
    total_cups = df_daily['count'].sum()
    st.info(f"📊 **3월 중간 리포트:** 총 **{total_cups}잔**을 마셨고, 하루 평균 **{avg_drink:.1f}잔**을 즐기고 계시네요!")
    
else:
    st.info("아직 소비 기록이 없습니다. 커피를 마시고 기록을 남겨보세요!")







