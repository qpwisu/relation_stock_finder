import datetime
import asyncio
import time

import pandas as pd
import schedule

from mysql_connector import MySQLDataConnector
from stock_crawler import StockCrawler
from word_embedding import WordEmbedding
from word_embedding_test import WordEmbeddingTest
from politician_crawler import PoliticianCrawler
from blog_analyzer  import BlogAnalyzer
from create_aggregate_table import CreateAggregateTable
def initial():
    crawler = StockCrawler()
    connector = MySQLDataConnector(user='root',
                                   password='1234',
                                   host='localhost',
                                   database='STOCK')

    # 하루 이전까지 데이터 크롤링
    now = datetime.now().date() - datetime.timedelta(days=1)
    now = now.strftime('%Y%m%d')

    """국내 종목 정보 25M 소요"""
    df_kr = crawler.kr_stock_info_crawler()
    connector.upload_dataframe(df_kr, 'KR_STOCK_INFO_TB')

    """국내 종목 주가 3M 소요"""
    kr_ticker = connector.select_columns("KR_STOCK_INFO_TB", ["ticker"])["ticker"].tolist()
    df_kr_price = crawler.kr_stock_price_crawler(kr_ticker, "20230801", now)
    connector.upload_dataframe(df_kr_price, 'KR_STOCK_PRICE_TB')

    '''
    국내 주식 업종, 테마 크롤링
    '''
    df_sector = crawler.sector_crawler()
    connector.upload_dataframe(df_sector, 'KR_STOCK_SECTOR_TB')
    df_thema = crawler.thema_crawler()
    connector.upload_dataframe(df_thema, 'KR_STOCK_THEMA_TB')
    '''
    정치인 테이블 업로드
    '''
    politician = pd.read_csv("data/politician.csv")
    connector.upload_dataframe(politician, 'politician_TB')

    '''
    네이버 테마 관련주 검색한 블로그글 크롤링 및 업로드
    '''
    themas = connector.select_columns("KR_STOCK_THEMA_TB",["thema"])["thema"].tolist()
    politician_crawler = PoliticianCrawler()
    themas_df = politician_crawler.politician_blog_crawler(themas, "20230801", now)
    themas_df.rename(columns={"name": "thema"}, inplace=True)
    connector.upload_dataframe(themas_df, 'thema_blog_TB')

    themas_blog_analyzer = BlogAnalyzer()
    themas_blog_df = connector.select_columns("politician_blog_TB")
    kr_thema_li = connector.select_columns("KR_STOCK_THEMA_TB", ["thema"])["thema"].tolist()
    themas_blog_analyzer_df = themas_blog_analyzer.word_extractor(themas_blog_df,kr_thema_li,"thema")
    connector.upload_dataframe(themas_blog_analyzer_df, 'blog_thema_analysis_TB')

    '''
    네이버 업종 관련주 검색한 블로그글 크롤링 및 업로드
    '''
    sector = connector.select_columns("KR_STOCK_SECTOR_TB",["sector"])["sector"].tolist()
    politician_crawler = PoliticianCrawler()
    sector_df = politician_crawler.politician_blog_crawler(sector, "20230801", now)
    sector_df.rename(columns={"name": "sector"}, inplace=True)
    connector.upload_dataframe(sector_df, 'sector_blog_TB')

    sector_blog_analyzer = BlogAnalyzer()
    sector_blog_df = connector.select_columns("sector_blog_TB")
    kr_sector_li = connector.select_columns("KR_STOCK_SECTOR_TB", ["sector"])["sector"].tolist()
    sector_blog_analyzer_df = sector_blog_analyzer.word_extractor(sector_blog_df,kr_sector_li,"sector")
    connector.upload_dataframe(sector_blog_analyzer_df, 'blog_sector_analysis_TB')


    '''
    네이버 정치인 관련주 검색한 블로그글 크롤링 및 업로드
    '''
    politician_names = connector.select_columns("politician_TB",["name"])["name"].tolist()
    politician_crawler = PoliticianCrawler()
    blog_df = politician_crawler.politician_blog_crawler(politician_names,"20230101",now)
    connector.upload_dataframe(blog_df, 'politician_blog_TB')

    '''
     네이버 정치인 관련주 블로그글에서 어떤 종목이 포함 됐는지 저장
    '''
    blog_analyzer = BlogAnalyzer()
    politician_blog_df = connector.select_columns("politician_blog_TB")
    kr_companyName_li = connector.select_columns("KR_STOCK_INFO_TB", ["companyName"])["companyName"].tolist()
    blog_analyzer_df = blog_analyzer.word_extractor(politician_blog_df,kr_companyName_li)
    connector.upload_dataframe(blog_analyzer_df, 'blog_stock_analysis_TB')
    connector.close()

    '''
    집계 테이블
    '''
    create_aggregate_table = CreateAggregateTable(connector)
    # 주식 관련 정치인 전체 언급 순위
    agg_df1 = create_aggregate_table.politician_topN(10)
    connector.upload_dataframe(agg_df1, 'total_category_aggregate_TB',if_exists = "replace")
    # 주식 테마 전체 언급 순위
    agg_df2 = create_aggregate_table.thema_topN(10)
    connector.upload_dataframe(agg_df2, 'total_category_aggregate_TB',if_exists = "append")
    # 주식 업종 전체 언급 순위
    agg_df3 = create_aggregate_table.sector_topN(10)
    connector.upload_dataframe(agg_df3, 'total_category_aggregate_TB',if_exists = "append")

    # 정치인 관련 주식 전체 언급 순위
    agg_df4 = create_aggregate_table.politician_relation_stock_topN(10)
    connector.upload_dataframe(agg_df4, 'total_stock_aggregate_TB',if_exists = "replace")
    # 테마 관련 주식 전체 언급 순위
    agg_df5 = create_aggregate_table.thema_relation_stock_topN(10)
    connector.upload_dataframe(agg_df5, 'total_stock_aggregate_TB',if_exists = "append")
    # 섹터 관련 주식 전체 언급 순위
    agg_df6 = create_aggregate_table.sector_relation_stock_topN(10)
    connector.upload_dataframe(agg_df6, 'total_stock_aggregate_TB',if_exists = "append")

    # 현재 주식 가격
    agg_df7 = create_aggregate_table.now_stock_price_topN(10)
    connector.upload_dataframe(agg_df7, 'KR_NOW_STOCK_PRICE_TB',if_exists = "replace")



