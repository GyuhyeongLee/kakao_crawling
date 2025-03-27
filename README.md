# KakaoGift-Rank-Tracker

카카오톡 선물하기의 차량용 방향제 랭킹(1~30위)을 추적하고, 시간별 데이터 저장 및 시각화하는 프로젝트입니다.

---

## 📌 주요 기능

### 1. 🕵️‍♂️ 순위별 상품 데이터 수집 (1~30위)
- 카카오 선물하기 "차량용 방향제" 검색 결과 페이지에서
- 매 시간마다 상위 1~30위 상품 정보를 추출해 CSV로 저장
- 저장 데이터:
  - 브랜드명 + 상품명 + 광고 여부 (`광고 / 일반`)
  - 수집시각 기준, 순위별 데이터 누적

### 2. 📊 시각화 기능
- 저장된 `kakao_gift_by_rank.csv` 파일을 기반으로
- 시간에 따른 **상품 순위 변동 그래프** 생성
- 단, **상품명이 수집 기간 내내 변하지 않은 상품만 시각화**

### 3. 🔍 특정 상품 검색 기능
- 상품명을 입력하면 해당 상품이 현재 몇 번째에 노출되고 있는지 확인
- 결과는 `product_rank_check.csv` 파일에 저장됨
- 형식: `수집시각, 검색어, 순위`

---

## 📁 파일 구조

```
axxcrollring/
├── scrape_kakao_gift.py         # 시간별 랭킹 1~30위 수집 스크립트
├── graph.py                     # 시각화 스크립트 (matplotlib)
├── find_rank_by_keyword.py     # 상품명으로 순위 검색하는 스크립트
├── kakao_gift_by_rank.csv      # 시간별 전체 순위 데이터 저장 파일
├── product_rank_check.csv      # 특정 상품 검색 시 결과 저장 파일
└── README.md
```

---

## ⚙️ 사용 방법

### 1. 패키지 설치
```bash
pip install selenium pandas matplotlib
```

### 2. ChromeDriver 필요
- 본인의 Chrome 브라우저 버전에 맞는 [ChromeDriver](https://chromedriver.chromium.org/downloads) 설치
- `PATH` 설정 또는 코드에서 직접 경로 지정

### 3. 데이터 수집
```bash
python scrape_kakao_gift.py
```

### 4. 시각화 실행
```bash
python graph.py
```

### 5. 특정 상품 순위 확인
```python
from find_rank_by_keyword import find_product_rank
find_product_rank("상품명 일부 또는 전체")
```

---

## 🕒 자동 실행 설정 (macOS 기준)

### 크론탭 등록
```bash
crontab -e
```

### 매 시간 정각마다 실행
```bash
0 * * * * /usr/bin/python3 /Users/본인경로/axxcrollring/scrape_kakao_gift.py >> /Users/본인경로/axxcrollring/cron_log.txt 2>&1
```

---

## 📌 예시 결과

| 수집시각           | 1                        | 2                       | ... |
|-------------------|--------------------------|-------------------------|-----|
| 2025-03-26 14:00 | PUREMOOD 차량방향제 (광고) | 무브랩 차량디퓨저 (일반) |     |
| 2025-03-26 15:00 | PUREMOOD 차량방향제 (광고) | NEWCOOL 디퓨저 (광고)    |     |

---

## 📬 기여 / 문의

이 프로젝트에 개선 아이디어나 제안이 있다면 언제든지 이슈를 남겨주세요!
