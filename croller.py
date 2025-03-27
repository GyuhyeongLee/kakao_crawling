from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import pytz
from datetime import datetime
import time
import os

def scrape_kakao_gift():
    url = "https://gift.kakao.com/search/result?query=%EC%B0%A8%EB%9F%89%EC%9A%A9%20%EB%B0%A9%ED%96%A5%EC%A0%9C"

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(3)

    # 스크롤 내려서 상품 더 로드
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    kst = pytz.timezone("Asia/Seoul")
    now = datetime.now(kst)
    timestamp = now.strftime("%Y-%m-%d %H:%M")

    row_data = {"수집시각": timestamp}

    for i in range(1, 31):
        try:
            name_xpath = f"/html/body/app-root/app-view-wrapper/div/div/main/article/app-pw-result/div/div[2]/app-search-result/app-search-result-list/div/cu-infinite-scroll/div/app-view-grid/div/ul/li[{i}]/app-product/div/div[2]/gc-link/a/strong"
            ad_xpath = f"/html/body/app-root/app-view-wrapper/div/div/main/article/app-pw-result/div/div[2]/app-search-result/app-search-result-list/div/cu-infinite-scroll/div/app-view-grid/div/ul/li[{i}]/app-product/div/div[2]/app-view-ad-tag/div/button"
            brand_xpath = f"/html/body/app-root/app-view-wrapper/div/div/main/article/app-pw-result/div/div[2]/app-search-result/app-search-result-list/div/cu-infinite-scroll/div/app-view-grid/div/ul/li[{i}]/app-product/div/div[2]/gc-link/a/span[1]/span[2]"

            name = driver.find_element(By.XPATH, name_xpath).text.strip()

            try:
                driver.find_element(By.XPATH, ad_xpath)
                ad_text = "광고"
            except NoSuchElementException:
                ad_text = "일반"

            try:
                brand = driver.find_element(By.XPATH, brand_xpath).text.strip()
            except NoSuchElementException:
                brand = ""

            combined = f"{brand} {name} ({ad_text})".strip()
            row_data[str(i)] = combined

        except:
            row_data[str(i)] = ""

    driver.quit()

    # 파일 저장
    filename = "kakao_gift_by_rank.csv"
    new_row = pd.DataFrame([row_data])

    if not os.path.exists(filename):
        # 새 파일 생성: 순위 1~30 컬럼 포함
        columns = ["수집시각"] + [str(i) for i in range(1, 31)]
        new_row.to_csv(filename, index=False, columns=columns, encoding='utf-8-sig')
    else:
        existing = pd.read_csv(filename)
        updated = pd.concat([existing, new_row], ignore_index=True)
        updated.to_csv(filename, index=False, encoding='utf-8-sig')

    print(f"{timestamp} 기준 데이터 저장 완료")

# 실행
scrape_kakao_gift()