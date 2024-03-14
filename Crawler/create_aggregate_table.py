import time
import datetime

import pandas as pd

from stock_crawler import StockCrawler


class CreateAggregateTable():

    def __init__(self,connector):
        self.connector = connector


    '''
    주식 테마 전체 언급 순위 
    '''
    def thema_topN(self, topN):
        df_list = []
        period_list = [1,7,30,90,180]
        for period in period_list:
            start_date = (datetime.datetime.now() - datetime.timedelta(days=1+period)).strftime('%Y-%m-%d')
            end_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            dff = self.connector.default_query(
                f"SELECT thema, COUNT(thema) AS cnt FROM thema_blog WHERE date >= '{start_date}' AND date <= '{end_date}' GROUP BY thema ORDER BY cnt DESC LIMIT {topN};")
            dff['ranking'] = dff.index + 1
            dff['period'] = period
            df_list.append(dff)


        df = pd.concat(df_list)
        df["category"] = "thema"
        df.rename(columns = {"thema":"name"},inplace = True)
        return df

    '''
    주식 섹터 전체 언급 순위 
    '''
    def sector_topN(self, topN):
        df_list = []
        period_list = [1,7,30,90,180]
        for period in period_list:
            start_date = (datetime.datetime.now() - datetime.timedelta(days=1+period)).strftime('%Y-%m-%d')
            end_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            dff = self.connector.default_query(
                f"SELECT sector, COUNT(sector) AS cnt FROM sector_blog WHERE date >= '{start_date}' AND date <= '{end_date}' GROUP BY sector ORDER BY cnt DESC LIMIT {topN};")
            dff['ranking'] = dff.index + 1
            dff['period'] = period
            df_list.append(dff)
        df = pd.concat(df_list)
        df.rename(columns = {"sector":"name"},inplace = True)
        df["category"] = "sector"
        return df

    '''
    주식 관련 정치인 전체 언급 순위 
    '''
    def politician_topN(self, topN):
        df_list = []
        period_list = [1,7,30,90,180]
        for period in period_list:
            start_date = (datetime.datetime.now() - datetime.timedelta(days=1+period)).strftime('%Y-%m-%d')
            end_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            dff = self.connector.default_query(
                f"SELECT name, COUNT(name) AS cnt FROM politician_blog WHERE date >= '{start_date}' AND date <= '{end_date}' GROUP BY name ORDER BY cnt DESC LIMIT {topN};")
            dff['ranking'] = dff.index + 1
            dff['period'] = period
            df_list.append(dff)
        df = pd.concat(df_list)
        df.rename(columns = {"politician":"name"},inplace = True)
        df["category"] = "politician"
        return df
    '''
    정치인 관련 주식 전체 언급 순위 
    '''
    def politician_relation_stock_topN(self, topN):
        df_list = []
        period_list = [1,7,30,90,180]
        for period in period_list:
            start_date = (datetime.datetime.now() - datetime.timedelta(days=1+period)).strftime('%Y-%m-%d')
            end_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            dff = self.connector.default_query(
                f"""
                SELECT bsa.company_name, count(*) as cnt 
                FROM ( SELECT * FROM politician_blog WHERE Date >= '{start_date}' AND Date <= '{end_date}' ) AS pb 
                INNER JOIN blog_politician_analysis AS bsa ON pb.blog_id = bsa.blog_id 
                WHERE bsa.company_name NOT IN ('레이')
                group by bsa.company_name 
                order by cnt desc 
                limit {topN};
                """)
            dff['ranking'] = dff.index + 1
            dff['period'] = period
            df_list.append(dff)
        df = pd.concat(df_list)
        df["category"] = "politician"

        return df

    '''
    테마 관련 주식 전체 언급 순위 
    '''
    def thema_relation_stock_topN(self, topN):
        df_list = []
        period_list = [1,7,30,90,180]
        for period in period_list:
            start_date = (datetime.datetime.now() - datetime.timedelta(days=1+period)).strftime('%Y-%m-%d')
            end_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            dff = self.connector.default_query(
                f"""
                SELECT bsa.company_name, count(*) as cnt 
                FROM ( SELECT * FROM sector_blog WHERE Date >= '{start_date}' AND Date <= '{end_date}' ) AS pb 
                INNER JOIN blog_thema_analysis AS bsa ON pb.blog_id = bsa.blog_id 
                WHERE bsa.company_name NOT IN ('레이')
                group by bsa.company_name 
                order by cnt 
                desc limit {topN};
                """)
            dff['ranking'] = dff.index + 1
            dff['period'] = period
            df_list.append(dff)
        df = pd.concat(df_list)
        df["category"] = "thema"

        return df

    '''
    정치인 관련 주식 전체 언급 순위 
    '''
    def sector_relation_stock_topN(self, topN):
        df_list = []
        period_list = [1,7,30,90,180]
        for period in period_list:
            start_date = (datetime.datetime.now() - datetime.timedelta(days=1+period)).strftime('%Y-%m-%d')
            end_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            dff = self.connector.default_query(
                f"""
                SELECT bsa.company_name, count(*) as cnt 
                FROM ( SELECT * FROM politician_blog WHERE Date >= '{start_date}' AND Date <= '{end_date}' ) AS pb 
                INNER JOIN blog_sector_analysis AS bsa ON pb.blog_id = bsa.blog_id 
                WHERE bsa.company_name NOT IN ('레이')
                group by bsa.company_name 
                order by cnt 
                desc limit {topN};
                """)
            dff['ranking'] = dff.index + 1
            dff['period'] = period
            df_list.append(dff)
        df = pd.concat(df_list)
        df["category"] = "sector"

        return df

    def test(self,topN):

        df = self.connector.default_query(
            f"""
            select company_name,name,count(*) as cnt 
                from politician_blog as pb 
                join blog_politician_analysis as ba on pb.blog_id = ba.blog_id 
                WHERE date >= '20240301' AND date <= '20240307'  AND company_name NOT IN ('레이')
                group by company_name,name 
            """
        )
        result = df.groupby('name').apply(lambda x: x.nlargest(10, 'cnt')).reset_index(drop=True)
        result['ranking'] = result.groupby('name').cumcount() + 1
        print(result)

        return df
    def stock_category_aggregate(self,topN):
        category_df_list = []
        stock_df_list = []

        period_list = [1,7,30,90,180]
        for period in period_list:
            start_date = (datetime.datetime.now() - datetime.timedelta(days=1+period)).strftime('%Y-%m-%d')
            end_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            df = self.connector.default_query(
                f"""
                select company_name,name,count(*) as cnt 
                    from politician_blog as pb 
                    join blog_politician_analysis as ba on pb.blog_id = ba.blog_id 
                    WHERE date >= '{start_date}' AND date <= '{end_date}'  AND company_name NOT IN ('레이')
                    group by company_name,name 
                """
            )
            df_c = df.groupby('company_name').apply(lambda x: x.nlargest(topN, 'cnt')).reset_index(drop=True)
            df_c['ranking'] = df_c.groupby('company_name').cumcount() + 1
            df_c['period'] = period
            df_c['category'] = "politician"
            category_df_list.append(df_c)

            df_s = df.groupby('name').apply(lambda x: x.nlargest(topN, 'cnt')).reset_index(drop=True)
            df_s['ranking'] = df_s.groupby('name').cumcount() + 1
            df_s['period'] = period
            df_s['category'] = "politician"
            stock_df_list.append(df_s)

            df = self.connector.default_query(
                f"""
                    select company_name,thema as name,count(*) as cnt 
                    from thema_blog as pb 
                    join blog_thema_analysis as ba on pb.blog_id = ba.blog_id  
                    WHERE date >= '{start_date}' AND date <= '{end_date}'  AND company_name NOT IN ('레이')
                    group by company_name,thema ;
                """
            )
            df_c = df.groupby('company_name').apply(lambda x: x.nlargest(topN, 'cnt')).reset_index(drop=True)
            df_c['ranking'] = df_c.groupby('company_name').cumcount() + 1
            df_c['period'] = period
            df_c['category'] = "thema"
            category_df_list.append(df_c)

            df_s = df.groupby('name').apply(lambda x: x.nlargest(topN, 'cnt')).reset_index(drop=True)
            df_s['ranking'] = df_s.groupby('name').cumcount() + 1
            df_s['period'] = period
            df_s['category'] = "thema"
            stock_df_list.append(df_s)

            df = self.connector.default_query(
                f"""
                    select company_name,sector as name,count(*) as cnt 
                    from sector_blog as pb 
                    join blog_sector_analysis as ba on pb.blog_id = ba.blog_id 
                    WHERE date >= '{start_date}' AND date <= '{end_date}'  AND company_name NOT IN ('레이')
                    group by company_name,sector ;
                """
            )
            df_c = df.groupby('company_name').apply(lambda x: x.nlargest(topN, 'cnt')).reset_index(drop=True)
            df_c['ranking'] = df_c.groupby('company_name').cumcount() + 1
            df_c['period'] = period
            df_c['category'] = "sector"
            category_df_list.append(df_c)

            df_s = df.groupby('name').apply(lambda x: x.nlargest(topN, 'cnt')).reset_index(drop=True)
            df_s['ranking'] = df_s.groupby('name').cumcount() + 1
            df_s['period'] = period
            df_s['category'] = "sector"
            stock_df_list.append(df_s)

        category_df = pd.concat(category_df_list)
        stock_df = pd.concat(stock_df_list)

        return category_df,stock_df



    def date_stock_category_aggregate(self):
        category_df_list = []
        period = 50
        start_date = (datetime.datetime.now() - datetime.timedelta(days=1+period)).strftime('%Y-%m-%d')
        end_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        df = self.connector.default_query(
            f"""
            select company_name as name,date ,count(*) as cnt 
            from politician_blog as pb 
            join blog_politician_analysis as ba on pb.blog_id = ba.blog_id
            WHERE date >= '{start_date}' AND date <= '{end_date}'  AND company_name NOT IN ('레이')
            group by company_name,date ;
            """
        )
        df['category'] = "stock"
        category_df_list.append(df)

        df2 = self.connector.default_query(
            f"""
            select name,date ,count(*) as cnt 
            from politician_blog as pb 
            join blog_politician_analysis as ba on pb.blog_id = ba.blog_id
            WHERE date >= '{start_date}' AND date <= '{end_date}' 
            group by name,date ;
            """
        )
        df2['category'] = "politician"
        category_df_list.append(df2)

        df = self.connector.default_query(
            f"""
            select company_name as name,date ,count(*) as cnt 
            from thema_blog as pb 
            join blog_thema_analysis as ba on pb.blog_id = ba.blog_id
            WHERE date >= '{start_date}' AND date <= '{end_date}' AND company_name NOT IN ('레이')
            group by company_name,date ;
            """
        )
        df['category'] = "stock"
        category_df_list.append(df)

        df2 = self.connector.default_query(
            f"""
            select thema as name,date ,count(*) as cnt 
            from thema_blog as pb 
            join blog_thema_analysis as ba on pb.blog_id = ba.blog_id
            WHERE date >= '{start_date}' AND date <= '{end_date}' 
            group by thema,date ;
            """
        )
        df2['category'] = "thema"
        category_df_list.append(df2)

        df = self.connector.default_query(
            f"""
            select company_name as name,date ,count(*) as cnt 
            from sector_blog as pb 
            join blog_sector_analysis as ba on pb.blog_id = ba.blog_id
            WHERE date >= '{start_date}' AND date <= '{end_date}' AND company_name NOT IN ('레이')


            group by company_name,date ;
            """
        )
        df['category'] = "stock"
        category_df_list.append(df)

        df2 = self.connector.default_query(
            f"""
            select sector as name,date ,count(*) as cnt 
            from sector_blog as pb 
            join blog_sector_analysis as ba on pb.blog_id = ba.blog_id
            WHERE date >= '{start_date}' AND date <= '{end_date}' 
            group by sector,date ;
            """
        )
        df2['category'] = "sector"
        category_df_list.append(df2)
        category_df = pd.concat(category_df_list)
        category_df = category_df.groupby(['category', 'name', 'date'])['cnt'].sum().reset_index()

        return category_df

    '''
    현재 주식 가격 
    '''
    def now_stock_price_topN(self,topN):
        # end_date = self.connector.default_query(f"select max(date) from stock_price;").values[0][0]
        # dff = self.connector.default_query(f"select pr.ticker,info.company_name, pr.close,pr.change_rate from stock_price as pr join stock_info as info on pr.ticker = info.ticker where pr.date = '{end_date}' order by pr.change_rate desc limit {topN}; ")
        # dff["ranking"]  = dff.index +1
        stock_info_df = self.connector.default_query(f"select company_name, ticker from stock_info;")
        """국내 종목 주가 업데이트"""
        crawler = StockCrawler()
        end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        df_kr_price = crawler.kr_now_stock_price_crawler(end_date)
        df_kr_price = pd.merge(left=df_kr_price, right=stock_info_df, how="inner", on="ticker")
        return df_kr_price