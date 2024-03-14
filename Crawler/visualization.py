from mysql_connector import MySQLDataConnector
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import pandas as pd
# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

class Visualization:

    def __init__(self):
        self.connector = MySQLDataConnector(user='root',
                                       password='1234',
                                       host='localhost',
                                       database='STOCK')
    '''
    #1
        기간동안 가장 많은 블로그글이 올라온 정치인 topN 
        input :  start_date, end_date, topN
    '''
    def visualization_politician_topN(self,start_date, end_date, topN):
        # 막대 그래프 그리기 가장 많은 블로그글이 올라온 정치인 topN
        dff = self.connector.default_query(
            f"SELECT name, COUNT(name) AS cnt FROM politician_blog WHERE date >= '{start_date}' AND date <= '{end_date}' GROUP BY name ORDER BY cnt DESC LIMIT {topN};")
        dff.plot.bar(x='name', y='cnt', rot=0)

        # 위 topN의 날짜별 언급 plot 그래프
        name_li = dff["name"].to_list()
        names_for_sql = ", ".join(f"'{name}'" for name in name_li)
        df = self.connector.default_query(f"SELECT name,date, COUNT(*) AS cnt FROM politician_blog WHERE name in ({names_for_sql}) and date >= '{start_date}' AND date <= '{end_date}' GROUP BY name, date ORDER BY name, date; ")
        df['date'] = pd.to_datetime(df['date'])

        # pivot을 사용하여 'name'을 컬럼으로, 'Date'를 인덱스로 재구성
        pivot_df = df.pivot(index='date', columns='name', values='cnt')

        # plot 그래프 그리기
        pivot_df.plot(kind='line', marker='o', figsize=(10, 6))
        plt.title('날짜별 정치인 언급 횟수')
        plt.xlabel('날짜')
        plt.ylabel('언급 횟수')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    '''
    #2  
        기간동안 가장 많은 블로그글이 올라온 주식 topN
        input :  start_date, end_date, topN
    '''
    def visualization_stock_topN(self,start_date, end_date, topN):
        dff= self.connector.default_query(f"SELECT bsa.company_name, count(*) as cnt FROM ( SELECT * FROM politician_blog WHERE Date >= '{start_date}' AND Date <= '{end_date}' ) AS pb INNER JOIN blog_politician_analysis AS bsa ON pb.blog_id = bsa.blog_id group by bsa.company_name order by cnt desc limit {topN};")
        dff.plot.bar(x='company_name', y='cnt', rot=0)

        # 위 topN의 날짜별 언급  그래프
        company_names_li = dff["company_name"].to_list()
        company_names_for_sql = ", ".join(f"'{company_name}'" for company_name in company_names_li)
        df = self.connector.default_query(f"select pb.date,bs.company_name, count(*) as cnt from blog_politician_analysis as bs join politician_blog as pb on  bs.blog_id= pb.blog_id where bs.company_name in ({company_names_for_sql}) and pb.date >= '{start_date}' AND pb.date <= '{end_date}' group by pb.date,bs.company_name; ")
        df['date'] = pd.to_datetime(df['date'])

        # pivot을 사용하여 'name'을 컬럼으로, 'Date'를 인덱스로 재구성
        pivot_df = df.pivot(index='date', columns='company_name', values='cnt')
        # plot 그래프 그리기
        pivot_df.plot(kind='line', marker='o', figsize=(10, 6))
        plt.title('날짜별 정치인 언급 횟수')
        plt.xlabel('날짜')
        plt.ylabel('언급 횟수')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    '''
        기간동안 정치인과 가장 많이 언급된 종목 topn의 언급수 그래프로 시각화
        input :  start_date, end_date, politician, topN
    '''
    def visualization_topN(self,start_date, end_date, politician, topN):
        df = self.connector.default_query(f"SELECT  pb.name,  bsa.company_name, count(*) as cnt FROM ( SELECT * FROM politician_blog WHERE Date >= '{start_date}' AND Date <= '{end_date}' ) AS pb INNER JOIN blog_politician_analysis AS bsa ON pb.blog_id = bsa.blog_id group by pb.name,bsa.company_name ;")
        df2 = df[df["name"] == politician].sort_values(by=["cnt"],ascending=False)[:topN]
        df2.plot.bar(x='company_name', y='cnt', rot=0 ,fontsize=6)

        company_name_li = df2["company_name"].to_list()
        company_names_for_sql = ", ".join(f"'{company_name}'" for company_name in company_name_li)
        df = self.connector.default_query(f"select pb.date,bs.company_name, count(*) as cnt from blog_politician_analysis as bs join politician_blog as pb on  bs.blog_id= pb.blog_id where pb.name = '{politician}' and bs.company_name in ({company_names_for_sql}) and pb.date >= '{start_date}' AND pb.date <= '{end_date}' group by pb.date,bs.company_name; ")
        df['date'] = pd.to_datetime(df['date'])
        # pivot을 사용하여 'name'을 컬럼으로, 'Date'를 인덱스로 재구성
        pivot_df = df.pivot(index='date', columns='company_name', values='cnt')
        # plot 그래프 그리기
        pivot_df.plot(kind='line', marker='o', figsize=(10, 6))
        plt.title('날짜별 종목 언급 횟수')
        plt.xlabel('날짜')
        plt.ylabel('언급 횟수')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


    '''
    
        기간동안 종목과 가장 많이 언급된 정치인 topn의 언급수 그래프로 시각화
        input :  start_date, end_date, company_name, topN
    '''
    def visualization_reverse_topN(self,start_date, end_date, company_name, topN):
        df = self.connector.default_query(f"SELECT pb.name, count(*) as cnt FROM ( SELECT * FROM politician_blog WHERE Date >= '{start_date}' AND Date <= '{end_date}' ) AS pb INNER JOIN blog_politician_analysis AS bsa ON pb.blog_id = bsa.blog_id where company_name = '{company_name}'  group by pb.name ;")
        df2 = df.sort_values(by=["cnt"],ascending=False)[:topN]
        df2.plot.bar(x='name', y='cnt', rot=0 ,fontsize=6)
        plt.show()
vslz = Visualization()
# df = vslz.visualization_politician_topN("20240227","20240227",10)
# df = vslz.visualization_stock_topN("20240220","20240227",5)
df2 = vslz.visualization_topN("20231101","20240227","조국",5)
# df2 = vslz.visualization_reverse_topN("20231101","20240227","대상",5)


