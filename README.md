# ☕ Coffee-Log: My Intelligent Capsule Management System

> **Personal Mini-Project (2026.03)** > **"데이터 무결성과 사용자 편의를 고민한 스마트 홈카페 기록장"**  
> > 본 프로젝트는 Python과 Streamlit을 활용해 실질적인 데이터 핸들링과 시각화를 구현한 개인 프로젝트입니다.

---

##  Project Overview
- **프로젝트 성격**: 개인 학습 및 실사용 목적의 1인 개발 미니 프로젝트
- **개발 기간**: 2026.03.21 ~ 2026.03.22 (주말 집중 스프린트)
- **기술적 도전 과제**: 
    - **관계형 데이터 설계**: MySQL 외래 키(FK) 제약 조건을 활용하여 캡슐 정보와 소비 로그 간의 엄격한 데이터 관계를 정의하고 참조 무결성을 보장함.
    - **데이터 시각화**: Pandas 전처리를 거친 시계열 데이터를 Plotly의 Area Chart와 Radar Chart로 구현하여 직관적인 소비 패턴 및 취향 분석 리포트 제공.
    - **데이터 정합성 확보**: `ON DUPLICATE KEY UPDATE`를 통한 효율적인 재고 병합 로직과, 데이터 유실 방지를 위한 `Soft Delete(is_active)` 방식을 적용하여 실제 운영 환경을 고려한 아키텍처 설계.
---

## 주요 기능

###  실시간 재고 관리 및 스마트 퀵 기록
* **원클릭 소비 기록**: `Streamlit` 인터페이스를 통해 '오늘의 커피'를 즉시 기록하고, DB의 재고(`stock_count`)를 실시간으로 `-1` 차감합니다.
* **지능형 재고 합치기**: 동일한 이름의 캡슐 등록 시, 중복 생성이 아닌 기존 재고에 합산되는 로직(`ON DUPLICATE KEY UPDATE`)을 구현했습니다.
* **데이터 보존형 삭제(Soft Delete)**: 과거 통계 데이터 유지를 위해 실제 삭제 대신 '숨기기(`is_active`)' 기능을 도입하여 데이터 무결성을 확보했습니다.

###  데이터 기반 대시보드 & 시각화 (Plotly & Pandas 활용)
* **재고 긴급도 알림**: 재고 0개(품절)와 5개 미만(임박)을 구분하여 대시보드 상단에 직관적인 시각적 경고를 제공합니다.
* **취향 밸런스 분석**: 소비한 캡슐의 강도와 산미 평균치를 **차트**로 시각화하여 본인의 취향 프로필을 한눈에 파악합니다.
* **시계열 소비 추이**: **영역 채우기(Area Chart)**가 적용된 선 그래프를 통해 3월 한 달간의 일자별 카페인 섭취 패턴을 추적하며, 데이터가 없는 날은 0으로 자동 전처리(Reindexing)합니다.

###  사용자 맞춤형 가이드
* **기기 최적화 가이드**: 일리 Y3.3 머신의 특성을 고려한 권장 추출 시간(25~28초) 가이드를 제공하여 일관된 커피 맛을 유지하도록 돕습니다.

---

## 🛠 기술 스택 (Tech Stack)

* **Language**: `Python 3.13`
* **Framework**: `Streamlit`
* **Database**: `MySQL`
* **Library**: `Pandas`, `Plotly`, `Numpy`, `PyMySQL`
* **Tools**: `DBeaver`, `Docker`

---

## 트러블슈팅 및 해결 과제 (Troubleshooting)

### ✅ 외래 키 제약 조건(Foreign Key Constraint) 해결
- **문제**: 중복 캡슐 삭제 시 `consumption_log` 테이블이 해당 ID를 참조하고 있어 `Error` 발생.
- **해결**: 데이터를 삭제하기 전 기존 기록의 주인(ID)을 변경하는 `UPDATE` 쿼리를 선행하고, 이후 안전하게 삭제하거나 `Soft Delete` 방식으로 전환하여 해결.

### ✅ 데이터 정합성 유지 (NoneType Error 방지)
- **문제**: DB 연산 과정에서 발생한 `NULL` 값으로 인해 Python 합계 계산 시 `TypeError` 발생.
- **해결**: SQL 레벨에서 `DEFAULT 0` 및 `NOT NULL` 제약을 추가하고, Python 코드에서 `(value or 0)` 형태의 방어적 프로그래밍 적용.

### ✅ 효율적인 데이터 마이그레이션
- **문제**: 테스트를 위한 다량의 소비 데이터가 필요함.
- **해결**: SQL 서브쿼리와 `DATE_ADD` 함수를 활용하여 3월 한 달간의 랜덤 소비 데이터를 생성하는 시드 스크립트 작성 및 실행.


---
<img width="785" height="920" alt="image" src="https://github.com/user-attachments/assets/d3f39d21-76e1-444a-98e5-bb30919dfb52" />



---

<img width="717" height="914" alt="image" src="https://github.com/user-attachments/assets/a998eca1-fd0e-41e5-bb77-8f0fa79d163f" />

구매한 캡슐은 새로운 캡슐 등록하기에서 브랜드, 캡슐명, 수량을 기입하고 등록하면 전체 재고에 등록되는 것을 확인 할 수 있습니다.
다 먹거나 더이상 마시시 않는 캡슐은 하단에서 캡슐 숨기기를 통해 삭제가 아닌 is_active 기능으로 숨기기만 합니다.

---

<img width="817" height="865" alt="image" src="https://github.com/user-attachments/assets/f639cacf-a4b8-45a7-a172-e085487f1928" />

남은 재고가 0개인 캡슐은 재고 관리 페이지에서 지우기가 가능합니다.

---

<img width="899" height="825" alt="image" src="https://github.com/user-attachments/assets/16e1e9b3-99d2-4a12-931c-7c682bda1984" />

<img width="919" height="517" alt="image" src="https://github.com/user-attachments/assets/a0867f76-99ba-483c-9705-ecf9c42001c2" />

<img width="837" height="721" alt="image" src="https://github.com/user-attachments/assets/b4fa1989-a1ea-40da-ad63-77582ed13ff1" />








