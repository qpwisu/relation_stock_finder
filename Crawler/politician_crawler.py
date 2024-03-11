from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
import pandas as pd
import time
from tqdm import tqdm
#
# '''
# 네이버 블로그에서 '정치인 관련주'로 검색을 해서 나온 제목들을 크롤링
# start_date와 end_date를 받아서 하루씩 검색되는 블로그글을 전부 크롤링
# 크롤링 방식은 무한 스크롤을 통해 블로그 테이블 맨 아래로 이동해 제목만 긁어오기
# 테이블은 정치인 , 뉴스제목, 뉴스헤더, 링크 , 날짜
# '''r
#
from concurrent.futures import ThreadPoolExecutor, as_completed

class PoliticianCrawler:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')  # 창 없는 모드
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        prefs = {"profile.managed_default_content_settings.images": 2,  # 이미지 로드 차단
                 "javascript.enabled": False}  # 자바스크립트 실행 차단
        self.options.add_experimental_option("prefs", prefs)

    def start_driver(self):
        max_attempts = 3  # 최대 시도 횟수
        for attempt in range(max_attempts):
            try:
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=self.options)
                return driver  # 드라이버 초기화에 성공하면 반환
            except Exception as e:
                print(f"ChromeDriverManager install failed. Attempt {attempt+1}/{max_attempts}. Error: {e}")
                if attempt < max_attempts - 1:
                    time.sleep(5)  # 다음 재시도 전 5초 대기
                else:
                    raise  # 최대 시도 횟수에 도달했으면 예외를 다시 발생시킴

    def blog_crawler(self, name, date):
        url = f'https://search.naver.com/search.naver?ssc=tab.blog.all&query={name} 관련주&sm=tab_opt&nso=so%3Ar%2Cp%3Afrom{date}to{date}'
        driver = self.start_driver()

        driver.get(url)
        last_height = driver.execute_script("return document.body.scrollHeight")
        last_time = time.time()

        try:
            while True:
                # 스크롤 다운
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # 현재 시간 가져오기
                current_time = time.time()

                # 마지막 높이 체크 이후 2초가 지났는지 확인
                if current_time - last_time > 2:
                    # 새로운 스크롤 높이를 계산
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        # 높이 변화가 없으면 종료
                        break
                    else:
                        # 높이 변화가 있으면 업데이트
                        last_height = new_height
                        last_time = time.time()  # 마지막 체크 시간 업데이트
                # time.sleep(0.1)  # 너무 빠른 스크롤 방지를 위해 짧은 대기 시간 추가
        except Exception as e:
            print(e)

        blog_titles = driver.find_elements(By.CSS_SELECTOR, 'div.title_area > a')
        title_list = [title.text for title in blog_titles]
        href_list = [title.get_property("href") for title in blog_titles]
        blog_header = driver.find_elements(By.CSS_SELECTOR, 'div.dsc_area > a.dsc_link')
        header_list = [header.text for header in blog_header]

        if len(title_list) != len(header_list): # 헤더가 없는 경우가 있어 에러 처리 필요 ex) 안철수 20230220
            header_list = []
            elements = driver.find_elements(By.CSS_SELECTOR, 'div.detail_box')
            for ele in elements:
                headers = ele.find_elements(By.CSS_SELECTOR, 'div.dsc_area > a.dsc_link')
                # headers가 존재하는 경우에만 리스트에 추가
                if len(headers) > 0:
                    header_list.append(headers[0].text)
                else:
                    header_list.append(None)


        if len(title_list) == len(header_list) == len(href_list):
            df = pd.DataFrame({
                'name': name,
                'title': title_list,
                'header': header_list,
                'href': href_list,
                'date': date
            })
        else:
            print("error not same length : ",name,date)
            return

        driver.quit()
        return df

    def politician_blog_crawler(self, name_list, start_date, end_date):
        df_li = []

        if isinstance(start_date, datetime):
            start_date = start_date.date()
        elif isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y%m%d').date()

        if isinstance(end_date, datetime):
            end_date = end_date.date()
        elif isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y%m%d').date()

        date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
        print(date_range)
        if not date_range:
            return False
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = []
            for name in name_list:
                for date in date_range:
                    futures.append(executor.submit(self.blog_crawler, name, date.strftime('%Y%m%d')))

            for future in tqdm(as_completed(futures), total=len(futures)):
                result = future.result()
                df_li.append(result) # 결과를 DataFrame에 추가하는 로직

        df_combined = pd.concat(df_li, ignore_index=True)
        return df_combined

# 사용 예시
# t = PoliticianCrawler()
# t.politician_blog_crawler(["이재명", "조국"], "20240201", "20240226")
