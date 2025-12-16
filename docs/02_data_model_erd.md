# Data Model (ERD) & Column Dictionary

A/B Test와 Cohort 분석이 가능하도록 최소 3개 테이블로 구성

---

## 1) ERD (Text Diagram)

users (1) ────< events (N)
users (1) ────< transactions (N)

- users: 사용자 기준 정보 및 A/B 그룹 정보
- events: 클릭/페이지뷰/장바구니 등 행동 로그
- transactions: 구매/결제 등 매출 이벤트

---

## 2) Table Schemas

### A. users
| column | type | description | example |
|---|---|---|---|
| user_id | STRING/INT | 사용자 고유 ID (PK) | U0001 |
| signup_date | DATE | 가입일 | 2025-10-01 |
| cohort_month | STRING | 코호트 기준 월(YYYY-MM) | 2025-10 |
| group_flag | STRING | A/B 그룹 (A=control, B=treatment) | A |
| channel | STRING | 유입 채널 | API / BSP / WEB / MOB |
| country | STRING | 국가/지역 | KR |

**Notes**
- cohort_month는 `signup_date`의 월 단위 파생값
- group_flag는 실험 배정 결과

---

### B. events
| column | type | description | example |
|---|---|---|---|
| event_id | STRING/INT | 이벤트 ID (PK) | E10001 |
| user_id | STRING/INT | 사용자 ID (FK → users.user_id) | U0001 |
| event_date | DATE | 이벤트 발생일 | 2025-10-05 |
| event_type | STRING | 이벤트 종류 | impression / click / add_to_cart |
| page | STRING | 페이지/화면 | home / product |
| session_id | STRING | 세션 ID | S9981 |

**Notes**
- CTR 계산: impression 대비 click 비율
- 이벤트는 하루에 여러 번 발생 가능

---

### C. transactions
| column | type | description | example |
|---|---|---|---|
| trx_id | STRING/INT | 거래 ID (PK) | T90001 |
| user_id | STRING/INT | 사용자 ID (FK) | U0001 |
| trx_date | DATE | 구매일 | 2025-10-06 |
| amount | NUMERIC | 구매 금액 | 59000 |
| order_id | STRING | 주문 ID | O7777 |
| is_refund | BOOLEAN/INT | 환불 여부 | 0 |

**Notes**
- 전환율(CVR) 계산: 구매 사용자 / 방문 사용자
- 구매율: 구매 이벤트 발생 수 / 전체 사용자 수

---

## 3) KPI 정의 (SQL 산출 기준)

### CTR (Click Through Rate)
- 정의: clicks / impressions
- events에서 event_type을 사용해 집계

### CVR (Conversion Rate)
- 정의: 구매 사용자 수 / 실험 대상 사용자 수
- transactions 기준으로 구매 사용자(user_id distinct) 집계

### Purchase Rate
- 정의: 구매 건수 / 사용자 수 또는 세션 수
- trx_id count 기준

---

## 4) Cohort 분석 정의

### 코호트 기준
- cohort_month = 가입월(YYYY-MM)

### 유지/전환 관찰
- 가입월 기준으로 N개월 뒤의 행동/구매를 추적
- 예: 가입월 0개월, 1개월, 2개월… 전환율 비교

---

## 5) 이상치/유효 사용자 필터링 규칙(초안)

- 내부 테스트 계정 제외 (예: user_id 패턴 또는 country='TEST')
- refund 거래 제외 또는 별도 처리
- 비정상적으로 이벤트가 과다한 사용자(봇 의심)는 제외 가능