'''
    업데이트는 하루 지나고 00시에 실행 
'''
def update_1D():
    crawler = StockCrawler()
    connector = MySQLDataConnector(user='root',
                                   password='1234',
                                   host='localhost',
                                   database='STOCK')

    """국내 종목 정보 업데이트"""
    kr_ticker = connector.select_columns("KR_STOCK_INFO_TB", ["ticker"])["ticker"].tolist()
    df_kr = crawler.kr_stock_info_crawler(kr_ticker)
    connector.upload_dataframe(df_kr, 'KR_STOCK_INFO_TB')

    """국내 종목 주가 업데이트"""
    kr_ticker = connector.select_columns("KR_STOCK_INFO_TB", ["ticker"])["ticker"].tolist()
    last_date = connector.search_last_date("KR_STOCK_PRICE_TB")
    start_date = str(last_date + datetime.timedelta(days=1)).replace("-", "")
    end_date = (datetime.datetime.now() - datetime.timedelta(days=1))
    df_kr_price = crawler.kr_stock_price_crawler(kr_ticker, start_date, end_date)
    connector.upload_dataframe(df_kr_price, 'KR_STOCK_PRICE_TB')

    '''
    테마, 업종 업테이트
    '''
    sectors = crawler.sector_crawler()["sector"].values
    exist_sector = connector.select_columns("KR_STOCK_SECTOR_TB",["sector"])["sector"].values
    result = [item for item in sectors if item not in exist_sector]
    if result:
        df_sector = pd.DataFrame({"sector":result})
        connector.upload_dataframe(df_sector, 'KR_STOCK_SECTOR_TB')

    themas = crawler.thema_crawler()
    exist_thema = connector.select_columns("KR_STOCK_THEMA_TB",["thema"])["thema"].values
    result = [item for item in themas if item not in exist_thema]
    if result:
        df_sector = pd.DataFrame({"thema":result})
        connector.upload_dataframe(df_sector, 'KR_STOCK_THEMA_TB')


    '''
    정치인 테이블 업데이트
    '''
    politician = pd.read_csv("data/politician.csv")
    connector.update_politician_dataframe(politician, 'politician_TB')
    '''
    네이버 정치인 관련주 검색한 블로그글 크롤링 및 업로드
    '''
    last_date = connector.search_last_date("politician_blog_TB")
    start_date = last_date + datetime.timedelta(days=1)
    end_date = datetime.datetime.now() - datetime.timedelta(days=1)
    politician_names = connector.select_columns("politician_TB",["name"])["name"].tolist()
    politician_crawler = PoliticianCrawler()
    blog_df = politician_crawler.politician_blog_crawler(politician_names,start_date,end_date)
    # blog_df = connector.default_query("select * from politician_blog_TB where blogid > 45350")

    if isinstance(blog_df, pd.DataFrame):
        connector.upload_dataframe(blog_df, 'politician_blog_TB')
        '''
         업데이트 네이버 정치인 관련주 블로그글에서 어떤 종목이 포함 됐는지 저장
        '''
        blog_analyzer = BlogAnalyzer()
        kr_companyName_li = connector.select_columns("KR_STOCK_INFO_TB", ["companyName"])["companyName"].tolist()
        blog_df = connector.default_query(f"select * from politician_blog_TB where date > {start_date}")
        blog_analyzer_df = blog_analyzer.word_extractor(blog_df,kr_companyName_li)
        connector.upload_dataframe(blog_analyzer_df, 'blog_stock_analysis_TB')
    '''
    네이버 테마 관련주 검색한 블로그글 크롤링 및 업로드
    '''
    last_date = connector.search_last_date("thema_blog_TB")
    start_date = last_date + datetime.timedelta(days=1)
    end_date = datetime.datetime.now() - datetime.timedelta(days=1)
    thema_names = connector.select_columns("KR_STOCK_THEMA_TB",["thema"])["thema"].tolist()
    politician_crawler = PoliticianCrawler()
    blog_df = politician_crawler.politician_blog_crawler(thema_names,start_date,end_date)
    # blog_df = connector.default_query("select * from thema_blog_TB")
    if isinstance(blog_df, pd.DataFrame):
        blog_df.rename(columns={"name": "thema"}, inplace=True)
        connector.upload_dataframe(blog_df, 'thema_blog_TB')

        blog_analyzer = BlogAnalyzer()
        kr_companyName_li = connector.select_columns("KR_STOCK_INFO_TB", ["companyName"])["companyName"].tolist()
        blog_df = connector.default_query(f"select * from thema_blog_TB where date > {start_date}")
        blog_analyzer_df = blog_analyzer.word_extractor(blog_df,kr_companyName_li)
        connector.upload_dataframe(blog_analyzer_df, 'blog_thema_analysis_TB')
    '''
    네이버 업종 관련주 검색한 블로그글 크롤링 및 업로드
    '''
    last_date = connector.search_last_date("sector_blog_TB")
    start_date = last_date + datetime.timedelta(days=1)
    end_date = datetime.datetime.now() - datetime.timedelta(days=1)
    sector_names = connector.select_columns("KR_STOCK_SECTOR_TB",["sector"])["sector"].tolist()
    politician_crawler = PoliticianCrawler()
    blog_df = politician_crawler.politician_blog_crawler(sector_names,start_date,end_date)
    if isinstance(blog_df, pd.DataFrame):
        blog_df.rename(columns={"name": "sector"}, inplace=True)
        connector.upload_dataframe(blog_df, 'sector_blog_TB')
        blog_analyzer = BlogAnalyzer()
        kr_companyName_li = connector.select_columns("KR_STOCK_INFO_TB", ["companyName"])["companyName"].tolist()
        blog_df = connector.default_query(f"select * from sector_blog_TB where date > {start_date}")
        blog_analyzer_df = blog_analyzer.word_extractor(blog_df,kr_companyName_li)
        connector.upload_dataframe(blog_analyzer_df, 'blog_sector_analysis_TB')

    '''
    집계 테이블
    '''
    create_aggregate_table = CreateAggregateTable(connector)
    # 주식 관련 정치인 전체 언급 순위
    agg_df1 = create_aggregate_table.politician_topN(10)
    connector.upload_dataframe(agg_df1, 'total_category_aggregate_TB',if_exists = "replace")
    # 주식 테마 전체 언급 순위
    agg_df2 = create_aggregate_table.thema_topN(10)
    connector.upload_dataframe(agg_df2, 'total_category_aggregate_TB',if_exists = "append")
    # 주식 업종 전체 언급 순위
    agg_df3 = create_aggregate_table.sector_topN(10)
    connector.upload_dataframe(agg_df3, 'total_category_aggregate_TB',if_exists = "append")

    # 정치인 관련 주식 전체 언급 순위
    agg_df4 = create_aggregate_table.politician_relation_stock_topN(10)
    connector.upload_dataframe(agg_df4, 'total_stock_aggregate_TB',if_exists = "replace")
    # 테마 관련 주식 전체 언급 순위
    agg_df5 = create_aggregate_table.thema_relation_stock_topN(10)
    connector.upload_dataframe(agg_df5, 'total_stock_aggregate_TB',if_exists = "append")
    # 섹터 관련 주식 전체 언급 순위
    agg_df6 = create_aggregate_table.sector_relation_stock_topN(10)
    connector.upload_dataframe(agg_df6, 'total_stock_aggregate_TB',if_exists = "append")

    #종목별 관련 정치인, 테마, 업종 언급 순위
    df_c,df_s = create_aggregate_table.stock_category_aggregate(10)
    # 종목명으로 각 카테고리의 언급 순위 출력
    connector.upload_dataframe(df_c, 'category_aggregate_TB',if_exists = "replace")
    # 카테고리별로 ex) 테마와 가장 많이 언급된 종목 순위 출력
    connector.upload_dataframe(df_s, 'stock_aggregate_TB',if_exists = "replace")


    connector.close()

