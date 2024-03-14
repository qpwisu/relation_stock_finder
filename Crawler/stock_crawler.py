import time
import pandas as pd
import FinanceDataReader as fdr
from playwright.sync_api import sync_playwright
from tqdm import tqdm
from pykrx import stock
from datetime import datetime
from playwright.async_api import async_playwright
import asyncio
import re

pd.set_option('display.max_rows', None)  # 모든 행을 출력하도록 설정
pd.set_option('display.max_columns', None)  # 모든 열을 출력하도록 설정
pd.set_option('display.width', 1000)  # 출력 너비를 넓게 설정
pd.set_option('display.max_colwidth', None)  # 열 내용 전체를 출력하도록 설정


class StockCrawler:

    '''
    df에 strip 처리 함수
    '''
    def df_strip(self, df):
        str_columns = df.select_dtypes(['object', 'string']).columns
        df[str_columns] = df[str_columns].applymap(lambda x: x.strip() if isinstance(x, str) else x)
        return df

    def extract_numbers_and_dots(self, text):
        # 숫자와 '.'만 찾아내는 정규 표현식
        if text == "N/A":
            return None
        numbers_and_dots = re.findall(r'[\d.]+', text)
        # 찾아낸 숫자와 '.'들을 연결
        return float(''.join(numbers_and_dots))

    # 국내 주식 정보 크롤러 티커, 종목명, 마켓, 기업개요 크롤링
    def kr_stock_info_crawler(self, exist_ticker=[]):
        df_kp = fdr.StockListing('KOSPI')[["Code", "Name"]]
        df_kd = fdr.StockListing('KOSDAQ')[["Code", "Name"]]
        df_kp.columns = ['ticker', 'company_name']
        df_kd.columns = ['ticker', 'company_name']
        df_kp["market"] = "KOSPI"
        df_kd["market"] = "KOSDAQ"
        df_combined = pd.concat([df_kp, df_kd], ignore_index=True)
        df_combined = self.df_strip(df_combined)

        # exist_ticker에 있는 티커를 제외
        df_combined = df_combined[~df_combined['ticker'].isin(exist_ticker)]

        # 기업 개요 크롤링
        ticker_list = df_combined["ticker"].to_list()
        company_description_list = []
        sector_list = []
        market_cap_list = []
        per_list = []
        eps_list = []
        pbr_list = []
        bps_list = []
        divided_list = []
        divided_rate_list = []
        count = 0
        with sync_playwright() as p:
            browser = p.chromium.launch()  # 또는 p.firefox.launch(), p.webkit.launch()
            page = browser.new_page()
            for ticker in tqdm(ticker_list):
                try:
                    url = f"https://finance.naver.com/item/main.nhn?code={str(ticker)}"
                    page.goto(url, timeout=10000)
                    # 업종 크롤링
                    try:
                        page.wait_for_selector("#content > div.section.trade_compare > h4 > em > a", timeout=1000)
                        sector_ele = page.locator("#content > div.section.trade_compare > h4 > em > a")
                        sector_list.append(sector_ele.inner_text())
                    except Exception as e:
                        print(f"섹터 크롤링 실패 {ticker}: {e}")
                        sector_list.append(None)
                    # 기업개요 크롤링
                    try:
                        page.wait_for_selector("#middle > div.h_company > div.wrap_company > div > em.summary > a",
                                               timeout=1000)
                        page.locator('#middle > div.h_company > div.wrap_company > div > em.summary > a').click()
                        elements_locator = page.locator('#summary_info > p')
                        elements_texts = elements_locator.all_text_contents()
                        company_description_list.append("\n".join(elements_texts))
                    except Exception as e:
                        print(f"기업개요 크롤링 실패 {ticker}: {e}")
                        company_description_list.append(None)

                    # 시총, per 등 크롤링
                    try:
                        page.goto(f"https://m.stock.naver.com/domestic/stock/{str(ticker)}/total", timeout=10000)
                        page.wait_for_selector("#content > div > div > div > div.StockInfo_article__2fBr3 > a",
                                               timeout=1000)
                        btn = page.locator("#content > div > div > div > div.StockInfo_article__2fBr3 > a")
                        if btn.inner_text() == "종목 정보 더보기":
                            btn.click()
                            time.sleep(0.5)

                        elements = page.query_selector_all("li.StockInfo_item__H7Aor > div.StockInfo_inner__8plY1")
                        dic = {}
                        for ele in elements:
                            tmp = ele.inner_text()
                            tmp = tmp.split("\n")
                            dic[tmp[0]] = tmp[1]

                        market_cap_list.append(self.extract_numbers_and_dots(dic["시총"]) * (10 ** 8))
                        per_list.append(self.extract_numbers_and_dots(dic["PER"]))
                        eps_list.append(self.extract_numbers_and_dots(dic["EPS"]))
                        pbr_list.append(self.extract_numbers_and_dots(dic["PBR"]))
                        bps_list.append(self.extract_numbers_and_dots(dic["BPS"]))
                        divided_list.append(self.extract_numbers_and_dots(dic["주당배당금"]))
                        divided_rate_list.append(self.extract_numbers_and_dots(dic["배당수익률"]))
                    except Exception as e:
                        print(f"이외 회사 정보 크로링 실패 {ticker}: {e}")
                        market_cap_list.append(None)
                        per_list.append(None)
                        eps_list.append(None)
                        pbr_list.append(None)
                        bps_list.append(None)
                        divided_list.append(None)
                        divided_rate_list.append(None)

                except Exception as e:
                    print(f"페이지 이동 실패 {ticker}: {e}")
                finally:
                    # 페이지를 주기적으로 닫아주지 않으면 AttributeError: 'dict' object has no attribute '_object 에러 발생
                    count += 1
                    if count == 100:
                        page.close()
                        count = 0
                        page = browser.new_page()
            browser.close()

        df_combined["company_description"] = company_description_list
        df_combined["sector"] = sector_list
        df_combined["market_cap"] = market_cap_list
        df_combined["per"] = per_list
        df_combined["eps"] = eps_list
        df_combined["pbr"] = pbr_list
        df_combined["bps"] = bps_list
        df_combined["divided"] = divided_list
        df_combined["divided_rate"] = divided_rate_list

        return df_combined

    '''
    나스닥 주식 정보 크롤러 티커, 종목명, 마켓, 기업개요 크롤링
    '''
    def nq_stock_info_crawler(self, exist_symbol=[]):
        df_nq = fdr.StockListing('NASDAQ')[["Symbol", "Name", "Industry"]]
        df_nq["market"] = "NASDAQ"
        df_nq.columns = ['symbol', 'company_name', "industry", 'market']
        df_nq = self.df_strip(df_nq)
        # exist_symbol에 있는 티커를 제외
        df_nq = df_nq[~df_nq['symbol'].isin(exist_symbol)]
        symbol_list = df_nq["symbol"].to_list()

        # 한글 종목명을 naver pay 증권 사이트에서 크롤링
        name_kr_list = []
        company_description_list = []
        sector_list = []
        market_cap_list = []
        per_list = []
        eps_list = []
        pbr_list = []
        bps_list = []
        divided_list = []
        divided_rate_list = []
        count = 0
        with sync_playwright() as p:
            browser = p.chromium.launch()  # 또는 p.firefox.launch(), p.webkit.launch()
            page = browser.new_page()

            for symbol in tqdm(symbol_list):
                try:
                    url = f"https://m.stock.naver.com/worldstock/stock/{symbol}.O/overview/"
                    page.goto(url)

                    # 회사 한글 이름
                    try:
                        page.wait_for_selector(".GraphMain_name__3XazJ", timeout=5000)  # 5000 milliseconds = 5 seconds
                        element = page.query_selector(".GraphMain_name__3XazJ")
                        text = element.inner_text()
                        name_kr_list.append(text)
                    except Exception as e:
                        print(f"회사 한글 이름 크롤링 실패 {symbol}: {e}")
                        name_kr_list.append(None)

                    # 기업개요
                    try:
                        page.wait_for_selector("div > .OverviewContainer_desc__unQ18", timeout=1000)
                        des_element = page.locator("div > .OverviewContainer_desc__unQ18")
                        text2 = des_element.all_text_contents()
                        company_description_list.append(text2)
                    except Exception as e:
                        print(f"기업 개요 크롤링 실패 {symbol}: {e}")
                        company_description_list.append(None)

                    # 시총, 업종, per 등 크롤링
                    try:
                        url = f"https://m.stock.naver.com/worldstock/stock/{symbol}.O/total/"
                        page.goto(url, timeout=10000)
                        time.sleep(0.5)
                        elements = page.query_selector_all("li.StockInfo_item__H7Aor > div.StockInfo_inner__8plY1 > strong")
                        elements_value = page.query_selector_all("li.StockInfo_item__H7Aor > div.StockInfo_inner__8plY1 > span")
                        dic = {}
                        for i in range(len(elements)) :
                            tmp = elements[i].inner_text()[:3]
                            dic[tmp] = elements_value[i].inner_text()
                        market_cap_list.append(self.extract_numbers_and_dots(dic["시총"].split("\n")[1]) * (10 ** 8))
                        per_list.append(self.extract_numbers_and_dots(dic["PER"]))
                        eps_list.append(self.extract_numbers_and_dots(dic["EPS"]))
                        pbr_list.append(self.extract_numbers_and_dots(dic["PBR"]))
                        bps_list.append(self.extract_numbers_and_dots(dic["BPS"]))
                        sector_list.append((dic["업종"]))
                        # 주당배당금, 배당수익률
                        divided_list.append(self.extract_numbers_and_dots(dic["주당배"]))
                        divided_rate_list.append(self.extract_numbers_and_dots(dic["배당수"]))
                    except Exception as e:
                        print(f"이외 회사 정보 크로링 실패 {symbol}: {e}")
                        market_cap_list.append(None)
                        per_list.append(None)
                        eps_list.append(None)
                        pbr_list.append(None)
                        sector_list.append(None)
                        bps_list.append(None)
                        divided_list.append(None)
                        divided_rate_list.append(None)

                except Exception as e:
                    print(f"페이지 이동 실패 {symbol}: {e}")

                finally:
                    # 페이지를 주기적으로 닫아주지 않으면 AttributeError: 'dict' object has no attribute '_object 에러 발생
                    count += 1
                    if count == 100:
                        page.close()
                        count = 0
                        page = browser.new_page()
            browser.close()
        df_nq["company_nameKR"] = name_kr_list
        df_nq["company_description"] = company_description_list
        df_nq["sector"] = sector_list
        df_nq["market_cap"] = market_cap_list
        df_nq["per"] = per_list
        df_nq["eps"] = eps_list
        df_nq["pbr"] = pbr_list
        df_nq["bps"] = bps_list
        df_nq["divided"] = divided_list
        df_nq["divided_rate"] = divided_rate_list

        return df_nq

    '''
    국내 주식 가격 크롤링
    '''
    def kr_stock_price_crawler(self, ticker_list, start_date, end_date):
        df_kr_price = pd.DataFrame()

        # 국내 종목 티커
        for ticker in tqdm(ticker_list):
            df = stock.get_market_ohlcv(start_date, end_date, ticker).reset_index()
            df["티커"] = ticker
            df_kr_price = pd.concat([df_kr_price, df], axis=0)

        df_kr_price.rename(columns={
            '날짜': 'date',
            '시가': 'open',
            '고가': 'high',
            '저가': 'low',
            '종가': 'close',
            '거래량': 'volume',
            '등락률': 'change_rate',
            '티커': 'ticker'
        }, inplace=True)
        df_kr_price = df_kr_price[['date', 'ticker', 'open', 'high', 'low', 'close', 'volume', 'change_rate']]
        return df_kr_price

    '''
    실시간 국내 주식 가격 크롤링
    '''
    def kr_now_stock_price_crawler(self,date):
        df_kr_price = pd.DataFrame()

        df_kr_price = pd.concat([stock.get_market_ohlcv(date,market="KOSPI") , stock.get_market_ohlcv(date,market="KOSDAQ")])
        df_kr_price["날짜"] = date
        df_kr_price.reset_index(inplace=True)

        df_kr_price.rename(columns={
            '날짜': 'date',
            '시가': 'open',
            '고가': 'high',
            '저가': 'low',
            '종가': 'close',
            '거래량': 'volume',
            '등락률': 'change_rate',
            '티커': 'ticker'
        }, inplace=True)
        df_kr_price = df_kr_price[['date', 'ticker', 'open', 'high', 'low', 'close', 'volume', 'change_rate']]
        return df_kr_price

    '''
     나스닥 주식 가격 크롤링
    '''
    def nq_stock_price_crawler(self, symbol_list, start_date, end_date):
        # 주가 데이터를 저장할 리스트를 생성합니다.
        stock_data_list = []
        for ticker in tqdm(symbol_list):
            try:
                # 각 티커에 대해 주가 데이터를 가져옵니다.
                df = fdr.DataReader(ticker, start_date, end_date)
                df['symbol'] = ticker  # 'Ticker' 열을 추가합니다. (컬럼명 'ticker' 대신 'Ticker'를 사용)
                stock_data_list.append(df)
            except Exception as e:
                print(f"Error retrieving data for {ticker}: {e}")

        # 리스트의 모든 DataFrame을 하나로 합칩니다.
        stock_data = pd.concat(stock_data_list)
        stock_data.reset_index(inplace=True)
        # 종가, 조정 종가중 조정 종가만 남김
        stock_data = stock_data.drop("Close", axis=1)
        stock_data.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'symbol']
        stock_data = stock_data[['date', 'symbol', 'open', 'high', 'low', 'close', 'volume']]
        return stock_data

    '''
    네이버 페이 증권에 국내, 나스닥 종목 뉴스 제목 크롤링 코드 
    약 13만개의 뉴스 제목 크롤링
    40분 정도 소요 
    '''

    async def crawler(self, semaphore, context, ticker, news_page, end_date, market):
        async with semaphore:
            try:
                page = await context.new_page()
                if market == "kr":
                    url = f"https://m.stock.naver.com/domestic/stock/{ticker}/news/title"
                elif market == "nq":
                    url = f"https://m.stock.naver.com/worldstock/stock/{ticker}.O/worldNews"

                await page.goto(url, timeout=30000)
                await asyncio.sleep(0.8)

                # 스크롤을 맨 밑으로 3번까지 내려서 더 많은 뉴스를 가져옴
                scroll_count = 3
                if scroll_count > news_page:
                    scroll_count == news_page

                show_more_button_count = 0
                if news_page > 3:
                    show_more_button_count = news_page - 3

                for _ in range(scroll_count):
                    await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                    await asyncio.sleep(0.5)
                # 더보기 버튼을 눌러 더 많은 뉴스를 가져옴
                for _ in range(show_more_button_count):
                    try:
                        await page.wait_for_selector("text=더보기", timeout=1000)  # 3초까지 기다림
                        await page.get_by_text("더보기").click()
                    except:
                        break
                await asyncio.sleep(0.5)
                elements = await page.query_selector_all(
                    ".NewsList_item__P7Uqz > div > a > span > .NewsList_title__32pfc")
                title_list = [await elem.inner_text() for elem in elements]
                date_elements = await page.query_selector_all(".NewsList_item__P7Uqz > div > a > span > span")
                date_list = []
                for elem in date_elements:
                    inner_text = await elem.inner_text()
                    tmp = inner_text.split(".")
                    # 오늘 뉴스의 경우 오후 2:27 형식이라 오늘 날짜로 변환
                    if len(tmp) == 1:
                        # 현재 날짜와 시간 가져오기
                        now = datetime.now()
                        date_list.append(now.date())
                    else:
                        tmp[0] = tmp[0][-4:]
                        date = "".join(tmp).strip()
                        date_list.append(datetime.strptime(date, "%Y%m%d").date())

                await page.close()
                await context.clear_cookies()  # context를 재사용하기 때문에 쿠키를 제거 해줘야한다
                n = len(date_list)
                tmp_df = pd.DataFrame({
                    "ticker": [ticker] * n,
                    "newsTitle": title_list,
                    "date": date_list
                })
                today = datetime.now().date()
                tmp_df = tmp_df[(tmp_df['date'] < today) & (tmp_df['date'] > end_date)]
                return tmp_df

            except Exception as e:  # 예외 처리를 추가합니다.
                print(f"Error occurred: {e} {ticker}")
                return

    async def stock_news_crawler(self, ticker_list, news_page, end_date, market="kr"):
        if market == "kr":
            ticker_or_symbol = "ticker"
        elif market == "nq":
            ticker_or_symbol = "symbol"
        else:
            print("market is kr or nq")
            return

        async with async_playwright() as p:
            # browser = await p.chromium.launch(headless=True)
            # chrome gpu 가속에 메모리 사용량이 너무 커서 끔
            browser = await p.chromium.launch(headless=True, args=['--disable-gpu'])
            context = await browser.new_context()
            semaphore = asyncio.Semaphore(4)
            tasks = [self.crawler(semaphore, context, ticker, news_page, end_date, market) for ticker in ticker_list]
            df_list = []

            for future in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
                tmp_df = await future
                df_list.append(tmp_df)

            df = pd.concat(df_list, ignore_index=True)
            # df.reset_index(inplace=True)
            df.rename(columns={"ticker": ticker_or_symbol}, inplace=True)
            await browser.close()
            return df


    def sector_crawler(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto("https://finance.naver.com/sise/sise_group.naver?type=upjong")
            # 지정된 요소들의 텍스트 가져오기
            elements = page.query_selector_all("tr > td > a")
            sector_list = [sector.text_content() for sector in elements]

            browser.close()
        df = pd.DataFrame({"sector" : sector_list})
        df = df.drop_duplicates()

        return df

    def thema_crawler(slef):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto("https://finance.naver.com/sise/theme.naver?&page=99")
            elements = page.query_selector_all("td.on")
            last_page = int(elements[0].text_content())
            thema_list = []
            for i in range(1, last_page + 1):
                page.goto(f"https://finance.naver.com/sise/theme.naver?&page={i}")
                elements = page.query_selector_all("tr > td.col_type1 > a")
                themas = [thema.text_content() for thema in elements]
                thema_list.extend(themas)

            browser.close()
        df = pd.DataFrame({"thema" : thema_list})
        df = df.drop_duplicates()
        return df
