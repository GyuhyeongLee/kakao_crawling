import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'AppleGothic'  # macOS용 한글 폰트
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

# 파일 불러오기
df = pd.read_csv("kakao_gift_by_rank.csv")

# 수집시각을 datetime으로 변환
df["수집시각"] = pd.to_datetime(df["수집시각"])

# 상품별 위치 추적용 딕셔너리
product_positions = {}

# 열 1~30만 순회
for rank in range(1, 31):
    col = str(rank)
    for time, value in zip(df["수집시각"], df[col]):
        if pd.isna(value):
            continue
        if value not in product_positions:
            product_positions[value] = []
        product_positions[value].append((time, rank))

# ✅ 조건에 맞는 상품만 필터링
valid_products = {}
for product, positions in product_positions.items():
    # 수집 횟수와 동일해야 중간에 바뀐 게 없는 상품
    if len(positions) == len(df):
        valid_products[product] = positions

# ✅ 그래프 그리기
plt.figure(figsize=(15, 8))

for product, time_rank_list in valid_products.items():
    times = [t for t, _ in time_rank_list]
    ranks = [r for _, r in time_rank_list]
    truncated_label = product[:20]
    plt.plot(times, ranks, marker='o', label=truncated_label)

plt.gca().invert_yaxis()  # 순위는 1이 위니까 뒤집기
plt.xlabel("수집 시각")
plt.ylabel("순위")
plt.title("상품별 순위 변화 추이")
plt.xticks(rotation=45)
plt.legend(loc="upper right", fontsize="small", ncol=2)
plt.tight_layout()
plt.show()