def update_1M():
    crawler = StockCrawler()
    connector = MySQLDataConnector(user='root',
                                   password='1234',
                                   host='localhost',
                                   database='STOCK')
    create_aggregate_table = CreateAggregateTable(connector)
    # 현재 주식 가격
    agg_df7 = create_aggregate_table.now_stock_price_topN(10)
    connector.upload_dataframe(agg_df7, 'KR_NOW_STOCK_PRICE_TB',if_exists = "replace")

    df_c = create_aggregate_table.date_stock_category_aggregate()
    connector.upload_dataframe(df_c, 'date_category_aggregate_TB',if_exists = "replace")
    connector.close()

def test():
    crawler = StockCrawler()
    connector = MySQLDataConnector(user='root',
                                   password='1234',
                                   host='localhost',
                                   database='STOCK')
    create_aggregate_table = CreateAggregateTable(connector)

    connector.close()

def run_task():
    now = datetime.now()
    if 9 <= now.hour < 16:  # 9시부터 오후 4시 사이인지 확인
        update_1M()

schedule.every().day.at("00:01").do(update_1D())
schedule.every().minute.do(run_task)

while True:
    schedule.run_pending()
    time.sleep(1)

# if __name__ == "__main__":
#     # initial()
#     update_1D()
#     update_1M()
#     # test()
